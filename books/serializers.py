from rest_framework import serializers
from .models import (
    Book, Rental, ReadingChallenge, BookClub, 
    ClubMembership, ClubDiscussion, FamilyRelationship
)

class BookSerializer(serializers.ModelSerializer):
    cover_image = serializers.ImageField(allow_null=True, required=False)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'total_copies', 'available_copies', 'description', 'cover_image']

class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = ['id', 'user', 'book', 'rental_date', 'return_date', 'is_returned']
        
class ReadingChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingChallenge
        fields = ['id', 'year', 'target', 'created_at']
        read_only_fields = ['id', 'created_at']

class BookClubSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    current_book_title = serializers.SerializerMethodField()

    class Meta:
        model = BookClub
        fields = ['id', 'name', 'description', 'current_book', 'current_book_title', 
                 'created_by', 'created_at', 'next_meeting', 'member_count']
        read_only_fields = ['id', 'created_at', 'created_by', 'member_count']

    def get_member_count(self, obj):
        return obj.members.count()

    def get_current_book_title(self, obj):
        return obj.current_book.title if obj.current_book else None

class ClubMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubMembership
        fields = ['id', 'user', 'club', 'role', 'joined_at']
        read_only_fields = ['id', 'joined_at']

class ClubDiscussionSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = ClubDiscussion
        fields = ['id', 'club', 'user', 'username', 'message', 'created_at', 'is_owner']
        read_only_fields = ['id', 'created_at', 'user', 'username', 'is_owner']

    def get_is_owner(self, obj):
        request = self.context.get('request')
        return request and request.user == obj.user

class FamilyRelationshipSerializer(serializers.ModelSerializer):
    user1_name = serializers.CharField(source='user1.username', read_only=True)
    user2_name = serializers.CharField(source='user2.username', read_only=True)

    class Meta:
        model = FamilyRelationship
        fields = ['id', 'user1', 'user1_name', 'user2', 'user2_name', 
                 'relationship', 'created_at']
        read_only_fields = ['id', 'created_at']