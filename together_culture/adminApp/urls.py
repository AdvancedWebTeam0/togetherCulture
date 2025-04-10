from django.urls import path

from . import views

urlpatterns = [
    path("", views.admin_dashboard, name="admin-dashboard"),
    path('update-card/<str:card_id>/', views.update_card, name='update-card'),
    path('insights/', views.insights, name='insights'),
    path('manage-events/', views.manage_events, name='manage-events'),
    path('add-members/', views.add_members, name='add-members'),
    path('members-list/', views.members_list, name='members-list'),
    path('member-search/', views.member_search, name='member-search'),
    path('user-list/', views.user_list, name='user-list'),
    path('user-search/', views.user_search, name='user-search'),
    path('manage-membership/', views.manage_membership, name='manage-membership'),
    path('save-tag/', views.save_tag, name='save-tag'),
    path('save-label/', views.save_label, name='save-label'),
    path('event-search/', views.event_search, name='event-search'),
    path('event-type-data/', views.event_type_data, name='event-type-data'),
    path('event-tag-data/', views.event_tag_data, name='event-tag-data'),
    path('event-label-data/', views.event_label_data, name='event-label-data'),
    path('events-per-month/', views.events_per_month, name='events-per-month'),
    path('event-search-date/', views.event_search_date, name='event-search-date'),
    path('event-data/', views.event_data, name='event-data'),
    path('events/<slug:slug>/', views.event_detail, name='event-detail'),
    path('members-list/<slug:slug>/', views.member_detail_view, name='member-detail'),
    path('search-user/<slug:slug>/', views.user_details_for_admin_view, name='user-details'),
    path('approve/<str:user_id>/', views.approve_user, name='approve_user'),
    path('members-history/', views.members_history, name='members-history'),
    path('users/', views.users_list, name='users_list'),
    path('users/<str:user_id>/membership-history/', views.user_membership_history, name='user_membership_history'),
    path('handle-add-member/', views.handle_add_member, name='handle-add-member'),


    

    

]
