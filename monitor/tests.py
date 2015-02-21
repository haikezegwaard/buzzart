from django.test import TestCase
from monitor import models, managers
from django.contrib.auth.models import User

class MonitorTestCase(TestCase):

    def setUp(self):
        self.first = models.Account.objects.create(name="testaccount")
        self.user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')
        self.jnjmodels.Role.objects.create(account=first,user=user,role="owner")

        models.Account.objects.create(name="secondtestaccount")

    def test_get_account_users(self):
        manager = managers.AccountManager()
    manager.get_account_members(account, role)