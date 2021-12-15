from django.test import TestCase

from weather.helpers import get_wind_description, get_cloudiness_description


class WeatherTestHelpers(TestCase):

    def test_get_wind_description(self):
        self.assertEqual(
            get_wind_description('something', 'wrong', 'metric'),
            'Must provide valid wind speed and degrees'
        )

        self.assertEqual(
            get_wind_description(3.6, 0, 'unknown'),
            'Invalid units'
        )

        self.assertEqual(
            get_wind_description(3.6, 340.87, 'metric'),
            'Gentle breeze, 3.6 m/s, north-northwest'
        )

        self.assertEqual(
            get_wind_description(10.8, 300.00, 'imperial'),
            'Gentle breeze, 3.6 m/h, west-northwest'
        )

    def test_get_cloudiness_description(self):
        self.assertEqual(get_cloudiness_description(5), 'Clear sky')
        self.assertEqual(get_cloudiness_description(15), 'Scattered clouds')
        self.assertEqual(get_cloudiness_description(51), 'Broken')
        self.assertEqual(get_cloudiness_description(91), 'Overcast')
