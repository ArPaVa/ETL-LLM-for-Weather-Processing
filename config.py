import os
from dotenv import load_dotenv

load_dotenv()  # loads variables from .env into the environment

OPENWHEATHERMAP_API_KEY = os.getenv("OPENWHEATHERMAP_API_KEY")
OPEN_METEO_API_KEY = os.getenv("OPEN_METEO_API_KEY")
