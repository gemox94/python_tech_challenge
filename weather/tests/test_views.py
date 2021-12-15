from rest_framework.test import APITestCase

WEATHER_URL = '/api/v1/weather'
DEGREES_SYMBOL = '°'


def _is_valid_location(weather, location_name):
    """Function to validate if a weather response has at least valida keys for a successful response"""

    return (
            'location_name' in weather and
            weather['location_name'] == location_name and
            'temperature' in weather and weather['temperature']
    )


def _is_valid_temperature_unit(weather, unit):
    unit_to_validate = f'{DEGREES_SYMBOL}C' if unit == 'metric' else f'{DEGREES_SYMBOL}F'
    return 'temperature' in weather and unit_to_validate in weather['temperature']


class WeatherTestViews(APITestCase):

    def __test_temperature_unit(self, unit):
        res = self.client.get(f"{WEATHER_URL}?city=bogota&country=co&units={unit}")
        status_code = res.status_code
        data = res.data
        self.assertEqual(status_code, 200)
        self.assertTrue(_is_valid_location(data, 'Bogota, CO'))
        self.assertTrue(_is_valid_temperature_unit(data, unit))

    def test_no_city_is_passed(self):
        res = self.client.get(f"{WEATHER_URL}")
        status_code = res.status_code
        data = res.data
        self.assertEqual(status_code, 400)
        self.assertEqual(data, 'city is required')

    def test_wrong_unit_passed(self):
        res = self.client.get(f"{WEATHER_URL}?city=puebla&units=unknown")
        status_code = res.status_code
        data = res.data
        self.assertEqual(status_code, 400)
        self.assertEqual(data, "Only 'metric' and 'imperial' are allowed units")

    def test_only_city_success(self):
        res = self.client.get(f"{WEATHER_URL}?city=puebla&units=metric")
        status_code = res.status_code
        data = res.data
        self.assertEqual(status_code, 200)
        self.assertTrue(_is_valid_location(data, 'Puebla, MX'))

    def test_city_and_state_success(self):
        res = self.client.get(f"{WEATHER_URL}?city=bogota&country=co&units=metric")
        status_code = res.status_code
        data = res.data
        self.assertEqual(status_code, 200)
        self.assertTrue(_is_valid_location(data, 'Bogota, CO'))

    def test_invalid_city_fails(self):
        res = self.client.get(f"{WEATHER_URL}?city=unknown&units=metric")
        status_code = res.status_code
        data = res.data
        self.assertEqual(status_code, 404)
        self.assertEqual(data, 'Location not found')

    def test_imperial_units(self):
        self.__test_temperature_unit('imperial')

    def test_metric_units(self):
        self.__test_temperature_unit('metric')
