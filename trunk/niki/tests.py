from django.test import TestCase
from django.core.urlresolvers import reverse
from nikiconverter import NikiConverter


# Create your tests here.
class NikiAPITest(TestCase):

    def setUp(self):
        self.manager = NikiConverter()
        self.resource = '/projects/54/AMVP9518'

    def test_api_request(self):
        response = self.manager.apiRequest(self.resource)
        self.assertIn('location', response, 'string "location" not in response')

    def test_get_availability(self):
        availability = self.manager.getAvailability(self.resource)
        self.assertEqual(len(availability), 3, 'length of availability array is not 3')

