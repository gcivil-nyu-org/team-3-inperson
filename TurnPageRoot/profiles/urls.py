from django.urls import path, include
from . import views

urlpatterns = [
    path("login", views.UserLoginView.as_view(), name="login"),
    path("logout", views.LogoutInterfaceView.as_view(), name="logout"),
    path("signup", views.SignupView.as_view(), name="signup"),
    path("user_profile", views.UserProfile.as_view(), name="user_profile"),
]
urlpatterns += [
    path('captcha/', include('captcha.urls')),
]