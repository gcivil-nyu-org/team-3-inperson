from django.test import SimpleTestCase
from django.urls import reverse, resolve
from profiles.views import ActivateAccount, ProfileView, ChangePasswordView, TokenSend, DeleteUser, SignupView, LogoutInterfaceView, UserLoginView



class TestUrls(SimpleTestCase):
    def test_ActivateAccount_url(self):
        url = reverse("profiles:ActivateAccount")
        # url = reverse('ActivateAccount')
        resolved = resolve(url)
        self.assertEqual(resolved.func, signup_page)
        self.assertEqual(resolved.namespace, "profiles")
        self.assertEqual(url, "/profiles/activate/uid/token/")

    def test_ProfileView_url(self):
        url = reverse("profiles:ProfileView")
        # url = reverse('ProfileView')
        resolved = resolve(url)
        self.assertEqual(resolved.func, login_page)
        self.assertEqual(resolved.namespace, "profiles")
        self.assertEqual(url, "/profiles/pk/")

    def test_ChangePasswordView_url(self):
        url = reverse("profiles:ChangePasswordView", args=["uid", "token"])
        # url = reverse('ChangePasswordView', args=['uid', 'token'])
        resolved = resolve(url)
        self.assertEqual(resolved.func, activate_account_page)
        self.assertEqual(resolved.namespace, "profiles")
        self.assertEqual(url, "/profiles/password-change/")

    def test_TokenSend_url(self):
        url = reverse("profiles:TokenSend")
        # url = reverse('TokenSend')
        resolved = resolve(url)
        self.assertEqual(resolved.func, logout_view)
        self.assertEqual(resolved.namespace, "profiles")
        self.assertEqual(url, "/profiles/token/")

    def test_DeleteUser_url(self):
        url = reverse("profiles:DeleteUser")
        # url = reverse('DeleteUser')
        resolved = resolve(url)
        self.assertEqual(resolved.func, logout_view)
        self.assertEqual(resolved.namespace, "profiles")
        self.assertEqual(url, "/profiles/delete_user/pk/")

    def test_SignupView_url(self):
        url = reverse("profiles:SignupView")
        # url = reverse('SignupView')
        resolved = resolve(url)
        self.assertEqual(resolved.func, logout_view)
        self.assertEqual(resolved.namespace, "profiles")
        self.assertEqual(url, "/profiles/signup/")

    def test_LogoutInterfaceView_url(self):
        url = reverse("profiles:LogoutInterfaceView")
        # url = reverse('LogoutInterfaceView')
        resolved = resolve(url)
        self.assertEqual(resolved.func, logout_view)
        self.assertEqual(resolved.namespace, "profiles")
        self.assertEqual(url, "/profiles/logout/")

    def test_UserLoginView_url(self):
        url = reverse("profiles:UserLoginView")
        # url = reverse('UserLoginView')
        resolved = resolve(url)
        self.assertEqual(resolved.func, logout_view)
        self.assertEqual(resolved.namespace, "profiles")
        self.assertEqual(url, "/profiles/login/")


# # from django.test import TestCase

# # class UrlTest(TestCase):

# #     def testHomePage(self):
# #         response = self.client.get('/')
# #         print(response)

# #         self.assertEqual(response.status_code, 200)

# from django.test import TestCase
# from django.urls import reverse, resolve
# from store.views import cart

# class UrlTest(TestCase):

# 	def testCartPage(self):

#     	url = reverse('cart')
#     	print("Resolve : ", resolve(url))

#     	self.assertEquals(resolve(url).func, cart)
