from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
#import sys
#sys.path.append("..")
from gpt2_json import proba_engine
# Create your views here.

class Gpt2SearchView(APIView):

    def get(self, request):
        if request.GET.get('q'):
            query = request.GET['q']
            message = 'You submitted: {}'.format(query)
            engine = proba_engine(query)
            json_response = engine.get_sentence_proba() 

            return Response(json_response)

        else:
            return Response({'tip':'To get an example result type "curl <port>/search/?q=<query_text>"'})
            
        return Response({'some':message})


class HomePageView(TemplateView):
        template_name = 'home.html'
