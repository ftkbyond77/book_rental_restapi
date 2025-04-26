from django.contrib import admin
from .models import Book, Rental, Category, Review, Achievement, ContactMessage

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