#!/usr/bin/env python

"""
Find indexes of words that need correction
cat words | ./basename $0 > output
Author:
Krzysztof J.
"""

import sys
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Find indexes of words that need correction')
    #parser.add_argument('--stdin', action="store_true", default=False, help="Process text from stdin")
    parser.add_argument('--file', type=str, help="Process text from file")
    parser.add_argument('--out', type=str, help="print output to a file instead of stdin")
    args = parser.parse_args()
    return args


def main(args):
    lines = get_lines(args)
    for line in lines:
        print(0,repr(line), end="")
    result = infer(args, lines)
    process_result(args, result)


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


def infer(args, lines):
    pass

def process_result(args, result):
    pass

if __name__ == "__main__":
    args = parse_args()
    main(args)
