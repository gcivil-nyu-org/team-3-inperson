# Generated by Django 4.1.2 on 2022-11-07 19:14

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("bookSwiping", "0016_rename_nyt_lists_book_nyt_lists"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Profile",
            new_name="UserDemographics",
        ),
    ]
