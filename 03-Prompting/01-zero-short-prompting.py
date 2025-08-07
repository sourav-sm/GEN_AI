from dotenv import load_dotenv
import os

# for gemini api
from google import genai
from google.genai import types

# loading dotenv file
load_dotenv()

api_key=os.getenv("GEMINI_API_KEY")

#create client with api key 
client=genai.Client(api_key=api_key)

#generating response
response=client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents="why sky is blue"
)

#printing response
print("zero-short-prompting-response ",response)