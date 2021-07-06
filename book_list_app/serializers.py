from rest_framework import serializers
from book_list_app import models


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Book
        fields = '__all__'
