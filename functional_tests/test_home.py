from selenium import webdriver
from bookSwiping.models import Book, Genre, User, BookGenre, UserGenre, Bookshelf
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse


class TestProjectHomePage(StaticLiveServerTestCase):
	def setup(self):
		self.browser = webdriver.Chrome('functional_tests/chromedriver.exe')

	def tearDown(self):
		self.browser.close()

    """
	def test_no_webpage_displayed(self):
		self.browser.get(self.live_server_url)
		alert = self.browser.find_element_by_class_name('')
		self.assertEquals(
            alert.find_element_by_tag_name('').text,
            'Your web page did not run'
			)

	def test_page_taking_to_login_page(self):
		self.browser.get(self.live_server_url)

		add_url = self.live_server_url + reverse('login')
		self.browser.find_element_by_tag_name('a').click()
		self.assertEquals(
               self.browser.current_url,
               add_url
			)
	"""