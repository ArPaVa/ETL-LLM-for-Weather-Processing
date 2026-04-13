from datetime import datetime
from config import *
import requests

#OWM = Openweathermap
def get_forecast_OWM(lat, lon, units="metric"):
    params = {
        "lat": lat,
        "lon": lon,
        "appid": OPENWEATHERMAP_API_KEY,
        "units": units,
    }

    response = requests.get(OPENWEATHERMAP_URL, params=params, timeout=10)
    response.raise_for_status()
    return response.json(),lat,lon

#WA = WeatherApi
def get_forecast_WA(lat, lon):

    params = {
        "key": WEATHERAPI_API_KEY,
        "q": f"{lat},{lon}",       # WeatherAPI expects "lat,lon" as 'q'
        "days": 5
    }
    
    response = requests.get(WEATHERAPI_URL, params=params, timeout=10)
    response.raise_for_status()
    return response.json(),lat,lon

def normalize_OWM(data):
    """Return dict: key = (lat, lon, date, time) -> fields"""
    data,lat,lon = data
    out = {}

    for item in data["list"]:
        dt = datetime.strptime(item["dt_txt"], "%Y-%m-%d %H:%M:%S")
        main = item.get("main", {})
        weather = item.get("weather", [{}])[0]
        wind = item.get("wind", {})
        clouds = item.get("clouds", {})

        key = (lat, lon, str(dt.date()), str(dt.time()))

        out[key] = {
            "temperature": main.get("temp"),
            "feels_like": main.get("feels_like"),
            "humidity": main.get("humidity"),
            "pressure": main.get("pressure"),
            "weather": weather.get("description"),
            "cloudiness": clouds.get("all"),
            "visibility": item.get("visibility"),
            "wind_speed": wind.get("speed"),
            "wind_gust": wind.get("gust"),
        }
    return out

def normalize_WA(data):
    out = {}
    data,lat,lon = data
    for day in data["forecast"]["forecastday"]:
        t_str = day["hour"][0]["time"]  # e.g., "2025-04-01 00:00"
        dt = datetime.fromisoformat(t_str).date()
        for hour in day["hour"]:
            t = datetime.fromisoformat(hour["time"]).time()
            astro = day.get("astro", {})
            cond = hour.get("condition", {}) if hour.get("condition") else {}

            key = (lat, lon, str(dt), str(t))

            out[key] = {
                "moon_phase": astro.get("moon_phase"),
                "moon_illumination": astro.get("moon_illumination"),
                "precip_mm": hour.get("precip_mm"),
                "snow_cm": hour.get("snow_cm"),
                "chance_of_rain": hour.get("chance_of_rain"),
                "chance_of_snow": hour.get("chance_of_snow"),
                "uv": hour.get("uv"),
                "short_rad": hour.get("short_rad"),
                "diff_rad": hour.get("diff_rad"),
            }
    return out

def combine_forecasts_by_key(owm_data, wa_data):
    owm_map = normalize_OWM(owm_data)
    wa_map = normalize_WA(wa_data)

    all_keys = sorted(owm_map.keys() & wa_map.keys())
    combined = []

    for key in all_keys:
        lat, lon, date_, time_ = key

        owm_row = owm_map.get(key, {})
        wa_row = wa_map.get(key, {})

        row = {
            "lat": lat,
            "lon": lon,
            "date": date_,
            "time": time_,
            "temperature": owm_row["temperature"],
            "feels_like": owm_row["feels_like"],
            "humidity": owm_row["humidity"],
            "pressure": owm_row["pressure"],
            "weather": owm_row["weather"],
            "cloudiness": owm_row["cloudiness"],
            "visibility": owm_row["visibility"],
            "wind_speed": owm_row["wind_speed"],
            "wind_gust": owm_row["wind_gust"],
            "moon_phase": wa_row["moon_phase"],
            "moon_illumination": wa_row["moon_illumination"],
            "precip_mm": wa_row["precip_mm"],
            "snow_cm": wa_row["snow_cm"],
            "chance_of_rain": wa_row["chance_of_rain"],
            "chance_of_snow": wa_row["chance_of_snow"],
            "uv": wa_row["uv"],
            "short_rad": wa_row["short_rad"],
            "diff_rad": wa_row["diff_rad"],
        }
        combined.append(row)

    return combined