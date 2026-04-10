# ETL-LLM-for-Weather-Processing
## Installation
### 2. Crear el entorno virtual

```bash
python -m venv .venv
```

### 3. Activar el entorno virtual

**En PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**En CMD:**

```bat
.\.venv\Scripts\activate.bat
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Desactivar el entorno virtual

```bash
deactivate
```

We are using 3 meteorogical APIs Openweathermap, wheatherapi and open-meteo from this 3 open-meteo is the only one that doesnt need an API key for the free plan.

OWM (Openweathermap)
| Key     | Meaning                                                                                                                                                              |
| ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| cod     | HTTP‑style code from OpenWeatherMap. 200 means “success”. openweathermap                                                                                             |
| message | Additional numeric message code (often 0 if all is OK). openweathermap                                                                                               |
| cnt     | Number of forecast entries in list (e.g., cnt: 40 → 40 time‑slots, one every 3 hours over 5 days). openweathermap                                                    |
| city    | Metadata about the city/location you queried (name, country, lat/lon, timezone, sunrise/sunset, etc.). openweathermap                                                |
| list    | List of forecast time‑slots (each is a dictionary with dt, main, weather, wind, clouds, pop, etc.). Each one is a prediction for a specific datetime. openweathermap |
What’s inside city
Typical keys under data["city"]:

"name" – city name (you’re seeing Kara‑Kulja, not NYC; that’s an indexing issue you can fix later).

"country" – country code (e.g., KG).

"coord": {"lat", "lon"} – latitude and longitude used.

"timezone" – seconds offset from UTC.

"sunrise" / "sunset" – Unix timestamps for sunrise/sunset at that location.

This block is not weather; it’s just where you are.

What’s inside list
data["list"] is a Python list of forecast points like:

python
[
  {
    "dt": 1775768400,            # Unix timestamp (UTC)
    "dt_txt": "2026-04-09 21:00:00",
    "main": { ... },              # temperature, humidity, pressure, etc.
    "weather": [ ... ],           # list of weather conditions (e.g., "overcast clouds")
    "wind": { ... },              # speed, direction, gusts
    "clouds": { ... },            # cloudiness %
    "visibility": 10000,          # m
    "pop": 0,                     # probability of precipitation (0–1)
    "snow": { ... },              # snow mm in 3h (if any)
    "sys": { ... },               # internal metadata, like day/night
  },
  ...
]
So a single forecast entry is:

main → temp, feels_like, humidity, pressure, temp_min, temp_max.

weather → list of condition objects (main, description, icon, id) describing the sky (e.g., "overcast clouds").

wind → speed, deg (direction in degrees), gust.

dt / dt_txt → the time this forecast is for.

So the whole response looks like this
python
{
  "cod": 200,           # success
  "message": 0,         # extra API message code
  "cnt": 40,            # 40 forecast time‑slots
  "city": { ... },      # info about the city
  "list": [              # list of 40 time‑point forecasts
    { ... },
    { ... },
    ...
  ]
}

WA(Weatherapi)