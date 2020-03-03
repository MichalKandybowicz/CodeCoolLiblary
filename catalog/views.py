from django.http import Http404
from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from catalog.forms import RenewBookForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
import datetime


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
    paginate_by = 10

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


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class LoanedAllBooks(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'borrowed_book_list.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )
    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'book_renew_librarian.html', context)


class BookCreate(CreateView):
    model = Book
    fields = '__all__'
    template_name = 'add_book_form.html'


@permission_required('catalog.can_mark_returned')
def borrow_book(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        form = RenewBookForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            book_instance.borrower = request.user
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.status = "o"
            book_instance.save()
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))
    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }
    print(context)

    return render(request, 'borrow_book.html', context)
