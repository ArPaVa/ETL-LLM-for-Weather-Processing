import os
from dotenv import load_dotenv

load_dotenv()  # loads variables from .env into the environment

OPENWEATHERMAP_API_KEY = os.getenv("OPENWHEATHERMAP_API_KEY")
WEATHERAPI_API_KEY = os.getenv("WEATHERAPI_API_KEY")
OPENWEATHERMAP_URL = "https://api.openweathermap.org/data/2.5/forecast"
WEATHERAPI_URL = "https://api.weatherapi.com/v1/forecast.json"
           #url = "http://api.weatherapi.com/v1/forecast.json"
PG_USER= os.getenv("DB_USERNAME")
PG_PASSWORD= os.getenv("DB_PASSWORD")
PG_HOST= os.getenv("DB_HOST")
PG_PORT= os.getenv("DB_PORT")
PG_DATABASE= os.getenv("DB_NAME")
DB_URL = (f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}")