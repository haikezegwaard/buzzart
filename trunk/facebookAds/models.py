from django.db import models

# Create your models here.
class FacebookAdsSettings(models.Model):
    access_token = models.CharField(max_length=400)
    expires = models.DateTimeField(blank=True)

