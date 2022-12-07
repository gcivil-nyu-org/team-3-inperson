from django.test import TestCase, LiveServerTestCase, RequestFactory, Client
import random
from .. import models
from django.contrib.auth.models import User
import environ
from django.urls import reverse
from .. import views
from bookSwiping.models import UserDemographics, Genre, NYT_List
from datetime import date

# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager


# from django.middleware import csrf


class TestUserBookInteraction(LiveServerTestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="test", email="jacob@…", password="12345"
        )

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
        self.object_list = models.Book.objects.all()

        self.env = environ.Env()
        environ.Env.read_env()


class TestBookStack(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="test", email="jacob@…", password="12345"
        )

        self.user2 = User.objects.create_user(
            username="test2", email="jacob@…", password="12345"
        )

        self.user3 = User.objects.create_user(
            username="test-blank", email="jacob@…", password="12345"
        )

        self.ud = UserDemographics.objects.create(
            user=self.user,
            gender="M",
            birth_date=date.today().replace(year=1991),
        )

        self.ud2 = UserDemographics.objects.create(
            user=self.user2,
            gender="M",
            birth_date=date.today().replace(year=1991),
        )

        self.list_hf = NYT_List.objects.create(
            list_name="hardcover-fiction",
            display_name="Hardcover Fiction",
            update_schedule="WEEKLY",
        )

        genres = [
            "Dystopian",
            "Fantasy",
            "Fiction",
        ]

        genres_nolist = ["Children", "Cooking", "LGBTQ+"]

        for g in genres:
            gen = Genre.objects.create(genre=g)
            gen.nyt_list.add(self.list_hf)
            self.ud.genre.add(gen)

        for g in genres_nolist:
            gen = Genre.objects.create(genre=g)
            self.ud2.genre.add(gen)

        for i in range(0, 15):
            b = models.Book.objects.create(
                title=str("test_" + str(i)),
                published_date="2020-01-01",
                author=str("test_" + str(i)),
                description="test",
                cover_img="test",
                isbn10="10" + str(i),
                isbn13="13" + str(i),
            )
            b.nyt_lists.add(self.list_hf)
        self.object_list = models.Book.objects.all()

    def test_books_can_be_created(self):
        test_book = models.Book.objects.create(
            title="test",
            published_date="2020-01-01",
            author="test",
            description="test",
            cover_img="test",
            isbn10="test",
            isbn13="test",
        )
        assert test_book is not None

    def test_random_stack(self):
        book_stack = self.object_list
        items = list(book_stack)
        random_item = random.sample(items, 5)
        top_book = random_item[0]
        assert top_book is not None
        assert random_item[1] is not None
        assert random_item[2] is not None
        assert random_item[3] is not None
        assert random_item[4] is not None

    def test_books_in_context_for_HomeView(self):
        self.client.login(username="test", password="12345")
        response = self.client.get(reverse("home"))
        self.assertIn("book01", response.context)
        self.assertIn("book02", response.context)
        self.assertIn("book03", response.context)
        self.assertIn("book04", response.context)
        self.assertIn("book05", response.context)
        self.assertIn("book06", response.context)
        self.assertIn("book07", response.context)
        self.assertIn("book08", response.context)
        self.assertIn("book09", response.context)
        self.assertIn("book10", response.context)
        self.assertIn("book11", response.context)
        self.assertIn("book12", response.context)
        self.assertIn("book13", response.context)
        self.assertIn("book14", response.context)

    def test_book_in_context_view_is_in_database(self):
        self.client.login(username="test2", password="12345")
        response = self.client.get(reverse("home"))
        assert response.context["book01"] in self.object_list
        assert response.context["book02"] in self.object_list
        assert response.context["book03"] in self.object_list
        assert response.context["book04"] in self.object_list
        assert response.context["book05"] in self.object_list
        assert response.context["book06"] in self.object_list
        assert response.context["book07"] in self.object_list
        assert response.context["book08"] in self.object_list
        assert response.context["book09"] in self.object_list
        assert response.context["book10"] in self.object_list
        assert response.context["book11"] in self.object_list
        assert response.context["book12"] in self.object_list
        assert response.context["book13"] in self.object_list
        assert response.context["book14"] in self.object_list

    def test_book_like_view(self):
        self.client.login(username="test", password="12345")
        request = self.factory.get(reverse("book_liked"))
        request.user = self.user

        response = views.book_like(request)
        assert response.status_code != 200

    def test_book_in_context_view_is_in_database_empty_list(self):
        self.client.login(username="test2", password="12345")
        response = self.client.get(reverse("home"))
        assert response.context["book01"] in self.object_list
        assert response.context["book02"] in self.object_list
        assert response.context["book03"] in self.object_list
        assert response.context["book04"] in self.object_list
        assert response.context["book05"] in self.object_list
        assert response.context["book06"] in self.object_list
        assert response.context["book07"] in self.object_list
        assert response.context["book08"] in self.object_list
        assert response.context["book09"] in self.object_list
        assert response.context["book10"] in self.object_list
        assert response.context["book11"] in self.object_list
        assert response.context["book12"] in self.object_list
        assert response.context["book13"] in self.object_list
        assert response.context["book14"] in self.object_list

    def test_book_in_context_view_is_in_database_no_userdemo(self):
        self.client.login(username="test-blank", password="12345")
        response = self.client.get(reverse("home"))
        assert response.context["book01"] in self.object_list
        assert response.context["book02"] in self.object_list
        assert response.context["book03"] in self.object_list
        assert response.context["book04"] in self.object_list
        assert response.context["book05"] in self.object_list
        assert response.context["book06"] in self.object_list
        assert response.context["book07"] in self.object_list
        assert response.context["book08"] in self.object_list
        assert response.context["book09"] in self.object_list
        assert response.context["book10"] in self.object_list
        assert response.context["book11"] in self.object_list
        assert response.context["book12"] in self.object_list
        assert response.context["book13"] in self.object_list
        assert response.context["book14"] in self.object_list


class TestLiveServer(LiveServerTestCase):
    def setUp(cls):
        cls.factory = RequestFactory()
        cls.user = User.objects.create_user(
            username="jacob", email="jacob@…", password="top_secret"
        )

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
        cls.object_list = models.Book.objects.all()

    """def test_home_page(self):
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.implicitly_wait(10)
        driver.get(self.live_server_url)
        self.assertIn("TurnPage", driver.page_source)"""

    # def test_size_of_random_stack(self):
    #     factory = self.factory
    #     request = factory.get("/")
    #     response = views.HomeView.as_view()(request)
    #     self.assertIsInstance(response.context_data, dict)
    #     self.assertEqual(
    #         response.context_data.__sizeof__(), response.context_data.__sizeof__()
    #     )
