from django.db import models
from django.core.exceptions import ValidationError
import re


def isbn_validator(value):
    if not re.search('^\d+$', value) or not (len(value) == 10 or len(value) == 13):
        raise ValidationError('ISBN number should contains numbers only, and its length must be 10 or 13.')


def pub_date_validator(value):
    if not re.search('^\d{4}-\d{2}-\d{2}$|^\d{4}-\d{2}$|^\d{4}$', value):
        raise ValidationError('Enter a valid date (ex. "YYYY", "YYYY-MM", "YYYY-MM-DD")')


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    pub_date = models.CharField(max_length=10, validators=[pub_date_validator], blank=True, null=True)
    isbn_number = models.CharField(max_length=13, validators=[isbn_validator], blank=True, null=True)
    page_count = models.PositiveIntegerField()
    front_cover_link = models.URLField(blank=True, null=True)
    language = models.CharField(max_length=45)

    def __str__(self):
        return f'{self.title} {self.author}'
