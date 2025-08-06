import os
from openai import OpenAI
api_key=os.getenv("GEMINI_API_KEY")

client=OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

text="my dog name is Tom"

response=client.embeddings.create(
    model="text-embedding-ada-004",
    input=text
)

print("vector emabedding",response)

print("Length",len(response.data[0].embedding))