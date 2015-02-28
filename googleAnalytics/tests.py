from django.test import TestCase
from googleAnalytics.analyticsmanager import AnalyticsManager
from django.contrib.auth.models import User
from mock import patch, Mock, MagicMock
import json

# Create your tests here.


class AnalyticsManagerTestCase(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.manager = AnalyticsManager()
        self.jsonstr = json.loads('{"name":"haike","sex":"male"}')
        self.manager.API_call = MagicMock(return_value = self.jsonstr)

    def test_api_call(self):
        apiresult = self.manager.API_call(self.manager.GA_REPORTING_URL)
        self.assertEqual(apiresult, self.jsonstr, "apicall result was not jsonstr")

