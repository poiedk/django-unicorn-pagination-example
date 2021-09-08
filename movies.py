from django_unicorn.components import UnicornView
from movies_app.models import *
from django.core.paginator import Paginator
from django.db.models import Count


class MoviesView(UnicornView):
    items_per_page = 10
    page_index = 1
    paginator = None
    page = None
    page_range = None

    class Meta:
        exclude = ()
        javascript_exclude = (
            "paginator",
            "page",
            "page_range",
        )
        
    movies = []
    movies_show_form = False

    category = ''
    categories = Categories.objects.all()

    movies_search_flag = False
    
    def mount(self):
      self.movies_list()

    def movies_list(self):
        self.page = ''
        movies_search_flag = False
        qs = Movies.objects.all()
        paginator = Paginator(qs, self.items_per_page)
        self.paginator = paginator
        self.page = self.paginator.page(self.page_index)
        self.page_range = self.paginator.get_elided_page_range(number=self.page_index, on_each_side=3, on_ends=2)
        return self.page

    def go_to_page(self, page):
        print("go_to_page")
        self.page_index = page
        if self.movies_search_flag == True:
            self.movies_search()
        else:
            self.movies_list()

    def movies_search_button(self):
        self.page_index = 1
        self.movies_search_flag = True
        self.movies_search()

    def movies_search(self):
        self.page = ''
        qs = Movies.objects.filter(speciality=self.speciality, area=self.area)
        paginator = Paginator(qs, self.items_per_page)
        self.paginator = paginator
        try:
            self.page = paginator.page(self.page_index)
            self.page_range = self.paginator.get_elided_page_range(number=self.page_index, on_each_side=3, on_ends=2)
            return self.page
        except EmptyPage:
            self.page = ''