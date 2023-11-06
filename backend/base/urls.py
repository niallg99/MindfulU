from django.urls import path
from base import views

urlpatterns = [
    path("protected/", views.protected_view, name="protected_view"),
    path("api/events/", views.get_events, name="get-events"),
    path("api/support_links/", views.get_support_links, name="support-link-list"),
    path("api/scraped-data/", views.get_scraped_data, name="get-scraped-data"),
    path("api/register/", views.register, name="register"),
    path("api/login/", views.login, name="login"),
    path("api/password-reset/", views.login, name="login"),
    path("api/mood-choices/", views.get_mood_choices, name="mood-choices"),
]
