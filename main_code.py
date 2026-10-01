
import os
from dotenv import load_dotenv
from google import genai

load_dotenv("api_key.env")
key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=key)

import time

response = None
for attempt in range(5):   # try up to 5 times
    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents="Explain what a drone swarm is in 2 sentences."
        )
        break   # it worked, so stop retrying
    except Exception as e:
        print(f"Attempt {attempt + 1} failed: {e}")
        time.sleep(5)   # wait 5 seconds, then try again

if response:
    print(response.text)
else:
    print("Still failing after 5 tries. Try again in a few minutes.")