from django.core.management.base import BaseCommand
from utils.nyt_load import *

# from utils.nytimes_api import nytapi


class Command(BaseCommand):
    def add_arguments(self, parser):
        # by default it will add all current lists
        parser.add_argument("--mass", action="store_true", help="load current lists")

    def handle(self, *args, **options):
        if options["mass"]:
            booklists = nytapi.get_db_lists().exclude(
                list_name="combined-print-and-e-book-fiction"
            )
            nytMassLoad(booklists, datetime.strptime("1700-01-01", "%Y-%m-%d").date())
        else:
            nytBookLoad()
