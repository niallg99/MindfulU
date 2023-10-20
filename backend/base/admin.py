from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User, ProfilePicture, MoodCause, Mood, Friendship

# Register the User model
admin.site.register(User)

# Register the ProfilePicture model
admin.site.register(ProfilePicture)

# Register the MoodCause model
admin.site.register(MoodCause)

# Register the Mood model
admin.site.register(Mood)

# Register the Friendship model
admin.site.register(Friendship)
