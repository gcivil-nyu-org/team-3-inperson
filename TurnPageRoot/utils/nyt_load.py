from utils.nytimes_api import nytapi
from utils.db_functions import loadBook
from bookSwiping.models import Book, NYT_List
from datetime import date


def loadBooklist(booklist):
    for b in booklist["books"]:
                # doesn't have published date :/
                loadBook(nytapi.make_book(b), booklist["list_name_encoded"])


def nytBookLoad(date="current"):
    booklists = nytapi.get_db_lists()
    for bl in booklists:
        books = nytapi.get_booklist(bl.list_name)
        loadBooklist(books)
    return 0


# this version uses a while loop to iterate backwards through previous booklists.
def nytMassLoad(stop_date=date.today(), date="current"):
    booklists = nytapi.get_db_lists()
    for bl in booklists:
        while date != "STOP" and (date == "current" or date >= stop_date):
            books = nytapi.get_booklist(bl.list_name, date)
            try:
                date = books["previous_published_date"]
            except:  # need to get the error type
                date = "STOP"
            loadBooklist(books)