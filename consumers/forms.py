from django import forms
from django.contrib.auth.models import User
from .models import Feedback
from .models import Music
from musicindex.models import Registration, MusicGenre, MusicLanguage


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

class MusicUploadForm(forms.ModelForm):
    genre = forms.ModelChoiceField(
        queryset=MusicGenre.objects.all(),  # Dropdown for genre
        widget=forms.Select(attrs={'class': 'form-control'}),  # Apply styling if needed
        label='Genre'
    )
    language = forms.ModelChoiceField(
        queryset=MusicLanguage.objects.all(),  # Dropdown for language
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Language'
    )
    class Meta:
        model = Music
        fields = ['title', 'artist', 'genre', 'language', 'mood', 'release_date', 'duration', 'music_file']  # Added mood field
        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date'}),
            'duration': forms.TimeInput(attrs={'type': 'time'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Music Title'}),
            'artist': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Artist Name'}),
            'music_file': forms.FileInput(attrs={'class': 'form-control'}),
        }
class MusicSearchForm(forms.Form):
    query = forms.CharField(max_length=255, required=False, label='Search Music')

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']  # Allow users to update username and email

class RegistrationUpdateForm(forms.ModelForm):
    genre = forms.ModelMultipleChoiceField(queryset=MusicGenre.objects.all(), widget=forms.CheckboxSelectMultiple)
    language = forms.ModelMultipleChoiceField(queryset=MusicLanguage.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Registration
        fields = ['phone', 'genre', 'language']  # Allow users to update phone, genres, and languages

