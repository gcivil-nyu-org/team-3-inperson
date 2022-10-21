from django.shortcuts import render
from django.views.generic import *
from .models import *


# Create your views here.
class HomeView(ListView):
    model = Book
    context_object_name = "books"
    template_name = 'bookSwiping/home.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_book'] = self.model.objects.order_by('?')[0]
        context['on_deck'] = self.model.objects.order_by('?')[1]
        return context



class LoginView(TemplateView):
    template_name = 'bookSwiping/login.html'
    extra_context = {}


class SignupView(TemplateView):
    template_name = 'bookSwiping/signup.html'
    extra_context = {}
