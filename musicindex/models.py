from django.db import models
from django.contrib.auth.models import User

class MusicGenre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class MusicLanguage(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Registration(models.Model):
    LIVE = 1
    DELETE = 0
    DELETE_CHOICES = ((LIVE, 'Live'), (DELETE, 'Delete'))

    name = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='User_prof')
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=100, unique=True)
    genre = models.ManyToManyField(MusicGenre)  
    language = models.ManyToManyField(MusicLanguage)  
    security_question = models.CharField(max_length=255, blank=True)
    security_answer = models.CharField(max_length=255, blank=True)

    delete_status = models.IntegerField(choices=DELETE_CHOICES, default=LIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"USER: {self.name} ({self.email})"
    class Meta:
        ordering = ['created_at']
        verbose_name = "User Registration"
        verbose_name_plural = "User Registrations"
