from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("bookshelf/", views.BookshelfView.as_view(), name="mybookshelf"),
    # the below path is to trigger the `book_like` function in views.py
    path("liked/", views.book_like, name="book_liked"),
    path("disliked/", views.book_dislike, name="book_disliked"),
    path("addToBookshelf/", views.book_shelf, name="addToBookshelf"),
    path("onboarding/", views.OnboardingView.as_view(), name="onboarding"),
    path("onboarding/genreselection", views.selected_genres, name="onboarding_genres"),
    path(
        "bookshelf/move_to_saved_books",
        views.move_to_saved_books,
        name="move_to_saved_books",
    ),
    path(
        "bookshelf/move_to_liked_books",
        views.move_to_liked_books,
        name="move_to_liked_books",
    ),
    path("bookshelf/delete_book", views.delete_book, name="delete_book"),
]
