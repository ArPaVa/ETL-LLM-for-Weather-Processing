from models.forecast import save_combined_forecasts, get_forecasts_without_recommendations, parse_and_store_recommendation
from api_ingestion.api_ingestion import get_forecast_OWM, get_forecast_WA
from api_ingestion.api_ingestion import combine_forecasts_by_key
from models.forecast import Base, WeatherForecast
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from llm.prompts import *
from llm.llm import *
from config import *

def db_creation():
    engine = create_engine(DB_URL, echo=False)
    Base.metadata.create_all(engine)   # creates table if not exists

    Session = sessionmaker(bind=engine)
    session = Session()
    return session

session = db_creation()

def extract_and_store_forecasts(lat, lon):
    # Checks if latitude and longitud are within the valid values
    if abs(lat)>90:
        print("Latitude wasn't a valid value")
        return
    if abs(lon)>180:
        print("Longitude wasn't a valid value")
        return
    
    # Makes the API request to Openweathermaps and Weatherapi with the lat and lon
    owm_data = get_forecast_OWM(lat, lon)
    wa_data = get_forecast_WA(lat, lon)
    # Creates one set data joining  both responses by lat/long/date/time
    combined_data = combine_forecasts_by_key(owm_data,wa_data)
    # Maps combined_data to a weatherforecast ORM object, and saves it to postgreSQL
    save_combined_forecasts(session, combined_data)

def generate_recommendations(session):
    # Makes a postgreSQL request to get a list of weatherforecast objects that dont have recomendations
    unrecommended_forecasts = get_forecasts_without_recommendations(session)
    if not unrecommended_forecasts:
        print("No forecasts without recommendations found.")
    else:
        # The for is limited to the first 10 objects to deal with Gemini's API free tier limitations
        for forecast in unrecommended_forecasts[:10]:
            # Creates a prompt that matches the current forecast by introducing the forecast variables in the prompt
            prompt = build_activity_prompt_from_row(forecast)
            # Makes a request the gemini's gemini 2.5 flash lite model wich is the functional model with more requests 
            # per day
            response = geminicall(prompt)
            # Parses the "JSON" response to an ORM object and saves it to postgreSQL
            parse_and_store_recommendation(session=session,weather_forecast_id=forecast.id,gemini_response_text=response.text)


generate_recommendations(session)
#print(f"Found {len(unrecommended_forecasts)} forecasts without LLM recommendations.")
