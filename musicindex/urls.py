from django.urls import path
from .views import home, register, login_view 
from musicindex import views

urlpatterns = [
    path('', home, name='home'),
    path('home/',views.home,name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('forgot/', views.forgot_pass, name='forgot_pass'),
    path('reset/<int:user_id>/', views.reset_password, name='reset_password'),
    path('lernmore/', views.lernmore, name='lernmore'),
    path('terms&condition/', views.terms, name='terms'),
]

