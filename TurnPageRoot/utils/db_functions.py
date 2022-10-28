from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from bookSwiping.models import Book, Genre, User, UserGenre, BookGenre, Bookshelf


# May want to make these async?
def addUserGenre(user: User, genre: Genre):
    # ug = UserGenre.objects.get(user=user, genre=genre)
    try:
        # first try to fetch from db
        ug = UserGenre.objects.get(user=user, genre=genre)
    except ObjectDoesNotExist:
        # If that fails, create a new one
        ug = UserGenre(user=user, genre=genre, likes=1)
    else:
        # if in db, add a like
        ug.likes = ug.likes + 1
    finally:
        # save the record whether new or updated
        ug.save()
        return ug


def addUserGenresFromBook(book: Book, user: User):
    for bg in BookGenre.objects.filter(book=book):
        addUserGenre(user, bg.genre)


# This can be used from the user profile. List all genres
# call this if you see one you don't want recommended anymore
def deleteUserGenre(user: User, genre: Genre):
    ug = UserGenre.objects.get(user=user, genre=genre)
    ug.delete()


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
        book.likes = len(Bookshelf.objects.filter(book=book))
        book.save()
        addUserGenresFromBook(book, user)
        return Bookshelf.objects.get(book=book, user=user)


# Normally a single line of Bookshelf.delete() would do the trick
# This might be used on the bookshelf if the UserBook objects are not readily available.
def deleteFromShelf(book: Book, user: User):
    b = Bookshelf.objects.get(book=book, user=user)
    b.delete()
    book.likes = len(Bookshelf.objects.filter(book=book))
    book.save()
