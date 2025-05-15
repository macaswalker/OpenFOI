import streamlit as st
from openfoi import data

if "requests" not in st.session_state:
    st.session_state.requests = data.load_requests()
if "current_request_id" not in st.session_state:
    st.session_state.current_request_id = None

st.title("Submit FOI Request")

with st.form("submit_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    org = st.text_input("Organisation (optional)")
    req_text = st.text_area("Describe the information you want", height=150)
    pref = st.selectbox("Preferred format", ["Digital (email)", "Hard copy (mail)", "Other"])
    sent = st.form_submit_button("Submit")

if sent:
    if not (name and email and req_text):
        st.error("All required fields must be filled.")
    else:
        req = data.new_request(name, email, req_text, org, pref)
        st.session_state.requests[req["id"]] = req
        st.session_state.current_request_id = req["id"]
        data.save_requests(st.session_state.requests)
        st.success(f"Submitted! Reference: {req['reference']}")
        st.sidebar.success("Navigate to 'Process Request'")