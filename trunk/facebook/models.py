from django.db import models


# Create your models here.
class FacebookSettings(models.Model):
    app_id = models.CharField(max_length=400)
    app_secret = models.CharField(max_length=400)
    token = models.CharField(max_length=400)

    def __unicode__(self):
        return 'app id: {}'.format(self.app_id)