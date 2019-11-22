import torch
from pytorch_transformers import *
try:
    from .proba_engine import TransformersLMEngine
except (SystemError, ImportError):
    from proba_engine import TransformersLMEngine

INPUT_TEXT = "I have a dream"

class Gpt2OddballnessEngine(TransformersLMEngine):
    pretrained_weights = 'gpt2-large'
    #pretrained_weights = 'gpt2-xl' # NOT yet updated to pip
    #pretrained_weights = 'gpt2'

    def __init__(self, text=None, pretrained_weights=None, **kwargs):
        if pretrained_weights is not None:
            self.pretrained_weights = pretrained_weights
        kwargs["tokenizer"] = GPT2Tokenizer.from_pretrained(self.pretrained_weights)
        kwargs["model"] = GPT2LMHeadModel.from_pretrained(self.pretrained_weights)
        kwargs["text"] = text
        #super(Gpt2OddballnessEngine, self).__init__(tokenizer=tokenizer,model=model,text=text)
        super(Gpt2OddballnessEngine, self).__init__(**kwargs)

    def _compute_outputs(self):
        r""" Compute outputs logits and probs for Gpt2LM model """
        self.outputs = self.model(input_ids=self.input_ids, labels=self.input_ids)
        loss, prediction_scores = self.outputs[:2]
        self.logits = prediction_scores[0]
        self.probs = torch.softmax(self.logits, 1)


    @TransformersLMEngine.input_text.setter
    def input_text(self, val):
        r"""
        Add <|endoftext|> token to the end and the beginning of a sentence, and call parent's input_text

        :param val: set input_text to "val + " <|endoftext|>"
        :return: None
        """
        if val:
            TransformersLMEngine.input_text.fset(self,val + " <|endoftext|>")
        else:
            TransformersLMEngine.input_text.fset(self,val)

    def get_sentence_oddballness(self, text=None):
        super().get_sentence_oddballness(text)
        self.sentence_data.pop()
        #self.sentence_data

if __name__ == "__main__":
    obj = Gpt2OddballnessEngine("I have a dream")
    print(obj.get_sentence_probability())
    print(obj.get_sentence_oddballness())
