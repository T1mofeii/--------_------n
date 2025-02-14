from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.username

class Problem(models.Model):
    CATEGORY_CHOICES = [
        ('repair', 'Ремонт'),
        ('cleaning', 'Уборка'),
        ('improvement', 'Благоустройство'),
        ('other', 'Другое'),
    ]
    
    timestamp = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=200)
    description = models.TextField(verbose_name='Описание проблемы', blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image_before = models.ImageField(upload_to='problems/before/')
    image_after = models.ImageField(upload_to='problems/after/', blank=True, null=True)
    is_solved = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='problems', null=True, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return self.title