# Generated by Django 4.1.2 on 2022-10-24 23:26

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("bookSwiping", "0007_alter_book_published_date"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="bookgenre",
            unique_together={("book_id", "genre_id")},
        ),
        migrations.AlterUniqueTogether(
            name="bookshelf",
            unique_together={("book_id", "user_id")},
        ),
        migrations.AlterUniqueTogether(
            name="usergenre",
            unique_together={("user_id", "genre_id")},
        ),
    ]