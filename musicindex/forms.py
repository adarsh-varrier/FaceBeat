from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Registration, MusicGenre, MusicLanguage

class RegistrationForm(UserCreationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),label='')
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20)
    genre = forms.ModelMultipleChoiceField(queryset=MusicGenre.objects.all(), widget=forms.CheckboxSelectMultiple)
    language = forms.ModelMultipleChoiceField(queryset=MusicLanguage.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2', 'genre', 'language']

    def save(self, commit=True):
        user = super().save(commit=False)  # Save the User model fields
        user.email = self.cleaned_data['email']  # Assign the email to the user

        if commit:
            try:
                user.save()  # Save the User instance to the database
                
                # Create Registration entry
                registration = Registration.objects.create(
                    user=user,
                    phone=self.cleaned_data['phone'],  # Save the phone number
                    email=self.cleaned_data['email']   # This should be the same as the User email
                )
                # Set many-to-many fields (genre and language)
                registration.genre.set(self.cleaned_data['genre'])  
                registration.language.set(self.cleaned_data['language'])
            except Exception as e:
                print(f"Error saving registration: {e}")  # Debugging line

        return user
