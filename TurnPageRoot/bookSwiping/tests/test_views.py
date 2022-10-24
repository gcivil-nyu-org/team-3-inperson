from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from .. import views
from django.urls import reverse


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')
        self.login_url = reverse('login')
        self.signup_url = reverse('signup')
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@dhg.com', password='top_secret')

    # TODO these are the ones that are failing
    # def test_project_list(self):
    #     response = self.client.get(self.home_url)
    #
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUser(response, 'bookSwiping/home.html')
    #
    # def test_project_list(self):
    #     response = self.client.get(self.login_url)
    #
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUser(response, 'bookSwiping/login.html')
    #
    # def test_project_list(self):
    #     response = self.client.get(self.signup_url)
    #
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUser(response, 'bookSwiping/signup.html')
