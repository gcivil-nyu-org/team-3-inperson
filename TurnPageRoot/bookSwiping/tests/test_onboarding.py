from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .. import models

class TestOnboarding(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="test", email="jacob@…", password="12345")
        # self.bookshelf = models.Bookshelf.objects.create(user=self.user, book_id=1, read_status="U")
        self.user_demo = models.UserDemographics(user=self.user)
        for i in range(0, 15):
            models.Book.objects.create(
                title=str("test_" + str(i)),
                published_date="2020-01-01",
                author=str("test_" + str(i)),
                description="test",
                cover_img="test",
                isbn10="10",
                isbn13="13",
            )
        self.all_books = models.Book.objects.all()

    def test_onboarding_view(self):
        self.client.login(username="test", password="12345")
        response = self.client.get(reverse('onboarding'))
        self.assertEqual(response.status_code, 200)

    def test_onboarding_view_post(self):
        self.client.login(username="test", password="12345")
        genres = ["fiction", "mystery", "nonfiction"]
        data = {
            "id": 2,
            "selected_genres": genres,
        }
        response = self.client.post(reverse('onboarding_genres'), data)
        self.assertEqual(response.status_code, 200)