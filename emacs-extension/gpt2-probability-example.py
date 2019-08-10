import torch
from math import exp
from pytorch_transformers import *

INPUT_TEXT = "I have a dream"
pretrained_weights = 'gpt2'

tokenizer = GPT2Tokenizer.from_pretrained(pretrained_weights)
model = GPT2LMHeadModel.from_pretrained(pretrained_weights)

input_ids = torch.tensor([tokenizer.encode(INPUT_TEXT)])

print("Running program for an input text: \n\t{}\n".format(INPUT_TEXT))
def log_print(*args,**kwargs):
    for i in args:
        print(">>>"+" {}".format(str(i)),sep = " ", end = "",**kwargs)
    print()

def logit2prob(l):
    odds = exp(l)
    return odds / (1 + odds)

log_print("input_ids {}".format(input_ids))
with torch.no_grad():
    outputs = model(input_ids=input_ids)
    logits = outputs[0][0]
    log_print("\n","size of logits:")
    print(logits.size())
    for ix in range(0, len(input_ids[0])):
        print("_"*15)
        probs = torch.softmax(logits, 1)

        sorted_probs, sorted_indices = torch.sort(probs[ix-1], descending=True)

        log_print("\n","sorted_indicies:")
        print(sorted_indices)
        log_print("\n","items and their proba:")
        print(tokenizer.decode(sorted_indices[0].item()), ' ', sorted_probs[0])

        token_id = input_ids[0][ix]
        log_print("\n","ix, ' ', token_id, ' ', tokenizer.decode(token_id.item()), ' ', probs[ix-1][token_id]")
        print(ix, ' ', token_id, ' ', tokenizer.decode(token_id.item()), ' ', probs[ix-1][token_id])
