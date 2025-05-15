"""
Page 2 – Process Request & auto-draft FOI response with OpenAI
"""
from __future__ import annotations
import os
from datetime import datetime
import streamlit as st
import pandas as pd
from textwrap import dedent
from openai import OpenAI

from openfoi import data, documents, config

# ── session bootstrap ─────────────────────────────────────────────────────────
if "requests" not in st.session_state:
    st.session_state.requests = data.load_requests()
if "documents" not in st.session_state:
    st.session_state.documents: dict[str, list] = {}
if "current_request_id" not in st.session_state:
    st.session_state.current_request_id = None
if "response_text" not in st.session_state:
    st.session_state.response_text = ""
# ──────────────────────────────────────────────────────────────────────────────

st.title("Process FOI Request")

# -----------------------------------------------------------------------------#
# Helper –  call the LLM and draft the response letter (as markdown)
# -----------------------------------------------------------------------------#
def draft_foi_letter(request: dict, docs_text: str) -> str:
    """
    Returns a markdown FOI response letter following the ICO template.
    Requires `OPENAI_API_KEY` env-var.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.warning("OPENAI_API_KEY not set – showing raw document text instead.")
        return docs_text or "[no extracted text]"

    client = OpenAI(api_key=api_key)

    # List exemptions for the prompt
    exemptions_list = "\n".join(f"- **{k}**: {v}" for k, v in config.FOI_EXEMPTIONS.items())

    template = dedent(
        """
        # Freedom of Information Response

        **Date:** [Date]  
        **Reference number:** [Reference number]

        ## Request

        **You asked us:**

        [Request wording]

        *We received your request on [date of receipt].*

        ## Our response

        (Populate this section – see ICO guidance)

        ## Advice and assistance

        (Populate)

        ## Next steps

        (Populate – internal review + ICO)
        """
    ).strip()

    today = datetime.now().strftime("%d %B %Y")
    user_prompt = dedent(
        f"""
        Using the following template, draft the full FOI response as markdown.
        Replace bracketed placeholders with actual values.

        TEMPLATE:
        \"\"\"{template}\"\"\"

        ### Values to inject
        Date: {today}
        Reference number: {request['reference']}
        Request wording: {request['request_text']}
        Date of receipt: {request['received_date'][:10]}

        ### Extracted documents (for context)
        \"\"\"{docs_text[:8000]}\"\"\"

        ### Exemptions you may cite (with explanations)
        {exemptions_list}

        ### Instructions
        - Produce valid GitHub-flavored markdown.
        - If any exemptions appear necessary, suggest them in plain English,
          **citing the section number** (eg 'S40 – personal data').
        - Use formal, concise tone.
        - Do NOT make up information not in the extracted documents.
        - Always include the 'Advice and assistance' and 'Next steps' sections.
        - Return ONLY the draft letter as markdown, nothing else.
        """
    ).strip()

    try:
        st.info("Generating draft letter (markdown) via OpenAI...")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": user_prompt}],
            temperature=0.3,
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"OpenAI call failed: {e}")
        return docs_text or "[no extracted text]"

# -----------------------------------------------------------------------------#
# UI logic
# -----------------------------------------------------------------------------#
action_req = st.session_state.current_request_id

if not action_req:
    # ── list view ─────────────────────────────────────────────────────────────
    df = pd.DataFrame(
        [
            {
                "Reference": r["reference"],
                "Requester": r["name"],
                "Status": r["status"],
                "ID": r["id"],
            }
            for r in st.session_state.requests.values()
        ]
    )
    if df.empty:
        st.info("No requests yet.")
        st.stop()

    chosen = st.selectbox("Choose request", df["Reference"].tolist())
    action_req = df.loc[df.Reference == chosen, "ID"].item()

    if st.button("Load Request"):
        st.session_state.current_request_id = action_req
        st.rerun()
else:
    # ── detail view ───────────────────────────────────────────────────────────
    req = st.session_state.requests[action_req]
    st.subheader(f"Request {req['reference']}")
    st.info(req["request_text"])

    # upload supporting doc
    upl = st.file_uploader("Upload supporting document")
    if upl:
        d = documents.save_document(upl, action_req, st.session_state.documents)
        if d:
            st.success(f"Uploaded {d['name']}")

    docs = st.session_state.documents.get(action_req, [])
    if docs:
        st.write("### Uploaded docs")
        st.table({d["name"]: d["content_type"] for d in docs})

        # ---- draft button ---------------------------------------------------
        if st.button("Generate AI Draft → Review & Redact"):
            combined_text = "\n\n".join(d["content"] for d in docs if d["content"])
            draft_letter = draft_foi_letter(req, combined_text)

            # store draft for the next page
            st.session_state.response_text = draft_letter or combined_text
            st.switch_page("pages/3_Review_and_Redact.py")
        elif st.session_state.response_text:
            st.markdown("#### Last draft:")
            st.markdown(st.session_state.response_text)
    else:
        st.info("Upload at least one supporting document to enable drafting.")

