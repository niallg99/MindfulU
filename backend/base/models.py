from django.db import models
from django.contrib.auth.models import User as DjangoUser


class ProfilePicture(models.Model):
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE)
    image_url = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username


class MoodCause(models.Model):
    CAUSE_CHOICES = [
        ("Academic", "Academic"),
        ("Financial", "Financial"),
        ("Relationship/Social", "Relationship/Social"),
        ("Other", "Other"),
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

    MOOD_CAUSE_CHOICES = MoodCause.CAUSE_CHOICES

    user = models.ForeignKey(DjangoUser, on_delete=models.CASCADE, related_name="moods")
    mood_type = models.CharField(max_length=50, choices=MOOD_CHOICES)
    mood_date = models.DateTimeField(auto_now_add=True)
    mood_cause = models.CharField(
        max_length=50, choices=MOOD_CAUSE_CHOICES, null=True, blank=True
    )
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.mood_type} on {self.mood_date}"


class Friends(models.Model):
    FRIENDSHIP_STATUS_CHOICES = [
        ("Requested", "Requested"),
        ("Accepted", "Accepted"),
        ("Blocked", "Blocked"),
    ]

    user = models.ForeignKey(
        DjangoUser, on_delete=models.CASCADE, related_name="friendships"
    )
    friend = models.ForeignKey(DjangoUser, on_delete=models.CASCADE)
    friendship_status = models.CharField(
        max_length=50, choices=FRIENDSHIP_STATUS_CHOICES, default="Requested"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ('user', 'friend')

    def get_most_recent_mood(self):
        return Mood.objects.filter(user=self.friend).order_by('-mood_date').first()
    
    def __str__(self):
        return f"{self.user.username} and {self.friend.username} - Status: {self.friendship_status}"


class ScrapedData(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    scraped_content = models.TextField(default="")

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


class SupportSection(models.Model):
    title = models.CharField(max_length=255)


class SupportLink(models.Model):
    section = models.ForeignKey(
        SupportSection,
        on_delete=models.CASCADE,
        default=None,
        null=True,
    )
    link_text = models.CharField(max_length=255)
    link_url = models.URLField()
