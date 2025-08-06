# importing tiktokn for visualizaton of encodign and decoding
import tiktoken

# selecting model 
encoder=tiktoken.encoding_for_model("gpt-4o")

text="Hello I am Sourav, and this is my first GEN_AI code"

# encoding above text
tokens=encoder.encode(text)

# lets check the tokens
print("Tokens: ",tokens)
tokens=[13225, 357, 939, 148083, 407, 11, 326, 495, 382, 922, 1577, 78255, 198596, 3490]

#lets decode it 
decoded=encoder.decode(tokens)

print("Decoded Text: ",decoded)

