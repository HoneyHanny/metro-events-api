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
    eventDate = models.DateField()
    eventDescription = models.TextField(null=True)
    eventNumberOfAttendees = models.IntegerField(default=0)
    eventLikes = models.IntegerField(default=0)
    eventOrganizer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    attendees = models.ManyToManyField(UserProfile, through='Attendee', related_name='attended_events')

    def __str__(self):
        return self.eventName

class EventLikers(models.Model):
    likers = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    eventLiked = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.likers.user.username} liked {self.eventLiked.eventName}'

class NonOrganizerEvent(models.Model):
    eventName = models.TextField(null=True)
    eventVenue = models.TextField(null=True)
    eventDate = models.DateField()
    eventDescription = models.TextField(null=True)
    eventNumberOfAttendees = models.IntegerField(default=0)
    eventLikes = models.IntegerField(default=0)
    eventOrganizer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

def __str__(self):
        return f"{self.user_profile.user.username}'s event: {self.eventName}"

class Attendee(models.Model):
    attendee = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    events = models.ForeignKey(Event, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.attendee.user.username


class Comment(models.Model):
    comment = models.TextField(null=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.comment}'

class JoinRequest(models.Model):
    attendee = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.attendee.user.username} requested to join {self.event.eventName}'

class Notification(models.Model):
    recipient = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self):
        return f'{self.recipient.user.username}'