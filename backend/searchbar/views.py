from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
#import sys
#sys.path.append("..")
from proba_engines.bert_proba_engine import BertOddballnessEngine
from proba_engines.gpt2_proba_engine import Gpt2OddballnessEngine
# Create your views here.

def get_threshold(model_name):
    return {
        "gpt2" : 0.8125,
        "gpt2-medium": 0.8125,
        "gpt2-large": 0.8125,
        "gpt2-xl": 0.8125,
    }[model_name]

class Gpt2SearchView(APIView):
    engine = Gpt2OddballnessEngine()
    threshold = get_threshold(engine.pretrained_weights)

    def get(self, request):
        r""" This function is used mainly for wget or Curl requests to generate colored output text

        :param request: json request in form of "q":"Some sentence here"
        :return: json response with probabilities, and oddballness scores
        """
        if request.GET.get('q'):
            query = request.GET['q']
            message = 'You submitted: {}'.format(query)
            engine = Gpt2OddballnessEngine(query)
            json_response = engine.get_sentence_oddballness()
            return Response(json_response)
        else:
            return Response({'tip':'To get an example result type "curl <port>/search/?q=<query_text>"'})

    # osobna metoda by robić niewielkie zmiany - pamiętać text który był wcześniej na serwerze
    def post(self, request):
        """Used by main frontend App to deal with text."""
        if request.data:
            print(request.data)
            query = request.data["queryText"]
            # json_response = self.engine.get_sentence_oddballness(text=query)
            response = self.engine.get_text_correction_proposal(input_text=query)
            for obj in response:
                obj["underlined"] =  True if obj["oddballness"] > self.threshold else False
            #mock_response = [{"name":"I","probability":6.9e-05,"oddballness":0.79},{"name":" Have","probability":0.00012486,"oddballness":0.6745542883872986},{"name":" a","probability":0.11080533266067505,"oddballness":0.0},{"name":" Dream","probability":0.07753866165876389,"oddballness":0.001621440052986145}]
            mock_response = [{"name": "I", "oddballness": 0.79, "corrections" : [" a", " b", " c"], "underlined": False},
                             {"name": " Have"," oddballness": 0.67, "corrections" : [" d", " e", " f"], "underlined": True},
                             {"name": " a", "oddballness": 0.0, "corrections" : [" g", " h", " i"], "underlined": False},
                             {"name": " Dream", "oddballness": 0.0016, "corrections" : [" j", " k", " l"], "underlined": True}]

            # run pipeline here.
            return Response(response)
            #return Response(json_response)
        else:
            # TODO
            return Response({"Is everything alright? Your request shuld contain JSON with \"queryText\":\"Your query\"!"})


class HomePageView(TemplateView):
        template_name = 'home.html'
