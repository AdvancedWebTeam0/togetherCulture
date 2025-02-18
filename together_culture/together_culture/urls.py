"""
URL configuration for together_culture project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from loginRegistrationApp import views

urlpatterns = [
    path("", include("nonmemberApp.urls")),
    path("member/", include("memberApp.urls")),
    path("admin/", include("adminApp.urls")),
    path('djangoadmin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('insertUser/', views.insertUser, name='insertUser'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashBoard, name='dashboard'),
    path('validateUser/', views.validateUser, name='validateUser'),
    path('insights/', views.insights, name='insights'),
    path('events/', views.events, name='events'),
    path('manage-member/', views.manage_member, name='manage_member'),
    path('membership/', views.membership, name='membership'),
]
