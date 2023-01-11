from django.db import models, transaction
from django.contrib.auth.models import User


class Author(models.Model):
    """
    Author model
    Attributes:
        name (str, 255): Should be unique. We're using a Charfield to validate the max_length at db level 
    """
    name = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Book model
    Attributes:
        author (author_id): ForeignKey to Author model. Each Book can only have one author. 
        title (str): Store the title of the book. We're using a Charfield to validate the max_length at db level 
        isbn (str): Unique identifier of our book. Should be unique and varchar(17) (https://stackoverflow.com/a/66837719/14986199)
        isbn (str): Store publication date
        stock (str): Track the current stock of a book in our library. We could have the same book in multiple copies.
    """
    author = models.ForeignKey(Author, on_delete=models.CASCADE, blank=False, null=False)
    title = models.CharField(max_length=255)
    isbn = models.CharField(unique=True, max_length=17)
    published_at = models.DateField()
    stock = models.IntegerField(default=1)

    def __str__(self):
        return self.title

    @transaction.atomic
    def rent(self):
        """
        When a book is rented we check if there's at least one available, then withdraw one from the stock.
        """
        if self.stock == 0:
            return
        self.stock = self.stock - 1
        self.save()

    @transaction.atomic
    def return_rent(self):
        """
        When a book is returned we add 1 to stock.
        """
        self.stock = self.stock + 1
        self.save()


class CurrentRent(models.Model):
    """
    CurrentRent Model
    I choose to have a separate model/entity here. We indeed need a way to track the rented books. 
    We could've add a ManyToManyRelations to User in Book model, 
    but with this other model we can separate concerns and easily serialize our data (We don't want to display the renters to the user)
    We don't want to expose this model to our API yet. 
    Attributes:
        book (book_id): ForeignKey to Book model. One rent = One record = One Book. Should'nt be blank or null.
        user (user_id): ForeignKey to Book model. One rent = One record = One User. Should'nt be blank or null.
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        """
        Human readable string representation
        """
        return self.book.title + " loaned by " + self.loaner.username
