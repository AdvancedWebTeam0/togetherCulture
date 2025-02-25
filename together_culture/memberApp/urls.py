from django.urls import path

from memberApp import views

urlpatterns = [
    path("", views.index, name="index"),
    path('memberDashboard/', views.memberdashBoard, name='memberDashboard'),
    path('events/', views.events, name='events'),
    path('benefits/', views.benefits, name='benefits'),
    path('digitalContent/', views.digitalContent, name='digitalContent'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    path('get_interests/', views.getInitialInterests, name='getInitialInterests'),
    path('saveInitialInterests/', views.saveInitialInterests, name='saveInitialInterests'),
]
