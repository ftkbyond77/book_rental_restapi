from rest_framework import serializers
from .models import Book, Rental

class BookSerializer(serializers.ModelSerializer):
    cover_image = serializers.ImageField(allow_null=True, required=False)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'total_copies', 'available_copies', 'description', 'cover_image']

class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = ['id', 'user', 'book', 'rental_date', 'return_date', 'is_returned']