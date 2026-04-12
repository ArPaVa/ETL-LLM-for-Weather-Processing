from api_ingestion.api_ingestion import get_forecast_OWM, get_forecast_WA

from datetime import datetime
from typing import Dict, Any
import json
from config import *
from sqlalchemy.orm import sessionmaker
from models.forecast import Base,WeatherForecast
from sqlalchemy import create_engine
from api_ingestion.api_ingestion import combine_forecasts_by_key
from models.forecast import save_combined_forecasts

def db_creation():
    engine = create_engine(DB_URL, echo=False)
    Base.metadata.create_all(engine)   # creates table if not exists

    Session = sessionmaker(bind=engine)
    session = Session()
    return session

# Usage (same as before)
owm_data = get_forecast_OWM(40.7128, -74.0060)  # New York City
wa_data = get_forecast_WA(40.7128, -74.0060)
combined_data = combine_forecasts_by_key(owm_data,wa_data)
print(json.dumps(combined_data,indent=2))


session = db_creation()
save_combined_forecasts(session, combined_data)

# data = get_forecast_OWM(40.7128, 74.0060) #New York City
# print(data)

# from datetime import datetime

# dataOWM = get_forecast_OWM(40.7128, -74.0060)  # your function

# city_lat = dataOWM["city"]["coord"]["lat"]
# city_lon = dataOWM["city"]["coord"]["lon"]
# api_source = "OpenWeatherMap"

# records = []

# for item in dataOWM["list"]:
#     dt_txt = item["dt_txt"]                      # "2026-04-09 21:00:00"
#     dt = datetime.fromisoformat(
#         dt_txt.replace(" ", "T")
#     )  # or use datetime.strptime(...) if needed

#     main = item["main"]
#     weather_descr = item["weather"][0]["description"] if item.get("weather") else "unknown"
#     wind = item.get("wind", {})

#     key = f"{city_lat}_{city_lon}_{dt.strftime('%Y%m%d_%H%M')}"

#     record = WeatherForecast(
#         key=key,
#         api_source=api_source,
#         lat=city_lat,
#         lon=city_lon,
#         date=dt.date(),
#         time=dt.time(),
#         temperature=main.get("temp"),
#         feels_like=main.get("feels_like"),
#         humidity=main.get("humidity"),
#         pressure=main.get("pressure"),
#         weather=weather_descr,
#         wind_speed=wind.get("speed"),
#         wind_gust=wind.get("gust"),
#         cloudiness=item.get("clouds", {}).get("all"),
#         visibility=item.get("visibility")
#     )
#     records.append(record)

# session.add_all(records)
# session.commit()
# session.close()