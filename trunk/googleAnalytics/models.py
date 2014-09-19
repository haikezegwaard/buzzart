from django.db import models
from monitor.models import Project
# Create your models here.

# Create your models here.
class AnalyticsSettings(models.Model):
    project = models.ForeignKey(Project)
    sessions_target = models.IntegerField()
    pageviews_target = models.IntegerField()
    ga_view = models.CharField(max_length = 100)
    goal_to_track = models.CharField(max_length = 50)

    def __unicode__(self):
        return self.project.name;
