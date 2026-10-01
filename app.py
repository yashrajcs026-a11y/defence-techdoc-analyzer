import os
import time
import json
import streamlit as st
import base64
from dotenv import load_dotenv
from google import genai
from pypdf import PdfReader

load_dotenv("api_key.env")
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-3.8-flash"


def ask_ai(prompt):
    """Send a prompt to the AI, retrying if the server is busy."""
    for attempt in range(5):
        try:
            response = client.models.generate_content(model=MODEL, contents=prompt)
            return response.text
        except Exception as e:
            if "429" in str(e):
                return "Rate limit reached. Please wait a minute and try again."
            time.sleep(5)
    return "The AI server is busy. Please try again in a minute."


def read_pdf(file):
    """Extract all text from an uploaded PDF."""
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += (page.extract_text() or "") + "\n"
    return text


def get_categorized_summary(text):
    """Ask the AI to categorize key points into history, application, and future."""
    prompt = (
        "You are a defence and technology analyst. Read the document below and extract "
        "8 to 12 key points. For EACH point, classify it into exactly one category:\n"
        "- 'history': past events, prior research, background, existing systems\n"
        "- 'application': current use, current capability, how it's deployed today\n"
        "- 'future': predictions, proposed improvements, limitations, next steps\n\n"
        "Respond with ONLY a JSON array, no other text, no markdown formatting, in this exact format:\n"
        '[{"category": "history", "point": "..."}, {"category": "application", "point": "..."}]\n\n'
        "Document:\n" + text[:30000]
    )

    raw = ask_ai(prompt)
    cleaned = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return None

def get_fake_summary_for_testing(text):
    """Fake AI response, just to test the color display without using API calls."""
    return [
        {"category": "history", "point": "This technology was first developed in the 1990s for military use."},
        {"category": "application", "point": "It is currently deployed in border surveillance systems."},
        {"category": "future", "point": "Researchers propose integrating AI-based target recognition by 2030."},
        {"category": "History", "point": "Testing capital letter category to check the .lower() fix."},
        {"category": "unknown_category", "point": "Testing an unrecognized category as a fallback check."},
    ]


st.set_page_config(page_title="Defence & Tech Analyzer", page_icon="🛰️", layout="wide")

def set_background(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)),
                               url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

set_background("background.png")

with st.sidebar:
    st.header("ℹ️ About")
    st.write("This tool extracts and categorizes key information from defence and technology documents using AI.")
    st.write("Built for ASTRA Club — Software Team") 

st.markdown(
    """
    <div style="text-align:center; padding:20px 0;">
        <h1 style="margin-bottom:0; color:white; text-shadow: 2px 2px 6px black;">Defence & Tech Document Analyzer</h1>
        <p style="color:#dddddd; font-size:18px; text-shadow: 1px 1px 4px black;">Upload a PDF — get an instant categorized intelligence brief</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    uploaded = st.file_uploader("📄 Upload a PDF", type="pdf")

if uploaded:
    text = read_pdf(uploaded)
    c1, c2 = st.columns(2)
    c1.metric("Characters extracted", f"{len(text):,}")
    c2.metric("Estimated pages", f"{len(text)//2000 or 1}")

    if len(text) == 0:
        st.error("No text found. This PDF may be a scanned image.")
    else:
        if st.button("Summarize"):
            with st.spinner("Analyzing..."):
                points = get_categorized_summary(text)

                if points is None:
                    st.error("Couldn't parse the AI's response. Try again.")
                else:
                    icons = {"history": "🕓", "application": "⚙️", "future": "🚀"}
                    colors = {
                        "history": "#1f3a5f",
                        "application": "#1f4d2e",
                        "future": "#5f4419",
                    }
                    icons = {"history": "🕓", "application": "⚙️", "future": "🚀"}
                    colors = {
                        "history": "#1f3a5f",
                        "application": "#1f4d2e",
                        "future": "#5f4419",
                    }
                    section_titles = {
                        "history": "History",
                        "application": "Application",
                        "future": "Future",
                    }

                    # Group all points by their category first
                    grouped = {"history": [], "application": [], "future": []}
                    for item in points:
                        cat = item.get("category", "application").strip().lower()
                        if cat not in grouped:
                            cat = "application"  # fallback for unexpected categories
                        grouped[cat].append(item.get("point", ""))

                    # Now display one section at a time, in a fixed order
                    for cat in ["history", "application", "future"]:
                        if grouped[cat]:  # only show the section if it has points
                            st.markdown(
                                f'<h3 style="color:white;">{icons[cat]} {section_titles[cat]}</h3>',
                                unsafe_allow_html=True,
                            )
                            for point_text in grouped[cat]:
                                st.markdown(
                                    f'''
                                    <div style="background-color:{colors[cat]}; padding:14px 18px;
                                                border-radius:10px; margin-bottom:8px;
                                                border-left:5px solid white;">
                                        <p style="margin:0; font-size:16px; color:white;">{point_text}</p>
                                    </div>
                                    ''',
                                    unsafe_allow_html=True,
                                )

        question = st.text_input("Ask a question about this document")
        if st.button("Ask") and question:
            with st.spinner("Thinking..."):
                prompt = (
                    "Answer the question using ONLY the document below. "
                    "If the answer isn't in the document, say so.\n\n"
                    f"Document:\n{text[:30000]}\n\nQuestion: {question}"
                )
                st.write(ask_ai(prompt))