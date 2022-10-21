from django.contrib import admin
from .models import *

# Register your models here.
from .models import Book
from .models import User
from .models import Genre
from .models import BookGenre
from .models import UserGenre
from .models import Bookshelf

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # list_display = ['title', 'author', 'published_date', 'date_created', 'isbn10', 'isbn13']
    # list_filter = ['published_date', 'date_created']
    search_fields = ['title', 'author', 'isbn10', 'isbn13']
    date_hierarchy = 'published_date'
    # ordering = ['published_date', 'date_created']


# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ['name', 'email']
#     search_fields = ['name', 'email']

admin.site.register(Genre)
admin.site.register(BookGenre)
admin.site.register(UserGenre)
admin.site.register(Bookshelf)
