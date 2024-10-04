from django.contrib import admin
from .models import MusicGenre, MusicLanguage

@admin.register(MusicGenre)
class MusicGenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(MusicLanguage)
class MusicLanguageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

