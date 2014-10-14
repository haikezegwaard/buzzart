from django.test import TestCase
import views
from django.http import HttpRequest, HttpResponse
from django.test.client import RequestFactory
# Create your tests here.


class CyfeNikiTests(TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.project = '/projects/54/AMVP9518'

    def test_nikisalecount(self):
        request = self.factory.get('/cyfe/niki/salecount/?project={}'.format(self.project))
        response = views.nikisalecount(request)
        self.assertContains(response, 'Te koop', count=1, status_code=200)
