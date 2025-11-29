import streamlit as st
import pandas as pd
import hashlib
import os
import time
import random
import re  # For simple text analysis

# --- Configuration and Initialization ---

# Define the user database file path
USERS_FILE = 'users.csv'

# Set page configuration with a custom title and layout
st.set_page_config(page_title="Secure Resume Scoring Agent", layout="wide")

# Custom CSS for the purple, black, and white theme (now with Red buttons)
st.markdown("""
    <style>
    /* Main Streamlit App styling */
    .stApp {
        background-color: #0d0d0d; /* Black/Dark Background */
        color: #ffffff; /* White text */
        font-family: 'Segoe UI', sans-serif;
    }

    /* Titles and Headers */
    h1, h2, h3, h4, .st-b5 { /* .st-b5 targets st.title */
        color: #9370DB; /* Medium Purple */
        font-weight: 700;
    }

    /* Sidebar styling */
    .css-1lcbmhc, .css-1lcbmhc.e1fqkh3o0 {
        background-color: #1a1a1a; /* Darker Black for Sidebar */
    }
    .css-1lcbmhc .css-1l2k1e3, .css-1lcbmhc .css-1l2k1e3 a { /* Sidebar links */
        color: #ffffff !important;
    }
    .css-1lcbmhc .css-1l2k1e3 a:hover {
        background-color: #333333 !important;
        color: #9370DB !important;
    }

    /* Button styling: Changed background to Red and hover to Purple */
    .stButton>button {
        background-color: #FF4B4B; /* Red background */
        color: #ffffff; /* White font color */
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
        transition: background-color 0.3s, transform 0.1s;
    }
    .stButton>button:hover {
        background-color: #9370DB; /* Purple on hover */
        transform: translateY(-2px);
    }

    /* File Uploader styling */
    div[data-testid="stFileUploader"] {
        background-color: #1a1a1a;
        padding: 20px;
        border-radius: 10px;
        border: 2px dashed #9370DB;
    }
    div[data-testid="stFileUploader"] label {
        color: #ffffff !important;
    }

    /* Metric/Data Display */
    [data-testid="stMetric"] {
        background-color: #333333;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #9370DB;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for authentication and navigation
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Login'
if 'username' not in st.session_state:
    st.session_state.username = None


# --- Utility Functions ---

def hash_password(password):
    """Hashes a password using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()


def load_users():
    """Loads user data from CSV, or creates an empty DataFrame if file doesn't exist."""
    if not os.path.exists(USERS_FILE):
        df = pd.DataFrame(columns=['username', 'password', 'email'])
        df.to_csv(USERS_FILE, index=False)
        return df
    return pd.read_csv(USERS_FILE)


def save_users(df):
    """Saves the user DataFrame back to CSV."""
    df.to_csv(USERS_FILE, index=False)


def check_login(username, password):
    """Checks credentials against the user database."""
    users_df = load_users()
    hashed_password = hash_password(password)
    user = users_df[(users_df['username'] == username) & (users_df['password'] == hashed_password)]
    return not user.empty


def register_user(username, password, email):
    """Registers a new user if the username is not already taken."""
    users_df = load_users()
    if username in users_df['username'].values:
        return False, "Username already exists."

    hashed_password = hash_password(password)
    new_user = pd.DataFrame([[username, hashed_password, email]], columns=['username', 'password', 'email'])
    users_df = pd.concat([users_df, new_user], ignore_index=True)
    save_users(users_df)
    return True, "Registration successful! Please log in."


def logout():
    """Resets session state for logout."""
    st.session_state.logged_in = False
    st.session_state.current_page = 'Login'
    st.session_state.username = None
    st.rerun()


# --- Placeholder Resume Parsing & Scoring Logic (Now Dynamic and Generous) ---

def extract_text_from_file(uploaded_file):
    """
    Placeholder to extract text from a file object.
    In a real app, you would use libraries like PyPDF2 or python-docx here.
    For this demo, we assume the file content is convertible to a string (e.g., if it were a .txt file).
    """
    try:
        # Attempt to read as text (suitable for most simple file uploads in Streamlit context)
        return uploaded_file.getvalue().decode('utf-8')
    except Exception:
        # Fallback for binary files (we'll just use a small chunk of the file for basic analysis)
        return str(uploaded_file.getvalue()[:2000])


def parse_resume(file_content):
    """
    Simple text-based parsing to extract key fields.
    """
    text = file_content.lower()

    # 1. Name: Simple placeholder
    name_match = re.search(r'name:\s*([a-z\s]+)', text)
    name = name_match.group(1).strip().title() if name_match else "Candidate Name"

    # 2. Email: Simple regex for email
    email_match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    email = email_match.group(0) if email_match else "contact@example.com"

    # 3. Keywords/Skills (Look for common section headers)

    # Example 1: Look for "skills" section
    skills_match = re.search(r'(skills|technical skills|key skills|expertise)[:\s\n]+(.+?)(?:\n\n|\Z)', text, re.DOTALL)

    # Example 2: Check for specific high-value keywords
    hight_value_keywords = ['python', 'javascript', 'sql', 'project management', 'machine learning', 'data analysis',
                            'cloud', 'aws', 'docker', 'agile']
    found_keywords = [kw for kw in hight_value_keywords if kw in text]

    return {
        "name": name,
        "email": email,
        "text_content": text,
        "keyword_count": len(found_keywords),
        "file_size_score_factor": len(text) // 500,  # Factor based on length (1 point per 500 characters)
        "skills_found": ", ".join(found_keywords) if found_keywords else "N/A",
        "has_skills_section": bool(skills_match)
    }


def score_resume(data):
    """
    Generates a dynamic score and feedback, aiming for scores near 80 for average input.
    """
    # Start with a generous base score (50 points out of 100)
    score = 50
    feedback_points = []
    text_content = data['text_content']

    # --- Scoring Rules (Additional 50 points max) ---

    # 1. Length/Completeness Score (Max 10 pts)
    # Give points easily based on length factor
    length_points = min(10, data['file_size_score_factor'] * 2)
    score += length_points
    if length_points < 4:
        feedback_points.append("Your resume appears quite brief. Aim for more detailed descriptions of your roles.")
    elif length_points >= 8:
        feedback_points.append("The resume is comprehensive and well-detailed in terms of length and content quantity.")

    # 2. Keyword Relevance Score (Max 20 pts)
    # Keywords are critical, award more points here
    keyword_points = data['keyword_count'] * 3
    score += min(20, keyword_points)
    if data['keyword_count'] == 0:
        feedback_points.append(
            "No high-value technical keywords were detected. Tailor your skills section to the job description.")
    elif data['keyword_count'] < 5:
        feedback_points.append(
            f"Only a few technical keywords ({data['keyword_count']}) were found. Increase technical terminology relevant to your target role.")
    else:
        feedback_points.append(f"Excellent! {data['keyword_count']} high-value technical keywords were identified.")

    # 3. Action Verb Check (Max 10 pts)
    action_verbs = ['managed', 'developed', 'created', 'led', 'implemented', 'analyzed', 'designed', 'optimized',
                    'achieved', 'streamlined']
    verb_count = sum(1 for verb in action_verbs if verb in text_content)
    verb_points = min(10, verb_count * 1)
    score += verb_points
    if verb_count < 5:
        feedback_points.append("Use stronger action verbs at the start of your bullet points to emphasize impact.")

    # 4. Contact/Section Check (Max 10 pts)
    contact_points = 0
    if data['email'] != "contact@example.com":
        contact_points += 4  # 4 points for email
    if data['has_skills_section']:
        contact_points += 3  # 3 points for a clear skills section
    phone_match = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text_content)
    if phone_match:
        contact_points += 3  # 3 points for phone number

    score += min(10, contact_points)
    if contact_points < 5:
        feedback_points.append(
            "Ensure your contact information and key sections (like Skills) are clearly visible and accurate.")

    # 5. Final Score Calculation (Cap at 100)
    final_score = min(100, int(score))

    # --- Generate Final Feedback ---
    feedback = "Overall Assessment:\n"
    if final_score < 70:
        feedback += "The resume is a work in progress. Focus on adding more substance, relevant keywords, and quantifiable achievements.\n"
    elif final_score < 85:
        feedback += "This is a solid, competitive resume. Focus on optimizing content by quantifying results and tailoring it to a specific job description.\n"
    else:
        feedback += "This resume is highly competitive! It demonstrates strong skills and experience. Minor tweaks to formatting and verb usage will make it outstanding.\n"

    feedback += "\nActionable Recommendations:\n" + "\n".join([f"- {p}" for p in feedback_points])

    return final_score, feedback


