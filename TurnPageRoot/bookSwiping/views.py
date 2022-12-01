from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.generic import ListView, TemplateView
from django.core import serializers
from .models import *
from utils.db_functions import *
import random


# Create your views here.
class OnboardingView(LoginRequiredMixin, TemplateView):
    template_name = "bookSwiping/onboarding.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        genre_list = Genre.objects.all()
        # genre_list = ["Romance", "Sci-Fi", "Fantasy", "Mystery", "Young Adult", "Philosophy", "Religion", "History", "Biography"]
        context["genre_list"] = genre_list
        return context


class BookshelfView(LoginRequiredMixin, TemplateView):
    model = Book
    template_name = "bookSwiping/bookshelf.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        liked_books = []
        liked_books_database = Bookshelf.objects.all().filter(
            user=user, read_status="U"
        )
        for book in liked_books_database:
            liked_books.append(book.book)

        context["bookshelf"] = liked_books
        saved_books = []
        saved_books_database = Bookshelf.objects.all().filter(
            user=user, read_status="R"
        )

        for book in saved_books_database:
            saved_books.append(book.book)

        context["saved_books"] = saved_books
        context["liked_books_json"] = serializers.serialize("json", liked_books)
        return context


@require_POST
@login_required
def selected_genres(request):
    # user = request.user
    genre_list = request.POST.getlist("selected_genres[]")
    if genre_list:
        for genre in genre_list:
            addUserGenre(request.user, genre)
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False})


@login_required
@require_POST
def move_to_saved_books(request):
    book_id = request.POST.get("book_id")
    if book_id:
        book = Book.objects.get(id=book_id)
        moveShelf(book, request.user, "R")
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False})


@login_required
@require_POST
def move_to_liked_books(request):
    book_id = request.POST.get("book_id")
    if book_id:
        book = Book.objects.get(id=book_id)
        moveShelf(book, request.user, "U")
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False})


@login_required
@require_POST
def delete_book(request):
    book_id = request.POST.get("book_id")
    if book_id:
        book = Book.objects.get(id=book_id)
        moveShelf(book, request.user, "T")
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False})


@login_required
@require_POST
def book_shelf(request):
    user = request.user
    book_id = request.POST.get("id")
    action = request.POST.get("action")
    if book_id or action:
        try:
            # DB Functions go below
            book = Book.objects.get(id=book_id)
            # book.users_liked_list.add(request.user)
            addToShelf(book, user, "R")
            # returns JSON response
            return JsonResponse({"status": "ok"})
        except Book.DoesNotExist:
            pass
    # if fails
    return JsonResponse({"status": "error"})


@login_required
@require_POST
def book_like(request):
    # get current user
    user = request.user
    # the below commented-put line is if we want to extend the user class in the future
    # t_user = TurnPageUser.objects.get(user=user)

    # get the book id from the request
    book_id = request.POST.get("id")
    # get action, if specified in HTML
    action = request.POST.get("action")
    if book_id or action:
        try:
            # DB Functions go below
            book = Book.objects.get(id=book_id)
            # book.users_liked_list.add(request.user)
            addToShelf(book, user, "U")
            # returns JSON response
            return JsonResponse({"status": "ok"})
        except Book.DoesNotExist:
            # if book doesn't exist, do nothing... we may want to log something to the console at some point.
            pass
    # if fails
    return JsonResponse({"status": "error"})


@login_required
@require_POST
def book_dislike(request):
    # get current user
    user = request.user
    # the below commented-put line is if we want to extend the user class in the future
    # t_user = TurnPageUser.objects.get(user=user)

    # get the book id from the request
    book_id = request.POST.get("id")
    # get action, if specified in HTML
    action = request.POST.get("action")
    if book_id or action:
        try:
            # DB Functions go below
            book = Book.objects.get(id=book_id)
            addToShelf(book, user, "T")
            # returns JSON response
            return JsonResponse({"status": "ok"})
        except Book.DoesNotExist:
            # if book doesn't exist, do nothing... we may want to log something to the console at some point.
            pass
    # if fails
    return JsonResponse({"status": "error"})


class HomeView(LoginRequiredMixin, ListView):
    model = Book
    context_object_name = "books"
    template_name = "bookSwiping/home.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        all_books = self.model.objects.all()
        
        try:
            ud = UserDemographics.objects.get(user=self.request.user)
            genres = list(ud.genre.all())
            lists = []
            for g in genres:
                nyt = list(g.nyt_list.all())
                for n in nyt:
                    if n not in lists:
                        lists.append(n)
            if lists:
                items = list(self.model.objects.filter(nyt_lists__in=lists))
            else:
                items = list(self.model.objects.all())
        except ObjectDoesNotExist:
            # if any of the above aren't found, give the default
            items = list(self.model.objects.all())

        # change to how many random items you want
        random_items = random.sample(items, 15)
        # creates a list of books, random for now, from the database
        context["all_books"] = all_books
        context["book01"] = random_items[0]
        context["book02"] = random_items[1]
        context["book03"] = random_items[2]
        context["book04"] = random_items[3]
        context["book05"] = random_items[4]
        context["book06"] = random_items[5]
        context["book07"] = random_items[6]
        context["book08"] = random_items[7]
        context["book09"] = random_items[8]
        context["book10"] = random_items[9]
        context["book11"] = random_items[10]
        context["book12"] = random_items[11]
        context["book13"] = random_items[12]
        context["book14"] = random_items[13]
        context["book15"] = random_items[14]
        context["random_books"] = serializers.serialize("json", random_items)
        return context
