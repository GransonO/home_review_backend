from django.db import models


class Support(models.Model):
    """Social Auth Model"""
    support_id = models.CharField(unique=True, max_length=250)
    user_id = models.CharField(max_length=500)
    email = models.CharField(unique=True, max_length=250)
    details = models.CharField(max_length=1250)
    title = models.CharField(max_length=550)
    photo = models.CharField(max_length=1250)
    tracker = models.BooleanField(default=True)
    response = models.CharField(max_length=1250, default='no response')

    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """ String representation of db object """
        return 'platform : {} ,user_id: {}'.format(
            self.social_auth_id, self.email)
