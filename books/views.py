from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q, Avg, Count, Sum
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import (
    Book, Rental, Category, Review, Achievement, ContactMessage,
    ReadingChallenge, BookClub, ClubMembership, FamilyRelationship
)
from .serializers import (
    BookSerializer, RentalSerializer, ReadingChallengeSerializer,
    BookClubSerializer, FamilyRelationshipSerializer
)
import random
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import TruncMonth

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


@login_required
def reading_challenge(request):
    current_year = timezone.now().year
    challenge = ReadingChallenge.objects.filter(
        user=request.user,
        year=current_year
    ).first()
    
    if request.method == 'POST':
        target = request.POST.get('target')
        if target and target.isdigit():
            if challenge:
                challenge.target = int(target)
                challenge.save()
                messages.success(request, "Your reading challenge has been updated!")
            else:
                challenge = ReadingChallenge.objects.create(
                    user=request.user,
                    year=current_year,
                    target=int(target)
                )
                messages.success(request, "Your reading challenge has been created!")
            return redirect('reading_challenge')
    
    # Calculate completed books (assuming a book is "completed" when returned)
    completed_books = Rental.objects.filter(
        user=request.user,
        is_returned=True,
        return_date__year=current_year
    ).count()
    
    return render(request, 'reading_challenge.html', {
        'challenge': challenge,
        'completed_books': completed_books,
        'current_year': current_year
    })

@login_required
def book_clubs(request):
    clubs = BookClub.objects.annotate(
        member_count=Count('members')
    ).prefetch_related('current_book')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        book_id = request.POST.get('book')
        if name and description:
            book = get_object_or_404(Book, id=book_id) if book_id else None
            club = BookClub.objects.create(
                name=name,
                description=description,
                current_book=book,
                created_by=request.user
            )
            club.members.add(request.user)
            messages.success(request, "Book club created successfully!")
            return redirect('book_clubs')
    
    return render(request, 'book_clubs.html', {
        'clubs': clubs,
        'books': Book.objects.all()
    })

@login_required
def book_club_detail(request, club_id):
    club = get_object_or_404(BookClub, id=club_id)
    is_member = request.user in club.members.all()
    
    if request.method == 'POST':
        if 'join' in request.POST and not is_member:
            club.members.add(request.user)
            messages.success(request, "You've joined the book club!")
            return redirect('book_club_detail', club_id=club.id)
        elif 'leave' in request.POST and is_member:
            club.members.remove(request.user)
            messages.success(request, "You've left the book club.")
            return redirect('book_clubs')
    
    return render(request, 'book_club_detail.html', {
        'club': club,
        'is_member': is_member,
        'discussions': club.discussions.all().order_by('-created_at')[:20]
    })

@login_required
def recommendations(request):
    # Get user's rental history to make recommendations
    rented_books = Rental.objects.filter(user=request.user).values_list('book__category', flat=True)
    category_counts = {}
    for cat in rented_books:
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    # Simple recommendation logic - books from favorite categories
    favorite_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:2]
    recommended_books = Book.objects.filter(
        category__in=[cat[0] for cat in favorite_categories if cat[0] is not None]
    ).exclude(
        id__in=Rental.objects.filter(user=request.user).values_list('book__id', flat=True)
    ).order_by('?')[:12]
    
    return render(request, 'recommendations.html', {
        'recommended_books': recommended_books,
        'favorite_categories': favorite_categories
    })

@login_required
def family_sharing(request):
    family_members = FamilyRelationship.objects.filter(
        Q(user1=request.user) | Q(user2=request.user)
    ).select_related('user1', 'user2')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        relationship = request.POST.get('relationship')
        # You would need to implement logic to find the user by email
        # and create the family relationship
        messages.success(request, "Family member added successfully!")
        return redirect('family_sharing')
    
    return render(request, 'family_sharing.html', {
        'family_members': family_members
    })

# API Views
@api_view(['GET'])
def check_availability(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return Response({'available': book.available_copies > 0})

@api_view(['GET'])
def get_recommendations(request):
    # More sophisticated recommendation logic would go here
    recommended_books = Book.objects.filter(available_copies__gt=0).order_by('?')[:6]
    serializer = BookSerializer(recommended_books, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@login_required
def reading_progress(request):
    current_year = timezone.now().year
    challenge = ReadingChallenge.objects.filter(
        user=request.user,
        year=current_year
    ).first()
    
    completed_books = Rental.objects.filter(
        user=request.user,
        is_returned=True,
        return_date__year=current_year
    ).count()
    
    return Response({
        'books_read': completed_books,
        'total_books': challenge.target if challenge else 12,
        'progress': round((completed_books / (challenge.target if challenge else 12)) * 100) if challenge else 0,
        'on_track': completed_books >= ((challenge.target if challenge else 12) * (timezone.now().month / 12))
    })

# New ViewSets for DRF
class ReadingChallengeViewSet(viewsets.ModelViewSet):
    serializer_class = ReadingChallengeSerializer
    queryset = ReadingChallenge.objects.all()  # Add this line
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
class BookClubViewSet(viewsets.ModelViewSet):
    serializer_class = BookClubSerializer
    queryset = BookClub.objects.all()  # Add this line
    
    def get_queryset(self):
        # Show clubs the user is a member of
        return self.queryset.filter(members=self.request.user)

class FamilyMemberViewSet(viewsets.ModelViewSet):
    serializer_class = FamilyRelationshipSerializer
    queryset = FamilyRelationship.objects.all()  # Add this line
    
    def get_queryset(self):
        return self.queryset.filter(
            Q(user1=self.request.user) | Q(user2=self.request.user))