from __future__ import annotations
import shutil
from pathlib import Path
from uuid import uuid4
from typing import Dict, Any

import PyPDF2              # pip install PyPDF2
import docx                # pip install python-docx

from .config import DOCUMENTS_DIR
from datetime import datetime


def _extract_pdf(path: Path) -> str:
    try:
        reader = PyPDF2.PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception:
        return ""


def _extract_docx(path: Path) -> str:
    try:
        d = docx.Document(str(path))
        return "\n".join(p.text for p in d.paragraphs)
    except Exception:
        return ""


def save_document(uploaded_file, request_id: str, docs_state: Dict[str, list]) -> Dict[str, Any] | None:
    # Prevent duplicate saves on rerun by file name
    if request_id in docs_state and any(d["name"] == uploaded_file.name for d in docs_state[request_id]):
        return None

    req_dir = DOCUMENTS_DIR / request_id
    req_dir.mkdir(parents=True, exist_ok=True)

    dst = req_dir / uploaded_file.name
    with open(dst, "wb") as f:
        shutil.copyfileobj(uploaded_file, f)

    # basic text extraction
    content = ""
    if uploaded_file.type == "application/pdf":
        content = _extract_pdf(dst)
    elif uploaded_file.type in {"application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"}:
        content = _extract_docx(dst)
    elif uploaded_file.type.startswith("text") or dst.suffix.lower() in {".md", ".txt", ".csv"}:
        content = dst.read_text(encoding="utf-8", errors="ignore")

    info = {
        "id": str(uuid4()),
        "name": uploaded_file.name,
        "path": str(dst),
        "uploaded_at": datetime.now().isoformat(),
        "content_type": uploaded_file.type,
        "size": dst.stat().st_size,
        "content": content,
    }

    docs_state.setdefault(request_id, []).append(info)
    return info