from django.urls import path, include
# from api.views import AuthorViewset, BookViewset
from rest_framework import routers


router = routers.SimpleRouter()
# router.register('author', AuthorViewset, basename='author')
# router.register('book', BookViewset, basename='book')

urlpatterns = [
    path('', include(router.urls)),
]
