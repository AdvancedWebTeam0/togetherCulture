from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('events_view/', views.events_view, name='events_view'),
    path('membership/', views.membership, name='membership'),
    path('about/', views.about, name='about'),
    path('resources/', views.resources, name='resources'),
]