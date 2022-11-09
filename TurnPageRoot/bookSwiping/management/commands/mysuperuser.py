from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ....profiles import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "myuser@myemail.com", "mypassword")
            models.Profile.objects.create(user=User.objects.get(username="admin"), email_confirmed=True)
            print("Superuser created")
        else:
            print("Custom superuser already exists")
