from bookSwiping.models import *
from django.test import TestCase


class GenreTest(TestCase):
    def setUp(cls):
        fiction = Genre(genre="Fiction")
        fiction.save()

    def test_Genre(self):
        genre = Genre.objects.get(genre="Fiction")
        self.assertEqual(str(genre), "Fiction")


class UserDemoTest(TestCase):
    def setUp(cls):
        u = User(username="john", email="john@blank.com", password="top_secret")
        u.save()
        ud = UserDemographics(user=u, birth_date="1991-10-02")
        ud.save()

    def test_age(self):
        import datetime

        today = datetime.date.today()
        u = User.objects.get(username="john")
        ud = UserDemographics.objects.get(user=u)
        test_bday = datetime.datetime.strptime("1991-10-02", "%Y-%m-%d").date()
        if test_bday > today:
            test = today.year - test_bday.year - 1
        else:
            test = today.year - test_bday.year

        self.assertEqual(ud.age(), test)
