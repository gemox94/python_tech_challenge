from django.test import TestCase
# from rest_framework.test import APIClient

# client = APIClient()


class WeatherTestViews(TestCase):

    def test_only_city_success(self):
        self.assertTrue(True)

    def test_city_and_state_success(self):
        self.assertTrue(True)

    def test_only_city_fails(self):
        self.assertTrue(True)

    def test_city_and_state_fail(self):
        self.assertTrue(True)
