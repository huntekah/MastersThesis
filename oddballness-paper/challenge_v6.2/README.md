Grammatical error detection
===========================

Detect errors in english text.

This is a Gonito.net challenge made with a purpose to serve ACL paper submission on oddballness,
all the data were taken from <https://www.cl.cam.ac.uk/research/nl/bea2019st/>.

MultiLabel-F0.5 and MultiLabel-F2 are used as the evaluation metric.

## Directory structure

* `README.md` — this file
* `config.txt` — configuration file
* `train/` — directory with training data
* `train/in.tsv` — Original input text for the dev set
* `train/expected.tsv` — Indexes taken by comparing original text with corrected text using damerau-levenshtein alignment. Indexes start from 1.
* `train/meta.tsv` — each line of this file represents the difficulty level of this text (A,ABCN,B,C,fce,N)
* `dev-0/` — directory with dev (test) data
* `dev-0/in.tsv` — Original input text for the dev set
* `dev-0/expected.tsv` — Indexes taken by comparing original text with corrected text using damerau-levenshtein alignment.
* `dev-0/meta.tsv` — each line of this file represents the difficulty level of this text (A,ABCN,B,C,fce,N)
* `test-A` — directory with test data
* `test-A/in.tsv` — Original english input text for the test set
* `train/meta.tsv` — each line of this file represents the difficulty level of this text (A,ABCN,B,C,fce,N)
* `utils/detokenizer.py` — detokenizer class.
* `utils/detokenize_stdin.py` — script that allows to detokenize spaCy text.

## Training sets

Some lines might not contain any indices, as some text's do not contain errors.

##  Test sets

Reference English data in the dev and test sets is tokenized with spaCy 1.9.0 and english model "en_core_web_sm".


-------------
## Additional information

### Damerau-levenshtein

This metric is described here: <https://www.aclweb.org/anthology/C16-1079.pdf>
It better reflects the alignment that a human would do.

### meta.tsv

Language levels `A` `B` and `C` are equivalent of CEFR language levels. `N` stands for 'Native' and `fce` is used for sentences that came from fce test (~B2).

### detokenization

Some algorithms may require you to use detokenized text. In order to do so, install `requirements.txt`, and then run:
` python -m spacy download en_core_web_sm`
` cat file.txt | python detokenize_text.py > result.txt`

