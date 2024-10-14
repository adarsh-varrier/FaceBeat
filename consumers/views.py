import random
from django.db.models import Avg, Q, F
from django.db.models.functions import Cast
from django.db.models import IntegerField
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import (
    AdminUserCreationForm,
    FeedbackForm,
    ReplyForm,
    MusicUploadForm,
    MusicSearchForm,
    UserUpdateForm,
    RegistrationUpdateForm,
)
from .models import Feedback, Music
from musicindex.models import MusicGenre, MusicLanguage, Registration
from django.utils import timezone
from .utils import get_plot  # Import the get_plot function


def user_dashboard(request):
    if request.user.is_authenticated:
        # Fetch relevant data
        users = User.objects.exclude(id=request.user.id)  # Exclude the logged-in user
        feedbacks = Feedback.objects.select_related('user').order_by('-created_at')  # Fetch latest feedback with user info
        average_rating = Feedback.objects.aggregate(Avg('rating'))['rating__avg']
        genres = MusicGenre.objects.all()
        languages = MusicLanguage.objects.all()
        user_details = Registration.objects.filter(user=request.user).first()

        # Ensure average_rating is rounded to 2 decimal places if needed
        average_rating = round(average_rating, 2) if average_rating is not None else 0  # In case no ratings exist
        
        # Initialize forms
        admin_form = AdminUserCreationForm()
        feedback_form = FeedbackForm()
        reply_form = ReplyForm()
        music_form = MusicUploadForm()  # Initialize music upload form
        music_records = Music.objects.all()
        music_search = MusicSearchForm()

        graph = get_plot(average_rating)

        rmv_music_list = []
        if 'query' in request.GET:
            search_form = MusicSearchForm(request.GET)
            if search_form.is_valid():
                query = search_form.cleaned_data['query']
                rmv_music_list = Music.objects.filter(title__icontains=query) | Music.objects.filter(artist__icontains=query)
        else:
            search_form = MusicSearchForm()

        # Initialize profile update forms
        user_form = UserUpdateForm(instance=request.user)
        registration_form = RegistrationUpdateForm(instance=user_details)

       # Get user's preferred genres and languages as strings
        preferred_genres = user_details.genre.all() if user_details else []
        preferred_languages = user_details.language.all() if user_details else []

        # Get names of preferred genres and languages
        preferred_genres_names = [genre.name for genre in preferred_genres]
        preferred_languages_names = [language.name for language in preferred_languages]

        # Fetch 5 random music records matching preferred genres or languages
        random_music_records = Music.objects.filter(
            Q(genre__in=preferred_genres_names) | 
            Q(language__in=preferred_languages_names)
        ).order_by('?')[:5]  # Random order, limit to 5 records

        
                # Get the search query from the GET request
        query = request.GET.get('query', '').strip()  # Use .strip() to remove any leading/trailing whitespace

        if query:
            # Filter music records based on the search query for title, artist, language, and genre
            music_records = Music.objects.filter(
                Q(title__icontains=query) |
                Q(artist__icontains=query) |
                Q(language__icontains=query) |
                Q(genre__icontains=query)|
                Q(mood__icontains=query)  # Search by mood
            )
        else:
            music_records = Music.objects.all()  # Return all records if no query

        if request.method == 'POST':
            # Handle profile update forms
            if 'update_profile' in request.POST:
                user_form = UserUpdateForm(request.POST, instance=request.user)
                registration_form = RegistrationUpdateForm(request.POST, instance=user_details)

                if user_form.is_valid() and registration_form.is_valid():
                    user_form.save()
                    registration_form.save()
                    messages.success(request, 'Your profile has been updated successfully.')
                    return redirect('user_dashboard')

            # Handle adding genre
            if 'add_genre' in request.POST:
                genre_name = request.POST.get('genre_name')
                if genre_name:
                    MusicGenre.objects.create(name=genre_name)
                    messages.success(request, 'Genre added successfully.')

            # Handle removing genre
            if 'remove_genre' in request.POST:
                genre_id = request.POST.get('genre_id')
                genre = get_object_or_404(MusicGenre, id=genre_id)
                genre.delete()
                messages.success(request, 'Genre removed successfully.')

            # Handle adding language
            if 'add_language' in request.POST:
                language_name = request.POST.get('language_name')
                if language_name:
                    MusicLanguage.objects.create(name=language_name)
                    messages.success(request, 'Language added successfully.')

            # Handle removing language
            if 'remove_language' in request.POST:
                language_id = request.POST.get('language_id')
                language = get_object_or_404(MusicLanguage, id=language_id)
                language.delete()
                messages.success(request, 'Language removed successfully.')

            # Handle admin creation form
            if 'create_admin' in request.POST:
                admin_form = AdminUserCreationForm(request.POST)
                if admin_form.is_valid():
                    admin_form.save()
                    messages.success(request, 'New admin user created successfully.')
                    return redirect('user_dashboard')

            # Handle feedback form submission
            if 'submit_feedback' in request.POST:
                feedback_form = FeedbackForm(request.POST)
                if feedback_form.is_valid():
                    feedback = feedback_form.save(commit=False)
                    feedback.user = request.user  # Assign feedback to the logged-in user
                    feedback.save()
                    messages.success(request, 'Thank you for your feedback!')
                    return redirect('user_dashboard')

            # Handle reply to feedback
            if 'reply_feedback' in request.POST:
                feedback_id = request.POST.get('feedback_id')  # Get the feedback ID to reply to
                feedback = get_object_or_404(Feedback, id=feedback_id)
                reply_form = ReplyForm(request.POST)
                if reply_form.is_valid():
                    feedback.reply_text = reply_form.cleaned_data['reply_text']
                    feedback.replied_at = timezone.now()  # Update reply timestamp
                    feedback.save()
                    messages.success(request, 'Reply submitted successfully.')
                    return redirect('user_dashboard')

            # Handle music upload
            if 'upload_music' in request.POST:
                music_form = MusicUploadForm(request.POST, request.FILES)  # Include request.FILES to handle file uploads
                if music_form.is_valid():
                    music_form.save()  # Save the music file and metadata
                    messages.success(request, 'Music uploaded successfully!')
                    return redirect('user_dashboard')

        # Return all forms to the template
        return render(request, 'user_dashboard.html', {
            'users': users,
            'admin_form': admin_form,
            'feedbacks': feedbacks,
            'feedback_form': feedback_form,
            'reply_form': reply_form,
            'music_form': music_form,  # Pass the music upload form to the template
            'music_records': music_records,
            'music_search': music_search,
            'average_rating': average_rating,
            'graph': graph,
            'genres': genres,
            'languages': languages,
            'user_form': user_form,  # Pass the user update form
            'registration_form': registration_form,  # Pass the registration form
            'user_details': user_details,
            'random_music_records': random_music_records,
            'music_list': rmv_music_list,
            'music_search': search_form,
        })
    else:
        return redirect('login')

def remove_user(request, user_id):
    if request.user.is_authenticated:
        user_to_remove = get_object_or_404(User, id=user_id)  # Get user by ID

        if user_to_remove != request.user:  # Prevent self-deletion
            user_to_remove.delete()  # Delete the user
            messages.success(request, f"User '{user_to_remove.username}' has been removed successfully.")
        else:
            messages.error(request, "You cannot remove your own account.")

        return redirect('user_dashboard')  # Redirect back to the user dashboard
    else:
        return redirect('login')  # Redirect to login if not authenticated
    
def delete_music(request, music_id):
    music = get_object_or_404(Music, id=music_id)
    if request.method == 'POST':
        music.delete()  # Delete the music instance
        return redirect('user_dashboard')  # Redirect to the user dashboard or another page after deletion
    return render(request, 'user_dashboard.html', {'music': music})  # Render a confirmation page if not a POST request
    




