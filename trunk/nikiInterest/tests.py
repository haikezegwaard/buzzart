from django.test import TestCase
from models import InterestAccount
import datetime
from views import IndexView
from interestmanager import InterestManager
from django.test.client import RequestFactory
from django.test import Client


# Create your tests here.
class NikiInterestTest(TestCase):

    def setUp(self):
        now = datetime.datetime.today()
        InterestAccount.objects.create(username="am@fundament.nl", password="%v5%h#*BdJD", lastUpdate=now)
        self.account = InterestAccount.objects.get(username = "am@fundament.nl")
        self.manager = InterestManager()
        self.project_id = '89CCAA70-1844-E011-A130-005056AA000E'
        self.factory = RequestFactory()
        self.client = Client()

    def test_getIdsByProjectFrom(self):
        from_date = datetime.datetime.today() - datetime.timedelta(days = 14)
        ids = self.manager.getIdsByProjectFrom(self.account, self.project_id, from_date)
        self.assertNotEqual(None, ids, 'ids was none')

    def test_getIdsByProject(self):
        ids = self.manager.getIdsByProject(self.account, self.project_id)
        self.assertNotEqual(None, ids, 'ids was none')

    def test_getByIds(self):
        ids = self.manager.getIdsByProject(self.account, self.project_id)
        result = self.manager.getByIds(self.account, ids)
        self.assertIsNotNone(result, 'result was None')

    """def test_niki_interest_subscription_dates(self):
        startstr = '20140801'
        endstr = '20141001'
        response = self.client.get('/cyfe/niki/subscriptions/?project={}&start_date={}&end_date={}'.format(self.project_id,startstr,endstr))
        self.assertEqual(response.status_code, 200)"""