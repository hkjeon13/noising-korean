import os
import argparse
import logging
from tqdm import tqdm
from multiprocessing import Pool,cpu_count
from functools import partial
from noising.noise_generator import NoiseGenerator

parser = argparse.ArgumentParser()
parser.add_argument('--input_dir', type=str, default=None, required=True, help='Directory of input files')
parser.add_argument('--output_dir', type=str, default=None, required=True, help='Directory of output files')
parser.add_argument('--noise_mode', type=str, default='vowel_noise', help='The number of cpu cores.')
parser.add_argument('--num_cores', type=str, default=None, help='The number of cpu cores.')
parser.add_argument('--path_pron', type=str, default='./noising/word_pron_pair.txt', help='Dictionary path for pronounciation noise.')
parser.add_argument('--delimiter', type=str, default='\n', help='Delimeter of the units.')
parser.add_argument('--noise_prob', type=float, default=0.1, help='Probability of generating a noise.')

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


if __name__ == '__main__':
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    num_cores = args.num_cores if args.num_cores else cpu_count()
    logging.info(f'the number of cpu cores: {num_cores}')
    input_files = [os.path.join(args.input_dir, fname) for fname in os.listdir(args.input_dir)]
    generator = NoiseGenerator(args.path_pron)
    func = None
    logging.info(f'**noise mode: {args.noise_mode}')
    if args.noise_mode == 'vowel_noise':
        func = generator.vowel_noise
    elif args.noise_mode == 'consonant_noise':
        func = generator.consonant_noise
    elif args.noise_mode == 'pronoun_noise':
        func = generator.pronoun_noise
    else:
        raise KeyError('Not Supported!')

    func = partial(func, prob=args.noise_prob)
    for input_file in input_files:
        logging.info(f"input file: {input_file}")
        contents = load_text(input_file)
        contents = contents.split(args.delimiter)
        noised_texts = run_imap_multiprocessing(func, contents, num_cores)
        path_output = os.path.join(args.output_dir, os.path.basename(input_file))
        write_text(path_output, str(args.delimiter).join(noised_texts))
        logging.info(f'Saved successfully in {path_output}')