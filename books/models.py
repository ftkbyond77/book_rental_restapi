from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    total_copies = models.PositiveIntegerField()
    available_copies = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)

    def __str__(self):
        return self.title

class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rental_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title} - {self.rating}"

    class Meta:
        unique_together = ('user', 'book')

class Achievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    awarded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.name}"

class ContactMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.submitted_at}"
    
class ReadingChallenge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.PositiveIntegerField()
    target = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'year')
        verbose_name_plural = "Reading Challenges"

    def __str__(self):
        return f"{self.user.username}'s {self.year} Challenge ({self.completed_books()}/{self.target})"
    
    def completed_books(self):
        return self.user.rentals.filter(is_returned=True, return_date__year=self.year).count()

class BookClub(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    current_book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, blank=True)
    members = models.ManyToManyField(User, through='ClubMembership')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_clubs')
    created_at = models.DateTimeField(auto_now_add=True)
    next_meeting = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

class ClubMembership(models.Model):
    ROLE_CHOICES = [
        ('member', 'Member'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(BookClub, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'club')
    
    def __str__(self):
        return f"{self.user.username} in {self.club.name} ({self.role})"

class ClubDiscussion(models.Model):
    club = models.ForeignKey(BookClub, on_delete=models.CASCADE, related_name='discussions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username}: {self.message[:50]}..."

class FamilyRelationship(models.Model):
    RELATIONSHIP_CHOICES = [
        ('parent', 'Parent'),
        ('child', 'Child'),
        ('spouse', 'Spouse'),
        ('sibling', 'Sibling'),
        ('other', 'Other'),
    ]
    
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='family_relationships1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='family_relationships2')
    relationship = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')
        verbose_name_plural = "Family Relationships"
    
    def __str__(self):
        return f"{self.user1.username} is {self.get_relationship_display()} of {self.user2.username}"