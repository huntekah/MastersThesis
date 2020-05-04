#!/usr/bin/env python
import spacy
import string


class Detokenizer:
    """ This class is an attempt to detokenize spaCy tokenized sentence """
    def __init__(self, model="en_core_web_sm"):
        self.nlp = spacy.load(model)
    
    def __call__(self, tokens : list):
        """ Call this method to get list of detokenized words """
        _tokens = tokens[:]
        while self._connect_next_token_pair(_tokens):
            pass
        return _tokens

    def get_sentence(self, tokens : list) -> str:
        """ call this method to get detokenized sentence """
        return " ".join(self(tokens))

    def _connect_next_token_pair(self, tokens : list):
        i = self._find_first_pair(tokens)
        if i == -1:
            return False
        tokens[i] = tokens[i] + tokens[i+1]
        tokens.pop(i+1)
        return True

    
    def _find_first_pair(self,tokens):
        if len(tokens) <= 1:
            return -1 
        for i in range(len(tokens)-1):
            if self._would_spaCy_join(tokens,i):
                return i
        return -1

    def _would_spaCy_join(self, tokens, index):
        """
        Check whether sum of lenghts of spaCy tokenized words is equal to length of joind and then spaCy tokenized words...
        
        In other words we say we should join only if the join is reversible.
        eg.:
            for the text ["The","man","."]
            we would joins "man" with "."
            but wouldn't join "The" with "man."
        """
        left_part = tokens[index]
        right_part = tokens[index+1]

        left_toks = self.nlp(left_part)
        right_toks = self.nlp(right_part)
        join_toks = self.nlp(left_part + right_part)

       
        ## The sentence would change after join and tokenize 
        ## (eg. "the red" -> "thered" -> "there d")
        if ([t.text for t in join_toks] 
                != ([t.text for t in left_toks] + [t.text for t in right_toks])):
            return False
        
        ## if this is an even quotation mark "\"" 
        ## it should stick to right neighbour, not left.
        elif (left_part == "\"" and 
              (sum([t.count("\"") for t in tokens[:index+1]])%2 == 1) and 
              right_part[0].isalnum()):
            return True
        elif (right_part == "\"" and
              (sum([t.count("\"") for t in tokens[:index+2]])%2 == 1)):
            return False
        ##first character is punctuation or a set of dots.
        elif (left_toks[-1].text in string.punctuation or
              left_toks[-1].text.count(".") == len(left_toks[-1].text)):
            return False
        ## There is a letter after a number like "70 km" or "5 am"
        elif (left_part[-1].isdigit() and
              right_part[0].isalpha()):
            return False
        ## check if they have the same length
        length_before_join = len(left_toks) + len(right_toks)
        length_after_join = len(join_toks)
        return length_before_join == length_after_join 



