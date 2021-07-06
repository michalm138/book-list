from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from book_list_app import models, serializers
from functools import reduce
import operator
from django.db.models import Q
from datetime import datetime
import requests
from rest_framework.generics import ListAPIView
from rest_framework import filters
import django_filters
from django_filters import rest_framework as drf_filters


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
                reduce(operator.and_,
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


def import_book_google(request):
    context = {}

    if request.method == 'GET' and request.GET.get('keywords'):
        context['books'] = []
        keywords = request.GET.get('keywords').strip()
        response_data = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={keywords}').json()
        for item in response_data['items']:
            data = {}
            data['title'] = item['volumeInfo']['title'] if 'title' in item['volumeInfo'] else 'Unknown'
            data['author'] = item['volumeInfo']['authors'][0] if 'authors' in item['volumeInfo'] else 'Unknown'
            data['pub_date'] = item['volumeInfo']['publishedDate'] if 'publishedDate' in item['volumeInfo'] else ''
            if 'industryIdentifiers' in item['volumeInfo']:
                if item['volumeInfo']['industryIdentifiers'][0]['type'] == 'ISBN_10' or item['volumeInfo']['industryIdentifiers'][0]['type'] == 'ISBN_13':
                    data['isbn_number'] = item['volumeInfo']['industryIdentifiers'][0]['identifier']
            else:
                data['isbn_number'] = ''
            data['page_count'] = item['volumeInfo']['pageCount'] if 'pageCount' in item['volumeInfo'] else 0
            data['front_cover_link'] = item['volumeInfo']['imageLinks']['thumbnail'] if 'imageLinks' in item['volumeInfo'] else ''
            data['language'] = item['volumeInfo']['language'] if item['volumeInfo']['language'] else ''

            context['books'].append(data)
    elif request.method == 'POST':
        serializer = serializers.BookSerializer(data={
            'title': request.POST.get('title'),
            'author': request.POST.get('author'),
            'pub_date': request.POST.get('pub_date'),
            'isbn_number': request.POST.get('isbn_number'),
            'page_count': request.POST.get('page_count'),
            'front_cover_link': request.POST.get('front_cover_link'),
            'language': request.POST.get('language')
        })
        if serializer.is_valid():
            serializer.save()
            return redirect('book-list')
        else:
            context['error'] = 'Book has not been added due to incorrect data.'

    return render(request, 'import.html', context)


class BookFilter(drf_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    author = django_filters.CharFilter(field_name='author', lookup_expr='icontains')
    language = django_filters.CharFilter(field_name='language', lookup_expr='icontains')
    pub_date_start = django_filters.CharFilter(field_name='pub_date', lookup_expr='gte')
    pub_date_end = django_filters.CharFilter(field_name='pub_date', lookup_expr='lte')

    class Meta:
        model = models.Book
        fields = [
            'title',
            'author',
            'language',
        ]


class BookListApi(ListAPIView):
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer
    filter_backends = [filters.OrderingFilter, drf_filters.DjangoFilterBackend]
    filterset_class = BookFilter
    ordering_fields = []
    ordering = ['-id']
