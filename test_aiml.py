from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://api.aimlapi.com/v1",
    api_key=os.getenv("AIMLAPI_API_KEY")
)

response = client.chat.completions.create(
    model="anthropic/claude-opus-4-8",
    messages=[
        {
            "role": "user",
            "content": "Say hello"
        }
    ]
)

print(response.choices[0].message.content)