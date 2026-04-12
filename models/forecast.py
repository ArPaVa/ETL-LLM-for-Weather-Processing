from sqlalchemy import create_engine, Column, Integer, String, Numeric, Date, Time, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.schema import Index
import datetime

Base = declarative_base()

class WeatherForecast(Base):
    __tablename__ = "weather_forecast"

    id = Column(Integer, primary_key=True)
    #key = Column(String, nullable=False)              # your unique key#REALLY??
    #Fields from OWM
    #location and time
    lat = Column(Numeric(precision=9, scale=6), nullable=False)
    lon = Column(Numeric(precision=9, scale=6), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)

    #temperature
    temperature = Column(Numeric(precision=6, scale=2))
    feels_like = Column(Numeric(precision=6, scale=2))

    #moisture
    humidity = Column(Numeric(precision=5, scale=1))
    pressure = Column(Numeric(precision=6, scale=0))

    #sky state
    weather = Column(String)
    cloudiness = Column(Integer)                       # 0–100
    visibility = Column(Numeric(precision=9, scale=0)) # meters or km

    #wind
    wind_speed = Column(Numeric(precision=5, scale=1))
    wind_gust = Column(Numeric(precision=5, scale=1))

    #fields from WA
    moon_phase = Column(String)                                 # "New Moon", "Full Moon", etc.
    moon_illumination = Column(Numeric(precision=5, scale=2))   # 0–100 %
    precip_mm = Column(Numeric(precision=7, scale=2))           
    snow_cm = Column(Numeric(precision=6, scale=2))             
    chance_of_rain = Column(Numeric(precision=5, scale=2))      # 0–100 %
    chance_of_snow = Column(Numeric(precision=5, scale=2))      # 0–100 %
    uv = Column(Numeric(precision=4, scale=2))                  # UV index

    # solar irradiance (if available from some API)
    short_rad = Column(Numeric(precision=7, scale=2))           # short‑wave radiation W/m²
    diff_rad = Column(Numeric(precision=7, scale=2))            # diffuse radiation W/m²
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


# Index to make it quicker to index in this values in PostgreSQL
WeatherForecast.__table__.append_constraint(
    Index("idx_weather_latlon_time", "lat", "lon", "date", "time")
)

def save_combined_forecasts(session: Session, combined_rows):
    objects = []

    for row in combined_rows:
        obj = WeatherForecast(
            lat=row["lat"],
            lon=row["lon"],
            date=row["date"],
            time=row["time"],
            temperature=row["temperature"],
            feels_like=row["feels_like"],
            humidity=row["humidity"],
            pressure=row["pressure"],
            weather=row["weather"],
            cloudiness=row["cloudiness"],
            visibility=row["visibility"],
            wind_speed=row["wind_speed"],
            wind_gust=row["wind_gust"],
            moon_phase=row["moon_phase"],
            moon_illumination=row["moon_illumination"],
            precip_mm=row["precip_mm"],
            snow_cm=row["snow_cm"],
            chance_of_rain=row["chance_of_rain"],
            chance_of_snow=row["chance_of_snow"],
            uv=row["uv"],
            short_rad=row["short_rad"],
            diff_rad=row["diff_rad"],
        )
        objects.append(obj)

    session.add_all(objects)
    session.commit()
    return objects