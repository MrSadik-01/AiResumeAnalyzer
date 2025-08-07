
'''
This script sets up a Flask web application that uses Google's Gemini Generative AI
to analyze resumes against job descriptions.

It does the following:
- Loads environment variables (like API keys) from a .env file
- Accepts resume PDF files and a job description as input
- Extracts text from the uploaded resume using PyMuPDF
- Sends both the resume text and job description to Gemini AI
- Parses Gemini's JSON response (score, explanation, skills match)
- Returns the analysis result as a JSON response for use in the frontend
'''


import os
import io
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

import fitz  # PyMuPDF
from dotenv import load_dotenv

from google import genai
# from google.genai import types optional for single model
# ========== Importing Required Libraries ==========

'''
os        : To access environment variables (like API keys) and manage file paths
io        : For in-memory file handling, useful for uploaded PDFs
json      : To encode/decode JSON data used in Gemini API and API responses

Flask     : Lightweight web framework to create REST APIs
request   : To handle HTTP POST/GET requests
jsonify   : To return responses as JSON
send_from_directory : To serve static files (e.g., HTML frontend)

CORS      : Allows frontend JavaScript apps to communicate with the backend (cross-origin)

fitz (PyMuPDF) : To extract text from uploaded PDF resumes

load_dotenv : Loads sensitive info like API keys from a .env file

google.genai : Google Generative AI SDK for calling Gemini models
types         : Data types and structure definitions used by the genai module
'''


# Load Google API key from .env
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Initialize Gemini Client
client = genai.Client(api_key=api_key)

# Setup Flask app
app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for frontend connection

# ========== Utilities ==========

# Convert uploaded PDF file to text
def pdf_to_text(file_stream) -> str:
    file_stream.seek(0)
    with fitz.open(stream=file_stream.read(), filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
        return text
'''
Function: pdf_to_text(file_stream) -> str

Purpose:
- This function extracts plain text content from a PDF file stream.

Parameters:
- file_stream: A file-like object (in-memory stream of the uploaded PDF)

Steps:
1. file_stream.seek(0):
   - Rewinds the file stream to the beginning (in case it's been read before).

2. fitz.open(...):
   - Uses PyMuPDF (imported as fitz) to open the PDF from the byte stream.

3. For each page in the document:
   - Extracts text using `page.get_text()` and appends it to the `text` variable.

4. Finally returns:
   - The full extracted text as a single string.
'''
    

def remove_code_fences(text):
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:].strip()  # remove ```json
    elif text.startswith("```"):
        text = text[3:].strip()  # remove ```
    if text.endswith("```"):
        text = text[:-3].strip()  # remove ending ```
    return text


# Call Gemini API to analyze resume vs job description
def call_gemini(resume_txt: str, jd_txt: str) -> dict:
    prompt = """
You are an expert HR professional and ATS (Applicant Tracking System) specialist.
Analyze the provided resume against the job description.

Respond ONLY with a valid JSON object, with NO extra text, markdown, or code fences.

JSON format:
{
  "score": <number between 0-100>,
  "explanation": "<summary>",
  "missing_skills": ["skill1", "skill2"],
  "present_skills": ["skill1", "skill2"]
}
"""
    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-pro",
            contents=[
                {"role": "user", "parts": [{"text": prompt}]},
                {"role": "user", "parts": [{"text": f"Resume:\n{resume_txt[:4000]}"}]},
                {"role": "user", "parts": [{"text": f"Job Description:\n{jd_txt[:2000]}"}]}
            ]
        )

        text = response.text.strip()
        print("Gemini raw response:", text)

        # Remove code fences if present
        clean_text = remove_code_fences(text)
        print("Gemini cleaned response:", clean_text)

        data = json.loads(clean_text)
        return {
            "score": data.get("score", 0),
            "explanation": data.get("explanation", ""),
            "missing_skills": data.get("missing_skills", []),
            "present_skills": data.get("present_skills", [])
        }

    except Exception as e:
        return {
            "score": 0,
            "explanation": f"AI analysis failed: {str(e)}",
            "missing_skills": [],
            "present_skills": []
        }
'''
Function: call_gemini(resume_txt: str, jd_txt: str) -> dict

Purpose:
- Sends a resume and job description to the Gemini 2.5 Pro model for AI-powered analysis.

How it works:
1. Builds a structured prompt:
   - Instructs the AI to behave like an HR/ATS expert.
   - Asks for JSON-only response without markdown or code fences.
   - Specifies expected output format: score, explanation, present/missing skills.

2. Sends prompt + resume text + JD text to Gemini using `client.models.generate_content()`.

3. Extracts and cleans the AI's response:
   - Uses `remove_code_fences()` to strip any ```json or ``` wrappers.
   - Parses the clean response string into a Python dictionary using `json.loads`.

4. Returns a dictionary with:
   - score (int),
   - explanation (str),
   - present_skills (list),
   - missing_skills (list).

Error Handling:
- If Gemini fails or JSON parsing fails, returns default error response with score 0 and a failure message.
'''


# ========== Flask Routes ==========

# Main endpoint: resume PDF + JD text
@app.route('/upload', methods=['POST'])
def upload_and_analyze():
    if 'resume' not in request.files or 'jd_text' not in request.form:
        return jsonify({'error': 'Missing resume file or job description text'}), 400

    resume_file = request.files['resume']
    jd_text = request.form['jd_text']

    resume_txt = pdf_to_text(resume_file.stream)
    result = call_gemini(resume_txt, jd_text)
    return jsonify(result)
'''
Route: /upload (POST)

Purpose:
- Handles the main backend logic for uploading a resume and analyzing it against a job description.

Workflow:
1. Validates incoming request:
   - Checks if both 'resume' file and 'jd_text' (job description) are provided in the form data.
   - If either is missing, returns a 400 Bad Request with an error message.

2. Extracts:
   - Resume file from `request.files['resume']`
   - Job description text from `request.form['jd_text']`

3. Converts the resume PDF into plain text using `pdf_to_text()`.

4. Calls `call_gemini()` to analyze the resume text against the job description.

5. Returns the AI-generated analysis as a JSON response:
   - Includes score, explanation, present skills, and missing skills.
'''


# Health route for frontend ping
@app.route('/health')
def health_check():
    return jsonify({'status': 'OK'})

# Optional static frontend
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

# Global error handler
@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({'error': str(e)}), 500
'''
Supporting Routes and Error Handler

1. /health  [GET]
   - Purpose: Used by frontend or monitoring tools to check if the backend server is running.
   - Returns: JSON {"status": "OK"}

2. /  [GET]
   - Purpose: Serves the frontend (index.html) from the 'static' directory.
   - Usage: When a user accesses the root URL, the main webpage loads.

3. Global Error Handler
   - Purpose: Catches any unhandled exceptions in the application.
   - Returns: JSON with the error message and a 500 status code.
   - Ensures all backend errors are returned in a consistent JSON format.
'''


#if __name__ == '__main__':
 #   app.run(debug=True, port=5000)
'''
uncommad  below for render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
'''
if __name__ == '__main__':
    # Check if running in development or production
    if os.getenv('FLASK_ENV') == 'production':
        app.run(host='0.0.0.0', port=int(os.getenv('PORT', 10000)))
    else:
'''
Main entry point of the Flask application.

- This block ensures the app only runs when this script is executed directly (not when imported).
- `debug=True` enables hot reloading and detailed error pages — useful during development.
- `port=5000` runs the server locally on http://127.0.0.1:5000

Note: Set `debug=False` when deploying to production.
'''

# ========== End of Flask App ==========

