import torch
from math import exp
from pytorch_transformers import *
import torch.nn.functional as F
import json
import sys




class TransformersLMEngine():
    pretrained_weights = None
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

    def __init__(self, tokenizer, model, text=None):
        r"""
        abstract constructor for TransformersLMEngine

        :param text: the sentence which will be corrected or used to generate next sentence
        """
        self.tokenizer = tokenizer
        self.model = model
        self.model.eval()  # deactivate DropOut modules to have reproducible results during evaluation
        self.model.to(self.device)
        self.input_text = text
        self._clear_results()

    @property
    def input_text(self):
        return self.__input_text

    @input_text.setter
    def input_text(self, val):
        r"""
        Calculates input_ids, indexed tokens and clears previous calculations.

        :param val: set input_text to val
        :return: None
        """
        if val:
            self.__input_text = val
            self.indexed_tokens = self.tokenizer.encode(self.input_text)
            self.input_ids = torch.tensor([self.indexed_tokens])
            self.input_ids = self.input_ids.to(self.device)
            self._clear_results()

    def _clear_results(self):
        r""" Clear results returned

        :return: None
        """
        self.sentence_data = []

    def get_sentence_probability(self, text=None):
        r""" Get json with probabilities for each token of a sentence
        The result is also stored in self.sentence_data attribute.

        :param text: the text used by LanguageModel
        :return: json representing array of tuples:
            name - name of the token
            probability - probability from LM of the given token
        """
        self.input_text = text
        self.sentence_data = []
        with torch.no_grad():
            self._compute_outputs()
            for ix in range(0, len(self.input_ids[0])):
                token_obj = self._get_token_probability(ix)
                self.sentence_data.append(token_obj)
        return json.dumps(self.sentence_data)

    def _compute_outputs(self, *args, **kwargs):
        r""" Compute outputs for LM, needs to be overwritten for gpt2 models"""
        pass
        # self.outputs = self.model(input_ids=self.input_ids, masked_lm_labels=self.input_ids)
        # self.logits = self.outputs[0][0]
        # self.probs = torch.softmax(self.logits, 1)

    def _get_token_probability(self, ix):
        token_id = self.input_ids[0][ix]
        token_obj = {}
        token_obj["name"] = self.tokenizer.decode(token_id.item())
        token_obj["probability"] = self.probs[ix - 1][token_id].item()
        return token_obj

    def get_sentence_oddballness(self, text=None):
        r""" Get json with probabilities and oddballness for each token of a sentence
        The result is also stored in self.sentence_data attribute.

        :param text: the text used by LanguageModel
        :return: json representing array of tuples:
            name - name of the token
            probability - probability from LM of the given token
            oddballness - F.Graliński oddballness metric calculeted on probabilities from LM
        """
        self.input_text = text
        self.sentence_data = []
        with torch.no_grad():
            self._compute_outputs()
            for ix in range(0, len(self.input_ids[0])):
                token_obj = self._get_token_probability(ix)
                token_obj["oddballness"] = self._get_oddballness_proba(token_obj["probability"], self.probs[ix - 1]).item()

                self.sentence_data.append(token_obj)
        return json.dumps(self.sentence_data)

    @staticmethod
    def _get_oddballness_proba(chosen_token_proba, tokens_proba, alpha=1):
        r""" Calculate value of oddballness for token according to F.Graliński's oddballness metric

        :param chosen_token_proba: probability of the token we'r calculating oddballness for
        :param tokens_proba: probability of all the other possible tokens
        :param alpha: exponent used in the oddballness function family
        :return: oddballness value
        """
        oddballness = torch.sum(F.relu(tokens_proba - chosen_token_proba) ** alpha)
        return oddballness

    #TODO
    def get_text_correction_proposal(self, input_text):
        r""" Return tokens that are likely to substitute each token on the entry.

        :param input_text:
        :return:
        """
        arr = []
        with torch.no_grad():
            for text_chunk in self._string_to_chunks(input_text):
                self.input_text = text_chunk  # set the text currently worked on (no bigger than 1024)
                self._compute_outputs()
                for ix in range(0, len(self.input_ids[0])):
                    token_obj = {}
                    token_id = self.input_ids[0][ix]

                    token_prob = self.probs[ix - 1][token_id]
                    ############
                    print("_" * 15, self.tokenizer.decode(token_id.item()), "_" * 15)
                    probs = torch.softmax(self.logits, 1)

                    sorted_probs, sorted_indices = torch.sort(probs[ix - 1], descending=True)

                    print("\n", "sorted_indicies:")
                    print(sorted_indices)
                    print("\n", "items and their proba:")
                    self._get_token_correction_proposal(ix)
                    for a in range(0, 20):
                        print(sorted_indices[a], self.tokenizer.decode(sorted_indices[a].item()), ' ', sorted_probs[a])

                    ####################
                    print("_" * 15)
                    print("My token id", token_id)
                    token_obj["name"] = self.tokenizer.decode(token_id.item())
                    token_obj["probability"] = token_prob.item()

                    token_obj["oddballness"] = self._get_oddballness_proba(token_prob, probs[ix - 1]).item()

                    arr.append(token_obj)

                self.token_array = arr
        return json.dumps(arr)

    @staticmethod
    def _string_to_chunks(text, **kwargs):
        r""" Return same text in chunks of at most text_limit characters

        :param text: String that will be splited into chunks
        :param text_limit: (optional) changes text_limit. by default set to 1024
        :return: lines that contain no more than text_limit characters total.
        """
        text_limit = kwargs.get('text_limit', 1024)
        lines = ""
        for line in text:
            if len(lines) + len(line) < text_limit:
                lines += line
            else:
                yield lines
                lines = line[0:text_limit]
        else:
            yield lines

    #TODO
    def _get_token_correction_proposal(self, index, num_tokens=10):
        r""" Return num_tokens tokens that could be used to correct token on the position index.
        half of the tokens are best tokens, the other half are tokens surrounding givev index

        :param index: index in Sentence of a token.
        :param num_tokens: How many correction proposals do you want
        :return: Array with correction proposals, their probabilities and oddballness scores.
        """
        self.sorted_probs, self.sorted_indices = torch.sort(self.probs[index - 1], descending=True)
        bt = self._get_best_tokens(index, num_tokens=int(num_tokens / 2))
        st = self._get_surrounding_tokens(index, num_tokens=int(num_tokens / 2))
        print("btst 0:")
        print(torch.cat((bt[0], st[0]), dim=0))
        print("btst 1:")
        print(torch.cat((bt[1], st[1]), dim=0))
        print([self.tokenizer.decode(token_id.item()) for token_id in torch.cat((bt[1], st[1]), dim=0)])
        # TODO
        # merge results

    #TODO
    def _get_best_tokens(self, index, num_tokens=5):
        r""" Return num_tokens tokens that have the highest probability for a given token

        :param index: index in Sentence of a token.
        :param num_tokens: How many correction proposals do you want
        :return: Array with correction proposals, their probabilities and oddballness scores.
        """
        return self.sorted_probs[:num_tokens], self.sorted_indices[:num_tokens]

    #TODO
    def _get_surrounding_tokens(self, index, num_tokens=5, min_index=5):
        r""" Return num_tokens tokens that have similar probability to given token

        :param index: index in Sentence of a token.
        :param num_tokens: How many correction proposals do you want
        :param min_index: index that indicates whether result's of _get_best_tokens intersect
        :return: Array with correction proposals, their probabilities and oddballness scores.
        """
        token_id = self.input_ids[0][index]
        sorted_index = (self.sorted_indices == token_id).nonzero()[0].item()
        lower_boundary = max(0 + min_index, int(sorted_index - num_tokens / 2))
        upper_boundary = lower_boundary + num_tokens  # min(len(self.sorted_probs)-1,int(sorted_index + num_tokens/2))
        print(lower_boundary, upper_boundary)

        return self.sorted_probs[lower_boundary:upper_boundary], self.sorted_indices[lower_boundary:upper_boundary]
