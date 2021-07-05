from django.urls import path
from book_list_app import views

urlpatterns = [
    path('app/book/list/', views.BookList.as_view(), name='book-list'),
]