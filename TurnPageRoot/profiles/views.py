from datetime import datetime
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm

from django.shortcuts import redirect


# Create your views here.
class UserLoginView(LoginView):
    template_name = 'profiles/login.html'


class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = 'profiles/signup.html'
    success_url = '/'

    # redirects to home if logged in
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('/')
        return super().get(request, *args, **kwargs)


class MyBookshelf(LoginRequiredMixin, TemplateView):
    pass
