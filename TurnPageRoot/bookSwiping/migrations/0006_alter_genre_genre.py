# Generated by Django 4.1.2 on 2022-10-24 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "bookSwiping",
            "0005_alter_bookshelf_user_id_alter_usergenre_user_id_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="genre",
            name="genre",
            field=models.CharField(max_length=128, unique=True),
        ),
    ]
