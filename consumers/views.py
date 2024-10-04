# consumers/views.py
from django.db.models import Avg
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import AdminUserCreationForm, FeedbackForm, ReplyForm # Ensure correct import path
from .models import Feedback
from django.utils import timezone


def user_dashboard(request):
    if request.user.is_authenticated:
        users = User.objects.exclude(id=request.user.id)  # Exclude the logged-in user
        feedbacks = Feedback.objects.select_related('user').all()  # Fetch all feedback with user info
        average_rating = Feedback.objects.aggregate(Avg('rating'))['rating__avg']
    
    # Ensure average_rating is rounded to 2 decimal places if needed
        if average_rating is not None:
            average_rating = round(average_rating, 2)
        else:
            average_rating = 0  # In case no ratings exist
        # Initialize both forms for a GET request or if neither form is submitted
        admin_form = AdminUserCreationForm()
        feedback_form = FeedbackForm()

        reply_form = ReplyForm()

        # Handle admin creation form
        if request.method == 'POST' and 'create_admin' in request.POST:  # Check which form is submitted
            admin_form = AdminUserCreationForm(request.POST)

            if admin_form.is_valid():
                admin_form.save()
                messages.success(request, 'New admin user created successfully.')
                return redirect('user_dashboard')

        # Handle feedback form submission
        elif request.method == 'POST' and 'submit_feedback' in request.POST:  # Check if feedback form is submitted
            feedback_form = FeedbackForm(request.POST)
            
            if feedback_form.is_valid():
                feedback = feedback_form.save(commit=False)
                feedback.user = request.user  # Assign feedback to the logged-in user
                feedback.save()
                messages.success(request, 'Thank you for your feedback!')
                return redirect('user_dashboard')
        elif 'reply_feedback' in request.POST:
                feedback_id = request.POST.get('feedback_id')  # Get the feedback ID to reply to
                feedback = get_object_or_404(Feedback, id=feedback_id)
                reply_form = ReplyForm(request.POST)

                if reply_form.is_valid():
                    feedback.reply_text = reply_form.cleaned_data['reply_text']
                    feedback.replied_at = timezone.now()  # Assuming you have imported timezone
                    feedback.save()
                    messages.success(request, 'Reply submitted successfully.')
                    return redirect('user_dashboard')

        # Return both forms regardless of which form was submitted
        return render(request, 'user_dashboard.html', {
            'users': users,
            'admin_form': admin_form,
            'feedbacks': feedbacks,  # Pass fetched feedbacks to the template
            'feedback_form': feedback_form,
            'reply_form': reply_form,  # Pass the reply form to the template
            'average_rating': average_rating,
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