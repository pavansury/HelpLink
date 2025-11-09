from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    bio = models.TextField(blank=True)

    def __str__(self):
        return self.full_name or self.user.username


class HelpRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Rejected', 'Rejected'),
    ]
    CATEGORY_CHOICES = [
        ('Loneliness', 'Loneliness'),
        ('Stress Handling', 'Stress Handling'),
        ('Communication', 'Communication'),
        ('Ride Sharing', 'Ride Sharing'),
        ('Electrical', 'Electrical'),
        ('Cleaning', 'Cleaning'),
        ('Pet Care', 'Pet Care'),
        ('Tutoring', 'Tutoring'),
        ('Shopping', 'Shopping'),
        ('Moving', 'Moving'),
        ('Other', 'Other'),
    ]
    
    URGENCY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='help_requests')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100)
    timeAgo = models.CharField(max_length=50, default='Just now')
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES)
    requester_name = models.CharField(max_length=100)
    requester_initials = models.CharField(max_length=5)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.title} - {self.user.username}"

