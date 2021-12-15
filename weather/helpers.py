"""Helper functions related to weather app"""


def get_wind_description(wind_speed, wind_degrees, units):
    """Function to get readable wind information"""
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
