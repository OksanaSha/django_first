from django.contrib import admin
from django.urls import path, register_converter

from books.views import books_view, show_book
from books.converters import PubDateConverter

register_converter(PubDateConverter, 'p_date')

urlpatterns = [
    path('books/', books_view, name='books'),
    path('books/<p_date:book_date>', show_book, name='book'),
]