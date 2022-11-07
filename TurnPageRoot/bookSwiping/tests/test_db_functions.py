from django.test import TestCase
from bookSwiping.models import *
from utils.db_functions import *
from datetime import datetime


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

    def test_add_to_shelf(self):
        book = Book.objects.get(title="Test1")
        user = User.objects.get(username="testuser")

        bs = addToShelf(book, user, "U")

        self.assertEqual(bs.book, book)
        self.assertEqual(bs.user, user)
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
