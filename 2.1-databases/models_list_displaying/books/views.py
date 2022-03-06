from django.core.paginator import Paginator
from django.http import HttpResponse, Http404
from django.shortcuts import render
import datetime

from books.models import Book

BOOKS = Book.objects.all()
PUB_DATES = sorted([book.pub_date for book in BOOKS])

def books_view(request):
    template = 'books/books_list.html'
    context = {'books': BOOKS}
    return render(request, template, context)

def show_book(request, book_date):
    _book_date = datetime.date(*[int(val) for val in book_date.split('-')])
    # dates_paginator = Paginator(PUB_DATES, 1)
    try:
        book_indx = PUB_DATES.index(_book_date)
    except ValueError:
        raise Http404()

    book = Book.objects.get(pub_date=_book_date)
    next_book = None
    prev_book = None
    if book_indx != len(PUB_DATES) - 1:
        next_date = PUB_DATES[book_indx + 1]
        next_book = Book.objects.get(pub_date=next_date)
    if book_indx != 0:
        prev_date = PUB_DATES[book_indx - 1]
        prev_book = Book.objects.get(pub_date=prev_date)

    # prev_url = prev_book.get_absolute_url()
    # next_url = prev_book.get_absolute_url()

    context = {
        'book': book,
        'next_book': next_book,
        'prev_book': prev_book
               }
    return render(request, 'books/show_book.html', context)


