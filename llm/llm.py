import os
from google import genai
from config import GEMINI_API_KEY

def listmodels():
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.list()
    print(response.page)

def geminicall(prompt):
    #model = "gemma-4-26b-it"  # or "models/gemma-3-27b-it" depending on provider proxy 
    #model = "gemma-4-26b-a4b-it"
    model = "gemini-2.5-flash-lite"
    client = genai.Client(api_key=GEMINI_API_KEY)
    #Call the model
    response = client.models.generate_content(model=model,
        contents=prompt,
        #config={"temperature": 0.7,"top_p": 0.95,"top_k": 40,"max_output_tokens": 2048,"response_mime_type": "application/json"}
        )
    return response

