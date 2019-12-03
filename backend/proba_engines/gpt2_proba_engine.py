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
        tokenizer = GPT2Tokenizer.from_pretrained(self.pretrained_weights)
        model = GPT2LMHeadModel.from_pretrained(self.pretrained_weights)
        self._add_bos_token(tokenizer, model)
        kwargs["tokenizer"] = tokenizer
        kwargs["model"] = model
        kwargs["text"] = text
        super(Gpt2OddballnessEngine, self).__init__(**kwargs)

    @staticmethod
    def _add_bos_token(tokenizer, model):
        special_tokens_dict = {'cls_token': '<|startoftext|>'}
        tokenizer.add_special_tokens(special_tokens_dict)
        model.resize_token_embeddings(len(tokenizer))

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
            TransformersLMEngine.input_text.fset(self,"<|startoftext|> " + val + " <|endoftext|>")
        else:
            TransformersLMEngine.input_text.fset(self,val)

    def get_sentence_oddballness(self, text=None):
        r""" Remove bos_token and eos_token after calling super().get_sentence_oddballness(text)

        :param text:
        :return:
        """
        super().get_sentence_oddballness(text)
        self.sentence_data.pop()
        self.sentence_data.pop(0)
        return self.sentence_data

if __name__ == "__main__":
    obj = Gpt2OddballnessEngine("Proability I have a dream")
    #obj = Gpt2OddballnessEngine("To be or not to be")
    print(obj.get_sentence_probability())
    obj.get_sentence_oddballness()
    print("\n".join([repr(elem) for elem in obj.sentence_data]))
