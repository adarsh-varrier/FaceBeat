from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login  # Rename import to avoid conflict
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages import constants as messages

# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')
    
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)  # Log in the user after registration
                messages.success(request, 'Registration successful!')  # Success message
                return redirect('login')  # Redirect to home page or dashboard
            except Exception as e:
                messages.error(request, f'Registration failed due to: {e}')  # Show any exceptions
        else:
            # If the form is not valid, show form errors
            messages.error(request, 'Registration failed. Please correct the errors below.')
            print(form.errors)  # Debugging: print form errors to the console
    else:
        form = RegistrationForm()
    
    return render(request, 'register.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)  # Log in the user
                return redirect('user_dashboard')  # Redirect to user dashboard
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

from django.contrib.auth import logout

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')  # Redirect to login after logout
    else:
        return redirect('home')  # If not POST, redirect to home or some other page