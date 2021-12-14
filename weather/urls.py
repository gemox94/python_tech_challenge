from django.urls import path

from weather.views import get_weather

app_name = 'weather'

urlpatterns = [
    path('', get_weather, name='weather'),
]
