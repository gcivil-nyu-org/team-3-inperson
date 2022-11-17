from utils.nytimes_api import nytapi
from utils.db_functions import loadBook
import time
from datetime import date, datetime
import logging


logging.basicConfig(level=logging.DEBUG)


def loadBooklist(booklist):
    for b in booklist["books"]:
        # doesn't have published date :/
        if nytapi.check_book(b):
            loadBook(nytapi.make_book(b), booklist["list_name_encoded"])


def nytBookLoad():
    booklists = nytapi.get_db_lists()
    for bl in booklists:
        time.sleep(6)
        books = nytapi.get_booklist(bl.list_name)
        loadBooklist(books)
    return 0


# this version uses a while loop to iterate backwards through previous booklists.
# if we hit 4000 requests it'll start failing! need to possibly work around this
def nytMassLoad(
    booklists=nytapi.get_db_lists(),
    date=date.today(),
    stop_date=datetime.strptime("1700-01-01", "%Y-%m-%d").date(),
):
    for bl in booklists:
        while date != "STOP" and (
            date == "current" or datetime.strptime(date, "%Y-%m-%d").date() >= stop_date
        ):
            time.sleep(6.5)
            logging.info(bl.list_name + " - " + date)
            print("loading list " + bl.display_name + " for date " + date)
            books = nytapi.get_booklist(bl.list_name, date)
            date = books["previous_published_date"]
            # when there is no prior date
            if date == "":
                date = "STOP"
            loadBooklist(books)
        date = "current"
    return 0
