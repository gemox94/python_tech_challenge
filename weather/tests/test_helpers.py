from django.test import TestCase

from weather.helpers import (
    get_wind_direction, get_wind_description, get_wind_full_description, get_cloudiness_description, get_city_forecasts
)

DEGREES_SYMBOL = '°'


class WeatherTestHelpers(TestCase):

    def __test_valid_city_forecasts(self, city_forecasts, units):
        self.assertTrue(len(city_forecasts) > 0)
        forecast = city_forecasts[0]
        degrees_unit = f'{DEGREES_SYMBOL}C' if units == 'metric' else f'{DEGREES_SYMBOL}F'
        self.assertTrue('temperature' in forecast)
        self.assertTrue(degrees_unit in forecast['temperature'])

    def test_get_wind_direction(self):
        self.assertEqual(get_wind_direction('something'), 'Must provide a valid wind degrees')
        self.assertEqual(get_wind_direction(337.50), 'north-northwest')
        self.assertEqual(get_wind_direction(320), 'northwest')
        self.assertEqual(get_wind_direction(202.50), 'south-southwest')
        self.assertEqual(get_wind_direction(180), 'south')
        self.assertEqual(get_wind_direction(145.5), 'southeast')
        self.assertEqual(get_wind_direction(90), 'east')
        self.assertEqual(get_wind_direction(48.6), 'northeast')
        self.assertEqual(get_wind_direction(5.6), 'north')

    def test_get_wind_description(self):
        self.assertEqual(get_wind_description('something', 'metric'), 'Must provide a valid wind speed')
        self.assertEqual(get_wind_description(.5, 'unknown'), 'Must provide a valid unit')
        self.assertEqual(get_wind_description(.5, 'metric'), 'Light air')
        self.assertEqual(get_wind_description(13, 'imperial'), 'Moderate breeze')
        self.assertEqual(get_wind_description(31.5, 'imperial'), 'Strong breeze')
        self.assertEqual(get_wind_description(1001, 'imperial'), 'Wind speed description not found')
        self.assertEqual(get_wind_description(1001, 'metric'), 'Wind speed description not found')

    def test_get_wind_full_description(self):
        self.assertEqual(
            get_wind_full_description('something', 'wrong', 'metric'),
            'Must provide valid wind speed and degrees'
        )

        self.assertEqual(
            get_wind_full_description(3.6, 0, 'unknown'),
            'Invalid units'
        )

        self.assertEqual(
            get_wind_full_description(3.6, 340.87, 'metric'),
            'Gentle breeze, 3.6 m/s, north-northwest'
        )

        self.assertEqual(
            get_wind_full_description(10.8, 300.00, 'imperial'),
            'Gentle breeze, 10.8 m/h, west-northwest'
        )

    def test_get_cloudiness_description(self):
        self.assertEqual(get_cloudiness_description(5), 'Clear sky')
        self.assertEqual(get_cloudiness_description(15), 'Scattered clouds')
        self.assertEqual(get_cloudiness_description(51), 'Broken')
        self.assertEqual(get_cloudiness_description(91), 'Overcast')

    def test_get_city_forecasts(self):

        self.assertEqual(
            get_city_forecasts('unknown', 'wrong_unit', country='mx'),
            'Invalid units'
        )
        self.assertTrue(len(get_city_forecasts('unknown', 'metric', country='mx')) == 0)

        city_forecasts = get_city_forecasts('Puebla', 'metric')
        self.__test_valid_city_forecasts(city_forecasts, 'metric')

        city_forecasts = get_city_forecasts('Puebla', 'metric', country='mx')
        self.__test_valid_city_forecasts(city_forecasts, 'metric')

        city_forecasts = get_city_forecasts('Bogota', 'imperial')
        self.__test_valid_city_forecasts(city_forecasts, 'imperial')

        city_forecasts = get_city_forecasts('Bogota', 'imperial', country='co')
        self.__test_valid_city_forecasts(city_forecasts, 'imperial')
