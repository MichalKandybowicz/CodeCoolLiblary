from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic

from django.db.models import Q


# Create your views here.


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    template_name = "book_list.html"
    model = Book

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['books_list'] = Book.objects.all()
        return context


class BookDetailView(generic.DetailView):
    model = Book
    template_name = "book_detail.html"

    def book_detail_view(request, primary_key):
        try:
            book = Book.objects.get(pk=primary_key)
        except Book.DoesNotExist:
            raise Http404('Book does not exist')

        return render(request, 'book_detail.html', context={'book': book})


class GenreListView(generic.ListView):
    template_name = "genre_list.html"
    model = Genre

    def get_context_data(self, **kwargs):
        context = super(GenreListView, self).get_context_data(**kwargs)
        context['genre_list'] = Genre.objects.all()
        return context


# TODO: generate list books with genre-name
# class GenreBooksListView(generic.DetailView):
#     template_name = "book_list.html"
#     queryset = Book.objects.all()
#
#     def genre_detail_view(request, genre_name):
#         try:
#             books = Book.objects.filter(genre__book__genre__=genre_name)
#         except Book.DoesNotExist:
#             raise Http404('Book does not exist')
#
#         return render(request, 'book_detail.html', context={'books_list': books})