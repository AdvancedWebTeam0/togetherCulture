from django.urls import path

from memberApp import views

urlpatterns = [
    path('', views.member_dashboard, name='member-dashboard'),
    path('events/', views.events, name='events'),
    path('benefits/', views.benefits, name='benefits'),
    path('digital-content/', views.digital_content, name='digital-content'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    path('get_interests/', views.getInitialInterests, name='getInitialInterests'),
    path('saveInitialInterests/', views.saveInitialInterests, name='saveInitialInterests'),
]
