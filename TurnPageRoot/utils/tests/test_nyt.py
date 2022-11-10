from django.test import TestCase
from utils.nytimes_api import *
from utils.nyt_load import *
from bookSwiping.models import Book, NYT_List


class TestNytLoad(TestCase):
    def setUp(cls):
        n = NYT_List(
            list_name="hardcover-fiction",
            display_name="Hardcover Fiction",
            update_schedule="WEEKLY",
        )
        n.save()
        nytBookLoad()

    # booklist = nytapi.get_booklist("hardcover-fiction")
    # loadBooklist(booklist)
    # print(Book.objects.all())

    def test_bookLoad(self):
        self.assertGreater(Book.objects.filter(nyt_lists__isnull=False).count(), 0)
