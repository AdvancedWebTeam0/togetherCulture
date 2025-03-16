from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('insertUser/', views.insert_user, name='insert_user'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashBoard, name='dashboard'),
    path('validateUser/', views.validate_user, name='validate_user'),
    path('manage-member/', views.manage_member, name='manage_member'),
    path('membership/', views.membership, name='membership'),
    path('logout/', views.logout, name='logout'),
]