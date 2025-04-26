from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q, Avg
from rest_framework import viewsets
from .models import Book, Rental, Category, Review, Achievement, ContactMessage
from .serializers import BookSerializer, RentalSerializer
import random
from django.utils import timezone

def home(request):
    books = Book.objects.all()[:12]
    recommended_books = Book.objects.filter(available_copies__gt=0).order_by('?')[:4]
    return render(request, 'home.html', {'books': books, 'recommended_books': recommended_books})

def dashboard(request):
    books = Book.objects.all()
    rentals = Rental.objects.filter(is_returned=False)
    stats = {
        'total_books': books.count(),
        'available_books': books.filter(available_copies__gt=0).count(),
        'active_rentals': rentals.count(),
    }
    return render(request, 'dashboard.html', {'books': books, 'rentals': rentals, 'stats': stats})

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    reviews = Review.objects.filter(book=book)
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    user_review = Review.objects.filter(book=book, user=request.user).first() if request.user.is_authenticated else None
    if request.method == 'POST' and request.user.is_authenticated:
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        if rating and 1 <= int(rating) <= 5:
            if user_review:
                user_review.rating = rating
                user_review.comment = comment
                user_review.save()
                messages.success(request, "Your review has been updated!")
            else:
                Review.objects.create(user=request.user, book=book, rating=rating, comment=comment)
                messages.success(request, "Your review has been submitted!")
            return redirect('book_detail', book_id=book.id)
        else:
            messages.error(request, "Please provide a valid rating (1-5).")
    return render(request, 'book_detail.html', {
        'book': book,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'user_review': user_review
    })

def search_books(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category')
    availability = request.GET.get('availability')
    books = Book.objects.all()
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(isbn__icontains=query)
        )
    if category:
        books = books.filter(category__slug=category)
    if availability == 'available':
        books = books.filter(available_copies__gt=0)
    categories = Category.objects.all()
    return render(request, 'search_results.html', {
        'books': books,
        'query': query,
        'categories': categories,
        'selected_category': category,
        'selected_availability': availability
    })

@login_required
def rent_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        if book.available_copies > 0:
            rental = Rental.objects.create(user=request.user, book=book)
            book.available_copies -= 1
            book.save()
            messages.success(request, f"Successfully rented {book.title}")
            # Award achievements
            rental_count = Rental.objects.filter(user=request.user).count()
            if rental_count == 1:
                Achievement.objects.get_or_create(user=request.user, name="First Rental", defaults={
                    'description': "Rented your first book!"
                })
            if rental_count == 5:
                Achievement.objects.get_or_create(user=request.user, name="Bookworm", defaults={
                    'description': "Rented 5 books!"
                })
        else:
            messages.error(request, "No copies available for rental")
        return redirect('book_detail', book_id=book.id)
    return render(request, 'book_detail.html', {'book': book})

@login_required
def account(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Your password was successfully updated!")
            return redirect('account')
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordChangeForm(user=request.user)
    achievements = Achievement.objects.filter(user=request.user)
    return render(request, 'account.html', {'form': form, 'achievements': achievements})

@login_required
def rental_history(request):
    rentals = Rental.objects.filter(user=request.user).order_by('-rental_date')
    return render(request, 'rental_history.html', {'rentals': rentals})

@login_required
def return_book(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id, user=request.user)
    if request.method == 'POST' and not rental.is_returned:
        rental.is_returned = True
        rental.return_date = timezone.now()
        rental.book.available_copies += 1
        rental.book.save()
        rental.save()
        messages.success(request, f"Successfully returned {rental.book.title}")
        return redirect('rental_history')
    return redirect('rental_history')

def categories(request):
    categories = Category.objects.all()
    selected_category = request.GET.get('category')
    books = Book.objects.all()
    if selected_category:
        books = books.filter(category__slug=selected_category)
    return render(request, 'categories.html', {
        'categories': categories,
        'books': books,
        'selected_category': selected_category
    })

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        ContactMessage.objects.create(
            user=request.user if request.user.is_authenticated else None,
            name=name,
            email=email,
            message=message
        )
        messages.success(request, "Your message has been sent! We'll get back to you soon.")
        return redirect('contact')
    return render(request, 'contact.html')

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class RentalViewSet(viewsets.ModelViewSet):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer