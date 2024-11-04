from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login  # Rename import to avoid conflict
from .forms import RegistrationForm, CustomAuthenticationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages import constants as messages
from .models import Registration
from .forms import ForgotPasswordForm, ResetPasswordForm
from django.contrib.auth.models import User  # Import the User model
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.hashers import check_password

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



def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
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
    
def forgot_pass(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            security_question = form.cleaned_data['security_question']
            security_answer = form.cleaned_data['security_answer']

            try:
                # Check if user exists based on username or email
                user = User.objects.get(username=username_or_email) or User.objects.get(email=username_or_email)
                registration = Registration.objects.get(user=user)

                 # Validate the security question
                if check_password(security_question, registration.security_question):
                    # Check if the hashed security answer matches the provided answer
                    if check_password(security_answer, registration.security_answer):
                        # Allow user to reset password
                        messages.success(request, "Security question validated. You can now reset your password.")
                        return redirect('reset_password', user_id=user.id)  # Pass user ID to the reset password view
                    else:
                        messages.error(request, "Invalid security answer.")
                else:
                    messages.error(request, "Invalid security question.")
            except User.DoesNotExist:
                messages.error(request, "User not found.")
            except Registration.DoesNotExist:
                messages.error(request, "Registration details not found.")
    else:
        form = ForgotPasswordForm()

    return render(request, 'forgot-pass.html', {'form': form})

def reset_password(request, user_id):
    try:
        user = User.objects.get(id=user_id)  # Ensure you get the correct user
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('forgot_pass')  # Redirect back to the forgot password page

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password1 = form.cleaned_data['new_password1']
            new_password2 = form.cleaned_data['new_password2']

            if new_password1 == new_password2:
                # Update the user's password
                user.set_password(new_password1)
                user.save()
                messages.success(request, "Your password has been reset successfully.")
                return redirect('login')  # Redirect to login page
            else:
                messages.error(request, "Passwords do not match.")
    else:
        form = ResetPasswordForm()

    return render(request, 'reset-pass.html', {'form': form})

def lernmore(request):
    return render(request, 'lernmore.html')
