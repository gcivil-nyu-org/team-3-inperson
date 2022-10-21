from django.db import models
from django.contrib.auth.models import User

# Language is commented out in all places it is called for the time being. I have included it where necessary if we decide to use it.
"""
class Language(models.Model):
    # 2 character ISO 639-1 language code. Contains 5 characters to accommodate cases like brazilian portugese, "pt-BR"
    code = models.CharField(max_length=5, primary_key=True)
"""

# Books
class Book(models.Model):
    title = models.CharField(max_length=1024)
    subtitle = models.CharField(
        max_length=1024)  # Is usually blank but we can chose to display this on the more info page when it is not.

    # A book can have more than one author... I think we should just take the first one instead of storing a list.
    author = models.CharField(max_length=256)
    description = models.CharField(max_length=8192)

    # We will be automatically generating image links from Google Books API results
    # By pulling the book's ID and inputting here replacing <id>:
    # https://books.google.com/books/publisher/content/images/frontcover/<id>?fife=w1333-h2000&source=gbs_api
    cover_img = models.URLField(max_length=1024)  # book cover provided as a URL.
    # date_created = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    published_date = models.DateField()

    # We won't use ISBN as our ID because there are 2 ISBNs: 10 and 13... and the data might not be complete on some Books
    # We will store the ISBNs bcause these will be useful for fetching data from other services, especially if we end up building the library check.
    isbn10 = models.IntegerField()
    isbn13 = models.IntegerField()

    # language = models.ForeignKey(Language, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title + " by " + self.author


# Genres
class Genre(models.Model):
    genre = models.CharField(max_length=128)


# User Profile is imported from the django default auth model in the header and the incorrect custom model has been deleted.

# Genres for each book. Many-to-Many
class BookGenre(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE)


# User's followed genres. Many to Many
class UserGenre(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE)


# Shelf, alternatively could be called UserBooks
class Bookshelf(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    read_status = models.BooleanField()  # FALSE = want to read, TRUE = read
