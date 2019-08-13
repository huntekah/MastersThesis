# MastersThesis
this repo will essentialy be just my masters thesis. It will probably be shared across other git repositories to allow for large corpus files.

## GPT2
To run gpt2 probability microservice:
 1. install python requirements.txt
 2. ``` cd emacsGpt2Extension; python manage.py migrate ```
 3. run server ``` python manage.py runserver ```
 4. ask questions: ``` curl http://127.0.0.1:8000/search/?q=I%20Have%20a%20Dream ```
