import torch
from math import exp
from pytorch_transformers import *
import torch.nn.functional as F
import json
import sys

INPUT_TEXT = "I have a dream"
pretrained_weights = 'gpt2'

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

def log_print(*args,**kwargs):
    for i in args:
        print(">>>"+" {}".format(str(i)),sep = " ", end = "",**kwargs)
    print()

def logit2prob(l):
    odds = exp(l)
    return odds / (1 + odds)

class proba_engine():
    def __init__(self, text=None):
        self.tokenizer = GPT2Tokenizer.from_pretrained(pretrained_weights)
        self.model = GPT2LMHeadModel.from_pretrained(pretrained_weights)
        self.model.to(device)
        if text:
            self.set_input_text(text)

    def set_input_text(self, text):
        self.text = text
        self.input_ids = torch.tensor([self.tokenizer.encode(self.text)])
        # clear all intermediate results here.
        # print("Running program for an input text: \n\t{}\n".format(text))

    def get_sentence_proba(self):
        """ probably could first calculate results and then just return jsons. will be done in the future as speedup. Tis is being made in the NeedForSpeed Deadline mode. """
        #log_print("gsp: Analizing {}".format(self.text))
        arr = []
        with torch.no_grad():
            outputs = self.model(input_ids=self.input_ids.to(device))
            logits = outputs[0][0]
            for ix in range(0, len(self.input_ids[0])):
                probs = torch.softmax(logits, 1)

                sorted_probs, sorted_indices = torch.sort(probs[ix-1], descending=True)
                token_id = self.input_ids[0][ix]
                arr.append( (self.tokenizer.decode(token_id.item()), probs[ix-1][token_id].item() ) )
            # print(arr)
            # print(json.dumps(arr))
        return json.dumps(arr)

    @staticmethod
    def _get_oddballness_proba(chosen_token_proba, tokens_proba):
        oddballness = torch.sum(F.relu(tokens_proba - chosen_token_proba))
        return oddballness

    def get_cumulative_search_result(self, text):
        """ probably could first calculate results and then just return jsons. will be done in the future as speedup. Tis is being made in the NeedForSpeed Deadline mode. """
        self.set_input_text(text)
        # log_print("gcsr: Analizing {}".format(self.text))
        arr = []
        with torch.no_grad():
            outputs = self.model(input_ids=self.input_ids.to(device))
            logits = outputs[0][0]
            probs = torch.softmax(logits, 1)
            for ix in range(0, len(self.input_ids[0])):
                token_obj = {}
                token_id = self.input_ids[0][ix]

                token_prob = probs[ix-1][token_id]
                token_obj["name"] = self.tokenizer.decode(token_id.item())
                token_obj["probability"] = token_prob.item()

                token_obj["oddballness"] = self._get_oddballness_proba(token_prob, probs[ix - 1]).item()

                arr.append(token_obj)

            self.token_array = arr
            #print(json.dumps(arr))
        return json.dumps(arr)

#    def create_html_for_entry(self, text = None):
#        if text:
#            self.set_input_text(text)

if __name__ == "__main__":
    obj = proba_engine("I have a dream")
    obj.get_sentence_proba()
    print(obj.get_cumulative_search_result())
