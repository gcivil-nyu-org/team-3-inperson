from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from profiles.views import ActivateAccount, ProfileView
from profiles.views import ChangePasswordView


urlpatterns = [
    path("login", views.UserLoginView.as_view(), name="login"),
    path("logout", views.LogoutInterfaceView.as_view(), name="logout"),
    path("signup", views.SignupView.as_view(), name="signup"),
    path("user_profile", views.UserProfile.as_view(), name="user_profile"),
    path("activate/<uidb64>/<token>/", ActivateAccount.as_view(), name="activate"),
    path(
        "reset_password",
        auth_views.PasswordResetView.as_view(
            template_name="profiles/password_reset.html"
        ),
        name="reset_password",
    ),
    path(
        "reset_password_sent/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="profiles/password_reset_send.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="profiles/password_reset_form.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="profiles/password_reset_done.html"
        ),
        name="password_reset_complete",
    ),
    path("password-change", ChangePasswordView.as_view(), name="password_change"),
    path("<int:pk>/", ProfileView.as_view(), name="profile"),
    path("delete_user/<int:pk>/", views.DeleteUser.as_view(), name="delete_user"),
]
urlpatterns += [
    path("captcha/", include("captcha.urls")),
]
