from django.contrib import admin
from .models import UserProfile, Notification, JoinRequest, Comment, EventLikers, Attendee, Event

admin.site.register(UserProfile)
admin.site.register(Event)
admin.site.register(EventLikers)
admin.site.register(Attendee)
admin.site.register(Comment)
admin.site.register(JoinRequest)
admin.site.register(Notification)
