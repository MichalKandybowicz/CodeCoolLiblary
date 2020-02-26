from django.http import Http404
from django.shortcuts import render

from catalog.models import Book, Author, BookInstance
from django.views import generic


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

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    template_name = "book_list.html"
    model = Book

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['books_list'] = Book.objects.all()
        print(context)
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
