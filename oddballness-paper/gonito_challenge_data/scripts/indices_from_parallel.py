import spacy
#from errant import 
from errant.scripts.rdlextra import WagnerFischer
from errant.scripts.align_text import AlignText

nlp = spacy.load("en")

def get_indices(orig_toks, cor_toks, policy = "levenshtein"):
    orig = applySpacy(orig_toks, nlp)
    cor = applySpacy(cor_toks, nlp)
    if policy == "levenshtein":
        alignments = WagnerFischer(orig_toks, cor_toks, orig, cor, substitution=AlignText.lev_substitution, transposition=AlignText.lev_transposition )
    else:
        alignments = WagnerFischer(orig_toks, cor_toks, orig, cor, substitution=AlignText.token_substitution)
    #print(alignments)
    alignment = next(alignments.alignments(True))
    edits = AlignText.get_edits_split(AlignText.get_opcodes(alignment))
    indices = []
    for edit in edits:
        #print(edit[1],orig_toks[edit[1]],edit[2] )
        indices.extend(list(range(edit[1],edit[2])))
    return indices


def applySpacy(sent, nlp):
    # Convert tokens to spacy tokens and POS tag and parse.
    sent = nlp.tokenizer.tokens_from_list(sent)
    nlp.tagger(sent)
    nlp.parser(sent)
    return sent

