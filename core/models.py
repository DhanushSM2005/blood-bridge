from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    BLOOD_GROUPS = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]
    
    full_name = models.CharField(max_length=200)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    city = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    phone = models.CharField(max_length=15, blank=True)
    
    class Meta:
        db_table = 'users'

class BloodRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    
    EMERGENCY_LEVELS = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]
    
    request_id = models.CharField(max_length=20, unique=True)
    blood_group = models.CharField(max_length=3)
    units_required = models.IntegerField()
    hospital_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    emergency_level = models.CharField(max_length=20, choices=EMERGENCY_LEVELS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assignments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        db_table = 'blood_requests'
        ordering = ['-created_at']
      