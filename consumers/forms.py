from django import forms
from django.contrib.auth.models import User
from .models import Feedback

# Define the rating choices as a class variable for easy access
RATING_CHOICES = [
    (1, '1 Star'),
    (2, '2 Stars'),
    (3, '3 Stars'),
    (4, '4 Stars'),
    (5, '5 Stars'),
]

class AdminUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Set the password properly
        user.is_staff = True  # Set user as admin
        user.is_superuser = True  # Set user as super admin (optional)
        if commit:
            user.save()
        return user

class FeedbackForm(forms.ModelForm):
    # Add a rating field to the FeedbackForm
    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect, label="Rating")

    class Meta:
        model = Feedback
        fields = ['feedback_text', 'rating']  # Include the rating field
        widgets = {
            'feedback_text': forms.Textarea(attrs={'placeholder': 'Enter your feedback here...'}),
        }

class ReplyForm(forms.Form):
    reply_text = forms.CharField(widget=forms.Textarea, label="Reply", max_length=500)
