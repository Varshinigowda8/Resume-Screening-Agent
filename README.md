# 🤖 AI Resume Screening Agent

An open-source AI-powered Resume Screening Agent that reads resumes (PDF/DOCX), scores them based on job relevance, and sends personalized feedback via email — all with a single click.

## 🌐 Live Demo

👉 https://resume-analyservarshini.streamlit.app/

---

## 📌 Overview

The Resume Screening Agent automates the process of evaluating resumes against job descriptions. It extracts text from resumes, analyzes skills, experience, and formatting, and generates a relevance score. Personalized feedback is then sent to candidates via email.  

This project is designed for:
- Recruiters who want faster shortlisting
- Career coaches providing resume feedback
- Job seekers optimizing their resumes for applications

---

## 🚀 Features

- 📂 Upload resumes in PDF or DOCX format
- 📊 AI-powered scoring based on skills, experience, and formatting
- 🧠 NLP-based keyword extraction and JD matching
- 📧 Automated personalized feedback via email
- 🗃️ Logs each screening for future reference
- 🖥️ Streamlit-based Web UI for easy use


---

## ⚠️ Limitations

- ❌ No support for image-based resumes (scanned PDFs)
- 📄 Limited to English-language resumes
- 📬 Email delivery may fail if SMTP credentials are misconfigured
- 📊 Scoring is heuristic-based (not trained on recruiter datasets)
- 📁 Maximum file size: 200MB

---

## 🧰 Tech Stack & APIs Used

- **Frontend**: Streamlit  
- **Backend**: Python  
- **NLP**: spaCy, NLTK  
- **File Handling**: PyPDF2, python-docx, pdfplumber  
- **Email**: smtplib, email-validator  
- **ML Scoring**: Custom heuristic model (can be replaced with trained ML model)  
- **Other Libraries**: pandas, numpy, tqdm, validators  

---
🌱 Potential Improvements
🤖 Replace heuristic scoring with a trained ML model using recruiter-labeled datasets
🌍 Add multilingual resume support
📈 Integrate analytics dashboard for resume trends
🔒 Add OAuth or token-based user authentication
📤 Enable bulk resume upload and batch feedback
🧪 Add unit tests and CI/CD pipeline for deployment


🏗️ Architecture Diagram (End-to-End Workflow)
Flow:
User → Streamlit Web UI
Candidate uploads resume (PDF or DOCX) via a simple drag-and-drop interface.
Streamlit handles the front-end interaction.
File Handling Layer
Libraries: PyPDF2, python-docx, pdfplumber
Extracts raw text from uploaded resumes.
Cleans and normalizes text for NLP processing.
NLP Processing Layer
Libraries: spaCy, NLTK
Performs keyword extraction, tokenization, and skill matching.
Identifies relevant sections (skills, projects, education, achievements).
Resume Scoring Engine
Heuristic/ML-based scoring model (scikit-learn or custom logic).
Evaluates resumes based on:
Skill-job relevance
Experience depth
Formatting quality
Keyword density
Feedback Generation
Uses a template (feedback_template.txt) to generate personalized feedback.
Inserts score and breakdown into the feedback message.
Email Delivery
Libraries: smtplib, email-validator
Sends feedback directly to the candidate’s email.
Ensures proper validation and secure delivery.
Logging & Storage
Each screening is logged (resume metadata, score, feedback).
Enables recruiters to track history and analytics.
Output → Candidate
Candidate receives a feedback email with score and improvement suggestions.
Recruiter can view logs for reference.

📊 Diagram Explanation (Narration)
Step 1: The user uploads a resume through the Streamlit Web UI.

Step 2: The resume file is passed to the File Handling Layer, which extracts text using PyPDF2, python-docx, and pdfplumber.

Step 3: The extracted text flows into the NLP Processing Layer, where spaCy and NLTK perform keyword extraction and skill matching.

Step 4: The Resume Scoring Engine evaluates the resume using heuristic or ML-based scoring logic.

Step 5: A Feedback Generator prepares a personalized message using a template, embedding the score and breakdown.

Step 6: The feedback is sent via SMTP Email Delivery, ensuring proper validation.

Step 7: All results are stored in Logs for recruiter reference.

Step 8: Finally, the candidate receives a feedback email with actionable insights.

## 🛠️ Setup & Run Instructions

```bash
# Clone the repo
git clone https://gitlab.com/your-username/resume-screening-agent.git
cd resume-screening-agent

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py

