from django.contrib import admin
from .models import (
    Book, Rental, Category, Review, Achievement, ContactMessage,
    ReadingChallenge, BookClub, ClubMembership, ClubDiscussion, FamilyRelationship
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'category', 'available_copies', 'total_copies')
    list_filter = ('author', 'category')
    search_fields = ('title', 'author', 'isbn')
    fields = ('title', 'author', 'isbn', 'category', 'total_copies', 'available_copies', 'description', 'cover_image')

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'rental_date', 'is_returned')
    list_filter = ('is_returned',)
    search_fields = ('user__username', 'book__title')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('user__username', 'book__title')

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'awarded_at')
    list_filter = ('name',)
    search_fields = ('user__username', 'name')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submitted_at', 'is_resolved')
    list_filter = ('is_resolved',)
    search_fields = ('name', 'email', 'message')
    
@admin.register(ReadingChallenge)
class ReadingChallengeAdmin(admin.ModelAdmin):
    list_display = ('user', 'year', 'target', 'created_at')
    list_filter = ('year',)
    search_fields = ('user__username',)

@admin.register(BookClub)
class BookClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'current_book', 'created_at')
    search_fields = ('name', 'created_by__username')
    # Remove filter_horizontal for 'members'
    raw_id_fields = ('current_book', 'created_by')  # Optional but helpful for large datasets
    
    # Add this to display members in admin
    filter_horizontal = ()  # Keep this empty since we can't use it with custom through model

@admin.register(ClubMembership)
class ClubMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'club', 'role', 'joined_at')
    list_filter = ('role', 'club')
    search_fields = ('user__username', 'club__name')
    raw_id_fields = ('user', 'club')  # Helpful for large datasets

@admin.register(ClubDiscussion)
class ClubDiscussionAdmin(admin.ModelAdmin):
    list_display = ('user', 'club', 'created_at', 'short_message')
    list_filter = ('club',)
    search_fields = ('user__username', 'message')
    
    def short_message(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    short_message.short_description = 'Message'

@admin.register(FamilyRelationship)
class FamilyRelationshipAdmin(admin.ModelAdmin):
    list_display = ('user1', 'relationship', 'user2', 'created_at')
    list_filter = ('relationship',)
    search_fields = ('user1__username', 'user2__username')