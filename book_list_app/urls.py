from django.urls import path
from book_list_app import views

urlpatterns = [
    path('app/book/list/', views.BookList.as_view(), name='book-list'),
    path('app/book/create/', views.CreateBook.as_view(), name='create-book'),
    path('app/book/update/<int:pk>/', views.UpdateBook.as_view(), name='update-book'),
    path('app/book/delete/<int:pk>/', views.DeleteBook.as_view(), name='delete-book'),
    path('app/book/import/', views.import_book_google, name='import-book'),
]