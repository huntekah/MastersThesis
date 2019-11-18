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

def parse_args():
    parser = argparse.ArgumentParser(description='Find indexes of words that need correction')
    #parser.add_argument('--stdin', action="store_true", default=False, help="Process text from stdin")
    parser.add_argument('--file', type=str, help="Process text from file")
    parser.add_argument('--out', type=str, help="print output to a file instead of stdin")
    args = parser.parse_args()
    return args


def main(args):
    lines = get_lines(args)
    indexes = infer(lines)
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


def infer(lines):
    result = []
    engine = Gpt2OddballnessEngine()
    for line in lines:
        line  = line.strip()
        engine.get_sentence_oddballness(line)
        print(engine.sentence_data())
        indexes = find_indexes(line, engine.sentence_data())
        result.append(indexes)
    return result


def find_indexes(line, sentence_data):
    oddballness_list = get_oddballness_per_word(line, sentence_data)
    #for element in sentence_data:
    #    sentence_scores
    #for index, word in enumerate(line.split()):
    #    for letter in word

def get_oddballness_per_word(line, sentence_data):
    sentence_reconstructed = "".join([x["name"] for x in sentence_data])
    print(sentence_reconstructed, line)
    assert len(sentence_reconstructed) == len(line)
    assert sentence_reconstructed == line
    letter_scores = [oddballness for x in sentence_data for oddballness in x["oddballness"] * len(x["name"]) ]
    last_id = 0
    sentence_scores = []
    #for word in line.split():
    #    sentence_scores
        

def return_result(args, indexes):
    pass

if __name__ == "__main__":
    args = parse_args()
    main(args)
