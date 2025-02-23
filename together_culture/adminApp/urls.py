from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('insights/', views.insights, name='insights'),
    path('manage-events/', views.insights, name='manage-events'),
    path('add-members/', views.insights, name='add-members'),
    path('manage-members/', views.insights, name='manage-members'),
    path('manage-membership/', views.insights, name='manage-membership'),
]