from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from bookSwiping.models import Book, Genre, BookGenre
from datetime import datetime
import json
import urllib.request
import csv
import unidecode


class Command(BaseCommand):
    def formatBook(self, book):
        badchars = ["(", ")", "'", '"', "'"]
        target = "https://www.googleapis.com/books/v1/volumes?q="
        for i in range(2):
            book[i] = book[i].replace(" ", "%20")
            for char in badchars:
                book[i] = book[i].replace(char, "")
        return unidecode.unidecode(target + book[0] + "%20" + book[1])

    def scanBooks(self, data, url):
        checks = [
            "title",
            "authors",
            "publishedDate",
            "description",
            "industryIdentifiers",
            "categories",
        ]
        inum = 0
        success = False
        for i in range(len(data["items"])):
            success = True
            for item in checks:
                try:
                    data["items"][i]["volumeInfo"][item]
                except KeyError:
                    success = False
                    break
            if success:
                inum = i
                break
        if not success:
            print("No suitable info found querying url, skipping load: " + url)
            return -1
        else:
            return inum

    def setDate(self, res):
        try:
            return datetime.strptime(res["publishedDate"], "%Y-%m-%d")
        except ValueError:
            try:
                return datetime.strptime(res["publishedDate"], "%Y-%m")
            except ValueError:
                try:
                    return datetime.strptime(res["publishedDate"], "%Y")
                except ValueError:
                    return None

    def loadBook(self, b, categories):
        try:
            save_book = Book.objects.get(title=b.title, author=b.author)
        except ObjectDoesNotExist:
            save_book = b
        save_book.save()
        print(save_book)
        print("saved")
        for category in categories:
            err_genres = []
            g = Genre(genre=category)
            try:
                g.save()
            except IntegrityError:
                err_genres.append(category)
            finally:
                bg = BookGenre(
                    book_id=save_book,
                    genre_id=Genre.objects.get(genre=category),
                )
                try:
                    bg.save()
                except IntegrityError:
                    pass
            if len(err_genres) != 0:
                print(
                    "The following genres already exist in the database and were not added: "
                )
                print(err_genres)
            print("\n")

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
            url = self.formatBook(book)
            data = json.loads(urllib.request.urlopen(url).read())
            inum = self.scanBooks(data, url)
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

            date = self.setDate(res)

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

            if options["print"] and not (options["dbload"]):
                print(b)

            if options["dbload"]:
                self.loadBook(b, res.get("categories", []))

        c.close()
