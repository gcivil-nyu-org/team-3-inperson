from django.shortcuts import render
from django.views.generic import *
from .models import *

# Create your views here.
class HomeView(TemplateView):
    model = Book
    context_object_name = "books"
    template_name = 'bookSwiping/home.html'
    extra_context = {}

class LoginView(TemplateView):
    template_name = 'bookSwiping/login.html'
    extra_context = {}

class SignupView(TemplateView):
    template_name = 'bookSwiping/signup.html'
    extra_context = {}