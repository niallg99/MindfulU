from django.db import models


class User(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)  # New field for first name
    last_name = models.CharField(max_length=255)  # New field for last name
    # Add other user-related fields if needed

    def __str__(self):
        return self.username


class ProfilePicture(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image_url = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username


class MoodCause(models.Model):
    CAUSE_CHOICES = [
        ("Academic", "Academic"),
        ("Financial", "Financial"),
        ("Relationship/Social", "Relationship/Social"),
    ]

    cause_type = models.CharField(max_length=50, choices=CAUSE_CHOICES)

    def __str__(self):
        return self.cause_type


class Mood(models.Model):
    MOOD_CHOICES = [
        ("Meh", "Meh"),
        ("Sad", "Sad"),
        ("Angry", "Angry"),
        ("Happy", "Happy"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mood_type = models.CharField(max_length=50, choices=MOOD_CHOICES)
    mood_date = models.DateTimeField()
    mood_cause = models.ForeignKey(
        MoodCause, on_delete=models.CASCADE, null=True, blank=True
    )
    description = models.TextField(blank=True)
    # Add other mood-related fields if needed

    def __str__(self):
        return f"{self.user.username} - {self.mood_type} on {self.mood_date}"


class Friendship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friendships")
    friend = models.ForeignKey(User, on_delete=models.CASCADE)
    friendship_status = models.CharField(max_length=50)
    # Add other friendship-related fields

    def __str__(self):
        return f"{self.user.username} and {self.friend.username} - Status: {self.friendship_status}"


class ScrapedData(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    scraped_content = models.TextField(default="")  # Specify the default value

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Scraped Data"
        verbose_name_plural = "Scraped Data"


class Event(models.Model):
    name = models.CharField(max_length=255, default="Event Name")
    date = models.CharField(max_length=100, default="Event Date")
    duration = models.CharField(max_length=100, default="Event Duration")
    day = models.CharField(max_length=30, default="Event Day")
    time = models.CharField(max_length=50, default="Event Time")
    venue = models.CharField(max_length=255, default="Event Venue")
    registration = models.TextField(default="Registration Information")

    def __str__(self):
        return self.name
