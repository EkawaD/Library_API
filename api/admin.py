from django.contrib import admin
from api.models import Book, Author, CurrentRent

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(CurrentRent)
