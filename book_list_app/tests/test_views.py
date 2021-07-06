from django.test import TestCase, Client
from django.urls import reverse
from book_list_app import models, serializers
import json


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

        self.book1 = models.Book.objects.create(
            id=0,
            title='string',
            author='string',
            pub_date='2021-07-06',
            isbn_number='1234567890',
            page_count=200,
            front_cover_link='',
            language='pl',
        )

        self.book2 = models.Book.objects.create(
            id=1,
            title='string1',
            author='string1',
            pub_date='2021-07-06',
            isbn_number='0987654321',
            page_count=250,
            front_cover_link='',
            language='en',
        )

    def test_api_book_list_view(self):
        response = self.client.get(reverse('book-list-api'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.dumps(response.data), json.dumps([
            {
                'id': 1,
                'title': 'string1',
                'author': 'string1',
                'pub_date': '2021-07-06',
                'isbn_number': '0987654321',
                'page_count': 250,
                'front_cover_link': '',
                'language': 'en',
            },
            {
                'id': 0,
                'title': 'string',
                'author': 'string',
                'pub_date': '2021-07-06',
                'isbn_number': '1234567890',
                'page_count': 200,
                'front_cover_link': '',
                'language': 'pl',
            }
        ]))

    def test_api_book_list_view_filtering(self):
        response = self.client.get(reverse('book-list-api'), data={
            'title': 'string',
            'author': 'string',
            'language': 'pl',
            'pub_date_start': '2021-01-01',
            'pub_date_end': '2021-12-31',
        })
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.dumps(response.data), json.dumps([
            {
                'id': 0,
                'title': 'string',
                'author': 'string',
                'pub_date': '2021-07-06',
                'isbn_number': '1234567890',
                'page_count': 200,
                'front_cover_link': '',
                'language': 'pl',
            }
        ]))
