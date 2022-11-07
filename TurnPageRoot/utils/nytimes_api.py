from datetime import datetime
from urllib.error import HTTPError
from bookSwiping.models import Book
from utils.amazon_affiliate import convertToAff
import urllib.request
import json
import environ
import os


class nytapi:
    url_base = "https://api.nytimes.com/svc/books/v3"
    default_date = "current"
    if "RDS_DB_NAME" in os.environ:
        api_key = os.environ["NYT_API_KEY"]
    else:
        env = environ.Env()
        environ.Env.read_env()
        api_key = env("NYT_API_KEY")

    @classmethod
    def query_nyt(self, url):
        return json.loads(urllib.request.urlopen(url).read())["results"]

    @classmethod
    def get_lists(self, date=default_date):
        # if default, we pull everything. Use the founding date of the NYT just for fun!
        if date == self.default_date:
            date = "1851-09-18"
        date = datetime.strptime(date, "%Y-%m-%d")
        url = self.url_base + "names.json?api-key=" + self.api_key
        try:
            data = self.query_nyt(url)
        except HTTPError:
            return 1
        else:
            for result in range(20):  # uses a range because we need to delete the index
                if datetime.strptime(
                    data[result]["newest_published_date"], "%Y-%m-%d"
                ) < datetime.strptime(date, "%Y-%m-%d"):
                    del data[result]
            return data

    # founding date of the NYT by default :)
    @classmethod
    def get_booklist(self, list, date=default_date):  
        if date != self.default_date:
            date = datetime.strptime(date, "%Y-%m-%d")
        url = self.url_base + date + "/" + list + ".json?api-key=" + self.api_key
        try:
            data = self.query_nyt(url)
        except HTTPError:
            return 1
        else:
            return data

    def make_book(self, b):
        book = Book(
            title=b[
                "title"
            ].title(),  # title case conversion bc NYT stores this in ALL CAPS
            author=b["author"],
            description=b["description"],
            cover_img=b["book_image"],  # this may not be high res enough
            isbn10=b["primary_isbn10"],
            isbn13=b["primary_isbn13"],
            amazon_url=convertToAff(b["amazon_product_url"]),
        )
        return book

