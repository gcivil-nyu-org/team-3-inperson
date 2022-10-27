from django.test import TestCase
from bookSwiping.models import *
from utils.db_functions import *
from datetime import datetime


class UserGenreTestCase(TestCase):
    def setUp(self):
        username = "testuser"
        User.objects.create_user(
            username=username,
            email="testuser@example.com",
            password="not a real password",
        )
        Genre.objects.create(genre="Fiction")
        Genre.objects.create(genre="Biography")
        UserGenre.objects.create(
            user=User.objects.get(username=username),
            genre=Genre.objects.get(genre="Fiction"),
        )

    def test_create_usergenre(self):
        user = User.objects.get(username="testuser")
        genre = Genre.objects.get(genre="Biography")
        ug = addUserGenre(user, genre)
        self.assertEqual(ug.likes, 1)

    def test_update_existing_usergenre(self):
        user = User.objects.get(username="testuser")
        genre = Genre.objects.get(genre="Fiction")
        ug = addUserGenre(user, genre)
        self.assertEqual(ug.likes, 2)

    def test_delete_usergenre(self):
        user = User.objects.get(username="testuser")
        genre = Genre.objects.get(genre="Fiction")

        deleteUserGenre(user, genre)
        ug = UserGenre(user=user, genre=genre)
        self.assertNotIn(ug, UserGenre.objects.filter(user=user))


class BookshelfTestCase(TestCase):
    def setUp(self):
        title = "Test1"
        username = "testuser"
        User.objects.create_user(
            username=username,
            email="testuser@example.com",
            password="not a real password",
        )
        Book.objects.create(
            title=title,
            subtitle="",
            author="Testman",
            description="An epic tale about a man drinking coffee on a Tuesday afternoon. NY Times Worst Seller.",
            cover_img="https://www.letseatcake.com/wp-content/uploads/2019/10/Nancy-Drew-Fake-Book-Covers-statue.jpg",
            published_date=datetime.strptime("2020-01-01", "%Y-%m-%d"),
            isbn10="0123456789",
            isbn13="0123456789012",
        )
        testbook = Book.objects.get(title=title)
        user = User.objects.get(username=username)
        Genre.objects.create(genre="Fiction")
        Genre.objects.create(genre="Biography")
        BookGenre.objects.create(
            book=testbook, genre=Genre.objects.get(genre="Fiction")
        )
        BookGenre.objects.create(
            book=testbook, genre=Genre.objects.get(genre="Biography")
        )

        # Assign the user Fiction as a liked genre
        genre = Genre.objects.get(genre="Fiction")
        UserGenre.objects.create(user=user, genre=genre, likes=1)

    def test_add_to_shelf(self):
        book = Book.objects.get(title="Test1")
        user = User.objects.get(username="testuser")

        bs = addToShelf(book, user, "U")

        fiction = UserGenre.objects.get(
            user=user, genre=Genre.objects.get(genre="Fiction")
        )
        biography = UserGenre.objects.get(
            user=user, genre=Genre.objects.get(genre="Biography")
        )

        self.assertEqual(bs.book, book)
        self.assertEqual(bs.user, user)
        self.assertEqual(fiction.likes, 2)
        self.assertEqual(biography.likes, 1)
        self.assertEqual(book.likes, 1)

    def test_existing_book_add_to_shelf(self):
        book = Book.objects.get(title="Test1")
        user = User.objects.get(username="testuser")

        addToShelf(book, user, "U")
        dup = addToShelf(
            book, user, "R"
        )  # Using R because it shouldn't matter the read_status

        self.assertEqual(
            dup, 1
        )  # addToShelf() returns 1 when the entry exists already.

    def test_delete_from_shelf(self):
        user = User.objects.get(username="testuser")
        book = Book.objects.get(title="Test1")

        addToShelf(book, user, "U")
        deleteFromShelf(book, user)
        bs = Bookshelf(user=user, book=book)
        self.assertNotIn(bs, Bookshelf.objects.filter(user=user))
