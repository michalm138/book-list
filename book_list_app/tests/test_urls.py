from django.test import SimpleTestCase
from django.urls import reverse, resolve
from book_list_app import views


class TestUrls(SimpleTestCase):

    def test_app_book_list(self):
        url = reverse('book-list')
        self.assertEquals(resolve(url).func.view_class, views.BookList)

    def test_app_book_create(self):
        url = reverse('create-book')
        self.assertEquals(resolve(url).func.view_class, views.CreateBook)

    def test_app_book_update(self):
        url = reverse('update-book', args=['0'])
        self.assertEquals(resolve(url).func.view_class, views.UpdateBook)

    def test_app_book_delete(self):
        url = reverse('delete-book', args=['0'])
        self.assertEquals(resolve(url).func.view_class, views.DeleteBook)

    def test_app_book_import(self):
        url = reverse('import-book')
        self.assertEquals(resolve(url).func, views.import_book_google)

    def test_api_book_list(self):
        url = reverse('book-list-api')
        self.assertEquals(resolve(url).func.view_class, views.BookListApi)
