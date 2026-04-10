from api_ingestion.api_ingestion import get_forecast_OWM

from datetime import datetime
from typing import Dict, Any
import json

# Usage (same as before)
data = get_forecast_OWM(40.7128, 74.0060)  # New York City

print(data.keys())


# data = get_forecast_OWM(40.7128, 74.0060) #New York City
# print(data)