import torch
from pytorch_transformers import *
from .proba_engine import TransformersLMEngine

INPUT_TEXT = "I have a dream"

class BertOddballnessEngine(TransformersLMEngine):
    #pretrained_weights = 'gpt2-large'
    pretrained_weights = 'bert-large-cased'

    def __init__(self, text=None):
        tokenizer = BertTokenizer.from_pretrained(self.pretrained_weights) # should i change special tokens like beginnigng of text unk and end of text?
        model = BertForMaskedLM.from_pretrained(self.pretrained_weights)
        super(BertOddballnessEngine, self).__init__(tokenizer=tokenizer, model=model, text=text)


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
