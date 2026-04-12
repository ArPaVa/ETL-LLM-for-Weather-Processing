import os
from google import genai
from config import GEMINI_API_KEY


activities_suitability_prompt = """
    You are an activity‑recommendation assistant. Given this weather snapshot:

    - Temperature: 25°C
    - Precipitation probability: 10%
    - Wind speed: 8 km/h
    - Humidity: 60%
    - UV index: 6
    - Visibility: 10 km
    - Is it day: yes

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
        "activity1": {{"assesment": "YES/MAYBE/NO", "Explanation": "..."}},
        ...
    }}
    ```
    """


def gemma3call(prompt):
    model = "gemma-3-27b-it"  # or "models/gemma-3-27b-it" depending on provider proxy
    client = genai.Client(api_key=GEMINI_API_KEY)
    #Call the model
    response = client.models.generate_content(model=model,
        contents=prompt,
        #config={"temperature": 0.7,"top_p": 0.95,"top_k": 40,"max_output_tokens": 2048,"response_mime_type": "application/json"}
        )

    print(response.text)