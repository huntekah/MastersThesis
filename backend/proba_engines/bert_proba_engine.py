import torch
from transformers import *
import json
from functools import reduce
import operator
from math import log, exp
try:
    from .proba_engine import TransformersLMEngine
except (SystemError, ImportError):
    from proba_engine import TransformersLMEngine


INPUT_TEXT = "I have a dream"

class BertOddballnessEngine(TransformersLMEngine):
    pretrained_weights = 'bert-large-cased'

    def __init__(self, text=None, pretrained_weights=None, **kwargs):
        if pretrained_weights is not None:
            self.pretrained_weights = pretrained_weights
        kwargs["tokenizer"] = BertTokenizer.from_pretrained(self.pretrained_weights) # should i change special tokens like beginnigng of text unk and end of text?
        kwargs["model"] = BertForMaskedLM.from_pretrained(self.pretrained_weights)
        kwargs["text"] = text
        super(BertOddballnessEngine, self).__init__(**kwargs)

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
        self.get_all_tokens_probability()
        self._get_words_oddballness()
        return json.dumps(self.sentence_data)

    def get_all_tokens_probability(self, text=None):
        self.input_text = text
        self.token_data = []
        with torch.no_grad():
            self._compute_outputs()
            for ix in range(0, len(self.input_ids[0])):
                token_obj = self._get_token_probability(ix)
                self.token_data.append(token_obj)


    def _get_words_oddballness(self):
        word_start_token_ix = 0
        input_word_index = 0
        self.sentence_data = []
        for ix, token in enumerate(self.token_data):
            #print(ix,token, self._is_end_token(ix))
            #sorted_probs, sorted_indices = torch.sort(self.probs[ix], descending=True)
            #for a in range(10):
            #    print(self.tokenizer.decode(sorted_indices[a].item()))
            if self._is_end_token(ix):
                word_obj = self._compute_word_probability(word_start_token_ix, ix, input_word_index)
                probas = self._compute_alternative_words_probabilities(word_start_token_ix, ix, word_obj["log_prob"])
                #print(torch.sum(probas))
                word_start_token_ix = ix+1
                input_word_index += 1
                word_obj["oddballness"] = self._get_oddballness_proba(word_obj["probability"], probas, alpha=self.alpha).item()
                #print(f"run({word_obj},{torch.sum(probas)})")
                self.sentence_data.append(word_obj)
        return self.sentence_data


    def _is_end_token(self,ix):
        r""" Return true for tokens that are last sub-tokens

        eg. for word "mistkae" we'll have tokenization:
        "m i s t" : False
        "# # k a" : False
        "# # e" : True """
        if ix >= len(self.token_data)-1:
            return True
        if not self._is_middle_token(ix+1):
            return True
        return False

    #TODO should work correctly for input like "##", now it doesnt.
    def _is_middle_token(self, ix):
        r""" Return true for tokens that are not first sub-tokens

        eg. for word "mistkae" we'll have tokenization:
        "m i s t" : False
        "# # k a" : True
        "# # e" : True """
        token_name = self.token_data[ix]["name"]
        return False if len(token_name) < 4 or token_name[:4] != "# # " else True

    def _compute_word_probability(self,start,end, word_index):
        word_obj = {}
        word_obj["name"] = self.input_text.split()[word_index]
        word_obj["log_prob"] = reduce(operator.add,[log(self.token_data[ix]["probability"]) for ix in range(start, end+1)])
        word_obj["probability"] = exp(word_obj["log_prob"])
        return word_obj

    def _compute_alternative_words_probabilities(self, start, end, log_origin):
        r""" Compute probabilities for all alternative words that could replace word between start and end

        since some words in BERT are being split into tokens, and bert gives us only probability for a token, we need to
        compute probabilities for whole words. BERT takes into consideration whole sentence - thus we substitute only one
        token at a time.
        :param start: index marking start of the word in a token_data array
        :param end:  index marking end of the word in token_data array
        :param original_word_probability: the probability of the word that was written to input
        :return: tensor of probabilities of alternative words.
        """
        return self.probs[start - 1]
        # if start == end:
        #     return self.probs[start-1]
        #
        # alternative_log_probas = torch.log(self.probs[start-1])
        # print(alternative_log_probas.size())
        # for pos in range(start+1, end+1):
        #     print("doing calculus")
        #     alternative_log_probas_pos = [alternative_log_probas + torch.log(x) for x in torch.log(self.probs[pos-1])]
        #     print("doing calculus2")
        #     print(len(alternative_log_probas_pos))
        #     alternative_log_probas = torch.cat(alternative_log_probas_pos)
        #     print("after calculus")
        #
        # return torch.exp(alternative_log_probas)

    def _compute_outputs(self):
        r""" Compute outputs logits and probs for BertLM model """
        self.outputs = self.model(input_ids=self.input_ids, masked_lm_labels=self.input_ids)  # use the model?
        loss, prediction_scores = self.outputs[:2]
        self.logits = prediction_scores[0]
        self.probs = torch.softmax(self.logits, 1)

if __name__ == "__main__":
    obj = BertOddballnessEngine("I have a dream")
    print(obj.get_sentence_probability())
    print(obj.get_sentence_oddballness())
