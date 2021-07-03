from django.db import models


class Reviews(models.Model):
    """Social Auth Model"""
    review_id = models.CharField(unique=True, max_length=250)
    user_id = models.CharField(max_length=500)
    reviewer = models.CharField(max_length=500)
    email = models.CharField(unique=True, max_length=250)
    review_details = models.CharField(max_length=1250)
    title = models.CharField(max_length=550)
    review_image = models.CharField(max_length=550, default="non")
    place_image = models.CharField(max_length=550, default="non")
    place_address = models.CharField(max_length=550, default="non")
    place_id = models.CharField(max_length=1250, default="non")
    place_name = models.CharField(max_length=1250, default="non")
    # Other ratings
    rating = models.FloatField(default=0.0)
    admin = models.FloatField(default=0.0)
    units = models.FloatField(default=0.0)
    environment = models.FloatField(default=0.0)
    amenities = models.FloatField(default=0.0)

    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """ String representation of db object """
        return 'platform : {} , email: {}'.format(
            self.review_id, self.email)
