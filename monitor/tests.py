from django.test import TestCase
from monitor import models, managers
from django.contrib.auth.models import User

class MonitorTestCase(TestCase):

    def setUp(self):
        self.first = models.Account.objects.create(name="testaccount")
        self.user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')
        

        models.Account.objects.create(name="secondtestaccount")

    