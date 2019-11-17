from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
#import sys
#sys.path.append("..")
#from gpt2_proba_engine import proba_engine
from bert_proba_engine import proba_engine
# Create your views here.

class Gpt2SearchView(APIView):

    def get(self, request):
        """This function is used mainly for wget or Curl requests to generate colored output text"""
        if request.GET.get('q'):
            query = request.GET['q']
            message = 'You submitted: {}'.format(query)
            engine = proba_engine(query)
            json_response = engine.get_cumulative_search_result()
            return Response(json_response)
        else:
            return Response({'tip':'To get an example result type "curl <port>/search/?q=<query_text>"'})

    # osobna metoda by robić niewielkie zmiany - pamiętać text który był wcześniej na serwerze
    def post(self, request):
        """Used by main frontend App to deal with text."""
        if request.data:
            query = request.data["queryText"]
            engine = proba_engine(query)
            json_response = engine.get_cumulative_search_result()
            # run pipeline here.
            return Response(json_response)
        else:
            # TODO
            return Response({"Is everything alright? Your request shuld contain JSON with \"queryText\":\"Your query\"!"})


class HomePageView(TemplateView):
        template_name = 'home.html'
