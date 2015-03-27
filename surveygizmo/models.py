'''
Created on Mar 27, 2015

@author: hz
'''
from django.db import models
from monitor.models import Project

class SurveyGizmoAccount(models.Model):
    project = models.OneToOneField(Project)
    username = models.CharField(max_length = 300)
    password = models.CharField(max_length = 300)
    