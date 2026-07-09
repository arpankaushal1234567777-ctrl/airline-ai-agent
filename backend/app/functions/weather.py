import requests

from app.config import WEATHER_API_KEY

WEATHER_API_URL = "http://api.weatherapi.com/v1/current.json"


def get_weather(city: str):

    city = city.strip()

    if not WEATHER_API_KEY:
        return {
            "success": False,
            "message": "Weather API key is not configured.",
        }

    try:
        response = requests.get(
            WEATHER_API_URL,
            params={
                "key": WEATHER_API_KEY,
                "q": city,
            },
            timeout=10,
        )

        if response.status_code != 200:
            return {
                "success": False,
                "message": f"Weather API error: {response.json().get('error', {}).get('message', 'Unknown error')}",
            }

        data = response.json()

        return {
            "success": True,
            "city": data["location"]["name"],
            "country": data["location"]["country"],
            "temperature_celsius": data["current"]["temp_c"],
            "feels_like_celsius": data["current"]["feelslike_c"],
            "condition": data["current"]["condition"]["text"],
            "humidity_percent": data["current"]["humidity"],
            "wind_kph": data["current"]["wind_kph"],
        }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "message": "Weather API request timed out.",
        }

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "message": f"Weather API request failed: {e}",
        }
