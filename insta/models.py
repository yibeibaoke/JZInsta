from django.db import models
from datetime import datetime

from imagekit.models import ProcessedImageField

from django.contrib.auth.models import AbstractUser

# Create your models here.

class InstaUser(AbstractUser):
    age = models.PositiveIntegerField(default=0)
    profile_pic = ProcessedImageField(
        upload_to='static/images/profiles',
        format='JPEG',
        options={ 'quality': 100},
        null=True,
        blank=True,
        )

    def get_number_of_followers(self):
        
        if self.followers.count():
            return self.followers.count() + 1
        else:
            return 0

    def get_number_of_following(self):
        if self.following.count():
            return self.following.count() + 1
        else:
            return 0

    def __str__(self):
        return self.username

class UserConnection(models.Model):
    instaUser = models.ForeignKey(
        InstaUser,
        unique = True,
        on_delete=models.CASCADE,
        related_name='connection'
        )
    followers = models.ManyToManyField('InstaUser',
        related_name="followers",
        blank=True)
    following = models.ManyToManyField('InstaUser',
        related_name="following",
        blank=True)

class Post(models.Model):
    author = models.ForeignKey( # a foreign key indicate a Many-To-One relationship
        InstaUser, #foreign key is InstaUser
        blank=True, 
        null=True,
        on_delete=models.CASCADE, # delete this author will delete all his posts
        related_name='posts', # we can use author.posts to get all posts belong to this user
        )
    title = models.TextField(blank=True, null=True)
    image = ProcessedImageField(
        upload_to='static/images/posts',
        format='JPEG',
        options={ 'quality': 100},
        blank=True,
        null=True,
        )
    posted_on = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.title