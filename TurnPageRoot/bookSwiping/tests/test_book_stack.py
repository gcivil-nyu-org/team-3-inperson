from django.test import TestCase, LiveServerTestCase, RequestFactory
import random
from .. import models
from django.contrib.auth.models import AnonymousUser, User
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from .. import views


class TestBookStack(TestCase):

    def test_books_can_be_created(self):
        test_book = models.Book.objects.create(title="test", published_date="2020-01-01", author="test",
                                               description="test", cover_img="test", isbn10="test", isbn13="test")
        assert test_book is not None

    def test_random_stack(self):
        book_stack = models.Book.objects.all()
        for i in range(0, 10):
            models.Book.objects.create(title=str("test_" + str(i)), published_date="2020-01-01",
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


class TestLiveServer(LiveServerTestCase):
    def setUp(cls):
        cls.factory = RequestFactory()
        cls.user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')

        for i in range(0, 15):
            models.Book.objects.create(title=str("test_" + str(i)), published_date="2020-01-01",
                                       author=str("test_" + str(i)), description="test", cover_img="test",
                                       isbn10="10", isbn13="13")
        cls.object_list = models.Book.objects.all()

    def test_home_page(self):
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get('http://127.0.0.1:8000/')
        self.assertIn('TurnPage', driver.page_source)

    def test_size_of_random_stack(self):
        factory = self.factory
        request = factory.get('/')
        response = views.HomeView.as_view()(request)
        self.assertIsInstance(response.context_data, dict)
        self.assertEqual(response.context_data.__sizeof__(), response.context_data.__sizeof__())




