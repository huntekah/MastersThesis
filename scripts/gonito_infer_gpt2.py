#!/usr/bin/env python

"""
Find indexes of words that need correction
cat words | ./basename $0 > output
Author:
Krzysztof J.
"""

import sys
import argparse
from proba_engines.gpt2_proba_engine import Gpt2OddballnessEngine
from tqdm import tqdm
from unidecode import unidecode

def parse_args():
    parser = argparse.ArgumentParser(description='Find indexes of words that need correction')
    parser.add_argument('--file', type=str, help="Process text from file")
    parser.add_argument('--out', type=str, help="print output to a file instead of stdin")
    parser.add_argument('--alpha', type=float, default=1, help="alpha value for Gpt2 proba engine")
    parser.add_argument('--threshold', type=float, default=0.85, help="threshold value when we assume a certain word is faulty")
    args = parser.parse_args()
    return args


def main(args):
    lines = get_lines(args)
    indexes = infer(args,lines)
    return_result(args,indexes)


def get_lines(args):
    if args.file is not None:
        return get_lines_from_file(args.file)
    return get_lines_from_stdin()


def get_lines_from_file(file_name):
    with open(file_name,"r") as file:
        while True:
            line = file.readline()
            if not line:
                break
            yield line


def get_lines_from_stdin():
    return sys.stdin.readlines()


def infer(args,lines):
    result = []
    engine = Gpt2OddballnessEngine(alpha=args.alpha)
    for line in tqdm(lines):
        line  = unidecode(line.strip())
        if len(line) == 0:
            result.append([])
            continue
        engine.get_sentence_oddballness(line)
        # print(engine.sentence_data)
        indexes = find_indexes(line, engine.sentence_data, args.threshold)
        result.append(indexes)
    return result


def find_indexes(line, sentence_data,threshold):
    oddballness_list = get_oddballness_per_word(line, sentence_data)
    return [i for i,e in enumerate(oddballness_list,1) if e>threshold]


def get_oddballness_per_word(line, sentence_data):
    r""" Calculate oddballness for each word as a max(token_0...token_i) for 0..i → word

    :param line: input line
    :param sentence_data: data calculated by engine
    :return: oddballness per word (space separated string)
    """
    sentence_reconstructed = "".join([x["name"] for x in sentence_data[:]]).strip()
    letter_scores = [oddballness for x in sentence_data for oddballness in [x["oddballness"]] * len(x["name"]) ]
    letter_scores.pop(0)
    last_id = 0

    sentence_scores = []
    for word in line.split():
        oddballness_value = max(letter_scores[last_id:last_id + len(word)])
        sentence_scores.append(oddballness_value)
        last_id = len(word) + last_id +1
    sentence_scores[0] = 0#sentence_scores[0]**30 #arbitrary fix for first token
    return sentence_scores
        

def return_result(args, indexes):
    print(indexes)
    output= "\n".join([" ".join(list(map(str, line))) for line in indexes])
    print(repr(output))
    if args.out is None:
        print(output)
    else:
        with open(args.out,"w") as file_out:
            print(output,file=file_out)


if __name__ == "__main__":
    args = parse_args()
    main(args)
