from sqlalchemy import create_engine, Column, Integer, String, Numeric, Date, Time, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship, join, outerjoin
from sqlalchemy.schema import Index
import datetime



Base = declarative_base()

class WeatherForecast(Base):
    __tablename__ = "weather_forecast"

    id = Column(Integer, primary_key=True)
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

class WeatherRecommendation(Base):
    __tablename__ = "weather_recommendations"

    id = Column(Integer, primary_key=True)

    # --- Foreign key to the weather data that generated this recommendation
    weather_forecast_id = Column(
        Integer,
        ForeignKey("weather_forecast.id", ondelete="CASCADE"),
        nullable=False,
    )

    # 1. running
    running_assessment = Column(String(16))  # YES/MAYBE/NO
    running_explanation = Column(Text)

    # 2. cycling
    cycling_assessment = Column(String(16))
    cycling_explanation = Column(Text)

    # 3. hiking
    hiking_assessment = Column(String(16))
    hiking_explanation = Column(Text)

    # 4. golfing
    golfing_assessment = Column(String(16))
    golfing_explanation = Column(Text)

    # 5. skydiving
    skydiving_assessment = Column(String(16))
    skydiving_explanation = Column(Text)

    # 6. swimming
    swimming_assessment = Column(String(16))
    swimming_explanation = Column(Text)

    # 7. surfing
    surfing_assessment = Column(String(16))
    surfing_explanation = Column(Text)

    # 8. birdwatching
    birdwatching_assessment = Column(String(16))
    birdwatching_explanation = Column(Text)

    # 9. picnics
    picnics_assessment = Column(String(16))
    picnics_explanation = Column(Text)

    # 10. photography
    photography_assessment = Column(String(16))
    photography_explanation = Column(Text)

    # 11. sunbathing
    sunbathing_assessment = Column(String(16))
    sunbathing_explanation = Column(Text)

    # 12. climbing
    climbing_assessment = Column(String(16))
    climbing_explanation = Column(Text)

    # 13. stargazing
    stargazing_assessment = Column(String(16))
    stargazing_explanation = Column(Text)

    # --- metadata
    created_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        nullable=False,
    )
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )

    # --- hook back to the weather row
    weather_forecast = relationship(
        "WeatherForecast",
        backref="recommendations",  # WeatherForecast.recommendations -> list of recommendations
    )

# --- index for fast lookups by weather snapshot
WeatherRecommendation.__table__.append_constraint(
    Index("idx_recommendation_weather", "weather_forecast_id")
)

def get_forecasts_without_recommendations(session: Session) -> list:
    """
    Return a list of WeatherForecast objects that do NOT have a recommendation yet.
    """

    # Use a LEFT JOIN and filter where the recommendation is NULL
    # i.e., forecast with no related WeatherRecommendation
    q = (
        session.query(WeatherForecast)
        .outerjoin(WeatherRecommendation, WeatherForecast.id == WeatherRecommendation.weather_forecast_id)
        .filter(WeatherRecommendation.id.is_(None))
    )

    return q.all()

import json
from sqlalchemy.orm import Session

def parse_and_store_recommendation(session: Session, weather_forecast_id, gemini_response_text):
    start = gemini_response_text.find("{")
    end   = gemini_response_text.rfind("}") + 1

    if start == -1 or end == 0 or start >= end:
        raise ValueError("No JSON object found in response")

    json_str = gemini_response_text[start:end]
    
    
    # 1. parse the raw JSON from Gemini
    data = json.loads(json_str)

    # 2. create a new WeatherRecommendation
    rec = WeatherRecommendation(
        weather_forecast_id = weather_forecast_id,

        # running
        running_assessment    = data["running"   ]["assessment"],
        running_explanation   = data["running"   ]["explanation"],

        # cycling
        cycling_assessment    = data["cycling"   ]["assessment"],
        cycling_explanation   = data["cycling"   ]["explanation"],

        # hiking
        hiking_assessment     = data["hiking"    ]["assessment"],
        hiking_explanation    = data["hiking"    ]["explanation"],

        # golfing
        golfing_assessment    = data["golfing"   ]["assessment"],
        golfing_explanation   = data["golfing"   ]["explanation"],

        # skydiving
        skydiving_assessment  = data["skydiving" ]["assessment"],
        skydiving_explanation = data["skydiving" ]["explanation"],

        # swimming
        swimming_assessment   = data["swimming"  ]["assessment"],
        swimming_explanation  = data["swimming"  ]["explanation"],

        # surfing
        surfing_assessment    = data["surfing"   ]["assessment"],
        surfing_explanation   = data["surfing"   ]["explanation"],

        # birdwatching
        birdwatching_assessment = data["birdwatching"]["assessment"],
        birdwatching_explanation= data["birdwatching"]["explanation"],

        # picnics
        picnics_assessment    = data["picnics"   ]["assessment"],
        picnics_explanation   = data["picnics"   ]["explanation"],

        # photography
        photography_assessment = data["photography"]["assessment"],
        photography_explanation= data["photography"]["explanation"],

        # sunbathing
        sunbathing_assessment = data["sunbathing"]["assessment"],
        sunbathing_explanation= data["sunbathing"]["explanation"],

        # climbing
        climbing_assessment   = data["climbing"  ]["assessment"],
        climbing_explanation  = data["climbing"  ]["explanation"],

        # stargazing
        stargazing_assessment = data["stargazing"]["assessment"],
        stargazing_explanation= data["stargazing"]["explanation"],
    )

    session.add(rec)
    session.commit()

    return rec

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