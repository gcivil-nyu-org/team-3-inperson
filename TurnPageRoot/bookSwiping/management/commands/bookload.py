from django.core.management.base import BaseCommand, CommandError
from bookSwiping.models import Book, Genre, BookGenre
from datetime import datetime
import json
import urllib.request
import csv
import unidecode

class Command(BaseCommand):

    badchars = ["(" , ")", "'", '"', "'"]
    target = "https://www.googleapis.com/books/v1/volumes?q="

    def add_arguments(self, parser):
        parser.add_argument('book_csv', nargs='+', type=str)
        parser.add_argument('--print',action='store_true',help='print results for debugging')
        parser.add_argument('--dbload',action='store_true',help='Upload results to db')



    def handle(self, *args, **options):
        c = open(options["book_csv"][0], "r", encoding="utf8")
        checks = ["title", "authors", "publishedDate", "description", "industryIdentifiers", "categories"]
        booksCsv = csv.reader(c)
        books = list(booksCsv)
        for book in books:
            for i in range(2):
                book[i] = book[i].replace(" ", "%20")
                for char in self.badchars:
                    book[i] = book[i].replace(char, "")
            url = unidecode.unidecode(self.target+book[0]+"%20"+book[1])

            data = json.loads(urllib.request.urlopen(url).read())

            # check for data completness or move to the next entry
            inum=0
            for i in range(len(data['items'])):
                success = True
                for item in checks:
                    try:
                        data["items"][i]["volumeInfo"][item]
                    except dataMissing:
                        success = False
                        break
                if success:
                    inum = i
                    break

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
            image_url = "https://books.google.com/books/publisher/content/images/frontcover/" + google_id + "?fife=w1333-h2000&source=gbs_api"

            # date: if it isn't the right format, default to 01/01 of the given Year
            try:
                date = datetime.strptime(res["publishedDate"], '%Y-%m-%d')
            except dateNotYMD:
                try:
                    date = datetime.strptime(res["publishedDate"], '%Y-%m')
                except dateNotYM:
                    try:
                        date = datetime.strptime(res["publishedDate"], '%Y')
                    except date.NotY:
                        date = None

            b = Book(
                title=res["title"],
                subtitle=res.get('subtitle', ''),
                author=res["authors"][0],
                description=res["description"],
                cover_img=image_url,
                published_date=date,
                isbn10=isbn_10,
                isbn13=isbn_13
            )

            if (options['print'] and not (options['dbload'])):
                print(b)

            if options['dbload']:
                try:
                    save_book = Book.objects.get(title=b.title, author=b.author)
                except BookNotFound:
                    save_book = b
                save_book.save()
                print(save_book)
                print("saved")
                for category in res.get("categories",[]):
                    err_genres = []
                    g = Genre(genre=category)
                    try:
                        g.save()
                    except genreAlreadyExists:
                        err_genres.append(category)
                    finally:
                        bg = BookGenre(book_id=save_book, genre_id=Genre.objects.get(genre=category))
                        try:
                            bg.save()
                        except bookGenreExists:
                            pass
                    if len(err_genres) != 0:
                        print("The following genres already exist in the database and were not added: ")
                        print(err_genres)
                    print("\n")
        c.close()
