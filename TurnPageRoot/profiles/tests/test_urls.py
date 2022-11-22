from django.test import SimpleTestCase
from django.urls import reverse, resolve
from profiles.views import ProfileView, ChangePasswordView, ActivateAccount, UserLoginView, SignupView, LogoutInterfaceView, DeleteUser, TokenSend


class TestProfileUrls(SimpleTestCase):
    def test_profile_url_is_resolved(self):
        url = reverse("profile", args=[1])
        self.assertEquals(resolve(url).func.view_class, ProfileView)

    def test_password_change_url_is_resolved(self):
        url = reverse("password_change")
        self.assertEquals(resolve(url).func.view_class, ChangePasswordView)

    def test_token_send_is_resolved(self):
        url = reverse("token")
        self.assertEquals(resolve(url).func.view_class, TokenSend)

    def test_delete_user_is_resolved(self):
        url = reverse('delete_user', args=[1])
        self.assertEquals(resolve(url).func.view_class, DeleteUser)

    def test_logout_url_is_resolved(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func.view_class, LogoutInterfaceView)

    def test_signup_url_is_resolved(self):
        url = reverse('signup')
        self.assertEquals(resolve(url).func.view_class, SignupView)

    def test_login_url_is_resolved(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func.view_class, UserLoginView)

    def test_activate_account_url_is_resolved(self):
        url = reverse('activate', args=[1, 2])
        self.assertEquals(resolve(url).func.view_class, ActivateAccount)
