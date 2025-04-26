from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'books', views.BookViewSet)
router.register(r'rentals', views.RentalViewSet)

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
    path('api/', include(router.urls)),
]