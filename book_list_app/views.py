from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from book_list_app import models
from functools import reduce
import operator
from django.db.models import Q
from datetime import datetime


class BookList(ListView):
    template_name = 'list.html'
    context_object_name = 'books'

    def get_queryset(self):
        data = self.request.GET
        title = data.get('title')
        author = data.get('author')
        language = data.get('language')
        pub_date_start = data.get('pub_date_start')
        pub_date_end = data.get('pub_date_end')

        query = {}

        if title:
            query['title__icontains'] = title
        if author:
            query['author__icontains'] = author
        if language:
            query['language__icontains'] = language
        if pub_date_start and pub_date_end:
            query['pub_date__range'] = (pub_date_start, pub_date_end)
        elif pub_date_start and not pub_date_end:
            query['pub_date__range'] = (pub_date_start, datetime.now().date())
        elif not pub_date_start and pub_date_end:
            query['pub_date__range'] = ('1970-01-01', pub_date_end)

        if query:
            response_data = models.Book.objects.filter(
                reduce(operator.or_,
                       (Q(q) for q in query.items()))
            ).order_by('-id')
        else:
            response_data = models.Book.objects.all().order_by('-id')

        return response_data


class CreateBook(CreateView):
    model = models.Book
    template_name = 'create.html'
    fields = [
        'title',
        'author',
        'pub_date',
        'isbn_number',
        'page_count',
        'front_cover_link',
        'language',
    ]
    success_url = '/app/book/list/'


class UpdateBook(UpdateView):
    model = models.Book
    template_name = 'update.html'
    fields = [
        'title',
        'author',
        'pub_date',
        'isbn_number',
        'page_count',
        'front_cover_link',
        'language',
    ]
    success_url = '/app/book/list/'


class DeleteBook(DeleteView):
    model = models.Book
    template_name = 'delete.html'
    success_url = '/app/book/list/'
