from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Registration, MusicGenre, MusicLanguage
from django.core.exceptions import ValidationError
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class RegistrationForm(UserCreationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),label='')
    email = forms.EmailField(
        required=True,  
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        label='')
    phone = forms.CharField(max_length=20, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
        label='')
    genre = forms.ModelMultipleChoiceField(queryset=MusicGenre.objects.all(), widget=forms.CheckboxSelectMultiple,label="genre")
    language = forms.ModelMultipleChoiceField(queryset=MusicLanguage.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2', 'genre', 'language']

    # Email validation method
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already registered.")
        

        email_regex = re.compile(
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z-]{2,}(\.[a-zA-Z-]{2,})*\.[a-zA-Z]{2,}$'
        )

        if not email_regex.match(email):
            raise ValidationError(
                _("Invalid email address. Please provide a valid domain and extension."),
                params={'email': email},
            )

        return email
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        
        # Check if the phone number contains only digits
        if not re.match(r'^\d{10}$', phone):
            raise ValidationError("Phone number must be exactly 10 digits and contain only numbers.")
        
        # Check if the phone number already exists in the Registration model
        if Registration.objects.filter(phone=phone).exists():
            raise ValidationError("This phone number is already registered.")
        
        return phone

    # Customizing the password fields
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label=''
    )

    def clean_password1(self):
        password = self.cleaned_data.get('password1')

        # Define a regex pattern to check for uppercase, lowercase, digits, and special characters
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$', password):
            raise ValidationError("Password must be at least 8 characters long and include an uppercase letter, a lowercase letter, a number, and a special character.")

        return password
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        label=''
    )

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
