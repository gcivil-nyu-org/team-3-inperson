from datetime import datetime
from urllib.error import HTTPError
from bookSwiping.models import Book, NYT_List
from utils.amazon_affiliate import convertToAff
import urllib.request
import json
import environ
import os


class nytapi:
    # there are two rate limits per API:
    # 4,000 requests per day and 10 requests per minute.
    # You should sleep 6 seconds between calls to avoid hitting
    # the per minute rate limit
    url_base = "https://api.nytimes.com/svc/books/v3/lists/"
    default_date = "current"
    if "RDS_DB_NAME" in os.environ:
        api_key = os.environ["NYT_API_KEY"]
    else:
        env = environ.Env()
        environ.Env.read_env()
        api_key = env("NYT_API_KEY")

    @classmethod
    def check_book(self, book):
        checks = [
            "title",
            "author",
            "description",
            "book_image",
            "primary_isbn10",
            "primary_isbn13",
            "amazon_product_url",
        ]
        for check in checks:
            if book[check] is None:
                return False
        return True

    @classmethod
    def query_nyt(self, url):
        return json.loads(urllib.request.urlopen(url).read())["results"]

    @classmethod
    def get_db_lists(self):
        return NYT_List.objects.all()

    # founding date of the NYT by default :)
    @classmethod
    def get_booklist(self, list, date=default_date):
        if date != self.default_date:
            date = datetime.strptime(date, "%Y-%m-%d").date()
        url = self.url_base + str(date) + "/" + list + ".json?api-key=" + self.api_key
        try:
            data = self.query_nyt(url)
        except HTTPError:
            return 1
        else:
            return data

    @classmethod
    def make_book(self, b):
        # Use NYT default image if blank. NOT A GOOD LONG TERM SOLUTION
        if b["book_image"] is None:
            img = "https://s1.nyt.com/du/books/images/default-image.png"
        else:
            img = b["book_image"]
        book = Book(
            title=b[
                "title"
            ].title(),  # title case conversion bc NYT stores this in ALL CAPS
            author=b["author"],
            description=b["description"],
            cover_img=img,  # this may not be high res enough
            isbn10=b["primary_isbn10"],
            isbn13=b["primary_isbn13"],
            amazon_url=convertToAff(b["amazon_product_url"]),
        )
        return book
