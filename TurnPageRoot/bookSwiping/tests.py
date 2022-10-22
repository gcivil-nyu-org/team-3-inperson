from django.test import TestCase
import random
from . import models


class TestBookStack(TestCase):

    def test_books_can_be_created(self):
        test_book = models.Book.objects.create(title="test", published_date="2020-01-01", author="test",
                                               description="test", cover_img="test", isbn10="test", isbn13="test")
        assert test_book is not None

    def test_random_stack(self):
        book_stack = models.Book.objects.all();
        for i in range(0, 10):
            temp = models.Book.objects.create(title=str("test_" + str(i)), published_date="2020-01-01",
                                              author=str("test_" + str(i)), description="test", cover_img="test",
                                              isbn10="10", isbn13="13")
        items = list(book_stack)
        random_item = random.sample(items, 5)
        top_book = random_item[0]
        assert top_book is not None
        assert random_item[1] is not None
        assert random_item[2] is not None
        assert random_item[3] is not None
        assert random_item[4] is not None



