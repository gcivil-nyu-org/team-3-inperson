from django.test import TestCase

from profiles.forms import UpdateUserForm, SignUpForm, ProfileForm


class TestUpdateUserForm(TestCase):
    def test_with_valid_data(self):
        data = {
            "username": "username",
            "first_name": "firstname",
            "last_name": "lastname",
            "email": "testuser@gmail.com",
        }
        form = UpdateUserForm(data)
        self.assertTrue(form.is_valid())

    def test_with_no_username(self):
        data = {
            "username": "",
            "first_name": "firstname",
            "last_name": "lastname",
            "email": "testuser@gmail.com",
        }
        form = UpdateUserForm(data)
        self.assertFalse(form.is_valid())


class TestSignUpForm(TestCase):
    # def test_with_valid_data(self):
    #     data = {
    #         "username": "username",
    #         "first_name": "firstname",
    #         "last_name": "lastname",
    #         "email": "testuser@gmail.com",
    #     }
    #     form = SignUpForm(data)
    #     self.assertTrue(form.is_valid())

    def test_with_no_username(self):
        data = {
            "username": "",
            "first_name": "firstname",
            "last_name": "lastname",
            "email": "testuser@gmail.com",
        }
        form = SignUpForm(data)
        self.assertFalse(form.is_valid())

    def test_with_no_email(self):
        data = {
            "username": "username",
            "first_name": "firstname",
            "last_name": "lastname",
            "email": "",
        }
        form = SignUpForm(data)
        self.assertFalse(form.is_valid())


class TestProfileForm(TestCase):
    def test_with_valid_data(self):
        data = {
            "username": "username",
            "first_name": "firstname",
            "last_name": "lastname",
            "email": "testuser@gmail.com",
        }
        form = ProfileForm(data)
        self.assertTrue(form.is_valid())

    def test_with_no_username(self):
        data = {
            "username": "",
            "first_name": "firstname",
            "last_name": "lastname",
            "email": "testuser@gmail.com",
        }
        form = ProfileForm(data)
        self.assertFalse(form.is_valid())


#     def test_with_no_email(self):
#         data = {
#             "username": "username",
#             "first_name": "firstname",
#             "last_name": "lastname",
#             "email": "",
#         }
#         form = ProfileForm(data)
#         self.assertFalse(form.is_valid())

#     def test_with_no_firstname(self):
#         data = {
#             "username": "username",
#             "first_name": "",
#             "last_name": "lastname",
#             "email": "testuser@gmail.com",
#         }
#         form = ProfileForm(data)
#         self.assertFalse(form.is_valid())

#     def test_with_no_lastname(self):
#         data = {
#             "username": "username",
#             "first_name": "firstname",
#             "last_name": "",
#             "email": "testuser@gmail.com",
#         }
#         form = ProfileForm(data)
#         self.assertFalse(form.is_valid())
