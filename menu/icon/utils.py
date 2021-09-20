from .models import *
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.cache import cache

menu = [
    {"title": "About", "url_name": "about"},
    {"title": "Add model page", "url_name": "add_page_model"},
]


class DataMixin(object):

    """Mixin for all clases that we have to
    make they shorter and fater"""
    paginate_by = 10   #needs to be queryset in function(not import tegs '{% load menu_tags %}' )  

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.all()
        woman = Woman.objects.filter(is_published=True).select_related('cat')

        user_menu = menu.copy()
        context["menu"] = user_menu
        context["cats"] = cats
        context["poster"] = woman

        return context

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form) 
      


class CapMixin(object):

    mix_prop = ""

    def get_title(self):

        return self.mix_prop.title()
