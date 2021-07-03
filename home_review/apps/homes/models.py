from django.db import models


class Homes(models.Model):
    """Home Model"""
    home_id = models.CharField(unique=True, max_length=250)
    user_id = models.CharField(max_length=500, null=True)
    description = models.CharField(max_length=1500, null=True)
    administrator = models.CharField(max_length=200, null=True)
    bathrooms = models.CharField(max_length=200, null=True)
    bedrooms = models.CharField(max_length=200, null=True)
    place_id = models.CharField(max_length=200, null=True)
    place_image = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=200, null=True)

    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """ String representation of db object """
        return 'platform : {} ,user_id: {}'.format(
            self.home_id, self.email)
