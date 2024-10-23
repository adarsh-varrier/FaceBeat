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
from django.contrib.auth import authenticate, login, get_user_model
from .txtemotion_utils import detect_emotion


def user_dashboard(request):
    if request.user.is_authenticated:

        average_rating = Feedback.objects.aggregate(Avg('rating'))['rating__avg']
        genres = MusicGenre.objects.all()
        languages = MusicLanguage.objects.all()
        user_details = Registration.objects.filter(user=request.user).first()

        # Ensure average_rating is rounded to 2 decimal places if needed
        average_rating = round(average_rating, 2) if average_rating is not None else 0  # In case no ratings exist

        graph = get_plot(average_rating)

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
           

        # Return all forms to the template
        return render(request, 'user_dashboard.html', {
            'average_rating': average_rating,
            'graph': graph,
            'genres': genres,
            'languages': languages,
            'user_details': user_details,
            'random_music_records': random_music_records,
        })
    else:
        return redirect('login')
    

# Engine
def image_scan(request):
    return render(request, 'image-scan.html')


#text_recommendation

def recommend_music(request):
    if request.method == "POST":
        user_text = request.POST.get("user_text")

        # Detect the emotion from the user's input
        detected_emotion = detect_emotion(user_text)

        # Define custom messages for each emotion
        emotion_messages = {
            'anger': "It seems like you're feeling angry. Take a deep breath and relax.",
            'happy': "You're in a happy mood! Keep smiling and enjoy your day.",
            'sad': "I think you are sad. Everything will be okay.",
            'overjoyed': "You're feeling overjoyed! Let's celebrate with some music.",
            'relax': "You seem to be in a relaxed mood. Enjoy the peaceful vibes.",
            'romance': "Feeling romantic? Here's some music to set the mood.",
            'satisfaction': "You're feeling satisfied. Keep up the good vibes.",
            'excitement': "You're excited! Let's keep the energy going with these tracks.",
            'interest': "You're interested and curious! Here's something to keep you engaged.",
            'surprise': "Life is full of surprises! Here's some music to match your mood.",
            'nostalgia': "Feeling nostalgic? Let these tracks take you back in time."
        }

        # Define a mapping from detected emotions to mood choices
        mood_mapping = {
            'anger': 'anger',
            'happy': 'happy',
            'sad': 'sad',
            'overjoyed': 'overjoyed',
            'relax': 'relax',
            'romance': 'romance',
            'satisfaction': 'satisfaction',
            'excitement': 'excitement',
            'interest': 'interest',
            'surprise': 'surprise',
            'nostalgia': 'nostalgia'
        }

        # Get the corresponding mood for the detected emotion
        mood = mood_mapping.get(detected_emotion)

        # Get the custom message for the detected emotion
        custom_message = emotion_messages.get(detected_emotion, "Here's some music for your mood.")

        # Filter music recommendations based on the detected mood
        recommended_music = Music.objects.filter(mood=mood)

        return render(request, 'image-scan.html', {
            'detected_emotion': detected_emotion,
            'custom_message': custom_message,
            'recommended_music': recommended_music
        })

    return render(request, 'image-scan.html')




User = get_user_model()  # Handle custom user models

def remove_user(request, user_id):
    if request.method == 'POST':
        password = request.POST.get('password')
        user_to_remove = get_object_or_404(User, id=user_id)

        # Ensure the user is not trying to delete their own account
        if user_to_remove == request.user:
            messages.error(request, "You cannot remove your own account.")
            return redirect('user_management')

        # Check if the target user is an admin
        if user_to_remove.is_staff:
            # Authenticate using the admin’s password entered during their creation
            admin_auth = authenticate(request, username=user_to_remove.username, password=password)
            
            if admin_auth is not None:  # Password is correct
                user_to_remove.delete()
                messages.success(request, f"Admin '{user_to_remove.username}' has been removed successfully.")
            else:
                messages.error(request, "Incorrect password. Unable to remove the admin.")
        else:
            # If the user is not an admin, no password check is required
            user_to_remove.delete()
            messages.success(request, f"User '{user_to_remove.username}' has been removed successfully.")

        return redirect('user_management')

    messages.error(request, "Invalid request. Use the form to remove a user.")
    return redirect('user_management')
    
    
def delete_music(request, music_id):
    music = get_object_or_404(Music, id=music_id)
    if request.method == 'POST':
        music.delete()  # Delete the music instance
        messages.success(request, 'Music deleted successfully!')
        return redirect('music_management')  # Redirect to the user dashboard or another page after deletion
    return render(request, 'music-management.html', {'music': music})  # Render a confirmation page if not a POST request



