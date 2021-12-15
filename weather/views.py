import requests
from datetime import datetime, timezone, timedelta
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from weather.helpers import get_wind_full_description, get_cloudiness_description


@api_view(['GET'])
def get_weather(request):

    city = request.query_params.get('city', None)
    country = request.query_params.get('country', None)
    units = request.query_params.get('units', 'metric')

    if not city:
        return Response('city is required', status=status.HTTP_400_BAD_REQUEST)

    allowed_units = ('metric', 'imperial')
    if units not in allowed_units:
        return Response("Only 'metric' and 'imperial' are allowed units", status=status.HTTP_400_BAD_REQUEST)

    if country:
        city += f',{country.lower()}'

    # Get weather data from API
    url = f'{settings.WEATHER_API_URL}/weather'
    params = {'q': city, 'units': units, 'appid': settings.WEATHER_API_KEY}
    res_weather = requests.get(url, params=params)
    status_code = res_weather.status_code

    if status_code == 404:
        return Response('Location not found', status=status.HTTP_404_NOT_FOUND)

    # TODO: Retrieve and include forecasts
    degree_unit = f"°{'C' if units == 'metric' else 'F'}"
    weather_data = res_weather.json()

    # Set up sunrise/sunset based in given timezone
    t_zone = timezone(timedelta(seconds=weather_data['timezone']))
    sunrise_datetime = datetime.fromtimestamp(weather_data['sys']['sunrise'], tz=t_zone)
    sunset_datetime = datetime.fromtimestamp(weather_data['sys']['sunset'], tz=t_zone)

    wind_speed = weather_data['wind']['speed']
    wind_degrees = weather_data['wind']['deg']
    payload = {
        "location_name": f"{weather_data['name']}, {weather_data['sys']['country']}",
        "temperature": f"{weather_data['main']['temp']} {degree_unit}",
        "wind": get_wind_full_description(wind_speed, wind_degrees, units),
        "cloudiness": get_cloudiness_description(weather_data['clouds']['all']),
        "pressure": f"{weather_data['main']['pressure']} hPa",
        "humidity": f"{weather_data['main']['humidity']}%",
        "sunrise": sunrise_datetime.strftime('%H:%M'),
        "sunset": sunset_datetime.strftime('%H:%M'),
        "geo_coordinates": f"[{weather_data['coord']['lat']},{weather_data['coord']['lon']}]",
        "requested_time": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        # TODO: Should retrieve forecasts
        # "forecast": []
    }

    return Response(payload, status=status_code)
