from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    isOrganizer = models.BooleanField(default=False)
  
    def __str__(self):
        return self.user.username