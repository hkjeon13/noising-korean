import os
import ast
import random
import argparse
import logging
from tqdm import tqdm
from multiprocessing import Pool, cpu_count
from functools import partial
from noising.noise_generator import NoiseGenerator

parser = argparse.ArgumentParser()
parser.add_argument('--input_dir', type=str, default=None, required=True, help='Directory of input files')
parser.add_argument('--output_dir', type=str, default=None, required=True, help='Directory of output files')
parser.add_argument('--noise_mode', type=str, default='spliting_noise', help='Mode for nosing texts(can be a comma '
                                                                             'seperated)')
parser.add_argument('--noise_prob', type=float, default=0.1, help='Probability of generating a noise.')
parser.add_argument('--prefix', type=str, default=None, help='Prefix for the output files.')
parser.add_argument('--delimiter', type=str, default='', help='Delimeter of the units.')
parser.add_argument('--num_cores', type=str, default=None, help='The number of cpu cores.')
parser.add_argument('--path_pron', type=str, default='./noising/word_pron_pair.txt',
                    help='Dictionary path for pronounciation noise.')

ESCAPE = {'\\n': '\n', '\\r': '\r', '\\t': '\t', '\\b': '\b', '\\f': '\f', '\\v': '\v'}


def run_imap_multiprocessing(func, argument_list, num_processes):
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


def gen_func(content, funcs, prob):
    return random.sample(funcs, k=1)[0](content, prob=prob)


if __name__ == '__main__':
    args = parser.parse_args()
    args.delimiter = None if not args.delimiter else args.delimiter
    logging.basicConfig(level=logging.INFO)
    num_cores = args.num_cores if args.num_cores else cpu_count()
    logging.info(f'the number of cpu cores: {num_cores}')
    input_files = [os.path.join(args.input_dir, fname) for fname in os.listdir(args.input_dir)]
    generator = NoiseGenerator(args.path_pron)
    functions = {'spliting_noise': generator.spliting_noise,
                 'consonant_noise': generator.consonant_noise,
                 'pronoun_noise': generator.pronoun_noise}
    logging.info(f'**noise mode: {args.noise_mode}')
    modes = args.noise_mode.split(',')
    func = partial(gen_func, funcs=[functions[m] for m in modes], prob=args.noise_prob)
    for input_file in input_files:
        logging.info(f"input file: {input_file}")
        contents = load_text(input_file)
        args.delimiter = ESCAPE[args.delimiter] if args.delimiter in ESCAPE else args.delimiter
        contents = contents.split(args.delimiter) if args.delimiter else [contents]
        noised_texts = run_imap_multiprocessing(func, contents, num_cores)
        path_output = os.path.join(args.output_dir, args.prefix + os.path.basename(input_file))
        write_text(path_output, args.delimiter.join(noised_texts))
        logging.info(f'Saved successfully in {path_output}')
