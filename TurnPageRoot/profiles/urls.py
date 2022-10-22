from django.urls import path, include
from . import views

urlpatterns = [
    path("login", views.UserLoginView.as_view(), name="login"),
    path("signup", views.SignupView.as_view(), name="signup"),
]
urlpatterns += [
    path('captcha/', include('captcha.urls')),
]