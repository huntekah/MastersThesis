Grammatica error detection dont peek
====================================

Detect errors in english text.

This is a Gonito.net challenge made with a purpose to serve ACL paper submission on oddballness,
all the data were taken from <https://www.cl.cam.ac.uk/research/nl/bea2019st/>.

F1 is used as the evaluation metric.

Directory structure
-------------------

* `README.md` — this file
* `config.txt` — configuration file
* `train/` — directory with training data
* `train/train.tsv` — File with original english text and detected error indexes
* `dev-0/` — directory with dev (test) data
* `dev-0/in.tsv` — Original input text for the dev set
* `dev-0/expected.tsv` — Indexes taken by comparing original text with corrected text using damerau-levenshtein alignment
* `test-A` — directory with test data
* `test-A/in.tsv` — Original english input text for the test set
* `test-A/expected.tsv` — Indexes taken by comparing original text with corrected text using damerau-levenshtein alignment

Training sets
-------------

Some lines might not contain any indices, as some text's do not contain errors.

Test sets
---------

Reference English data in the dev and test sets is not tokenised.


Damerau-levenshtein
-------------------

This metric is described here: <https://www.aclweb.org/anthology/C16-1079.pdf>

