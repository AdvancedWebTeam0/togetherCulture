from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('insert-user', views.insertUser, name='insert-user'),
    path('login/', views.login, name='login'),
    path('admin-dashboard', views.adminDashboard, name='admin-dashboard'),
    path('validate-user', views.validateUser, name='validate-user'),
    path('manage-member/', views.manage_member, name='manage-member'),
    path('membership/', views.membership, name='membership'),
    path('logout/', views.logout, name='logout'),
]