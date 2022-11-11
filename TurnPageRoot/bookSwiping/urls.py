from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("bookshelf/", views.BookshelfView.as_view(), name="mybookshelf"),
    # the below path is to trigger the `book_like` function in views.py
    path('liked/', views.book_like, name="book_liked"),
    path('addToBookshelf/', views.book_shelf, name="addToBookshelf"),
    path("onboarding/", views.OnboardingView.as_view(), name="onboarding")
]
