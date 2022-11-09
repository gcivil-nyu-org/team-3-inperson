from django.core.management.base import BaseCommand, CommandError
from utils.nyt_load import *
from utils.nytimes_api import nytapi


class Command(BaseCommand):


    def add_arguments(self, parser):
        #by default it will add all current lists
        parser.add_argument(
            "--mass", action="store_true", help="load current lists"
        )

    def handle(self, *args, **options):
        if options["mass"]:
            nytMassLoad()
        else:
            nytBookLoad()


