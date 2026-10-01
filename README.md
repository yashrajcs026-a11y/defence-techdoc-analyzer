# Defence & Tech Document Analyzer

An AI-powered tool that reads defence/technology PDFs and generates a categorized
intelligence brief, sorting key points into History, Application, and Future.

## Demo Video
[Watch the demo][([PASTE_YOUR_VIDEO_LINK_HERE](https://youtu.be/ClesWrI6ZuQ))]

## How it works
1. User uploads a PDF
2. Text is extracted using pypdf
3. Gemini AI analyzes the text and categorizes key points
4. Results are displayed as color-coded cards, grouped by category
5. Users can also ask free-form questions about the document

## Tech stack
- Python
- Streamlit (web interface)
- Google Gemini API (AI analysis)
- pypdf (PDF text extraction)

## Setup
1. Clone this repo
2. Run `pip install -r requirements.txt`
3. Get a free Gemini API key from aistudio.google.com
4. Create a file named `api_key.env` in the project folder with:
   `GEMINI_API_KEY=your_key_here`
5. Run `streamlit run app.py`

6. ##a samll not
7. I apologise for the quality of the video.
