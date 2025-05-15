"""Utility to apply inline redactions."""
from typing import List, Dict


def apply_redactions(text, redactions):
    """Replace redacted regions in text with markdown redaction marker."""
    # Sort redactions by start index (descending, to avoid messing up indices)
    redactions = sorted(redactions, key=lambda r: r['start'], reverse=True)
    for r in redactions:
        code = r["exemption"]
        marker = f"**[REDACTED {code}]**"
        text = text[:r['start']] + marker + text[r['end']:]
    return text


# ===== file: main.py =====
"""Entry point. Sets global page config and declares custom CSS."""
import streamlit as st

st.set_page_config(
    page_title="OpenFOI",
    page_icon="📑",
    layout="wide",
)

# custom CSS once for all pages
st.markdown(
    """
    <style>
    .download-btn{display:inline-block;padding:10px 20px;background:#4CAF50;color:#fff;
    text-decoration:none;border-radius:4px;margin-top:10px;font-weight:bold;}
    .download-btn:hover{background:#45a049;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.write("## Welcome to OpenFOI")
st.write("Use the sidebar to navigate through the FOI workflow.")