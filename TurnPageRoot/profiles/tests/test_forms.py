from django.test import TestCase

from profiles.forms import UpdateUserForm


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
