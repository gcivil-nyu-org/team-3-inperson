from django.core.management.base import BaseCommand, CommandError
from utils.nyt_load import *
from utils.nytimes_api import nytapi


class Command(BaseCommand):


    def add_arguments(self, parser):
        #by default it will add all current lists
        parser.add_argument(
            "--mass", action="store_true", help="load current lists"
        )
        parser.add_argument(
            "--list", action="store_true", help="only load one list"
        )
        parser.add_argument("list_name", nargs="+", type=str)

    def handle(self, *args, **options):
        if options["mass"]:
            nytMassLoad()
        if options["list"]:
            books = nytapi.get_booklist(options["list"][0])
            loadBooklist(books)

