import os
from dotenv import load_dotenv

load_dotenv()  # loads variables from .env into the environment

OPENWEATHERMAP_API_KEY = os.getenv("OPENWHEATHERMAP_API_KEY")
OPEN_METEO_API_KEY = os.getenv("OPEN_METEO_API_KEY")
OPENWEATHERMAP_URL = "https://api.openweathermap.org/data/2.5/forecast"