from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('genre/', views.GenreListView.as_view(), name='genre'),
    # fixme: genre/<int:pk> to genre/<str:pk> ??
    # path('genre/<int:pk>', views.GenreBooksListView.as_view(), name='genre-detail'),
]
urlpatterns += [
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
]