from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'books', views.BookViewSet, basename='book')
router.register(r'rentals', views.RentalViewSet, basename='rental')
router.register(r'reading-challenges', views.ReadingChallengeViewSet, basename='readingchallenge')
router.register(r'book-clubs', views.BookClubViewSet, basename='bookclub')
router.register(r'family-members', views.FamilyMemberViewSet, basename='familymember')

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('book/<int:book_id>/rent/', views.rent_book, name='rent_book'),
    path('search/', views.search_books, name='search_books'),
    path('account/', views.account, name='account'),
    path('rentals/', views.rental_history, name='rental_history'),
    path('rentals/return/<int:rental_id>/', views.return_book, name='return_book'),
    path('categories/', views.categories, name='categories'),
    path('contact/', views.contact, name='contact'),
    
    # New pages
    path('reading-challenge/', views.reading_challenge, name='reading_challenge'),
    path('book-clubs/', views.book_clubs, name='book_clubs'),
    path('book-clubs/<int:club_id>/', views.book_club_detail, name='book_club_detail'),
    path('recommendations/', views.recommendations, name='recommendations'),
    path('family-sharing/', views.family_sharing, name='family_sharing'),
    
    # API endpoints
    path('api/check-availability/<int:book_id>/', views.check_availability, name='check_availability'),
    path('api/get-recommendations/', views.get_recommendations, name='get_recommendations'),
    path('api/reading-progress/', views.reading_progress, name='reading_progress'),
    
    # Include router URLs only once
    path('api/', include(router.urls)),
]