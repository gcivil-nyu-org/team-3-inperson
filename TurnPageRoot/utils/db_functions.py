from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from bookSwiping.models import Book, Genre, User, UserGenre, BookGenre, Bookshelf


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
