from dotenv import load_dotenv
import os

from google import genai
from google.genai import types

# Load environment variables from .env file
load_dotenv()

api_key=os.getenv("GEMINI_API_KEY")

client=genai.Client(api_key=api_key)

# NOTE TRY TO GIVE AS MUCH POSSIBLE GOOD EXPAMPLE AS THIS WILL IMPROVE YOUR MODELS RESPONSE

# lets give a system promp
system_prompt="""
 You are an AI Assistant who is specialized in maths.
 You should not answer any query thta is not related to maths.

 For a given query help user to solve that along with explanation

 Example:
 Input : 2+2
 Output: 4 which is calculated by adding 2 with 2

 Input : 3*10
 Output: 30 which is calculated by multipling 3 with 10

 Input : why sky is blue?
 Output: bruh ? you alright? is it a math query ?



"""
contents = [
    types.Content(
        role="user",
        parts=[
            types.Part(text=system_prompt),
            types.Part(text="5*18")
        ]
    )
]

# generate response
response=client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=contents
    
)

print(response.text)
