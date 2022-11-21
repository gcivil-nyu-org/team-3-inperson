from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from bookSwiping.models import Book, User, Bookshelf, NYT_List, UserDemographics, Genre
import requests


# This can be used from the user profile. List all genres
# call this if you see one you don't want recommended anymore


def addToShelf(book: Book, user: User, read: str):
    b = Bookshelf(book=book, user=user, read_status=read)
    try:
        b.save()
    except IntegrityError:
        # it already exists, don't need to do anything else
        # This shouldn't happen because shelf entries should never be recommended...
        # but it can, especially while we still build functionality
        return 1
    else:
        url_base = "https://8kwwql5a02.execute-api.us-east-1.amazonaws.com/dev/?"
        if read == "R":
            direc = "down"
        elif read == "U":
            direc = "right"
        else:
            direc = "left"
        url = (
            url_base
            + "bid="
            + str(book.id)
            + "&uid="
            + str(user.id)
            + "&direc="
            + direc
        )
        # print(url)
        requests.get(url)
        book.likes = len(Bookshelf.objects.filter(book=book))
        book.save()

        return Bookshelf.objects.get(book=book, user=user)


# Normally a single line of Bookshelf.delete() would do the trick
# This might be used on the bookshelf if the UserBook objects are not readily available.
def deleteFromShelf(book: Book, user: User):
    b = Bookshelf.objects.get(book=book, user=user)
    b.delete()
    book.likes = len(Bookshelf.objects.filter(book=book))
    book.save()


def loadBook(b, list=""):
    try:
        save_book = Book.objects.get(title=b.title, author=b.author)
        print(b.title + " already exists, updating")
    except ObjectDoesNotExist:
        save_book = b
        print(b.title + " added to the database")
    save_book.save()
    if list != "":
        db_list = NYT_List.objects.get(list_name=list)
        save_book.nyt_lists.add(db_list)


def addUserGenre(user: User, genre: Genre):
    try:
        ud = UserDemographics.objects.get(user=user)
    except ObjectDoesNotExist:
        ud = UserDemographics(user=user)
        ud.save()
    ud.genre.add(genre)
    return
