from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('event/', views.event, name='event'),
    path('membership/', views.membership, name='membership'),
    path('about/', views.about, name='about'),
    path('resources/', views.resources, name='resources'),
]