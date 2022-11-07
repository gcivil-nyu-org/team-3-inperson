from django.contrib import admin

# Register your models here.
from .models import *


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "published_date", "isbn10", "isbn13"]
    list_filter = ["published_date"]
    search_fields = ["title", "author", "isbn10", "isbn13"]
    date_hierarchy = "published_date"


admin.site.register(UserDemographics)
admin.site.register(Bookshelf)
admin.site.register(NYT_List)
