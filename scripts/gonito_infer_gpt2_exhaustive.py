#!/usr/bin/env python

"""
Find indexes of words that need correction
cat words | ./basename $0 > output
Author:
Krzysztof J.
"""

import sys
import argparse
from numpy import arange
from tqdm import tqdm
from unidecode import unidecode

from statistics import mean
from proba_engines.gpt2_proba_engine import Gpt2OddballnessEngine
from multiLabelFbetaScore import MeanMultiLabelFbeta

def parse_args():
    parser = argparse.ArgumentParser(description='Find indexes of words that need correction')
    parser.add_argument('--file', type=str, help="Process text from file")
    parser.add_argument('--out', type=str, help="print output to a file instead of stdin")
    parser.add_argument('--alpha', type=float, default=1, help="alpha value for Gpt2 proba engine")
    parser.add_argument('--threshold', type=float, default=0.85,
                        help="threshold value when we assume a certain word is faulty")
    parser.add_argument('--expected', type=str, help="File with expected output to calculate Fbeta score")
    parser.add_argument('--complexity', type=int, default=50, help="How many alternative tikens should model take into account?")
    args = parser.parse_args()
    return args


class InferGPT2():
    def __init__(self, file, out, alpha, **kwargs):
        self.file = file
        self.out = out
        self.alpha = alpha
        self.engine = Gpt2OddballnessEngine(alpha=alpha)
        self.kwargs = kwargs
        self.indexes = None
        self.best_threshold = None
        self.multilabel_fbeta = MeanMultiLabelFbeta()
        self.complexity = kwargs.get("complexity",20)

    def __call__(self, *args, **kwargs):
        self.compute_model()

    def get_lines(self):
        if self.file is not None:
            self.get_lines_from_file()
            return
        self.get_lines_from_stdin()

    def get_lines_from_file(self):
        self.lines = []
        with open(self.file, "r") as file:
            while True:
                line = file.readline()
                if not line:
                    break
                self.lines.append(line)

    def get_lines_from_stdin(self):
        self.lines = sys.stdin.readlines()

    def compute_model(self):
        self.sentence_data = []
        self.get_lines()
        for line in tqdm(self.lines):
            line = unidecode(line.strip())
            if len(line) == 0:
                self.sentence_data.append([])
                continue
            self.engine.get_sentence_oddballness_exhausive(text=line,complexity=self.complexity)
            self.sentence_data.append((self.engine.sentence_data))
            # print(engine.sentence_data)
            # indexes = find_indexes(line, engine.sentence_data, args.threshold)
            # result.append(indexes)
        # return result

    def find_best_threshold(self, min_thr=0.0, max_thr=1.0-0.000000001, precision=5, maxdepth=10, beta=0.5):
        self.score_type=f"F{beta}"
        expected = self.read_expected()
        scores = []
        step = (max_thr - min_thr) / precision
        for threshold in arange(min_thr, max_thr + step, step ):
            indexes = self.find_indexes(threshold)
            score = self.multilabel_fbeta(expected, indexes,beta=beta)
            #print(f"Score {score} for threshold {threshold}")
            scores.append((threshold, score))
        (low_thr, low_score), (high_thr, high_score) = self._find_new_threshold_boundaries(scores)
        if self.best_threshold is None or low_score > self.best_score:
            self.best_threshold, self.best_score = (low_thr, low_score)
        if self.best_threshold is None or high_score > self.best_score:
            self.best_threshold, self.best_score = (high_thr, high_score)
        if maxdepth == 0:
            indexes = self.find_indexes()
            f2_score = self.multilabel_fbeta(expected, indexes,beta=2.0)
            f05_score = self.multilabel_fbeta(expected, indexes,beta=0.5)
            print(f"{self.best_threshold}\t{f2_score}\t{f05_score}\t{self.alpha}")
            return self.best_threshold
        return self.find_best_threshold(min(self.best_threshold,low_thr), max(self.best_threshold,high_thr), precision, maxdepth - 1, beta)

    @staticmethod
    def _find_new_threshold_boundaries(scores):
        max_average = 0.0
        best_boundaries = (0, 0)
        for low, high in zip(scores, scores[1:]):
            low_thr, low_score = low
            high_thr, high_score = high
            if mean((low_score, high_score)) > max_average:
                max_average = mean((low_score, high_score))
                best_boundaries = (low, high)
        return best_boundaries

    def read_expected(self):
        if 'expected' not in self.kwargs:
            raise FileNotFoundError("You are trying to read expected.tsv file without passing the required argument!")
        expected_indexes = []
        with open(self.kwargs["expected"]) as expected:
            while True:
                line = expected.readline()
                if not line:
                    break
                expected_indexes.append(list(map(int, line.strip().split())))
        return expected_indexes

    def find_indexes(self, threshold=None):
        indexes = []
        if threshold == None:
            threshold = self.best_threshold if self.best_threshold is not None else self.kwargs["threshold"]
        for line, sentence_data in zip(self.lines, self.sentence_data):
            if sentence_data == []:
                indexes.append([])
            oddballness_list = self._get_oddballness_per_word(line, sentence_data)
            indexes.append([i for i, e in enumerate(oddballness_list, 1) if e > threshold])
        return indexes

    @staticmethod
    def _get_oddballness_per_word(line, sentence_data):
        r""" Calculate oddballness for each word as a max(token_0...token_i) for 0..i → word

        :param line: input line
        :param sentence_data: data calculated by engine
        :return: oddballness per word (space separated string)
        """
        # sentence_reconstructed = "".join([x["name"] for x in sentence_data[:]]).strip()
        letter_scores = [oddballness for x in sentence_data for oddballness in [x["oddballness"]] * len(x["name"])]
        letter_scores.pop(0)
        last_id = 0

        sentence_scores = []
        for word in line.split():
            oddballness_value = max(letter_scores[last_id:last_id + len(word)])
            sentence_scores.append(oddballness_value)
            last_id = len(word) + last_id + 1
        return sentence_scores

    def return_result(self,**kwargs):
        indexes = self.find_indexes()
        output = "\n".join([" ".join(list(map(str, line))) for line in indexes])
        if self.out is None:
            print(output)
        else:
            self._save_result(output, **kwargs)

    def _save_result(self,output,suffix="",):
        with open(self.out + suffix, "w") as file_out:
            print(output, file=file_out)


if __name__ == "__main__":
    args = parse_args()
    model = InferGPT2(**vars(args))
    model()
    if args.expected is not None:
        model.find_best_threshold(precision=101, beta=2.0, maxdepth=2 )
        model.return_result(suffix="_f2.0")
        model.best_threshold = None
        model.find_best_threshold(precision=101, beta=0.5, maxdepth=2)
        model.return_result(suffix="_f0.5")
    else:
        model.return_result()
