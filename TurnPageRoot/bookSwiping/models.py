from django.db import models
from django.contrib.auth.models import User
from location_field.forms.plain import PlainLocationField
from multiselectfield import MultiSelectField


class Profile(models.Model):
    from modelChoices import GENDER_CHOICES, ETHNICITY_CHOICES, RELIGION_CHOICES 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=24, choices=GENDER_CHOICES)
    location = PlainLocationField(
        based_fields=["city"], initial="40.790278, -73.959722"
    )
    birth_date = models.DateField(default=None)
    ethnicity = MultiSelectField(choices=ETHNICITY_CHOICES)
    religion = models.MultiSelectField(choices=RELIGION_CHOICES)  # need to build choice list for this.
    lgbtq = models.BooleanField(default=False) # will help us cater books for LGBTQ+ audiences, its not a dating app so asking specifics here probably isn't useful

    # for all this info, we should have information popups on why we're asking for it!!! VERY IMPORTANT!!!

    def __str__(self):
        return self.user + "'s Profile"

    def age(self):
        import datetime

        today = datetime.date.today()
        try:
            birthday = self.birth_date.replace(year=today.year)
        except ValueError:  # Feb 29th on non-leap years
            birthday = self.birth_date.replace(
                year=today.year, month=self.birth_date.month + 1, day=1
            )
        if birthday > today:
            return today.year - self.birth_date.year - 1
        else:
            return today.year - self.birth_date.year


# Books
class Book(models.Model):
    title = models.CharField(max_length=1024)
    # Is usually blank but we can chose to display this on the more info page when it is not.
    subtitle = models.CharField(max_length=1024, blank=True)

    # A book can have more than one author... I think we should just take the first one instead of storing a list.
    author = models.CharField(max_length=256)
    description = models.CharField(max_length=8192)

    # We will be automatically generating image links from Google Books API results
    # By pulling the book's ID and inputting here replacing <id>:
    # https://books.google.com/books/publisher/content/images/frontcover/<id>?fife=w1333-h2000&source=gbs_api
    cover_img = models.URLField(max_length=1024)  # book cover provided as a URL.
    # date_created = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    published_date = models.DateField(null=True, default=None)

    # We won't use ISBN as our ID because there are 2 ISBNs: 10 and 13... and the data might not be complete on some Books
    # We will store the ISBNs bcause these will be useful for fetching data from other services, especially if we end up building the library check.
    isbn10 = models.CharField(max_length=10, blank=True)
    isbn13 = models.CharField(max_length=13, blank=True)

    # language = models.ForeignKey(Language, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title + " by " + self.author

    # debated excluding this- what if one author wrote 2 books with the same name? But I don't know of any examples.
    class Meta:
        unique_together = ("title", "author")


# Shelf, alternatively could be called UserBooks
class Bookshelf(models.Model):
    from modelChoices import READ_CHOICES
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read_status = models.CharField(max_length=24, choices=READ_CHOICES, default=TRASH)

    def __str__(self):
        return (
            self.user.username + " - " + self.book.title + " - " + self.book.read_status
        )

    class Meta:
        unique_together = ("book", "user")


# Language is commented out in all places it is called for the time being. I have included it where necessary if we decide to use it.
"""
class Language(models.Model):
    # 2 character ISO 639-1 language code. Contains 5 characters to accommodate cases like brazilian portugese, "pt-BR"
    code = models.CharField(max_length=5, primary_key=True)
"""
