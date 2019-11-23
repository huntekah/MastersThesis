import torch
from pytorch_transformers import *
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
