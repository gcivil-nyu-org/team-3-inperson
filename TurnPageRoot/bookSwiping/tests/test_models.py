from django.test import TestCase
from django.contrib.auth.models import User
from .. import models


class TestModels(TestCase):
    object_list = []

    def setUp(self):
        self.user = User.objects.create_user(
            username="jacob", email="jacob@…", password="top_secret"
        )

    def test_user(self):
        self.assertEqual(self.user.username, "jacob")
