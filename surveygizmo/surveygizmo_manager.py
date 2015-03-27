'''
Created on Mar 27, 2015

@author: hz
'''
from monitor.models import Project
import requests
import json
import logging

class SurveyGizmoManager():
    
    SG_API_BASE_URL = 'https://restapi.surveygizmo.com/'
    SG_API_VERSION = 'v4'
    SG_API_URL = '{}{}'.format(SG_API_BASE_URL, SG_API_VERSION)
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def get_auth_credentials(self, project):
        account = project.surveygizmoaccount
        return {'user:pass': '{}:{}'.format(account.username, account.password),
                '_method': 'GET'}
        
    def get_survey(self, project):
        creds = self.get_auth_credentials(project)
        url = '{}/survey/{}'.format(self.SG_API_URL, project.surveygizmo_survey_id)
        self.logger.debug('surveygizmo: {}'.format(url))
        response = requests.get(url, params=creds)
        return json.loads(response.content)
        
    def get_survey_statistics(self, project):
        creds = self.get_auth_credentials(project)
        url = '{}/survey/{}/surveystatistic'.format(self.SG_API_URL, project.surveygizmo_survey_id)
        response = requests.get(url, params=creds)
        return json.loads(response.content)
    
    def get_survey_report(self, project):
        creds = self.get_auth_credentials(project)
        url = '{}/survey/{}/surveyreport'.format(self.SG_API_URL, project.surveygizmo_survey_id)
        response = requests.get(url, params=creds)
        return json.loads(response.content)
        
        
        
        