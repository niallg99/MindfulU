from django.urls import path
from base import views

urlpatterns = [
    path("protected/", views.protected_view, name="protected_view"),
    path("api/events/", views.get_events, name="get-events"),
    path(
        "api/custom_support_links/",
        views.get_support_links_view,
        name="custom_support_links",
    ),
    path("api/scraped-data/", views.get_scraped_data, name="get-scraped-data"),
    path("api/register/", views.register, name="register"),
    path("api/login/", views.login, name="login"),
    path("api/password-reset/", views.login, name="login"),
    path("api/mood-choices/", views.get_mood_choices, name="mood-choices"),
    path("api/get-mood-causes/", views.get_mood_causes, name="get-mood-causes"),
    path("api/moods/", views.post_mood, name="post-mood"),
    path("api/user-moods/<str:user_id>/", views.get_user_moods, name="get_user_moods"),
    path("api/get-csrf-token/", views.get_csrf_token, name="get-csrf-token"),
    path('api/friends/', views.get_friends_list_view, name='friends_list'),
    path('api/friends/<str:user_id>/', views.get_user_friends, name='get_user_friends'),
    path('api/send-friend-request/<str:username>/', views.send_friend_request, name='send_friend_request'),
    path('api/accept-friend-request/<str:friend_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('api/reject-friend-request/<str:friend_id>/', views.reject_friend_request, name='reject_friend_request'),
    path('api/remove-friend/<str:friend_id>/', views.remove_friend, name='remove_friend'),
]
