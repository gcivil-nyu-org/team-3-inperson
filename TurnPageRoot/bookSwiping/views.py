from django.shortcuts import render
from django.views.generic import *


# Create your views here.
class HomeView(TemplateView):
    template_name = 'bookSwiping/home.html'
    extra_context = {}
