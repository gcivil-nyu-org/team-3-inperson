from django.db import models
from django.contrib.auth.models import User
from location_field.forms.plain import PlainLocationField
from utils.age import ageCalc


class NYT_List(models.Model):
    list_name = models.CharField(max_length=256)
    display_name = models.CharField(max_length=256)
    update_schedule = models.CharField(
        max_length=8
    )  # storing this for reference, we don't really need to use it

    def __str__(self):
        return self.display_name


class Genre(models.Model):
    genre = models.CharField(max_length=128, unique=True)
    nyt_list = models.ManyToManyField(NYT_List, blank=True)

    def __str__(self):
        return self.genre


class UserDemographics(models.Model):
    from bookSwiping.modelChoices import GENDER_CHOICES

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=24, choices=GENDER_CHOICES, null=True)
    location = PlainLocationField(
        based_fields=["city"], initial="40.790278, -73.959722", null=True
    )
    birth_date = models.DateField(default=None, null=True)
    genre = models.ManyToManyField(Genre)
    following = models.ManyToManyField(User)

    def __str__(self):
        return str(self.user) + "'s Profile"

    def age(self):
        return ageCalc(self.birth_date)


# Books
class Book(models.Model):
    title = models.CharField(max_length=1024)
    # Is usually blank but we can chose to display this on the more info page when it is not.
    subtitle = models.CharField(max_length=1024, blank=True)

    # A book can have more than one author... I think we should just take the first one instead of storing a list.
    author = models.CharField(max_length=256)
    description = models.CharField(max_length=8192)
    cover_img = models.URLField(max_length=1024)  # book cover provided as a URL.
    # date_created = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    published_date = models.DateField(null=True, default=None)

    # We won't use ISBN as our ID because there are 2 ISBNs: 10 and 13... and the data might not be complete on some Books
    # We will store the ISBNs bcause these will be useful for fetching data from other services, especially if we end up building the library check.
    isbn10 = models.CharField(max_length=10, blank=True)
    isbn13 = models.CharField(max_length=13, blank=True)
    amazon_url = models.CharField(max_length=1024, blank=True)
    nyt_lists = models.ManyToManyField(NYT_List)

    # language = models.ForeignKey(Language, on_delete=models.SET_NULL)

    # tracking user likes

    def __str__(self):
        return self.title + " by " + self.author

    # debated excluding this- what if one author wrote 2 books with the same name? But I don't know of any examples.
    class Meta:
        unique_together = ("title", "author")


# Shelf, alternatively could be called UserBooks
class Bookshelf(models.Model):
    from bookSwiping.modelChoices import READ_CHOICES, TRASH

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read_status = models.CharField(max_length=24, choices=READ_CHOICES, default=TRASH)

    def __str__(self):
        return self.user.username + " - " + self.book.title + " - " + self.read_status

    class Meta:
        unique_together = ("book", "user")

class Book_Report(models.Model):
    from bookSwiping.modelChoices import BR_CATEGORY_CHOICES, BR_STATUS_CHOICES
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    category = models.CharField(max_length=24,choices=BR_CATEGORY_CHOICES)
    status = models.CharField(max_length=24, choices=BR_STATUS_CHOICES)
    report_body = models.CharField(max_length=2056)

    def __str__(self):
        return self.book.title + " - " + self.category + " - " + self.status



# Language is commented out in all places it is called for the time being. I have included it where necessary if we decide to use it.
"""
class Language(models.Model):
    # 2 character ISO 639-1 language code. Contains 5 characters to accommodate cases like brazilian portugese, "pt-BR"
    code = models.CharField(max_length=5, primary_key=True)
"""
