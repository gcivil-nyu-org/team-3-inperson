from captcha.fields import CaptchaField
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import View, UpdateView
from .forms import SignUpForm, ProfileForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import login
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.core import mail
from django.utils.html import strip_tags


# Create your views here.
class UserLoginView(LoginView):
    template_name = "profiles/login.html"


class CustomUserCreationForm(UserCreationForm):
    captcha = CaptchaField()

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "email")


class SignupView(View):
    form_class = SignUpForm
    template_name = "profiles/signup.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            email = form.cleaned_data["email"]
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account till it is confirmed
            user.save()

            current_site = get_current_site(request)
            subject = "Activate Your MySite Account"
            message = render_to_string(
                "profiles/emails/account_activation_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            recipient_list = [email]
            #            user.email_user(subject, message)

            email_from = settings.EMAIL_HOST_USER

            plain_message = strip_tags(message)

            mail.send_mail(
                subject, plain_message, email_from, recipient_list, html_message=message
            )

            messages.success(
                request, ("Please Confirm your email to complete registration.")
            )

            return redirect("success_email")

        return render(request, self.template_name, {"form": form})


class UserProfile(LoginRequiredMixin, TemplateView):
    template_name = "profiles/user_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request, ("Your account have been confirmed."))
            return redirect("login")
        else:
            messages.warning(
                request,
                (
                    "The confirmation link was invalid, possibly because it has already been used."
                ),
            )
            return redirect("login")


class LogoutInterfaceView(LogoutView):
    template_name = "profiles/logout.html"


class ProfileView(UpdateView):
    model = User
    form_class = ProfileForm
    success_url = reverse_lazy("login")
    template_name = "profiles/profile.html"


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = "profiles/change_password.html"
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy("login")


class DeleteUser(LoginRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    model = User
    login_url = "login"
    template_name = "profiles/delete_user.html"
    success_message = "User has been deleted"
    success_url = reverse_lazy("login")


class UserEmailSucessView(View):
    template_name = "profiles/success_email.html"
