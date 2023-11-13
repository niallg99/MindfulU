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
    path("api/get-csrf-token/", views.get_csrf_token, name="get-csrf-token"),
]