from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
from django.contrib import admin
from .models import (
    ProfileInfo,
    MoodCause,
    Mood,
    Friends,
    Event,
    SupportLink,
    SupportSection,
)


# Register the ProfilePicture model
admin.site.register(ProfileInfo)

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

class UserAdmin(BaseUserAdmin):
    list_display = ("id", "username", "email", "first_name", "last_name", "is_staff", "get_phonenumber")

    def get_phonenumber(self, obj):
        return obj.profileinfo.phonenumber if hasattr(obj, 'profileinfo') else 'N/A'

    get_phonenumber.short_description = 'Phone Number'


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
