#!/usr/bin/env python

"""
abstract class for gonito_infer(...) files
Author:
Krzysztof J.
"""

import sys
import argparse
import spacy
import subprocess
import shlex
from numpy import linspace
from tqdm import tqdm
from unidecode import unidecode


from statistics import mean
from proba_engines.gpt2_proba_engine import Gpt2OddballnessEngine
from multiLabelFbetaScore import MeanMultiLabelFbeta
from utils.detokenize import Detokenizer

#metrics = [r"Mean/MultiLabel-F0.5",
#        r"Mean/MultiLabel-F2", 
#        r"MultiLabel-F0.5:P<2>N<F0.5>", 
#        r"MultiLabel-F2:P<2>N<F2>",
#        r"Accuracy:s<^(\d+)(\s\d+)*$><\1>P<2>N<AccFstError>",
#        r"Accuracy:s<^(\d+)(\s\d+)*$><WRONG>P<2>N<AccAnyError>"]

metrics = [shlex.quote(r"Mean/MultiLabel-F0.5"),
        shlex.quote(r"Mean/MultiLabel-F2"), 
        shlex.quote(r"MultiLabel-F0.5:P<2>N<F0.5>"), 
        shlex.quote(r"MultiLabel-F2:P<2>N<F2>"),
        shlex.quote(r"Accuracy:s<^(\d+)(\s\d+)*$><\1>P<2>N<AccFstError>"),
        shlex.quote(r"Accuracy:s<^(\d+)(\s\d+)*$><WRONG>P<2>N<AccAnyError>")]

def parse_args():
    parser = argparse.ArgumentParser(description='Find indexes of words that need correction')
    parser.add_argument('--file', type=str, help="Process text from file")
    parser.add_argument('--out', type=str, help="print output to a file instead of stdin")
    parser.add_argument('--detokenized', type=str, help="Detokenized version of a file to save time during inference.")
    parser.add_argument('--alpha', type=float, default=1, help="alpha value for Gpt2 proba engine")
    parser.add_argument('--threshold', type=float, default=0.85,
                        help="threshold value when we assume a certain word is faulty")
    parser.add_argument('--expected', type=str, help="File with expected output to calculate Fbeta score")
    args = parser.parse_args()
    return args


class AbstractInference():
    def __init__(self, file, out, alpha, **kwargs):
        self.file = file
        self.out = out
        self.alpha = alpha
        self.engine = Gpt2OddballnessEngine(alpha=alpha)
        self.kwargs = kwargs
        self.indexes = None
        self.best_threshold = None
        self.multilabel_fbeta = MeanMultiLabelFbeta()
        self.detokenizer = Detokenizer()

    def __call__(self, *args, **kwargs):
        self.compute_model()

    def get_lines(self):
        if self.file is not None:
            self.get_lines_from_file()
        else:
            self.get_lines_from_stdin()
        self.get_detokenized_lines()

    def get_lines_from_file(self):
        self.lines = []
        with open(self.file, "r") as file:
            while True:
                line = file.readline()
                if not line:
                    break
                self.lines.append(unidecode(line))

    def get_lines_from_stdin(self):
        self.lines = sys.stdin.readlines()

    def get_detokenized_lines(self):
        if 'detokenized' not in self.kwargs:
            self.detokenize_lines()
        else:
            self.get_detokenized_lines_from_file()

    def detokenize_lines(self):
        self.detokenized_lines = []
        print("detokenizing lines on the go. This is the slow, consider loading them from the file!",file=sys.stderr)
        for line in self.lines:
            detokenized_line = self.detokenizer.get_sentence(unidecode(line.strip()).split())
            self.detokenized_lines.append(detokenized_line)
    
    def get_detokenized_lines_from_file(self):
        self.detokenized_lines = []
        file_name = self.kwargs["detokenized"]
        print("reading detokenized lines",file=sys.stderr)
        with open(file_name, "r") as file:
            while True:
                line = file.readline()
                if not line:
                    break
                self.detokenized_lines.append(unidecode(line))


    def compute_model(self):
        self.sentence_data = []
        self.get_lines()
        for line in tqdm(self.detokenized_lines):
            if len(line) == 0:
                self.sentence_data.append([])
                continue
            self.engine.get_sentence_oddballness(line)
            self.sentence_data.append((self.engine.sentence_data))
 
    def find_best_threshold(self, metric, min_thr=0.0, max_thr=1.0, precision=5, maxdepth=4):
        self.score_type=f"{''.join(filter(lambda x: x.isalnum(),metric))}"
        expected = self.read_expected()
        scores = []
        #print(f"d: {maxdepth}\t low: {min_thr}\t hi: {max_thr}",file=sys.stderr)
        for threshold in linspace(min_thr, max_thr, precision):
            indexes = self.find_indexes(threshold)
            #score = self.multilabel_fbeta(expected, indexes,beta=beta)
            score = self.get_evaluation_score(expected, indexes,metric)
            #print(f"\tScore {score} for threshold {threshold}",file=sys.stderr)
            scores.append((threshold, score))
        (low_thr, low_score), (high_thr, high_score) = self._find_new_threshold_boundaries(scores)
        if self.best_threshold is None or low_score > self.best_score:
            self.best_threshold, self.best_score = (low_thr, low_score)
        if self.best_threshold is None or high_score > self.best_score:
            self.best_threshold, self.best_score = (high_thr, high_score)
        if maxdepth == 0:
            indexes = self.find_indexes()
            ###### HERE LIST ALL THE METRICS ######
            #f2_score = self.multilabel_fbeta(expected, indexes,beta=2.0)
            #f05_score = self.multilabel_fbeta(expected, indexes,beta=0.5)
            print(f"{self.best_threshold}\t{self.alpha}",end="")
            for _metric in metrics:
                score_m = self.get_evaluation_score(expected, indexes, _metric)
                print(f"\t{score_m}",end="")
            print()
            return self.best_threshold
        return self.find_best_threshold(metric,min(self.best_threshold,low_thr), max(self.best_threshold,high_thr), precision, maxdepth - 1)


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

    def get_evaluation_score(self, expected, indexes, metric):
        """ run geval to get a score of a given metric"""
        out_file = "tmp_out.tsv"
        exp_file = self.kwargs["expected"]
        
        output = "\n".join([" ".join(list(map(str, line))) for line in indexes])
        with open(out_file, "w") as file_out:
            print(output, file=file_out)
        cmd = "./geval --expected-file {} --out-file {} --alt-metric {}".format(exp_file, out_file, metric)
        result = subprocess.run(shlex.split(cmd),stdout=subprocess.PIPE)
        return float(result.stdout.decode("utf-8"))

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
        for line, sentence_data in zip(self.lines, 
                self.sentence_data):
            if sentence_data == []:
                indexes.append([])
            oddballness_list = self._get_score_per_word(line, sentence_data)
            indexes.append([i for i, e in enumerate(oddballness_list, 1) if e > threshold])
        return indexes

    def _get_score_per_word(self, line, sentence_data):
        r""" Calculate score for each word.

        :param line: input line
        :param sentence_data: data calculated by engine
        :return: score per word (space separated string)
        """
        pass

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


