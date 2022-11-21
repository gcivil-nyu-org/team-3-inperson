from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .forms import SignUpForm


# Create your tests here.
class TestIsUserAuth(TestCase):
    def setUp(self):
        self.form = SignUpForm
        self.user = User.objects.create_user(
            username="test", password="test", email="test@test.com"
        )
        self.request = self.client.get("signup")

    def test_user(self):
        self.client.login(username="test", password="test")
        assert self.user.is_authenticated

    def test_user_can_login(self):
        login = self.client.login(username="test", password="test")
        self.assertEquals(login, True)

    def test_user_cant_login_with_wrong_password(self):
        login = self.client.login(username="test", password="hfhf")
        self.assertEquals(login, False)

    def test_user_cant_see_signup_page(self):
        self.client.login(username="test", password="test")
        response = self.client.get("signup")
        assert response.status_code == 404

    def test_user_cant_see_login_page(self):
        self.client.login(username="test", password="test")
        response = self.client.get("login")
        assert response.status_code == 404

    def test_cant_login_with_username_that_is_taken(self):
        form = SignUpForm(
            {
                "username": "test",
                "first_name": "James",
                "last_name": "Joyce",
                "email": "James@Joyce.com",
                "password1": "test",
                "password2": "test",
            }
        )
        self.assertFormError(
            form, "username", "A user with that username already exists."
        )

    # def test_cant_login_with_email_that_is_taken(self):
    #
    #     form = SignUpForm(
    #         {
    #             "username": "Bloomsday2022",
    #             "first_name": "James",
    #             "last_name": "Joyce",
    #             "email": "test@test.com",
    #             "password1": "test",
    #             "password2": "test",
    #         })
    #     self.assertFormError(form, "email", "A user with that email already exists.")

    def test_form_errors(self):
        form = SignUpForm(
            {
                "username": "test",
                "first_name": "James",
                "last_name": "Joyce",
                "email": "test",
                "password1": "123",
                "password2": "123",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors["email"], ["Enter a valid email address."])

    def test_user_profile_view(self):
        self.client.login(username="test", password="test")
        response = self.client.get(reverse("user_profile"))
        self.assertTemplateUsed(response, "profiles/user_profile.html")

    def test_user_profile_context_data(self):
        self.client.login(username="test", password="test")
        response = self.client.get(reverse("user_profile"))
        self.assertEquals(response.context["user"], self.user)

    def test_signup_view(self):
        response = self.client.get(reverse("signup"))
        self.assertTemplateUsed(response, "profiles/signup.html")
