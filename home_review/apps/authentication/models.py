from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class SocialAuth(models.Model):
    """Social Auth Model"""
    social_auth_id = models.CharField(unique=True, max_length=500)
    email = models.CharField(unique=True, max_length=250)
    fullname = models.CharField(max_length=250)
    phone = models.CharField(max_length=250)
    photo = models.CharField(max_length=1250)
    location = models.CharField(max_length=250)
    birthDate = models.DateTimeField(null=True)
    gender = models.CharField(max_length=250, default='non')

    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """ String representation of db object """
        return 'platform : {} ,user_id: {}'.format(
            self.social_auth_id, self.email)
