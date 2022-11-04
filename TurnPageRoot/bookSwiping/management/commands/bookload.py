from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from bookSwiping.models import Book, Genre, BookGenre
from datetime import datetime
from utils.db_functions import loadBook
from utils.google_books_api import *
import json
import time
import urllib.request
import csv
import unidecode


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("book_csv", nargs="+", type=str)
        parser.add_argument(
            "--print", action="store_true", help="print results for debugging"
        )
        parser.add_argument(
            "--dbload", action="store_true", help="Upload results to db"
        )

    def handle(self, *args, **options):
        c = open(options["book_csv"][0], "r", encoding="utf8")

        books = csv.reader(c)
        for book in books:
            url = formatBook(book)
            data = json.loads(urllib.request.urlopen(url).read())
            if "items" not in data:
                continue
            inum = scanBooks(data, url)
            if inum == -1:
                continue

            google_id = data["items"][inum]["id"]
            res = data["items"][inum]["volumeInfo"]

            # parsing things before loading

            # ISBNs
            isbn_10 = ""
            isbn_13 = ""
            for id in res["industryIdentifiers"]:
                if id["type"] == "ISBN_10":
                    isbn_10 = id["identifier"]
                elif id["type"] == "ISBN_13":
                    isbn_13 = id["identifier"]
            # image link
            image_url = (
                "https://books.google.com/books/publisher/content/images/frontcover/"
                + google_id
                + "?fife=w1333-h2000&source=gbs_api"
            )

            date = setDate(res)

            b = Book(
                title=res["title"],
                subtitle=res.get("subtitle", ""),
                author=res["authors"][0],
                description=res["description"],
                cover_img=image_url,
                published_date=date,
                isbn10=isbn_10,
                isbn13=isbn_13,
            )

            time.sleep(0.25) # hopefully this stops 503 errors

            if options["print"]:
                print(b)

            if options["dbload"]:
                loadBook(b, res.get("categories", []))
            

        c.close()
