from django.urls import path

from memberApp import views

urlpatterns = [
    path("", views.index, name="index"),
    path('member_dashboard/', views.member_dashboard, name='member-dashboard'),
    path('events/', views.events, name='events'),
    path('benefits/', views.benefits, name='benefits'),
    path('digital_content/', views.digital_content, name='digital-content'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
]