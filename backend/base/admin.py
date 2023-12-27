from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
from django.contrib import admin
from .models import (
    MoodCause,
    Mood,
    Friends,
    Event,
    SupportLink,
    SupportSection,
    UserProfile,
)

# Register the MoodCause model
admin.site.register(MoodCause)

# Register the Mood model
admin.site.register(Mood)

# Register the Friendship model
admin.site.register(Friends)

# Register the Event model
admin.site.register(Event)

# Register the SupportLink model
admin.site.register(SupportLink)

# Register the SupportLink model
admin.site.register(SupportSection)

# Register the UserProfile model
admin.site.register(UserProfile)

class UserAdmin(BaseUserAdmin):
    list_display = ("id", "username", "email", "first_name", "last_name", "is_staff")

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
