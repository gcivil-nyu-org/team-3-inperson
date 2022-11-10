from bookSwiping.models import *
from django.test import TestCase

class GenreTest(TestCase):
    def setUp(cls):
        fiction = Genre(genre="Fiction")
        print(fiction)
        fiction.save()
    
    def test_Genre(self):
        genre = Genre.objects.get(genre="Fiction")
        self.assertEqual(str(genre), "Fiction")

