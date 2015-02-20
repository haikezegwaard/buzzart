from django.test import TestCase
from googleAnalytics.analyticsmanager import AnalyticsManager
from django.contrib.auth.models import User
# Create your tests here.


class AnalyticsManagerTestCase(TestCase):

    analytics_manager = None

    def setUp(self):
        TestCase.setUp(self)
        self.user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')
        self.analytics_manager = AnalyticsManager()


