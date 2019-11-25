#!/usr/bin/env python

"""
Find indexes of words that need correction
cat words | ./basename $0 > output
Author:
Krzysztof J.
"""

import sys
import argparse
from proba_engines.bert_proba_engine import BertOddballnessEngine
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
    engine = BertOddballnessEngine(alpha=args.alpha)
    for line in tqdm(lines):
        line  = unidecode(line.strip())
        if len(line) == 0:
            result.append([])
            continue
        engine.get_sentence_oddballness(line)
        # for elem in engine.sentence_data:
        #     print(elem)
        # exit()
        indexes = find_indexes(line, engine.sentence_data, args.threshold)
        result.append(indexes)
    return result


def find_indexes(line, sentence_data,threshold):
    oddballness_list = [data["oddballness"] for data in sentence_data]
    return [i for i,e in enumerate(oddballness_list,1) if e>threshold]

def return_result(args, indexes):
    #print(indexes)
    output= "\n".join([" ".join(list(map(str, line))) for line in indexes])
    #print(repr(output))
    if args.out is None:
        print(output)
    else:
        with open(args.out,"w") as file_out:
            print(output,file=file_out)


if __name__ == "__main__":
    args = parse_args()
    main(args)
