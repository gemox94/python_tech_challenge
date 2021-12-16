"""Helper functions related to weather app"""

import requests
from datetime import datetime, timezone, timedelta
from django.conf import settings

WIND_RANGES = [
    {
        'imperial_min': 0,
        'imperial_max': 1,
        'metric_min': 0,
        'metric_max': 0.2,
        'label': 'Calm'
    },
    {
        'imperial_min': 1,
        'imperial_max': 4,
        'metric_min': 0.2,
        'metric_max': 1.5,
        'label': 'Light air'
    },
    {
        'imperial_min': 4,
        'imperial_max': 8,
        'metric_min': 1.5,
        'metric_max': 3.3,
        'label': 'Light breeze'
    },
    {
        'imperial_min': 8,
        'imperial_max': 13,
        'metric_min': 3.4,
        'metric_max': 5.4,
        'label': 'Gentle breeze'
    },
    {
        'imperial_min': 13,
        'imperial_max': 19,
        'metric_min': 5.4,
        'metric_max': 7.9,
        'label': 'Moderate breeze'
    },
    {
        'imperial_min': 19,
        'imperial_max': 25,
        'metric_min': 7.9,
        'metric_max': 10.7,
        'label': 'Fresh breeze'
    },
    {
        'imperial_min': 25,
        'imperial_max': 32,
        'metric_min': 10.7,
        'metric_max': 13.8,
        'label': 'Strong breeze'
    },
    {
        'imperial_min': 32,
        'imperial_max': 39,
        'metric_min': 13.8,
        'metric_max': 17.1,
        'label': 'Near gale'
    },
    {
        'imperial_min': 39,
        'imperial_max': 47,
        'metric_min': 17.1,
        'metric_max': 20.7,
        'label': 'Gale'
    },
    {
        'imperial_min': 47,
        'imperial_max': 55,
        'metric_min': 20.7,
        'metric_max': 24.4,
        'label': 'Strong gale'
    },
    {
        'imperial_min': 55,
        'imperial_max': 64,
        'metric_min': 24.4,
        'metric_max': 28.4,
        'label': 'Whole gale'
    },
    {
        'imperial_min': 64,
        'imperial_max': 75,
        'metric_min': 28.4,
        'metric_max': 32.6,
        'label': 'Storm force'
    },
    {
        'imperial_min': 75,
        'imperial_max': 1000,
        'metric_min': 32.6,
        'metric_max': 1000,
        'label': 'Hurricane force'
    },
]


def get_datetime_from_city_timestamp(datetime_milliseconds, timezone_seconds):
    t_zone = timezone(timedelta(seconds=timezone_seconds))
    return datetime.fromtimestamp(datetime_milliseconds, tz=t_zone)


def get_wind_direction(wind_degrees):
    """Function to get wind direction based in wind degrees"""
    valid_types = (int, float)
    if type(wind_degrees) not in valid_types:
        return 'Must provide a valid wind degrees'

    if wind_degrees >= 337.50:
        direction = 'north-northwest'
    elif wind_degrees >= 315:
        direction = 'northwest'
    elif wind_degrees >= 292.50:
        direction = 'west-northwest'
    elif wind_degrees >= 270:
        direction = 'west'
    elif wind_degrees >= 247.50:
        direction = 'west-southwest'
    elif wind_degrees >= 225:
        direction = 'southwest'
    elif wind_degrees >= 202.50:
        direction = 'south-southwest'
    elif wind_degrees >= 180:
        direction = 'south'
    elif wind_degrees >= 157.50:
        direction = 'south-southeast'
    elif wind_degrees >= 135:
        direction = 'southeast'
    elif wind_degrees >= 112.50:
        direction = 'east-southeast'
    elif wind_degrees >= 90:
        direction = 'east'
    elif wind_degrees >= 67.50:
        direction = 'east-northeast'
    elif wind_degrees >= 45:
        direction = 'northeast'
    elif wind_degrees >= 22.50:
        direction = 'north-northeast'
    else:
        direction = 'north'

    return direction


def get_wind_description(wind_speed, units):

    valid_types = (int, float)
    if type(wind_speed) not in valid_types:
        return 'Must provide a valid wind speed'

    valid_units = ('metric', 'imperial')
    if units not in valid_units:
        return 'Must provide a valid unit'

    min_field = 'metric_min' if units == 'metric' else 'imperial_min'
    max_field = 'metric_max' if units == 'metric' else 'imperial_max'
    wind_label = next(
        (w_range['label'] for w_range in WIND_RANGES if w_range[min_field] <= wind_speed < w_range[max_field]), None
    )

    if not wind_label:
        return 'Wind speed description not found'

    return wind_label


def get_wind_full_description(wind_speed, wind_degrees, units):
    """Function to get readable wind information"""

    valid_types = (int, float)
    if type(wind_speed) not in valid_types or type(wind_degrees) not in valid_types:
        return 'Must provide valid wind speed and degrees'

    valid_units = ('metric', 'imperial')
    if units not in valid_units:
        return 'Invalid units'

    wind_speed_unit = 'm/s' if units == 'metric' else 'm/h'
    wind_direction = get_wind_direction(wind_degrees)
    wind_description = get_wind_description(wind_speed, units)

    return f"{wind_description}, {wind_speed} {wind_speed_unit}, {wind_direction}"


def get_cloudiness_description(cloud_percentage):
    """Function to get readable cloudiness information"""
    desc = 'Clear sky'
    if 10 < cloud_percentage <= 50:
        desc = 'Scattered clouds'
    elif 50 < cloud_percentage <= 90:
        desc = 'Broken'
    elif cloud_percentage > 90:
        desc = 'Overcast'

    return desc


def get_city_forecasts(city, units, country=None):

    valid_units = ('metric', 'imperial')
    if units not in valid_units:
        return 'Invalid units'

    url = f'{settings.WEATHER_API_URL}/forecast'
    q = f'{city},{country}' if country else city
    params = {'q': q, 'units': units, 'appid': settings.WEATHER_API_KEY}
    res = requests.get(url, params=params)

    if res.status_code != 200:
        return []

    forecasts_data = res.json()
    forecasts_list = forecasts_data['list']
    tz_seconds = forecasts_data['city']['timezone']
    degrees_unit = f"°{'C' if units == 'metric' else 'F'}"

    return [
        {
            'date': get_datetime_from_city_timestamp(forecast['dt'], tz_seconds).strftime('%Y-%m-%d'),
            'time': get_datetime_from_city_timestamp(forecast['dt'], tz_seconds).strftime('%H:%M'),
            'temperature': f"{forecast['main']['temp']} {degrees_unit}",
            'feels_like': f"{forecast['main']['feels_like']} {degrees_unit}",
            'min_temperature': f"{forecast['main']['temp_min']} {degrees_unit}",
            'max_temperature': f"{forecast['main']['temp_max']} {degrees_unit}",
            'pressure': f"{forecast['main']['pressure']} hPa",
            'humidity': f"{forecast['main']['humidity']}%",
        } for forecast in forecasts_list
    ]

