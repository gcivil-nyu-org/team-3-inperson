from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('login', views.LoginView.as_view(), name='login'),
    path('signup', views.SignupView.as_view(), name='signup')
]
