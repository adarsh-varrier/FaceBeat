# consumers/models.py

from django.db import models
from django.contrib.auth.models import User

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link feedback to user
    feedback_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    reply_text = models.TextField(blank=True, null=True)  # Field to store replies
    replied_at = models.DateTimeField(blank=True, null=True)  # Optional: Timestamp for when the reply was made
    rating = models.IntegerField(default=0)  # Add a field to store rating (1 to 5)

    def __str__(self):
        return f"Feedback from {self.user.username} on {self.created_at}"

from django.db import models

class Music(models.Model):
    MOOD_CHOICES = [
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        ('fear', 'Fear'),
        ('surprised', 'Surprised'),
        ('anger', 'Anger'),
        ('relax', 'Relax'),
    ]
    
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255, blank=True)
    genre = models.CharField(max_length=100, blank=True)
    language = models.CharField(max_length=100, blank=True)
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES, blank=True)  # Added mood field
    release_date = models.DateField(blank=True, null=True)
    duration = models.TimeField(blank=True, null=True)
    music_file = models.FileField(upload_to='music/')
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


