import unidecode
from datetime import datetime


def formatBook(book):
    badchars = ["(", ")", "'", '"', "'"]
    target = "https://www.googleapis.com/books/v1/volumes?q="
    for i in range(2):
        book[i] = book[i].replace(" ", "%20")
        for char in badchars:
            book[i] = book[i].replace(char, "")
    return unidecode.unidecode(target + book[0] + "%20" + book[1])


def scanBooks(data, url):
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
    if "items" not in data:
        return 1  # no book found for query- skip it
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


def setDate(res):
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
