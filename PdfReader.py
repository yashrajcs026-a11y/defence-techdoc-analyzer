import os
import time
from dotenv import load_dotenv
from google import genai
from pypdf import PdfReader

load_dotenv("api_key.env")
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 1. Extract text from the PDF
reader = PdfReader("sample.pdf")
text = ""
for page in reader.pages:
    text += (page.extract_text() or "") + "\n"

print("Characters extracted:", len(text))

# 2. Ask the AI about it
prompt = (
    "You are a defence and technology analyst. "
    "Summarize this document in 5 bullet points and list the key technologies mentioned.\n\n"
    + text[:30000]   # limit the text so it isn't too long
)

response = None
for attempt in range(5):
    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )
        break
    except Exception as e:
        print(f"Attempt {attempt + 1} failed: {e}")
        time.sleep(5)

print(response.text if response else "Failed after 5 tries.")