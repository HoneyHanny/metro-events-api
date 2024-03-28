from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    isOrganizer = models.BooleanField(default=False)
  
    def __str__(self):
        return self.user.username

class Event(models.Model):
    eventName = models.TextField(null=True)
    eventVenue = models.TextField(null=True)
    eventDate = models.DateTimeField(auto_now=True)
    eventDescription = models.TextField(null=True)
    eventNumberOfAttendees = models.IntegerField(default=0)
    eventLikes = models.IntegerField(default=0)
    eventOrganizer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.eventName

class Attendee(models.Model):
    eventOrganizer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    events = models.ManyToManyField(Event, related_name='attendees')

    def __str__(self):
        return self.eventOrganizer.user.username