from dotenv import load_dotenv
from openai import OpenAI
import pandas as pd
import os

load_dotenv()
client = OpenAI(api_key = os.getenv("API_KEY"))

def chat_with_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

print(chat_with_gpt('are yoiu working'))