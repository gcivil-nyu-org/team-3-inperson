# Generated by Django 4.1.2 on 2022-10-22 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bookSwiping", "0003_remove_book_date_created"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="isbn10",
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name="book",
            name="isbn13",
            field=models.CharField(blank=True, max_length=13),
        ),
    ]
