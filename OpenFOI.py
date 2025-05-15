"""Entry point. Sets global page config and declares custom CSS."""
import streamlit as st
from dotenv import load_dotenv

# --- Set global page config (title, icon, sidebar, etc)
st.set_page_config(
    page_title="openfoi",
    page_icon="🗂️",  # You can use any emoji or a custom image
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Load .env for API keys and secrets
load_dotenv()

# --- Custom CSS for download button (and can add more global styles here)
st.markdown(
    """
    <style>
    .download-btn{
        display:inline-block;
        padding:10px 20px;
        background:#4CAF50;
        color:#fff;
        text-decoration:none;
        border-radius:4px;
        margin-top:10px;
        font-weight:bold;
        transition: background 0.2s;
    }
    .download-btn:hover{
        background:#45a049;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Main page welcome/description
st.write("# Welcome to OpenFOI 🗂️")
st.write(
    """
    **OpenFOI** is your streamlined platform for managing Freedom of Information (FOI) requests.
    
    - Submit, track, and process FOI requests efficiently.
    - Generate draft responses with AI assistance.
    - Review, redact, and export professional responses as PDF or DOCX.
    
    👉 **Use the sidebar to navigate each step of the FOI workflow.**
    """
)
