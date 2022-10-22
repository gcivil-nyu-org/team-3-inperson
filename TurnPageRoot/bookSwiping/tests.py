from django.test import TestCase
from . import models

class TestBookStack(TestCase):

    def test_books_can_be_created(self):
        test_book = models.Book.objects.create(title="test", published_date="2020-01-01", author="test", description="test", cover_img="test", isbn10="test", isbn13="test")
        assert test_book is not None
