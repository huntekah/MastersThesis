#!/usr/bin/env python

from detokenizer import Detokenizer
import sys
from tqdm import tqdm


if __name__ == "__main__":
    detokenizer = Detokenizer()
    lines = sys.stdin.readlines()
    for line in tqdm(lines):
        print(detokenizer.get_sentence(line.split()))
