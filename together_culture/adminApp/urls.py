from django.urls import path

from . import views

urlpatterns = [
    path("", views.admin_dashboard, name="admin-dashboard"),
    path('update-card/<str:card_id>/', views.update_card, name='update-card'),
    path('insights/', views.insights, name='insights'),
    path('events-per-month/', views.events_per_month, name='events-per-month'),
    path('manage-events/', views.manage_events, name='manage-events'),
    path('add-members/', views.add_members, name='add-members'),
    path('manage-members/', views.manage_members, name='manage-members'),
    path('manage-membership/', views.manage_membership, name='manage-membership'),
    path('save-tag/', views.save_tag, name='save-tag'),
    path('save-label/', views.save_label, name='save-label'),
    path('event-search/', views.event_search, name='event-search'),
    path('event-type-data/', views.event_type_data, name='event-type-data'),
    path('event-tag-data/', views.event_tag_data, name='event-tag-data'),
    path('event-label-data/', views.event_label_data, name='event-label-data'),
]

