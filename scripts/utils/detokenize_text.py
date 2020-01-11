#!/usr/bin/env python

from detokenize import Detokenizer
import sys
from tqdm import tqdm
import string


if __name__ == "__main__":
    detokenizer = Detokenizer()
    lines = sys.stdin.readlines()
    for line in lines:
        print(detokenizer.get_sentence(line.split()))
