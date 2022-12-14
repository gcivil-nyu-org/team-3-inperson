# Generated by Django 4.1.2 on 2022-11-10 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bookSwiping", "0019_book_amazon_url"),
    ]

    operations = [
        migrations.CreateModel(
            name="Genre",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("genre", models.CharField(max_length=128, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name="userdemographics",
            name="genre",
            field=models.ManyToManyField(to="bookSwiping.genre"),
        ),
    ]
