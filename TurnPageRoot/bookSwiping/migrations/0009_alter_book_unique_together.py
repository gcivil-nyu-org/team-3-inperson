# Generated by Django 4.1.2 on 2022-10-25 12:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("bookSwiping", "0008_alter_bookgenre_unique_together_and_more"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="book",
            unique_together={("title", "author")},
        ),
    ]
