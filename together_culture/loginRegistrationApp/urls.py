from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('insert-user/', views.insert_user, name='insert-user'),
    path('login/', views.login, name='login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('validate-user', views.validate_user, name='validate-user'),
    path('manage-member/', views.manage_member, name='manage-member'),
    path('membership/', views.membership, name='membership'),
    path('logout/', views.logout, name='logout'),
]