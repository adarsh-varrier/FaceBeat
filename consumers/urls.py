# consumers/urls.py
from django.urls import path
from .views import user_dashboard, remove_user, delete_music
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('remove_user/<int:user_id>/', remove_user, name='remove_user'),  # URL for removing a user
    path('logout/', LogoutView.as_view(), name='logout'),
    path('delete_music/<int:music_id>/', delete_music, name='delete_music'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


