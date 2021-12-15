"""Helper functions related to weather app"""


def get_wind_direction(wind_degrees):
    """Function to get wind direction based in wind degrees"""
    pass


def get_wind_description(wind_speed, wind_degrees, units):
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
