from captcha.fields import CaptchaField
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm

from django.shortcuts import redirect


# Create your views here.
class UserLoginView(LoginView):
    template_name = "profiles/login.html"


class CustomUserCreationForm(UserCreationForm):
    captcha = CaptchaField()

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')


class SignupView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "profiles/signup.html"
    success_url = "/"

    # redirects to home if logged in
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("/")
        return super().get(request, *args, **kwargs)


class MyBookshelf(LoginRequiredMixin, TemplateView):
    pass


class UserProfile(LoginRequiredMixin, TemplateView):
    template_name = "profiles/user_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class LogoutInterfaceView(LogoutView):
    template_name = "profiles/logout.html"
