from django.test import TestCase
from bookSwiping.models import *
from utils.db_functions import *
from datetime import datetime


class BookshelfTestCase(TestCase):
    def setUp(self):
        titles = ["TestR", "TestU", "TestT"]
        username = "testuser"
        User.objects.create_user(
            username=username,
            email="testuser@example.com",
            password="not a real password",
        )
        for title in titles:
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

    def test_add_like_to_shelf(self):
        book = Book.objects.get(title="TestU")
        user = User.objects.get(username="testuser")

        bs = addToShelf(book, user, "U")

        self.assertEqual(bs.book, book)
        self.assertEqual(bs.user, user)
        self.assertEqual(book.likes, 1)

    def test_add_read_to_shelf(self):
        book = Book.objects.get(title="TestR")
        user = User.objects.get(username="testuser")

        bs = addToShelf(book, user, "R")

        self.assertEqual(bs.book, book)
        self.assertEqual(bs.user, user)
        self.assertEqual(book.likes, 1)

    def test_add_to_trash(self):
        book = Book.objects.get(title="TestT")
        user = User.objects.get(username="testuser")

        bs = addToShelf(book, user, "T")

        self.assertEqual(bs.book, book)
        self.assertEqual(bs.user, user)
        self.assertEqual(book.likes, 1)

    def test_existing_book_add_to_shelf(self):
        book = Book.objects.get(title="TestR")
        user = User.objects.get(username="testuser")

        addToShelf(book, user, "R")
        dup = addToShelf(
            book, user, "R"
        )  # Using R because it shouldn't matter the read_status

        self.assertEqual(
            dup, 1
        )  # addToShelf() returns 1 when the entry exists already.


    def test_move_to_new_shelf(self):
        user = User.objects.get(username="testuser")
        book = Book.objects.get(title="TestU")

        addToShelf(book, user, "U")
        moveShelf(book, user, "R")
        bs = Bookshelf(user=user, book=book, read_status="R")
        self.assertEqual(bs.book, Bookshelf.objects.filter(user=user).first().book)
        self.assertEqual(bs.user, Bookshelf.objects.filter(user=user).first().user)
        self.assertEqual(bs.read_status, Bookshelf.objects.filter(user=user).first().read_status)


    def test_move_to_trash(self):
        user = User.objects.get(username="testuser")
        book = Book.objects.get(title="TestU")
        addToShelf(book, user, "U")
        likes_before = book.likes
        moveShelf(book, user, "T")
        likes_after = book.likes
        bs = Bookshelf(user=user, book=book, read_status="T")
        self.assertEqual(bs.book, Bookshelf.objects.filter(user=user).first().book)
        self.assertEqual(bs.user, Bookshelf.objects.filter(user=user).first().user)
        self.assertEqual(bs.read_status, Bookshelf.objects.filter(user=user).first().read_status)
        self.assertEqual(likes_before-1, likes_after)


class userGenreTestCase(TestCase):
    def setUp(self):
        u1 = User(
            username="testuser1",
            email="testuser1@example.com",
            password="not a real password",
        )
        u1.save()
        u2 = User(
            username="testuser2",
            email="testuser2@example.com",
            password="not a real password",
        )
        u2.save()
        ud1 = UserDemographics(user=u1)
        ud1.save()

        g1 = Genre(genre="Fantasy")
        g1.save()
        g2 = Genre(genre="Young Adult")
        g2.save()

        ud1.genre.add(g1)

    def test_create_ud_add_genre(self):
        user = User.objects.get(username="testuser2")
        genre = Genre.objects.get(genre="Fantasy")
        addUserGenre(user, genre)
        test_ud = UserDemographics.objects.get(user=user)
        test_udg = UserDemographics.objects.filter(user=user, genre__genre="Fantasy")
        self.assertEqual(test_ud, test_udg[0])

    def test_existing_ud_add_new_genre(self):
        user = User.objects.get(username="testuser1")
        genre = Genre.objects.get(genre="Young Adult")
        addUserGenre(user, genre)
        test_ud = UserDemographics.objects.get(user=user)
        test_udg = UserDemographics.objects.filter(
            user=user, genre__genre="Young Adult"
        )
        self.assertEqual(test_ud, test_udg[0])

    def test_existing_ud_add_existing_genre(self):
        user = User.objects.get(username="testuser1")
        genre = Genre.objects.get(genre="Fantasy")
        test_udg1 = UserDemographics.objects.filter(user=user, genre__genre="Fantasy")
        addUserGenre(user, genre)
        test_udg2 = UserDemographics.objects.filter(user=user, genre__genre="Fantasy")
        self.assertEqual(test_udg1[0], test_udg2[0])
