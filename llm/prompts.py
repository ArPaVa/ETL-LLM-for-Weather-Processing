activities_suitability_prompt = """
    You are an activity‑recommendation assistant. Given this weather snapshot:

    - Time: {time}
    - Temperature: {temperature}°C
    - Feels like: {feels_like}°C
    - Humidity: {humidity}%
    - Pressure: {pressure} mb
    - Weather: {weather}
    - Cloudiness: {cloudiness}%
    - Visibility: {visibility} km
    - Wind speed: {wind_speed} km/h
    - Wind gust: {wind_gust} km/h
    - Moon phase: {moon_phase}
    - Moon illumination: {moon_illumination}%
    - Precipitation: {precip_mm} mm
    - Snow: {snow_cm} cm
    - Chance of rain: {chance_of_rain}%
    - Chance of snow: {chance_of_snow}%
    - UV index: {uv}
    - Short-wave radiation: {short_rad}
    - Diffuse radiation: {diff_rad}

    Respond with a JSON object indicating if each activity is:
    - "YES" (good idea),
    - "MAYBE" (OK with caution), or
    - "NO" (bad idea).
    And provide an explanation based on the weather conditions.

    Activities:
    - running
    - cycling 
    - hiking 
    - golfing
    - skydiving 
    - swimming 
    - surfing 
    - birdwatching 
    - picnics 
    - photography 
    - sunbathing 
    - climbing 
    - stargazing

    Format your reply as valid JSON only. Expected structure: 
    ```json
    {{
        "activity1": {{"assessment": "YES/MAYBE/NO", "explanation": "..."}},
        ...
    }}
    ```
    """

def build_activity_prompt_from_row(row):
    return activities_suitability_prompt.format(
        date=row.date,
        time=row.time,
        temperature=row.temperature,
        feels_like=row.feels_like,
        humidity=row.humidity,
        pressure=row.pressure,
        weather=row.weather,
        cloudiness=row.cloudiness,
        visibility=row.visibility,
        wind_speed=row.wind_speed,
        wind_gust=row.wind_gust,
        moon_phase=row.moon_phase,
        moon_illumination=row.moon_illumination,
        precip_mm=row.precip_mm,
        snow_cm=row.snow_cm,
        chance_of_rain=row.chance_of_rain,
        chance_of_snow=row.chance_of_snow,
        uv=row.uv,
        short_rad=row.short_rad,
        diff_rad=row.diff_rad,
    )