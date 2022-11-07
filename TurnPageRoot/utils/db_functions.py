# from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from bookSwiping.models import Book, User, Bookshelf


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


def createBookGenres(categories, save_book):
    for category in categories:
        err_genres = []
        g = Genre(genre=category)
        try:
            g.save()
        except IntegrityError:
            err_genres.append(category)
        finally:
            bg = BookGenre(
                book_id=save_book,
                genre_id=Genre.objects.get(genre=category),
            )
            try:
                bg.save()
            except IntegrityError:
                pass
            except TypeError:  # this happens if the book exists, should also pass here
                pass


def loadBook(b, categories):
    try:
        save_book = Book.objects.get(title=b.title, author=b.author)
    except ObjectDoesNotExist:
        save_book = b
    save_book.save()
    createBookGenres(categories, save_book)
