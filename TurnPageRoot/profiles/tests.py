from django.test import TestCase
from django.contrib.auth.models import User


# Create your tests here.
class Test_is_user_auth(TestCase):
    def test_user(self):
        user = User.objects.create_user(username="test", password="test")
        self.client.login(username="test", password="test")
        print("Test User is authenticated correctly")
        assert user.is_authenticated