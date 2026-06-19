from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("AIMLAPI_API_KEY"),
    base_url="https://api.aimlapi.com/v1"
)

try:
    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {"role": "user", "content": "hello"}
        ]
    )

    print("SUCCESS")
    print(response.choices[0].message.content)

except Exception as e:
    print("FAILED")
    print(str(e))