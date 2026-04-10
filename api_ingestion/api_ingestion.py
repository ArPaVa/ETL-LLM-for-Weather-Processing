import os
import requests
from config import *

#OWM = OPENWHEATERMAP
def get_forecast_OWM(lat, lon, units="metric"):
    params = {
        "lat": lat,
        "lon": lon,
        "appid": OPENWEATHERMAP_API_KEY,
        "units": units,
    }

    response = requests.get(OPENWEATHERMAP_URL, params=params, timeout=10)
    response.raise_for_status()
    return response.json()

