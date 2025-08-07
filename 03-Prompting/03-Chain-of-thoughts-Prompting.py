from dotenv import load_dotenv
import os

#FOR GEMINI API
from google import genai
from google.genai import types

# load dotenv file
load_dotenv()

#API KEY FROM .ENV FILE
api_key=os.getenv("GEMINI_API_KEY")

# Creating client with api key
client=genai.Client(api_key=api_key)

system_prompt="""
   You are an AI assistant who is  expert in breaking down problems and then resolves user query
    
    For the given user input , analyse the input and break down the problem step by step .
    Atleast think 5-6 steps on how to solve the problem before solving it down

    The Steps are you get a user input, you analyse , you think and you agin think for several times and then return a output with explantion and then finally validate the output as well before giving final result
    
    Follow this steps in sequence that is "analyse","think","output","validate",finally "result"
     
    Rules.
    1.Follow the strict JSON output as per Output schema
    2. Perform all steps in sequence in one response, from analyse to result.
    3.Carefully analyse the user query

    Output Format:
    {{step:"string",content:"string"}}


    Examples:
    Input: what is 2+2
    Output:{{step:"anaslyse",content:"Alright! the user is interested in maths query and he is asking a basic arthematic operations"}}
    Output:{{step:"think",content:"To perform the addition i must go from left to right and add all the operands"}}
    Output:{{step:"output",content:"4"}}
    Output:{{step:"validate",content:"seems like 4 is correct ans for this 2+2"}}
    Output:{{step:"result",content:"2+2=4 and this is calculated by adding all the numbers"}}

"""

contents = [
    types.Content(
        role="user",
        parts=[
            types.Part(text=system_prompt),
            types.Part(text="why sky is blue?")
        ]
    )
]


## generate response
response=client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=contents
)

print(response.text)