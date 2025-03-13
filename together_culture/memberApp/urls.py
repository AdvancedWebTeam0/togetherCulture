from django.urls import path
from memberApp import views

urlpatterns = [
    path('', views.member_dashboard, name='member-dashboard'),
    path('events/', views.events, name='events'),
    path('benefits/', views.benefits, name='benefits'),
    path('use-benefit/<int:benefit_id>/', views.use_benefit, name='use-benefit'),
    path('digital-content/', views.digital_content, name='digital-content'),
    path('digital-content/book/<int:module_id>/',
         views.book_module, name='book-module'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
]
