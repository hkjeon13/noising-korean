import os
import random
import argparse
import logging
from tqdm import tqdm
from multiprocessing import Pool, cpu_count
from functools import partial
from noising.noise_generator import *

parser = argparse.ArgumentParser()
parser.add_argument('--input_dir', type=str, default=None, required=True, help='Directory of input files')
parser.add_argument('--output_dir', type=str, default=None, required=True, help='Directory of output files')
parser.add_argument('--noise_mode', type=str, default='splitting', help='Mode for nosing texts(can be a comma '
                                                                             'seperated)')
parser.add_argument('--noise_prob', type=float, default=0.1, help='Probability of generating a noise.')
parser.add_argument('--prefix', type=str, default='', help='Prefix for the output files.')
parser.add_argument('--delimiter', type=str, default='', help='Delimeter of the units.')

parser.add_argument('--num_cores', type=str, default=None, help='The number of cpu cores for the multi-process.')
parser.add_argument('--parallel', type=str, default='intra', help='The way to use the cpu cores for the data'
                                                                  '("intra" - multiprocessing on the files, '
                                                                  '"inter" - multiprocessing in one data files).')


def run_imap_multi_1(func, argument_list, num_processes, deli=None):
    pool = Pool(processes=num_processes)
    deli = '' if not deli else deli
    for result in tqdm(pool.imap(func=func, iterable=argument_list), total=len(argument_list)):
        contents, path = result
        write_text(path, deli.join(contents))


def run_imap_multi_2(func, argument_list, num_processes):
    pool = Pool(processes=num_processes)
    result_list_tqdm = []
    for result in tqdm(pool.imap(func=func, iterable=argument_list), total=len(argument_list)):
        result_list_tqdm.append(result)
    return result_list_tqdm


def load_text(path):
    with open(path, 'r', encoding='utf-8') as r:
        content = r.read()
    return content


def write_text(path, content):
    with open(path, 'w', encoding='utf-8') as w:
        w.write(content)


def generating_from_string(content, funcs, prob):
    return random.sample(funcs, k=1)[0](content, prob=prob)


def generating_from_file(in_out, funcs, deli, prob):
    _func = random.sample(funcs, k=1)[0]
    contents = [_func(c, prob=prob) for c in load_text(in_out[0]).split(deli)]
    return contents, in_out[1]


def refine_delimiter(delimiter):
    ESCAPE = {'\\n': '\n', '\\r': '\r', '\\t': '\t', '\\b': '\b', '\\f': '\f', '\\v': '\v'}
    delimiter = None if not delimiter else delimiter
    delimiter = ESCAPE[delimiter] if delimiter in ESCAPE else delimiter
    return delimiter


def get_input_files(path_dir):
    return [os.path.join(args.input_dir, f) for f in os.listdir(path_dir)]


def get_noise_functions(func_names=[]):
    dict_func = {'splitting': splitting_noise,
                 'vowel': vowel_noise,
                 'phonological': phonological_process}
    return [dict_func[f] for f in func_names if f in dict_func]


if __name__ == '__main__':
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)

    delimiter = refine_delimiter(args.delimiter)

    num_cores = args.num_cores if args.num_cores else cpu_count()
    logging.info(f'** the number of cpu cores: {num_cores}')

    functions = get_noise_functions(args.noise_mode.split(','))
    logging.info(f'** noise mode: {args.noise_mode}')

    input_files = get_input_files(args.input_dir)
    output_files = [os.path.join(args.output_dir, args.prefix + os.path.basename(i)) for i in input_files]

    if args.parallel == 'intra':
        func = partial(generating_from_file, funcs=functions, deli=delimiter, prob=args.noise_prob)
        run_imap_multi_1(func, list(zip(input_files,output_files)), num_cores, deli=delimiter)
    else:
        func = partial(generating_from_string, funcs=functions, prob=args.noise_prob)
        for input_file, output_file in zip(input_files, output_files):
            logging.info(f"input file: {input_file}")
            contents = load_text(input_file)
            contents = contents.split(delimiter) if delimiter else [contents]
            contents = run_imap_multi_2(func, contents, num_cores)
            contents = args.delimiter.join(contents)
            write_text(output_file, contents)
            logging.info(f'Saved successfully in {output_file}')
