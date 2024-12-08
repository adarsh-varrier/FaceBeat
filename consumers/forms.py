from django import forms
from django.contrib.auth.models import User
from .models import Feedback
from .models import Music
from musicindex.models import Registration, MusicGenre, MusicLanguage



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
        user.set_password(self.cleaned_data['password']) 
        user.is_staff = True  
        user.is_superuser = True  
        if commit:
            user.save()
        return user

class FeedbackForm(forms.ModelForm):
    # Add a rating field to the FeedbackForm
    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect, label="Rating")

    class Meta:
        model = Feedback
        fields = ['feedback_text', 'rating']  
        widgets = {
            'feedback_text': forms.Textarea(attrs={'placeholder': 'Enter your feedback here...'}),
        }

class ReplyForm(forms.Form):
    reply_text = forms.CharField(widget=forms.Textarea, label="Reply", max_length=500)

class MusicUploadForm(forms.ModelForm):
    genre = forms.ModelChoiceField(
        queryset=MusicGenre.objects.all(),  
        widget=forms.Select(attrs={'class': 'form-select',}),  
        label='Genre'
    )
    language = forms.ModelChoiceField(
        queryset=MusicLanguage.objects.all(),  
        widget=forms.Select(attrs={'class': 'form-select',}),
        label='Language'
    )
    class Meta:
        model = Music
        fields = ['title', 'artist', 'genre', 'language', 'mood', 'release_date', 'duration', 'music_file']  
        widgets = {
             'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter Music Title'
            }),
            'artist': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter Artist Name'
            }),
            'release_date': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control'
            }),
            'duration': forms.TimeInput(attrs={
                'type': 'time', 
                'class': 'form-control'
            }),
            'music_file': forms.FileInput(attrs={
                'class': 'form-control'
            }),
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

