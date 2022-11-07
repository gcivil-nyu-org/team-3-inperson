from utils.nytimes_api import *
from utils.db_functions import loadBook
from bookSwiping.models import Book
from datetime import date


def nytBookLoad(date="current"):
    booklists = nytapi.get_lists(date)
    for bl in booklists:
        books = nytapi.get_booklist(bl, date)
        for b in books["books"]:
            # doesn't have published date :/
            db_book = nytapi.make_book(b)
            loadBook(db_book)
    return 0


# this version uses a while loop to iterate backwards through previous booklists.
def nytMassLoad(stop_date=date.today(), date="current"):
    booklists = nytapi.get_lists(date)
    for bl in booklists:
        while date != "STOP" and (date == "current" or date >= stop_date):
            books = nytapi.get_booklist(bl, date)
            try:
                date = books["previous_published_date"]
            except:  # need to get the error type
                date = "STOP"
            for b in books["books"]:
                # doesn't have published date :/
                db_book = nytapi.make_book(b)
                loadBook(db_book)
