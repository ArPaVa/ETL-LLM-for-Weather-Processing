from config import GEMINI_API_KEY
from google import genai

def listmodels():
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.list()
    print(response.page)

def geminicall(prompt):
    #model = "gemma-4-26b-it"
    #model = "gemma-4-26b-a4b-it"
    model = "gemini-2.5-flash-lite"
    client = genai.Client(api_key=GEMINI_API_KEY)
    #Call the model
    response = client.models.generate_content(model=model, contents=prompt)
    
    return response

