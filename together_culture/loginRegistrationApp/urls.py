from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('insertUser/', views.insertUser, name='insertUser'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashBoard, name='dashboard'),
    path('validateUser/', views.validateUser, name='validateUser'),
    path('manage-member/', views.manage_member, name='manage_member'),
    path('membership/', views.membership, name='membership'),
    path('logout/', views.logout, name='logout'),
    path('get_interests/', views.getInitialInterests, name='getInitialInterests'),
    path('saveInitialInterests/', views.saveInitialInterests, name='saveInitialInterests'),
]