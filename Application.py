import streamlit as st
import tempfile
import os
import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv()

# Configure Google API for audio processing
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

def process_audio(audio_file_path, user_prompt):
    """Process the audio using the user's prompt with Google's Generative API."""
    model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
    audio_file = genai.upload_file(path=audio_file_path)
    response = model.generate_content(
        [
            user_prompt,
            audio_file
        ]
    )
    return response.text

def save_uploaded_file(uploaded_file):
    """Save uploaded file to a temporary file and return the path."""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.' + uploaded_file.name.split('.')[-1]) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            return tmp_file.name
    except Exception as e:
        st.error(f"Error handling uploaded file: {e}")
        return None

# Streamlit app interface
st.title('AI-Powered Audio Processing App')

# Profile Sidebar
st.sidebar.title('About Me')
st.sidebar.image('TOni ANotherpic.jpg', width=100)  # Replace URL
st.sidebar.markdown("""
**Name:** Toni Ramchandani  
**Bio:** Driven by Sports, Adventure, Technology & Innovations.  
[LinkedIn Profile](https://www.linkedin.com/in/toni-ramchandani/)
""")

# Inject custom CSS for styling
st.markdown("""
    <style>
    .stButton>button {
        width: 150px;
        height: 50px;
        border-radius: 5px;
        border: 2px solid #FF4B4B;
        background-color: #FF4B4B;
        color: white;
        font-size: 16px;
        font-weight: bold;
        margin: 10px;
        transition: background-color 0.3s, color 0.3s;
    }
    .stButton>button:hover {
        background-color: #FF0000;
        color: yellow;
    }
    .stTextInput>div>div>input {
        font-size: 16px;
        height: 40px;
        width: 100%;
        border-radius: 5px;
    }
    .stTextArea>div>div>textarea {
        font-size: 16px;
        height: 200px;
        width: 100%;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

user_prompt = st.text_input("Enter your custom AI prompt:", placeholder="E.g., 'Please summarize the audio:'")

audio_file = st.file_uploader("Upload Audio File", type=['wav', 'mp3'])
if audio_file is not None:
    audio_path = save_uploaded_file(audio_file)
    st.audio(audio_path)

    if st.button('Process Audio'):
        with st.spinner('Processing...'):
            processed_text = process_audio(audio_path, user_prompt)
            st.text_area("Processed Output", processed_text, height=300)
