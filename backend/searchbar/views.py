from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
#import sys
#sys.path.append("..")
from proba_engines.bert_proba_engine import BertOddballnessEngine
from proba_engines.gpt2_proba_engine import Gpt2OddballnessEngine
# Create your views here.

class Gpt2SearchView(APIView):

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
            query = request.data["queryText"]
            engine = Gpt2OddballnessEngine(query)
            json_response = engine.get_sentence_oddballness()
            # run pipeline here.
            return Response(json_response)
        else:
            # TODO
            return Response({"Is everything alright? Your request shuld contain JSON with \"queryText\":\"Your query\"!"})


class HomePageView(TemplateView):
        template_name = 'home.html'
