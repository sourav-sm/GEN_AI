# from dotenv import load_dotenv
# import os
# import json
# import requests
# from google import genai
# from google.genai import types

# # load env
# load_dotenv()

# # store api key
# api_key=os.getenv("GEMINI_API_KEY")

# #create client
# client=genai.Client(api_key=api_key)

# ## now we are adding it hands so that it can go over internet and search what is current wheather of patiyala 

# def get_weather(city:str):
#     # todo add a actual api call
#     url=f"https://wttr.in/{city}?format=%C+%t"
#     response=requests.get(url)
#     # this is f formating like `${city} in js`

#     if response.status_code==200:
#         return f"The weather in {city} is {response.text}."
#     else:
#         return "Sorry I could not get the weather data for the city"
    
# available_tools={
#     "get_weather":get_weather
# }



# system_prompt="""
#   You are an helpfull AI Assistant who is speciallized in resolving user query 
#   You work on start, plan, action observe mode.
#   For the given user query and available tools , plan the step byt step execution, based on the planning , 
#   select the relevent tool from the available tool. and based on the tool selection you perform an action to call the tool.
#   wait for the observation and based on the observation from the tool call resolve the user query.

#   Rules.
#     1.Follow the strict JSON output as per Output schema
#     2. Perform all steps in sequence in one response, from analyse to result.
#     3.Carefully analyse the user query

#   Output JSON Format:
#   {{
#     "step":"String:,
#     "content":"string",
#     "funtion":"the name of function if the step is action",
#     "input":"the input parameter for the funtion"
#   }}

#   Available Tools:
#   - "get_weather":Takes a city name as input and returns the weather of that city.

#   Example:
#   User Query: What is the weather of new york?
#   Ouput: {{"step":"plan","content":"the user is interested in weather data of new york "}} 
#   Ouput: {{"step":"plan","content":"from the availabe tools i should call get_weather"}} 
#   Ouput: {{"step":"action","funtion":"get_weather","input":"new york"}}
#   Ouput: {{"step":"observe","output":"12 degree Celsius" }}
#   Ouput: {{"step":"output","content":"The weather of new york seems to be 12 degree Celsius"}}


# """

# ## now lets make is full agent

# messages = [
#     {"role": "system", "content": system_prompt},
# ]

# while True:
#     query = input("> ")
#     messages.append({"role": "user", "content": query})

#     while True:
#         response = client.chat.completions.create(
#             model="gemini-2.0-flash-001",
#             response_format={"type": "json_object"},
#             messages=messages
#         )

#         messages.append(
#             {"role": "assistant", "content": response.choices[0].message.content})
#         parsed_response = json.loads(response.choices[0].message.content)

#         if parsed_response.get("step") == "plan":
#             print(f"🧠: {parsed_response.get('content')}")
#             continue

#         if parsed_response.get("step") == "action":
#             tool_name = parsed_response.get("function")
#             tool_input = parsed_response.get("input")

#             print(f"🔨 Calling Tool: {tool_name} with input: {tool_input}")

#             if available_tools.get(tool_name) != False:
#                 output = available_tools[tool_name](tool_input)
#                 messages.append({"role": "user", "content": json.dumps(
#                     {"step": "observe", "output": output})})
#                 continue

#         if parsed_response.get("step") == "output":
#             print(f"🤖: {parsed_response.get('content')}")
#             break
     
from dotenv import load_dotenv
import os
import json
import requests
from openai import OpenAI
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


def get_weather(city: str) -> str:
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}."
    else:
        return "Sorry, I couldn't get the weather data for the city"


available_tools = {
    "get_weather": get_weather
}

SYSTEM_PROMPT = f"""
    You are a helpful AI Assistant who is specialized in resolving user query.
    You work on start, plan, action, observe mode.

    For the given user query and available tools, plan the step by step execution, based on the planning,
    select the relevant tool from the available tool. And based on the tool selected you perform an action to call the tool.

    Wait for the observation and based on the observation from the tool call resolve the user query.

    Rules:
    - Follow the Output JSON Format.
    - Always perform one step at a time and wait for the next input.
    - Carefully analyse the user query.

    Output JSON Format:
    {{
        "step": "string",
        "content": "string",
        "function": "The name of function if the step is action",
        "input": "The input parameter for the function",
        "output": "The output of the function"
    }}

    Available Tools:
    - "get_weather": Takes a city name as input and returns the weather of the city.

    Example:
    Input: What is the weather in Hyderabad?
    Output: {{ "step": "plan", "content": "The user is interested in weather data of Hyderabad. So I will use the get_weather tool to get the weather data of Hyderabad." }}
    Output: {{ "step": "plan", "content": "From the available tools, I should call get_weather" }}
    Output: {{ "step": "action", "function": "get_weather", "input": "Hyderabad" }}
    Output: {{ "step": "observe", "content": "24 degrees C" }}
    Output: {{ "step": "output", "content": "The weather for Hyderabad seems to be 24 degrees C" }}
"""

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
]

while True:
    query = input("> ")
    messages.append({"role": "user", "content": query})

    while True:
        response = client.chat.completions.create(
            model="gemini-2.0-flash",
            response_format={"type": "json_object"},
            messages=messages
        )

        messages.append(
            {"role": "assistant", "content": response.choices[0].message.content})
        parsed_response = json.loads(response.choices[0].message.content)

        if parsed_response.get("step") == "plan":
            print(f"🧠: {parsed_response.get('content')}")
            continue

        if parsed_response.get("step") == "action":
            tool_name = parsed_response.get("function")
            tool_input = parsed_response.get("input")

            print(f"🔨 Calling Tool: {tool_name} with input: {tool_input}")

            if available_tools.get(tool_name) != False:
                output = available_tools[tool_name](tool_input)
                messages.append({"role": "user", "content": json.dumps(
                    {"step": "observe", "output": output})})
                continue

        if parsed_response.get("step") == "output":
            print(f"🤖: {parsed_response.get('content')}")
            break
