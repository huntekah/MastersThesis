# MastersThesis
this repo will essentialy be just my masters thesis. It will probably be shared across other git repositories to allow for large corpus files.

## GPT2
To run gpt2 probability microservice:
 1. install python requirements.txt
 2. ``` cd backend; python manage.py migrate ```
 3. run server ``` python manage.py runserver 8000```
 4. ask questions: ``` curl http://127.0.0.1:8000/search/?q=I%20Have%20a%20Dream ```

## Oddballness html creator
To generate a webpage with words colored according to their oddballness, run:
 1. install python requirements.txt
 2. ```cd scripts```
 3. ``` cat <text file> | python oddballness_create_html.py > your_result.html```
 The script will ~~prompt you with the detailed oddballness for each word, as well as~~ create html page with the name: gpt2_parsed_document_<timestamp>.html. It also outputs the result to STDIN.
