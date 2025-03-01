from django.urls import path

from . import views

urlpatterns = [
    path("", views.admin_dashboard, name="admin-dashboard"),
    path('update-card/<str:card_id>/', views.update_card, name='update-card'),
    path('insights/', views.insights, name='insights'),
    path('manage-events/', views.manage_events, name='manage-events'),
    path('add-members/', views.add_members, name='add-members'),
    path('manage-members/', views.manage_members, name='manage-members'),
    path('manage-membership/', views.manage_membership, name='manage-membership'),
    path('save-tag/', views.save_tag, name='save-tag'),
    path('save-label/', views.save_label, name='save-label'),
    path('event-search/', views.event_search, name='event-search'),
]