from django.contrib.auth.models import User
from django.test import TestCase
from ..models import Book


class TestBookshelf(TestCase):
    def setUp(cls):
        cls.user = User.objects.create_user(
            username="jacob", email="jacob@…", password="top_secret"
        )
        cls.user.save()

        for i in range(0, 15):
            Book.objects.create(
                title=str("test_" + str(i)),
                published_date="2020-01-01",
                author=str("test_" + str(i)),
                description="test",
                cover_img="https://books.google.com/books/publisher/content/images/frontcover/WrQTEAAAQBAJ?fife=w1333-h2000&source=gbs_api",
                isbn10="10",
                isbn13="13",
            )
        cls.bookshelf_contents = Book.objects.all()

    def test_call_view_deny_anonymous(self):
        response = self.client.get("/bookshelf/")
        self.assertRedirects(
            response,
            "/profiles/login?next=/bookshelf/",
            status_code=302,
            fetch_redirect_response=True,
        )

    def test_call_view_allow_authenticated(self):
        self.client.login(username="jacob", password="top_secret")
        response = self.client.get("/bookshelf/")
        self.assertEqual(response.status_code, 200)

    def text_BookshelfView_context_data(self):
        self.client.login(username="jacob", password="top_secret")
        response = self.client.get("/bookshelf/")
        self.assertIn(response.context["bookshelf"], self.bookshelf_contents)

    def test_BookshelfView_template_used(self):
        self.client.login(username="jacob", password="top_secret")
        response = self.client.get("/bookshelf/")
        self.assertTemplateUsed(response, "bookSwiping/bookshelf.html")