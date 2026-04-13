from models.forecast import save_combined_forecasts, get_forecasts_without_recommendations, parse_and_store_recommendation
from api_ingestion.api_ingestion import get_forecast_OWM, get_forecast_WA
from api_ingestion.api_ingestion import combine_forecasts_by_key
from models.forecast import Base, WeatherForecast
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from llm.prompts import *
from llm.llm import *
from config import *
import argparse
import sys

def db_creation():
    engine = create_engine(DB_URL, echo=False)
    Base.metadata.create_all(engine)   # creates table if not exists

    Session = sessionmaker(bind=engine)
    session = Session()
    return session

session = db_creation()

def extract_and_store_forecasts(lat, lon):
    # Checks if latitude and longitud are within the valid values
    print(f"Starting extraction for {lat}, {lon}")
    if abs(lat)>90:
        print("Latitude wasn't a valid value")
        return
    if abs(lon)>180:
        print("Longitude wasn't a valid value")
        return
    # Makes the API request to Openweathermaps and Weatherapi with the lat and lon
    owm_data = get_forecast_OWM(lat, lon)
    print("Request to Openweathermap successful")
    wa_data = get_forecast_WA(lat, lon)
    print("Request to Weatherapi successful")
    # Creates one set data joining  both responses by lat/long/date/time
    combined_data = combine_forecasts_by_key(owm_data,wa_data)
    print("APIs data successfully combined")
    # Maps combined_data to a weatherforecast ORM object, and saves it to postgreSQL
    save_combined_forecasts(session, combined_data)

def generate_recommendations(llm_calls=10):
    # Makes a postgreSQL request to get a list of weatherforecast objects that dont have recomendations
    unrecommended_forecasts = get_forecasts_without_recommendations(session)
    if not unrecommended_forecasts:
        print("No forecasts without recommendations found.")
    else:
        print("Unrecommended forecasts loaded from database")
        sorted_unrecommended_forecasts = sorted(unrecommended_forecasts, key=lambda x: x.id)
        i = 1
        # The for is limited to the first 10 objects to deal with Gemini's API free tier limitations
        for forecast in sorted_unrecommended_forecasts[:llm_calls]:
            print(f"Starting recommendation {i} from {llm_calls}")
            # Creates a prompt that matches the current forecast by introducing the forecast variables in the prompt
            prompt = build_activity_prompt_from_row(forecast)
            print(f"Prompt number {i} created")
            # Makes a request the gemini's gemini 2.5 flash lite model wich is the functional model with more requests 
            # per day
            print("Sending request to Gemini")
            response = geminicall(prompt)
            # Parses the "JSON" response to an ORM object and saves it to postgreSQL
            print("Saving recommendation forecast to database")
            parse_and_store_recommendation(session=session,weather_forecast_id=forecast.id,gemini_response_text=response.text)
            print(f"Creation of recommendation {i} from {llm_calls} finished")
            print("")
            i = i + 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    # subcommand: extract_and_store_forecasts
    extract_parser = subparsers.add_parser("extract", help="Fetch weather and save to DB")
    extract_parser.add_argument("lat", type=float, help="Latitude")
    extract_parser.add_argument("lon", type=float, help="Longitude")

    # subcommand: generate_recommendations
    gen_parser = subparsers.add_parser("recommend", help="Generate LLM recommendations for missing forecasts")
    gen_parser.add_argument("calls", type=int, default=10, help="Number of LLM calls to make (default: 10)")
    args = parser.parse_args()

    if args.command == "extract":
        extract_and_store_forecasts(args.lat, args.lon)
        print(f"Extracted and stored forecasts for lat={args.lat}, lon={args.lon}")

    elif args.command == "recommend":
        generate_recommendations(llm_calls=args.calls)
        print("Recommendations generated (or none needed).")

