# consumers/urls.py
from django.urls import path
from .views import user_dashboard, remove_user, delete_music, user_management, music_management, feedback_view, image_scan, music_search, feedback_give, user_settings, recommend_music
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('usermanagement/', user_management, name='user_management'),
    path('musicmanagement/', music_management, name='music_management'),
    path('feedbackview/', feedback_view, name='feedback_view'),
    path('imagescan/', image_scan, name='image_scan'),
    path('musicsearch/', music_search, name='music_search'),
    path('feedbackgive/', feedback_give, name='feedback_give'),
    path('settings/', user_settings, name='user_settings'),
    path('remove_user/<int:user_id>/', remove_user, name='remove_user'),  
    path('logout/', LogoutView.as_view(), name='logout'),
    path('delete_music/<int:music_id>/', delete_music, name='delete_music'),
    path('recommend/', recommend_music, name='recommend_music'),
    path('genre/<int:id>/', views.music_by_genre, name='music_by_genre'),
    path('language/<int:id>/', views.music_by_language, name='music_by_language'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


