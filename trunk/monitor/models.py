from django.db import models
from nikiInterest.models import InterestAccount


# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=400)
    manager = models.CharField(max_length=400)
    email = models.EmailField()
    url = models.URLField()
    nikiProject = models.CharField(max_length=1000)
    # ga_view = models.CharField(max_length = 1000)
    mailchimp_list_id = models.CharField(max_length=1000)
    mailchimp_api_token = models.CharField(max_length=1000)
    fanpage_id = models.CharField(max_length=1000)

    def __unicode__(self):
        return self.name


# Account for SOAP interest service
class InterestProject(models.Model):
    project = models.ForeignKey(Project)
    nikiProjectId = models.CharField(max_length=400)
    interestAccount = models.ForeignKey(InterestAccount)


# Periodic summary
class Summary(models.Model):
    project = models.ForeignKey(Project)

    introduction = models.TextField(blank=True)
    traffic_advice = models.TextField(blank=True)
    availability_advice = models.TextField(blank=True)
    facebook_advice = models.TextField(blank=True)
    mailchimp_advice = models.TextField(blank=True)
    conversion_advice = models.TextField(blank=True)

    dateStart = models.DateField()
    dateEnd = models.DateField()

    def __unicode__(self):
        return '{}: {} - {}'.format(self.project.name, self.dateStart, self.dateEnd)


class BuzzartUpdate(models.Model):
    project = models.ForeignKey(Project)
    update = models.TextField(blank=True)
    title = models.CharField(max_length=1000, blank=True)
    posted = models.DateTimeField(blank=True)
    fa_class = models.TextField(max_length=1000, default='fa-check')

    def __unicode__(self):
        return '{}: {} - {}'.format(self.project.name, self.title, self.posted)
