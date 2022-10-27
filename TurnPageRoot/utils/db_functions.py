from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from bookSwiping.models import Book, Genre, User, UserGenre, BookGenre, Bookshelf


# May want to make these async?
def addUserGenre(user: User, genre: Genre):
    try:
        # first try to fetch from db
        ug = UserGenre.objects.get(user=user, genre=genre)
    except IntegrityError:
        # If that fails, create a new one
        ug = UserGenre(user=user, genre=genre, likes=1)
    else:
        # if in db, add a like
        ug.likes = ug.likes + 1
    finally:
        # save the record whether new or updated
        ug.save()



def addUserGenresFromBook(book: Book, user: User):
    bookGenres = BookGenre.objects.get(book=book)
    for bg in bookGenres:
        addUserGenre(user, bg.genre)


def addToShelf(book: Book, user: User, read: bool):
    b = Bookshelf(book=book, user=user, read_status=read)
    try:
        b.save()
    except IntegrityError:
        # it already exists, don't need to do anything else
        # This shouldn't happen because shelf entries should never be recommended...
        # but it can, especially while we still build functionality
        pass
    else:
        book.likes = book.likes + 1
        book.save()
        addUserGenresFromBook(book)


# Normally a single line of Bookshelf.delete() would do the trick
# This might be used on the bookshelf if the UserBook objects are not readily available.
def deleteFromShelf(book: Book, user: User):
    b = Bookshelf.objects.get(book=book, user=user)
    b.delete()
    book.likes = book.likes - 1
    book.save()


# This can be used from the user profile. List all genres
# call this if you see one you don't want recommended anymore
def deleteUserGenre(user: User, genre: Genre):
    ug = UserGenre.objects.get(user=user, genre=genre)
    ug.delete()
