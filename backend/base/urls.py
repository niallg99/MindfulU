from django.urls import path
from base import views

urlpatterns = [
    path('protected/', views.protected_view, name='protected_view'),
    path('api/events/', views.get_events, name='get-events'),
    path('api/scraped-data/', views.get_scraped_data, name='get-scraped-data'),
]
