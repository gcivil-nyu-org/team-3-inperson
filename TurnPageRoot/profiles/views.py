from captcha.fields import CaptchaField
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect


from django.views.generic import View


from profiles.models import Profile  # new
from django.shortcuts import redirect, render  # old
from django.contrib.auth.models import User  # new
from django.contrib import messages  # new
from .models import *  # new
import uuid  # new
from django.conf import settings  # new
from django.core.mail import send_mail  # new
from django.contrib.auth import authenticate, login  # new
from django.contrib.auth.decorators import login_required  # new


# Create your views here.
class UserLoginView(LoginView):
    template_name = "profiles/login.html"


class CustomUserCreationForm(UserCreationForm):
    captcha = CaptchaField()

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "email")


class SignupView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "profiles/signup.html"
    success_url = "/"

    # redirects to home if logged in
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("/")
        return super().get(request, *args, **kwargs)


class UserProfile(LoginRequiredMixin, TemplateView):
    template_name = "profiles/user_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class LogoutInterfaceView(LogoutView):
    template_name = "profiles/logout.html"


"""
class TokenView(View):
    template_name = "profiles/token_send.html"

class SuccessView(View):
    template_name = "profiles/success.html"

class ErrorView(View):
    template_name = "profiles/error.html"
"""


def SuccessView(request):
    return render(request, "success.html")


def TokenView(request):
    return render(request, "token_send.html")


def ErrorView(request):
    return render(request, "error.html")


# ======================================================================================================#

"""

@login_required
def home(request):
    return render(request , 'user_profile.html')
"""

"""
def login_attempt(request):
    if request.method == 'POST':
        username = request.POST.get({{ form.username }})
        password = request.POST.get({{ form.password }})

        user_obj = User.objects.filter(username = {{ form.password }}).first()
        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('/profiles/profiles/login')
        
        
        profile_obj = Profile.objects.filter(user = user_obj ).first()

        if not profile_obj.is_verified:
            messages.success(request, 'Profile is not verified check your mail.')
            return redirect('/profiles/profiles/login')

        user = authenticate(username = username , password = password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('/profiles/profiles/login')
        
        login(request , user)
        return redirect('/')

    return render(request , 'login.html')
"""


def login_attempt(request):
    if request.method == "POST":
        username = request.POST.get({{form.username}})
        password = request.POST.get({{form.password}})

        user_obj = User.objects.filter(username={{form.password}}).first()

        profile_obj = Profile.objects.filter(user=user_obj).first()

        if not profile_obj.is_verified:
            messages.success(request, "Profile is not verified check your mail.")
            return redirect("/profiles/profiles/login")

        user = authenticate(username={{form.username}}, password={{form.password}})
        if user is None:
            messages.success(request, "Wrong password.")
            return redirect("/profiles/profiles/login")

        login(request, user)
        return redirect("/")

    return render(request, "login.html")


"""
def register_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(password)

        try:
            if User.objects.filter(username = username).first():
                messages.success(request, 'Username is taken.')
                return redirect('/signup')

            if User.objects.filter(email = email).first():
                messages.success(request, 'Email is taken.')
                return redirect('/signup')
            
            user_obj = User(username = username , email = email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user = user_obj , auth_token = auth_token)
            profile_obj.save()
            send_mail_after_registration(email , auth_token)
            return redirect('/token')

        except Exception as e:
            print(e)

    return render(request , 'signup.html')
"""


def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, "Your account is already verified.")
                return redirect("/profiles/login")
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, "Your account has been verified.")
            return redirect("/profiles/login")
        else:
            return redirect("/error")
    except Exception as e:
        print(e)
        return redirect("/")


def send_mail_after_registration(email, token):
    subject = "Your accounts need to be verified"
    message = (
        f"Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}"
    )
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
