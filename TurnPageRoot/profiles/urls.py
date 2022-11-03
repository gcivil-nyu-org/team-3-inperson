from django.urls import path, include
from django.contrib import admin
from . import views
from .views import *

urlpatterns = [
    path("login", views.UserLoginView.as_view(), name="login"),
    path("logout", views.LogoutInterfaceView.as_view(), name="logout"),
    path("signup", views.SignupView.as_view(), name="signup"),
    path("user_profile", views.UserProfile.as_view(), name="user_profile"),
    path("token", TokenView, name="token_sende"),
    path("success", SuccessView, name="success"),
    path("verify/<auth_token>", verify, name="verify"),
    path("error", ErrorView, name="error"),
]
urlpatterns += [
    path("captcha/", include("captcha.urls")),
]


"""
path('token' , views.TokenView.as_view() , name="token_sende"),
    path('success' , views.SuccessView.as_view() , name='success'),
    path('verify/<auth_token>' , verify , name="verify"),
    path('error' , views.ErrorView.as_view() , name="error")

"""
"""
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('' ,  home  , name="home"),
    path('register' , register_attempt , name="register_attempt"),
    path('accounts/login/' , login_attempt , name="login_attempt"),
    path('token' , token_send , name="token_send"),
    path('success' , success , name='success'),
    path('verify/<auth_token>' , verify , name="verify"),
    path('error' , error_page , name="error")

    
   
]

"""
