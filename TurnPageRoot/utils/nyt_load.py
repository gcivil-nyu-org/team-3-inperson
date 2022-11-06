from utils.nytimes_api import *
from utils.amazon_affiliate import convertToAff
from bookSwiping.models import Book


def loadBooks(date="current"):
    booklists = nytapi.get_lists(date)
    for bl in booklists:
        books = nytapi.get_books(bl, date)
        for b in books["books"]:
            #doesn't have published date :/
            db_book = Book(
                title = b["title"].title(), # title case conversion bc NYT stores this in ALL CAPS
                author=b["author"],
                description=b["description"],
                cover_img=b["book_image"], # this may not be high res enough
                isbn10=b["primary_isbn10"],
                isbn13=b["primary_isbn13"],
                amazon_url=convertToAff(b["amazon_product_url"]),
            )


"""
Notes
We can potentially use the list results,
which include previous published date,
to iterate backwards through prior lists to fill the db
"""