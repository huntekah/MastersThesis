import torch
from math import exp
from pytorch_transformers import *
import json

INPUT_TEXT = "I have a dream"
pretrained_weights = 'gpt2'


def log_print(*args,**kwargs):
    for i in args:
        print(">>>"+" {}".format(str(i)),sep = " ", end = "",**kwargs)
    print()

def logit2prob(l):
    odds = exp(l)
    return odds / (1 + odds)

class proba_engine():
    def __init__(self, text):
        self.tokenizer = GPT2Tokenizer.from_pretrained(pretrained_weights)
        self.model = GPT2LMHeadModel.from_pretrained(pretrained_weights)
        
        self.text = text
        self.input_ids = torch.tensor([self.tokenizer.encode(self.text)])
        print("Running program for an input text: \n\t{}\n".format(text))

    def get_sentence_proba(self):
        """ problably could first calculate results and then just return jsons. will be done in the future as speedup. Tis is being made in the NeedForSpeed Deadline mode. """
        log_print("Analizing {}".format(self.text))
        arr = []
        with torch.no_grad():
            outputs = self.model(input_ids=self.input_ids)
            logits = outputs[0][0]
            for ix in range(0, len(self.input_ids[0])):
                probs = torch.softmax(logits, 1)
                
                sorted_probs, sorted_indices = torch.sort(probs[ix-1], descending=True)
                token_id = self.input_ids[0][ix]
                arr.append( (self.tokenizer.decode(token_id.item()), probs[ix-1][token_id].item() ) )
            #print(arr)
            print(json.dumps(arr))
        return json.dumps(arr)

obj = proba_engine("I have a dream")
obj.get_sentence_proba()
