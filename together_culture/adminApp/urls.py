from django.urls import path

from . import views

urlpatterns = [
    path("", views.admin_dashboard, name="admin-dashboard"),
    path('insights/', views.insights, name='insights'),
    path('manage-events/', views.manage_events, name='manage-events'),
    path('add-members/', views.add_members, name='add-members'),
    path('manage-members/', views.manage_members, name='manage-members'),
    path('manage-membership/', views.manage_membership, name='manage-membership'),
]