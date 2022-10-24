from django.views.generic import *
from django.views.generic import ListView
from .models import *
import random


# Create your views here.
class HomeView(ListView):
    model = Book
    context_object_name = "books"
    template_name = "bookSwiping/home.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        items = list(self.model.objects.all())
        # change to how many random items you want
        random_items = random.sample(items, 2)

        context["top_book"] = random_items[0]
        context["on_deck"] = random_items[1]
        return context
