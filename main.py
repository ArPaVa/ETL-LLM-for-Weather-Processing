import json
from config import *
from llm.llm import *
from llm.prompts import *
from typing import Dict, Any
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.forecast import Base,WeatherForecast
from api_ingestion.api_ingestion import combine_forecasts_by_key
from api_ingestion.api_ingestion import get_forecast_OWM, get_forecast_WA
from models.forecast import save_combined_forecasts, get_forecasts_without_recommendations, parse_and_store_recommendation

def db_creation():
    engine = create_engine(DB_URL, echo=False)
    Base.metadata.create_all(engine)   # creates table if not exists

    Session = sessionmaker(bind=engine)
    session = Session()
    return session

# Usage (same as before)
#owm_data = get_forecast_OWM(40.7128, -74.0060)  # New York City
#wa_data = get_forecast_WA(40.7128, -74.0060)
#combined_data = combine_forecasts_by_key(owm_data,wa_data)

#session = db_creation()
#save_combined_forecasts(session, combined_data)

def generate_recommendations(session):

    unrecommended_forecasts = get_forecasts_without_recommendations(session)
    if not unrecommended_forecasts:
        print("No forecasts without recommendations found.")
    else:
        for forecast in unrecommended_forecasts[:10]:
            prompt = build_activity_prompt_from_row(forecast)
           
            response = geminicall(prompt)
            #print(response.text)
            parse_and_store_recommendation(session=session,weather_forecast_id=forecast.id,gemini_response_text=response.text)

session = db_creation()
generate_recommendations(session)
#print(f"Found {len(unrecommended_forecasts)} forecasts without LLM recommendations.")