# --- Page Renderers ---

def render_login_page():
    """Renders the login form."""
    st.title("🔐 Login to Resume Scorer")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            if check_login(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.current_page = 'Home'
                st.success("Login Successful!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username or password.")

    st.markdown("---")
    if st.button("New User? Register Here", key="login_register_btn"):
        st.session_state.current_page = 'Register'
        st.rerun()


def render_register_page():
    """Renders the registration form."""
    st.title("📝 Register New Account")

    with st.form("register_form"):
        new_username = st.text_input("Choose Username")
        new_email = st.text_input("Email Address")
        new_password = st.text_input("Choose Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submitted = st.form_submit_button("Register")

        if submitted:
            if new_password != confirm_password:
                st.error("Passwords do not match.")
            elif not new_username or not new_password or not new_email:
                st.error("All fields are required.")
            else:
                success, message = register_user(new_username, new_password, new_email)
                if success:
                    st.success(message)
                    time.sleep(1)
                    st.session_state.current_page = 'Login'
                    st.rerun()
                else:
                    st.error(message)

    st.markdown("---")
    if st.button("Back to Login", key="register_back_to_login_btn"):
        st.session_state.current_page = 'Login'
        st.rerun()


def render_home_page():
    """Renders the Home page content."""
    st.title(f"Welcome, {st.session_state.username}!")
    st.markdown("""
        <div style="padding: 20px; border-radius: 10px; background-color: #1a1a1a;">
            <h2>AI Resume Scoring Dashboard</h2>
            <p>
                This platform uses advanced AI to analyze, score, and provide actionable feedback on your resume. 
                Navigate to the <b>Resume Scorer</b> page to begin your assessment.
            </p>
            <h3>Key Features:</h3>
            <ul>
                <li>Automated parsing of PDF/DOCX resumes (via placeholder text extraction).</li>
                <li>Objective scoring based on completeness, keyword relevance, and structure.</li>
                <li>Detailed, personalized feedback.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.info("💡 Use the sidebar to navigate between features.")


def render_resume_scorer_page():
    """Renders the core resume scoring functionality."""
    st.title("📄 Resume Scoring & Feedback")

    # File uploader
    uploaded_file = st.file_uploader("Upload a Resume (.pdf or .docx)", type=["pdf", "docx"])

    if uploaded_file:
        st.info("Processing Resume...")

        # 1. Extract raw text from the file object
        file_content = extract_text_from_file(uploaded_file)

        if not file_content or len(file_content) < 50:
            st.error("❌ Could not extract enough readable text. Please try another file or ensure it's text-based.")
            return

        # 2. Parse the text content
        parsed_data = parse_resume(file_content)
        st.success("✅ Resume Parsed (Basic Text Extraction Complete)!")

        # 3. Display Extracted Data
        st.subheader("🧠 Extracted Resume Info:")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Candidate Name", parsed_data.get("name", "N/A"))
        with col2:
            st.metric("Contact Email", parsed_data.get("email", "N/A"))
        st.text_area("Keywords Found", parsed_data.get("skills_found", "N/A"), height=100)

        # 4. Score the resume dynamically
        st.subheader("📊 Resume Score:")
        score, feedback = score_resume(parsed_data)

        st.markdown(f"""
        <div style="text-align: center; background-color: #333333; padding: 30px; border-radius: 15px;">
            <h1 style="color: #9370DB; font-size: 80px; margin: 0;">{score} / 100</h1>
        </div>
        """, unsafe_allow_html=True)

        st.text_area("📋 Personalized Feedback", feedback, height=300)

        # --- Email functionality (Mocked) ---
        # FIX: Added unique keys to buttons to resolve StreamlitDuplicateElementId error

        # Button 1: Tries to send email if a valid one was parsed
        if st.button("✉️ Send Feedback Email (Mock)", key="send_email_valid"):
            if parsed_data.get("email") != "contact@example.com":
                # NOTE: Actual email sending code remains commented out
                st.success(f"Mock Email sent to {parsed_data['email']}. (Actual function call is commented out)")
            else:
                st.warning("No valid email address found in the parsed resume data. Cannot send mock email.")


def render_contact_page():
    """Renders the Contact page content."""
    st.title("📞 Contact & Support")
    st.markdown(f"""
        <div style="padding: 20px; border-radius: 10px; background-color: #1a1a1a;">
            <h2>Get in Touch</h2>
            <p>
                We are here to help you get the best use out of the AI Resume Scoring Agent.
            </p>
            <h3 style="color: #9370DB;">Support Details</h3>
            <ul>
                <li><strong>Email:</strong> support@resumescorer.com</li>
                <li><strong>Phone:</strong> +1 (555) 123-4567</li>
                <li><strong>Hours:</strong> Mon - Fri, 9am - 5pm EST</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)


# --- Main Application Flow ---

if not st.session_state.logged_in:
    # Show Login or Register page
    if st.session_state.current_page == 'Register':
        render_register_page()
    else:
        render_login_page()
else:
    # --- Authenticated User Interface ---

    # 1. Sidebar Navigation
    st.sidebar.markdown(f"""
        <div style="text-align: center; padding: 10px; background-color: #9370DB; border-radius: 5px;">
            <h3 style="color: white; margin: 0;">Welcome, {st.session_state.username}!</h3>
        </div>
    """, unsafe_allow_html=True)

    st.sidebar.header("Navigation")

    # Use radio buttons for navigation
    page = st.sidebar.radio("Go to",
                            ['Home', 'Resume Scorer', 'Contact'],
                            index=['Home', 'Resume Scorer', 'Contact'].index(
                                st.session_state.current_page) if st.session_state.current_page in ['Home',
                                                                                                    'Resume Scorer',
                                                                                                    'Contact'] else 0
                            )

    st.session_state.current_page = page

    st.sidebar.markdown("---")

    # Logout button in the sidebar
    if st.sidebar.button("🔓 Logout", key="sidebar_logout_btn"):
        logout()

    # 2. Main Content Rendering
    if st.session_state.current_page == 'Home':
        render_home_page()
    elif st.session_state.current_page == 'Resume Scorer':
        render_resume_scorer_page()
    elif st.session_state.current_page == 'Contact':
        render_contact_page()

# Ensure the users.csv file exists for the app to start cleanly
if not os.path.exists(USERS_FILE):
    load_users()

# --- End of Main Application Flow ---