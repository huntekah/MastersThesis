# scripts
## Oddballness html creator
This is stand-alone html creator. To generate a webpage with words colored according to their oddballness, run:
 1. install python requirements.txt
 2. ```cd scripts```
 3. ``` cat <text file> | python oddballness_create_html.py > your_result.html```
 4. install ```python -m spacy download en_core_web_sm```

 The script will ~~prompt you with the detailed oddballness for each word, as well as~~ create html page with the name: gpt2_parsed_document_<timestamp>.html. It also outputs the result to STDIN.
