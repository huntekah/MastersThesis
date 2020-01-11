from detokenize import Detokenizer     
import spacy                           

dt = Detokenizer()                     

#sentence = "I am the man, who dont dont know. And who won't. be doing"
sentence = "I am the man, the red doctor \"who is\" € 2,000 in , who dont dont know. And who won't. be doing"
nlp = spacy.load("en_core_web_sm")      
spaCy_tokenized = nlp(sentence)                      

string_tokens = [a.text for a in spaCy_tokenized]           

sentence_reconstructed = dt.get_sentence(string_tokens)
list_of_words = dt(string_tokens)

print(sentence)
print(sentence_reconstructed)
print(string_tokens)
print(list_of_words)

