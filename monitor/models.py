from django.db import models
from nikiInterest.models import InterestAccount
from django.contrib.auth.models import User
import settings
from south.tests.fakeapp.models import Recursive
from relativefilepathfield.fields import RelativeFilePathField

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=400)
    manager = models.CharField(max_length=400)
    email = models.EmailField()
    url = models.URLField()
    nikiProject = models.CharField(max_length=1000, null= True, blank=True)    
    mailchimp_list_id = models.CharField(max_length=1000, null= True, blank=True)
    mailchimp_api_token = models.CharField(max_length=1000, null= True, blank=True)
    fanpage_id = models.CharField(max_length=1000, null= True, blank=True)
    fanpage_token = models.CharField(max_length=1000, null= True, blank=True)
    surveygizmo_survey_id = models.CharField(max_length=1000, null= True, blank=True)
    
    template_dir = '{}/dashboard/templates'.format(settings.PROJECT_ROOT)
    template = RelativeFilePathField(path=template_dir, 
                                    recursive=True, 
                                    allow_files=False, 
                                    allow_folders=True, blank=False, null=False,
                                    default='')

    def __unicode__(self):
        return self.name
    
    class Meta:
        permissions = (
            ('view_project', 'View Project'),
        )
        

class Account(models.Model):
    name = models.CharField(max_length=512, blank=False, null=False)
    users = models.ManyToManyField(User, related_name='accounts', blank=True)    

    def __unicode__(self):
        return self.name

# Account for SOAP interest service
class InterestProject(models.Model):
    project = models.ForeignKey(Project)
    nikiProjectId = models.CharField(max_length=400)
    interestAccount = models.ForeignKey(InterestAccount)

    def __unicode__(self):
        return self.project.name


# Periodic summary
class Summary(models.Model):
    project = models.ForeignKey(Project)

    introduction = models.TextField(blank=True)
    traffic_advice = models.TextField(blank=True)
    availability_advice = models.TextField(blank=True)
    facebook_advice = models.TextField(blank=True)
    mailchimp_advice = models.TextField(blank=True)
    conversion_advice = models.TextField(blank=True)

    mail_sent = models.BooleanField(blank=False, default=False)

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
    mail_sent = models.BooleanField(default=False)

    def __unicode__(self):
        return '{}: {} - {}'.format(self.project.name, self.title, self.posted)
