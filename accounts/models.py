from django.db import models
from django.contrib.auth.models import User
from email.policy import default
from datetime import datetime

class Post(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='profile_pictures/def_pfp.png')
    bio =  models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username
