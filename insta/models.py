from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.

class Post(models.Model):
    caption = models.TextField()

class InstaUser(AbstractUser):
    age = models.PositiveIntegerField(default=0)