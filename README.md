## TL;DR
Python tech challenge!

Should consume Open Weather API and return weather and forcast for a given city:

```json
{
  "location_name": "Puebla, MX",
  "temperature": "22.87 °C",
  "wind": "Gentle breeze, 3.76 m/s, east",
  "cloudiness": "Clear sky",
  "pressure": "1014 hPa",
  "humidity": "39%",
  "sunrise": "06:57",
  "sunset": "17:57",
  "geo_coordinates": "[18.8333,-98]",
  "requested_time": "2021-12-15 23:59:31",
  "forecast": [
    {
      "date": "2021-12-15",
      "time": "18:00",
      "temperature": "22.87 °C",
      "feels_like": "22.23 °C",
      "min_temperature": "17.97 °C",
      "max_temperature": "22.87 °C",
      "pressure": "1014 hPa",
      "humidity": "39%"
    }
  ]
}
```

## `.env` file

We set up django to load `.env` file, here we've defined the following variables to interact with open weather API.

* WEATHER_API_URL
* WEATHER_API_KEY

## Local setup

1. Create virtual environment
   1. `python3 -m venv {path_to_your_venv}`
2. Activate environment
   1. `. {path_to_your_venv}/bin/activate`
3. Install project dependencies
   1. `pip install -r requirements.txt`
4. Run project
   1. `python manage.py runserver` this will be into port **8000**

## Endpoints

---

**GET:** `/api/v1/weather`

**query params:**

`city` - city name to search weather and forecasts

`country` - (optional) city country

`units` - (default: metric) measurement units, options: _metric_, _imperial_

---

## Tests

Inside the **weather** app is a folder called **tests**.

1. Activate environment
   1. `. {path_to_your_venv}/bin/activate`
2. Run tests
   1. `python manage.py test`

