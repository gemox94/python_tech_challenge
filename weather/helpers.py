"""Helper functions related to weather app"""


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


def get_wind_full_description(wind_speed, wind_degrees, units):
    """Function to get readable wind information"""

    valid_types = (int, float)
    if type(wind_speed) not in valid_types or type(wind_degrees) not in valid_types:
        return 'Must provide valid wind speed and degrees'

    valid_units = ('metric', 'imperial')
    if units not in valid_units:
        return 'Invalid units'

    return ''


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
