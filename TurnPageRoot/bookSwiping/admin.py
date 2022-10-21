from django.contrib import admin

# Register your models here.
from .models import Book
from .models import User
from .models import Genre
from .models import BookGenre
from .models import UserGenre
from .models import Bookshelf

admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(BookGenre)
admin.site.register(UserGenre)
admin.site.register(Bookshelf)
