#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Find indexes of words that need correction
cat words | ./basename $0 > output
Author:
Krzysztof J.
"""

from tqdm import tqdm
from abstract_gonito_infer import parse_args
from abstract_gonito_infer import AbstractInference
from shlex import quote


class InferGPT2(AbstractInference):
    def __init__(self, **kwargs):
        super(InferGPT2, self).__init__(**kwargs)
        self.complexity = kwargs.get("complexity",20)

    def compute_model(self):
        self.sentence_data = []
        self.get_lines()
        for line in tqdm(self.detokenized_lines):
            if len(line) == 0:
                self.sentence_data.append([])
                continue
            self.engine.get_sentence_oddballness_exhausive(text=line,complexity=self.complexity)
            self.sentence_data.append((self.engine.sentence_data))

    def _get_score_per_word(self, line, sentence_data):
        return self.get_oddballness_per_word(line, sentence_data)


    @staticmethod
    def get_oddballness_per_word(line,sentence_data):
        r""" Calculate oddballness for each word as a max(token_0...token_i) for 0..i → word. Use Spacy tokenizer "en_core_web_sm" model

        :param line: input line
        :param sentence_data: data calculated by engine
        :return: oddballness per word (space separated string)
        """
        sentence_reconstructed = "".join([x["name"] for x in sentence_data[:]]).strip() #sentence according to gpt2, commas may differ
        letter_scores = [oddballness for x in sentence_data for oddballness in [x["oddballness"]] * len(x["name"])]
        letter_score_pairs = [(letter,score) for letter, score in zip(list(sentence_reconstructed), letter_scores)]

        sentence_scores = []
        last_id = 0
        for word in line.strip().split(): 
            values_in_word = []
            for letter in word:
                while letter_score_pairs[last_id][0] != letter: # compare letters
                    last_id += 1
                values_in_word.append(letter_score_pairs[last_id][1]) # append score
                last_id += 1
            oddballness_value = max(values_in_word)
            sentence_scores.append(oddballness_value)
        return sentence_scores

metrics = [quote(r"Mean/MultiLabel-F0.5"),
        quote(r"Mean/MultiLabel-F2"), 
        quote(r"MultiLabel-F0.5:P<2>N<F0.5>"), 
        quote(r"MultiLabel-F2:P<2>N<F2>"),
        quote(r"Accuracy:s<^(\d+)(\s\d+)*$><\1>P<2>N<AccFstError>"),
        quote(r"Accuracy:s<^(\d+)(\s\d+)*$><WRONG>P<2>N<AccAnyError>")]

def run_inference(args):
    model = InferGPT2(**vars(args))
    model()
    if args.expected is not None:
        for metric in metrics:
            model.find_best_threshold(precision=5, maxdepth=2, metric=metric)
            model.return_result(suffix=f"{''.join(filter(lambda x: x.isalnum(),metric))}")
            model.best_threshold = None
    else:
        model.return_result()

if __name__ == "__main__":
    args = parse_args()
    run_inference(args)
