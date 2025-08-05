# 🤖 AI Resume Analyzer – Beat the ATS with Gemini AI

An AI-powered web application that analyzes your resume against a job description using Google's Gemini Pro (Generative AI) to improve your chances of passing Applicant Tracking Systems (ATS) and getting more interviews.

---

## 🚀 Features

✅ ATS compatibility check  
✅ Resume-to-job matching score  
✅ Missing and present skills detection  
✅ Keyword optimization  
✅ Actionable feedback to improve your resume  
✅ Fast, simple UI with file upload (PDF only)

---

## 🧱 Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python Flask
- **AI Engine**: Google Gemini 2.5 Pro (via [Google Generative AI SDK](https://github.com/google/generative-ai-python))
- **PDF Parsing**: PyMuPDF (`fitz`)
- **Environment Config**: `python-dotenv`
- **Cross-Origin Support**: `flask-cors`

---

## 📁 Project Structure

ai-resume-analyzer/
│
├── static/
│ └── index.html # Frontend HTML/CSS/JS
├── app.py # Flask backend
├── .env # Contains GOOGLE_API_KEY (not pushed to GitHub)
├── requirements.txt # Python dependencies
├── README.md # This file


---

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/ai-resume-analyzer.git
cd ai-resume-analyzer
```


``` Set up Python environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
Configure Google Gemini API: 
Create a .env file in the root directory:
GOOGLE_API_KEY=your_google_gemini_api_key
...You can get your key from Google AI Studio...

```Run the Flask server
python app.py
```

Access the Frontend
Once Flask is running:

```Open your browser and go to:
http://localhost:5000
```
You’ll see a UI where you can:
Upload a resume PDF
Paste a job description
Click "Analyze My Resume" and get instant feedback

```requirements.txt
You can create this file with the following content:

nginx
Copy
Edit
Flask
flask-cors
python-dotenv
google-generativeai
PyMuPDF
```

```Then run:
pip install -r requirements.txt
```
💡 How It Works
User uploads a resume PDF and pastes a job description

The resume is parsed to plain text using PyMuPDF

Both resume and job description are sent to Gemini 2.5 Pro

Gemini returns:

Match score

Explanation

Skills present

Skills missing

Results are displayed in the frontend



Max file size allowed: 16MB

File type allowed: PDF only

🧑‍💻 Author
```Built by 
Sadik Habibulla  (https://github.com/MrSadik-01) 
Naveen K K       (https://github.com/Naveenkk-0793)
```

---

### ✅ Next Steps (for GitHub)

1. Save this as `README.md` in your project root
2. Create a `.gitignore` file (if not already):

```txt
.env
__pycache__/
venv/
*.pyc
```


