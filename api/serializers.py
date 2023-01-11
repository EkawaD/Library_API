from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from api.models import Book, Author


class AuthorSerializer(ModelSerializer):

    class Meta:
        model = Author
        fields = "__all__"  # ["name"]


class BookSerializer(ModelSerializer):
    """
    Serialize our book model.
    we serialize author (wich is an id in our model) to the corresponding name for user readability.
    we could have go with author = AuthorSerializer if we want to show the id or others author's attributes.
    """
    author = serializers.CharField(source="author.name")

    def create(self, validated_data):
        """ 
        Create an author if it doesn't exist in our database. 
        Otherwise link the existing author to the book.
        """
        author = validated_data.pop('author')
        author_instance, created = Author.objects.get_or_create(name=author["name"])
        book_instance = Book.objects.create(**validated_data, author=author_instance)
        return book_instance

    def update(self, instance, validated_data):
        """ 
        Create an author if it doesn't exist in our database. 
        Otherwise link the existing author to the book.
        TODO We could refactor the duplicate logic here
        """
        author = validated_data.pop('author')
        author_instance, created = Author.objects.get_or_create(name=author["name"])
        instance.author = author_instance
        book_instance = super(BookSerializer, self).update(instance, validated_data)
        return book_instance

    class Meta:
        model = Book
        fields = "__all__"
        # fields = ["id", "author", "title", "published_at"] if we want to not display stocks.
