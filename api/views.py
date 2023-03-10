from cmath import exp
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, AllowAny

from api.models import Book, Author
from api.serializers import BookSerializer, AuthorSerializer
from api.models import CurrentRent
from api.permissions import IsAdminAuthenticated


class AuthorViewset(ModelViewSet):
    """ 
    Author View
    We want to be able to perform all CRUD operations on author.
    In this case ModelViewSet is cleaner and shorter than APIView
    """
    serializer_class = AuthorSerializer

    # Only Admin can perform CRUD operations on Author
    permission_classes = [IsAdminAuthenticated]

    def get_queryset(self):
        return Author.objects.all()


class BookViewset(ModelViewSet):
    serializer_class = BookSerializer

    def get_queryset(self):
        """
        We add support for http parameters here. For complex query we may need a separate endpoint.
        Users can perform a query on the author/title/isbn to retrieve the wanted book
        ex: /api/book/?author=J.R.R Tolkien
        Returns:
            filtered queryset
        """
        queryset = Book.objects.all()
        title = self.request.GET.get('title')
        author = self.request.GET.get('author')
        isbn = self.request.GET.get('isbn')
        if title is not None:
            queryset = queryset.filter(title=title)
        if author is not None:
            try:
                author = Author.objects.get(name=author)  # raise an Error insted of returnin null values ?
            except:
                return []
            queryset = queryset.filter(author=author.id)
        if isbn is not None:
            queryset = queryset.filter(isbn=isbn)
        return queryset

    def get_permissions(self):
        # Only Admin can perform CUD operations on Book
        if self.action in ['update', 'partial_update', 'destroy', 'create']:
            self.permission_classes = [IsAdminAuthenticated, ]
        # User can perform rent and return_rent operations on Book
        elif self.action in ['rent', 'return_rent']:
            self.permission_classes = [IsAuthenticated, ]
        # Anyone can read and list Book
        else:
            self.permission_classes = [AllowAny, ]
        return super().get_permissions()

    @action(detail=True, methods=['get'])
    def rent(self, request, pk):
        """
        /api/book/{id}/rent
        GET feels the most appropriate here but i can be wrong 
        """
        book = self.get_object()
        if book.stock <= 0:
            raise PermissionDenied("This book can't be rented")
        book.rent()
        CurrentRent.objects.create(user=request.user, book=book)
        return Response({"status": "success", "message": f"You successfully rented {book.title}"})

    @action(detail=True, methods=['get'])
    def return_rent(self, request, pk):
        """
        /api/book/{id}/return_rent
        GET feels the most appropriate here but i can be wrong 
        """
        book = self.get_object()
        book.return_rent()
        try:
            # Can return more than one record so we delete the frist found record.
            CurrentRent.objects.filter(user=request.user, book=book)[0].delete()
        except IndexError:
            raise PermissionDenied(
                "You are trying to return a rented book but you didn't rent this one or it has been already returned")
        return Response({"status": "success", "message": f"You successfully returned {book.title}"})