def user_management(request):
    users = User.objects.exclude(id=request.user.id)  # Exclude the logged-in user
    # Initialize forms
    admin_form = AdminUserCreationForm()
    # Handle admin creation form
    if 'create_admin' in request.POST:
        admin_form = AdminUserCreationForm(request.POST)
        if admin_form.is_valid():
            admin = admin_form.save(commit=False)  # Save without committing to handle password properly
            admin.set_password(admin_form.cleaned_data['password'])  # Hash the password
            admin.is_staff = True  # Mark as admin
            admin.is_superuser = True  # Optional: Mark as superuser if needed
            admin.save()
            messages.success(request, 'New admin user created successfully.')
            return redirect('user_management')

    return render(request, 'user-management.html', {
        'users': users,
        'admin_form': admin_form,
    })



def music_management(request):
    
    genres = MusicGenre.objects.all()
    languages = MusicLanguage.objects.all()
    music_form = MusicUploadForm()  # Initialize music upload form

    

    if request.method == 'POST':
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

        # Handle music upload
        if 'upload_music' in request.POST:
            music_form = MusicUploadForm(request.POST, request.FILES)  # Include request.FILES to handle file uploads
            if music_form.is_valid():
                music_form.save()  # Save the music file and metadata
                messages.success(request, 'Music uploaded successfully!')
                return redirect('music_management')
    
    rmv_music_list = []
    if 'query' in request.GET:
        search_form = MusicSearchForm(request.GET)
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            rmv_music_list = Music.objects.filter(title__icontains=query) | Music.objects.filter(artist__icontains=query)
    else:
        search_form = MusicSearchForm()

    return render(request, 'music-management.html',{
        'genres': genres,
        'languages': languages,
        'music_form': music_form,  # Pass the music upload form to the template
        'music_list': rmv_music_list,
        'music_search': search_form,
    })

def feedback_view(request):

    feedbacks = Feedback.objects.select_related('user').order_by('-created_at')  # Fetch latest feedback with user info
    reply_form = ReplyForm()


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
            return redirect('feedback_view')

    return render(request, 'feedback-view.html',{
        'feedbacks': feedbacks,
        'reply_form': reply_form,
    })


def music_search(request):

    music_records = Music.objects.all()
    music_search = MusicSearchForm()

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
    
    genres = MusicGenre.objects.all()  # Fetch all genres
    languages = MusicLanguage.objects.all()  # Fetch all languages

    return render(request, 'music-search.html',{
        'music_records': music_records,
        'music_search': music_search,
        'genres': genres,
        'languages': languages,
    })

def feedback_give(request):

    # Initialize forms
    feedback_form = FeedbackForm()
    feedbacks = Feedback.objects.select_related('user').order_by('-created_at')  # Fetch latest feedback with user info
    # Handle feedback form submission
    if 'submit_feedback' in request.POST:
        feedback_form = FeedbackForm(request.POST)
        if feedback_form.is_valid():
            feedback = feedback_form.save(commit=False)
            feedback.user = request.user  # Assign feedback to the logged-in user
            feedback.save()
            messages.success(request, 'Thank you for your feedback!')
            return redirect('feedback_give')    
    return render(request, 'feedback-give.html',{
        'feedbacks': feedbacks,
        'feedback_form': feedback_form,
    })

def user_settings(request):
    # Initialize profile update forms
    user_details = Registration.objects.filter(user=request.user).first()
    user_form = UserUpdateForm(instance=request.user)
    registration_form = RegistrationUpdateForm(instance=user_details)

    if request.method == 'POST':
        # Handle profile update forms
        if 'update_profile' in request.POST:
            user_form = UserUpdateForm(request.POST, instance=request.user)
            registration_form = RegistrationUpdateForm(request.POST, instance=user_details)

            if user_form.is_valid() and registration_form.is_valid():
                user_form.save()
                registration_form.save()
                messages.success(request, 'Your profile has been updated successfully.')
                return redirect('user_settings')

    return render(request, 'user-settings.html',{
        'user_form': user_form,  # Pass the user update form
        'registration_form': registration_form,  # Pass the registration form
        'user_details': user_details,
    })


def music_by_genre(request, id):
    # Get the genre by ID or return a 404 if not found
    genre = get_object_or_404(MusicGenre, id=id)

    # Filter music records by the selected genre
    music_records = Music.objects.filter(genre=genre)

    return render(request, 'music_by_genre.html', {
        'genre': genre,
        'music_list': music_records,  # Ensure you're passing the filtered music list
    })

def music_by_language(request, id):
    # Get the language by ID or return a 404 if not found
    language = get_object_or_404(MusicLanguage, id=id)

    # Filter music records by the selected language
    music_records = Music.objects.filter(language=language)

    return render(request, 'music_by_language.html', {
        'language': language,
        'music_list': music_records,  # Ensure you're passing the filtered music records
    })


    




