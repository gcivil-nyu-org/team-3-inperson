from django.test import TestCase
from bookSwiping.models import User, UserDemographics
from utils.age import ageCalc
import datetime

class ageTestCase(TestCase):
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
        u3 = User(
            username="testuser3",
            email="testuser3@example.com",
            password="not a real password",
        )
        u3.save()
        today = datetime.date.today()
        bday = today.replace(year=today.year-20)
        leap_bday = datetime.datetime.strptime("2000-02-29", "%Y-%m-%d").date()

        UserDemographics.objects.create(user=u1, birth_date=bday)
        UserDemographics.objects.create(user=u2, birth_date=leap_bday)
        UserDemographics.objects.create(user=u3)

    def test_bday(self):
        ud = UserDemographics.objects.get(user=User.objects.get(username="testuser1"))
        self.assertEqual(ageCalc(ud.birth_date), 20)

    def test_leap_bday(self):
        ud = UserDemographics.objects.get(user=User.objects.get(username="testuser2"))
        today = datetime.date.today()
        if today > today.replace(
            month=2, day=28
        ):
            age = today.year-2000
        else:
            age = today.year - 2001
        self.assertEqual(ageCalc(ud.birth_date), age)


    def test_blank_bday(self):
        ud = UserDemographics.objects.get(user=User.objects.get(username="testuser3"))
        self.assertEqual(ageCalc(ud.birth_date), -1)

    def test_ud_model_age(self):
        ud = UserDemographics.objects.get(user=User.objects.get(username="testuser1"))
        self.assertEqual(ud.age(), 20)