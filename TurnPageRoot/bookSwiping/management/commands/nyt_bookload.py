from django.core.management.base import BaseCommand
from utils.nyt_load import *
from bookSwiping.models import NYT_List

# from utils.nytimes_api import nytapi


class Command(BaseCommand):
    def add_arguments(self, parser):
        # by default it will add all current lists
        parser.add_argument("--mass", action="store_true", help="load current lists")

    def handle(self, *args, **options):
        if options["mass"]:
            booklists = [NYT_List(list_name="young-adult-hardcover", display_name="")]
            nytMassLoad(booklists, "2022-11-15")
        else:
            nytBookLoad()
