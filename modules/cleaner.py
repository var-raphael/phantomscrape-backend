import os
from groq import Groq 
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def clean_data(text: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a data cleaning assistant. Given raw scraped web text, you must: remove noise and junk, normalize fields, extract key data like titles, prices, dates, and names, and provide a brief summary. Return clean structured text only."
            },
            {
                "role": "user",
                "content": text
            }
        ]
    )
    return response.choices[0].message.content
  