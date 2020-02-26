from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), {'my_template_name': 'some_path'}, name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), {'my_template_name': 'another_path'}, name='book-detail'),

]
