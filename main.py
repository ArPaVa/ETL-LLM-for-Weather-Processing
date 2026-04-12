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



session = db_creation()
save_combined_forecasts(session, combined_data)
