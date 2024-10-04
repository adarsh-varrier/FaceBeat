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
