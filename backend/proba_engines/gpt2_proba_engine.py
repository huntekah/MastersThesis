# /usr/bin/env python
import sys
import torch
import os
from transformers import *
from hashlib import md5
import pickle
import re, string

try:
    from .proba_engine import TransformersLMEngine
except (SystemError, ImportError):
    from proba_engine import TransformersLMEngine
# from functools import reduce
# import operator
from math import log, exp

INPUT_TEXT = "I have a dream"


class Gpt2OddballnessEngine(TransformersLMEngine):
    pretrained_weights = 'gpt2-large'

    #pretrained_weights = 'gpt2-xl' # NOT yet updated to pip
    #pretrained_weights = 'gpt2-medium'

    def __init__(self, text=None, pretrained_weights=None, **kwargs):
        if pretrained_weights is not None:
            self.pretrained_weights = pretrained_weights
        tokenizer = GPT2Tokenizer.from_pretrained(self.pretrained_weights)
        model = GPT2LMHeadModel.from_pretrained(self.pretrained_weights)
        self._add_bos_token(tokenizer, model)
        kwargs["tokenizer"] = tokenizer
        kwargs["model"] = model
        kwargs["text"] = text
        super(Gpt2OddballnessEngine, self).__init__(**kwargs)
        self.oryginal_input_text = text

    @staticmethod
    def _add_bos_token(tokenizer, model):
        special_tokens_dict = {'cls_token': '<|startoftext|>'}
        tokenizer.add_special_tokens(special_tokens_dict)
        model.resize_token_embeddings(len(tokenizer))

    def _compute_outputs(self):
        r""" Compute outputs logits and probs for Gpt2LM model """
        #commented out cause it took too much space
        #if self.is_compute_outputs_loadable():
        #    return self.load_compute_outputs_data()
        self.outputs = self.model(input_ids=self.input_ids, labels=self.input_ids)
        loss, prediction_scores = self.outputs[:2]
        self.logits = prediction_scores[0]
        self.probs = torch.softmax(self.logits, 1)
        #self.save_compute_outputs()

    @TransformersLMEngine.input_text.setter
    def input_text(self, val):
        r"""
        Add <|endoftext|> token to the end and the beginning of a sentence, and call parent's input_text

        :param val: set input_text to "val + " <|endoftext|>"
        :return: None
        """
        if val:
            #val = re.sub(r'([^\s\w]|_)+', '', val)
            #print(val)
            TransformersLMEngine.input_text.fset(self, "<|startoftext|> " + val + " <|endoftext|>")
        else:
            #self.original_input_text = val
            TransformersLMEngine.input_text.fset(self, val)

    def get_sentence_oddballness(self, text=None):
        r""" Remove bos_token and eos_token after calling super().get_sentence_oddballness(text)

        :param text:
        :return: an array of objects that have their token name, probability and oddballness computed
        """
        super().get_sentence_oddballness(text)
        self.sentence_data.pop();
        self.sentence_data.pop(0)
        return self.sentence_data

    def get_sentence_oddballness_exhausive(self, **kwargs):
        r""" The idea behind Graliński's exhaustive oddballness is to compute probability for whole sentence,
        instead of a token alone.
        It can be explained in a simple pseudo-algorithm:
            1. Compute the probability S_a of a sentence by multiplying probabilities for tokens
            2. For each token t_i in the sentence find `n` (where n = complexity) best tokens t_i_j that could replace
                 it.
            3. For each token t_i do:
                3.1 For each j substitute t_i with t_i_j and do 3.2
                3.2 compute probability for this new sentence and save it as S_i_j
            4. For each token t_i its oddballness is defined as sum(relu( S_a - S_i_j) ** alpha)

        :param text: the text used by LanguageModel
        :param complexity: How many alternative tokens should model use?
        :return: an array of objects that have their token name, probability and oddballness computed
        """
        self.oryginal_input_text = kwargs.get("text", self.oryginal_input_text)
        self.input_text = self.oryginal_input_text
        self.complexity = kwargs.get("complexity", 10)
        if self.is_sentence_data_loadable():
            return self.load_sentence_data()
        self.sentence_data = []
        with torch.no_grad():
            self._compute_exhaustive_outputs(**kwargs)
            # print(f"Oryginal sentence was: \'{self.input_text}\'")
            # print(exp(self.sentence_probability))
            # print(self.probs)
            for ix in range(self.input_size):
                token_id = self.input_ids[0][ix]
                token_obj = {}
                token_obj["name"] = self.tokenizer.decode(token_id.item())
                token_obj["probability"] = self.normalized_token_prob[ix]
                # print("suma: ",sum(self.probs[ix]) , " of ", self.probs[ix])
                # print(token_obj["probability"])
                token_obj["oddballness"] = self._get_oddballness_proba(token_obj["probability"], self.probs[ix],
                                                                       alpha=self.alpha).item()

                self.sentence_data.append(token_obj)
        self.save_sentence_data()
        self.sentence_data.pop()
        self.sentence_data.pop(0)
        return self.sentence_data

    def _compute_exhaustive_outputs(self, **kwargs):
        self._compute_outputs()
        # compute S_a
        self.sentence_probability = self._get_sentence_log_probability()
        # compute alternative tokens
        alternative_tokens = self._find_alternative_tokens(**kwargs)
        # print("\n".join([repr(a) for a in alternative_tokens]))
        # compute S_i_j probabilities
        self._compute_alternative_probabilities(alternative_tokens, **kwargs)

    def _get_sentence_log_probability(self):
        r""" Return probability for whole sentence by multiplying probabilities for each token
        For tokens that have probability equal to 0.0, we substitute it with sys.float_info.epsilon

        :return: log of the probability of sentence.
        """
        get_token_prob = lambda ix: self.probs[ix - 1][self.input_ids[0][ix]].item()
        get_smooth_token_log_prob = lambda ix: log(
            get_token_prob(ix) if get_token_prob(ix) != 0.0 else sys.float_info.epsilon)

        return torch.tensor([sum([get_smooth_token_log_prob(ix)
                                  for ix in range(self.input_size)])])

    def _find_alternative_tokens(self, **kwargs):
        alternative_tokens = []
        for ix in range(self.input_size):
            self.sorted_probs, self.sorted_indices = torch.sort(self.probs[ix - 1], descending=True)
            _, alternative_token_ids = self._get_best_tokens(num_tokens=self.complexity)
            alternative_tokens.append([self.tokenizer.decode(token_id.item()) for token_id in alternative_token_ids])
        return alternative_tokens

    def _compute_alternative_probabilities(self, alternative_tokens, **kwargs):
        #oryginal_text = "".join([x for x in self.tokenizer.decode(self.indexed_tokens[1:-1])]).strip()
        probs = [torch.tensor([sys.float_info.epsilon])] #for <|startoftext|> , to not calculate it
        self.normalized_token_prob = [torch.tensor([sys.float_info.epsilon])]

        for ix in range(1,self.input_size - 1):
            # dla kazdego tokenu, wybierz każdy z tokenów zastępczych.
            # stwórz nowe zdanie. policz prawdopodobieństwo wystąpienia takiego zdania.
            get_token_name = lambda x: self.tokenizer.decode(self.input_ids[0][x].item())
            alternate_token_probs = []
            for alternative_token in alternative_tokens[ix]:
                new_tokens = [get_token_name(idx)
                              if idx != ix
                              else alternative_token
                              for idx in range(1, self.input_size - 1)]
                # alternative_sentence = self.tokenizer.convert_tokens_to_string(new_tokens) #doesnt work
                alternative_sentence = "".join([x for x in new_tokens]).strip()
                # print(alternative_sentence)
                self.input_text = alternative_sentence
                self._compute_outputs()
                # compute S__i_j
                sentence_probability = self._get_sentence_log_probability()
                # print(sentence_probability)

                alternate_token_probs.append(sentence_probability)
                # print(f"orig: {self.oryginal_input_text}")
                self.input_text = self.oryginal_input_text
            alternate_token_probs.append(self.sentence_probability) #add probability for the original sentence
            normalized_alternate_token_probs = torch.softmax(torch.tensor(alternate_token_probs),0) #make it a probability distribution
            probs.append(normalized_alternate_token_probs) #save the alternative probabilities
            self.normalized_token_prob.append(normalized_alternate_token_probs[-1]) # add normalized sentence probability as probability for token ix
        self.input_text = self.oryginal_input_text
        probs.append(torch.tensor([sys.float_info.epsilon]))  # for <|endoftext|> , to not calculate it
        self.normalized_token_prob.append(torch.tensor([sys.float_info.epsilon]))
        self.probs = probs

    def save_sentence_data(self,**kwargs):
        f_name = self._get_sentence_data_file_name(**kwargs).format(self.complexity)
        os.makedirs(os.path.dirname(f_name), exist_ok=True)
        with open(f_name,"wb") as sentence_data_file:
            pickle.dump((self.sentence_data, self.probs), sentence_data_file)
    
    def is_sentence_data_loadable(self, **kwargs): 
        f_name = self._get_sentence_data_file_name(**kwargs)
        res = False
        for i in range(self.complexity,100):
            res = res or os.path.isfile(f_name.format(i))
            if res:
                break
        return res

    def load_sentence_data(self, **kwargs):
        f_name = self._get_sentence_data_file_name(**kwargs)
        source_complexity = 0
        for i in range(self.complexity,100):
            if os.path.isfile(f_name.format(i)):
                f_name = f_name.format(i)
                source_complexity = i
                break
        complexity_diff = self.complexity - source_complexity - 1
        with open(f_name, "rb") as sentence_data_file:
            self.sentence_data, self.probs = pickle.load(sentence_data_file)
        #print("_"*20)
        #print(len(self.probs))
        #print(len(self.probs[1]))
        probs = [torch.tensor([sys.float_info.epsilon])]
        for prob in self.probs[1:-1]:
            new_prob = torch.softmax(torch.log(torch.cat((prob[:complexity_diff or None],prob[-1:]))),0)
            probs.append(new_prob)
        probs.append(torch.tensor([sys.float_info.epsilon]))  # for <|endoftext|>
        self.probs = probs

        #print(len(self.probs))
        #print(len(self.probs[1]))       
        for ix in range(len(self.sentence_data)):
            self.sentence_data[ix]["probability"] = self.probs[ix][-1]
            self.sentence_data[ix]["oddballness"] = \
                    self._get_oddballness_proba(self.sentence_data[ix]["probability"], \
                    self.probs[ix],\
                    alpha=self.alpha).item()
        self.sentence_data.pop()
        self.sentence_data.pop(0)
        return self.sentence_data

    def load_compute_outputs_data(self, **kwargs):
        f_name =  self._get_compute_outputs_file_name(**kwargs)
        with open(f_name, "rb") as sentence_data_file:
            self.outputs, self.logits, self.probs = pickle.load(sentence_data_file)
    
    def _get_sentence_data_file_name(self, **kwargs):
        text_to_encode = self.pretrained_weights +\
                                self.input_text +\
                                str(self.complexity)
        suffix = "_sentence_data_{}"
        directory = "saved_sentence_data"
        return self._get_data_filename(suffix, directory, text_to_encode)
    
    def _get_data_filename(self, suffix="", directory="", text_to_encode=""):
        if text_to_encode == "":
            text_to_encode = self.pretrained_weights +\
                                self.input_text +\
                                str(self.complexity)
        name = md5(bytes(text_to_encode, encoding='utf-8')).hexdigest() + suffix +\
            ".pickle"
        return os.path.join("./", directory, name)

if __name__ == "__main__":
    sentence = "I have a kat."
    print("Analyzing: ", sentence)
    #obj = Gpt2OddballnessEngine("I have a dream")
    obj = Gpt2OddballnessEngine(sentence)
    # obj = Gpt2OddballnessEngine(r"Ten or eleven years at school make them tired in spite of pupils don'tice it")
    # obj = Gpt2OddballnessEngine("To be or not to be")
    # print(obj.get_sentence_probability())
    obj.get_sentence_oddballness()
    # obj.get_sentence_oddballness_exhausive(complexity=5)
    # exit()
    print("\n".join([repr(elem) for elem in obj.sentence_data]))
    import json
    for word_obj in obj.get_text_correction_proposal("I have a kat."):
        print(word_obj)
    # print(obj.get_text_correction_proposal("I have a library."))

