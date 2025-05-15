import streamlit as st
import re
from uuid import uuid4
from openfoi.redaction import apply_redactions
from openfoi.config import FOI_EXEMPTIONS

if "response_text" not in st.session_state or not st.session_state.response_text:
    st.error("No text loaded – go back to Process page.")
    st.stop()

if "redactions" not in st.session_state:
    st.session_state.redactions = []

st.title("Review & Redact")

resp = st.text_area("Response Text", st.session_state.response_text, height=300)
if resp != st.session_state.response_text:
    st.session_state.response_text = resp

st.markdown("#### Find & Redact (by phrase or regex)")

with st.form("bulk_redact"):
    col1, col2 = st.columns([3,2])
    with col1:
        search = st.text_input("Phrase or Regex", value="")
    with col2:
        ex = st.selectbox("Exemption", FOI_EXEMPTIONS.keys(), format_func=lambda k: f"{k} - {FOI_EXEMPTIONS[k]}")
    submit_bulk = st.form_submit_button("Redact All Matches")
    
if submit_bulk and search:
    # Find all matches and add redactions
    matches = [m for m in re.finditer(search, resp)]
    if matches:
        for m in matches:
            st.session_state.redactions.append({
                "id": str(uuid4()),
                "start": m.start(),
                "end": m.end(),
                "exemption": ex
            })
        st.success(f"Redacted {len(matches)} matches for '{search}'.")
    else:
        st.warning("No matches found.")

# (Optional) Show all current redactions as table with option to remove
if st.session_state.redactions:
    st.write("#### Current Redactions")
    # Table with a remove button for each
    for i, r in enumerate(st.session_state.redactions):
        r_str = f"({r['start']}-{r['end']}) [{r['exemption']}] …{resp[r['start']:r['end']][:40]}…"
        c1, c2 = st.columns([8,1])
        c1.markdown(r_str)
        if c2.button("❌", key=f"delred_{i}"):
            st.session_state.redactions.pop(i)
            st.experimental_rerun()

st.markdown("---")

# Preview redacted version
redacted_markdown = apply_redactions(resp, st.session_state.redactions)
st.markdown("#### Redacted Markdown Preview")
st.markdown(redacted_markdown, unsafe_allow_html=True)
st.text_area("Redacted Text (for PDF etc)", redacted_markdown, height=150)

if st.button("Generate Response →"):
    st.session_state.redacted_text = redacted_markdown  # Save for next step
    st.switch_page("pages/4_Generate_Response.py")
