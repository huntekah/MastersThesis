# backend
this repo will essentialy be just my masters thesis. It will probably be shared across other git repositories to allow for large corpus files.

## GPT2 - django
To run gpt2 probability & oddballness microservice:
 1. pip install -r ~/requirements.txt
 2. ``` python manage.py migrate ```
 3. run server ``` python manage.py runserver 8000```
 4. ask questions: ``` curl http://127.0.0.1:8000/search/?q=I%20Have%20a%20Dream ```

