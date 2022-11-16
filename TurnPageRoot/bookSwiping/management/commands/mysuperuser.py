from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from profiles.models import Profile


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(username="superuser").exists():
            User.objects.create_superuser(
                "superuser", "myuser@myemail.com", "mypassword"
            )
            Profile.objects.create(
                user=User.objects.get(username="superuser"), email_confirmed=True
            )
            print("Superuser created")
        else:
            print("Custom superuser already exists")
