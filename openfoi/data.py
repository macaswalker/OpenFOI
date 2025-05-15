"""Load / save persistent request state."""
from __future__ import annotations
import json
from datetime import datetime, timedelta
from uuid import uuid4
from typing import Dict, Any

from .config import REQUESTS_JSON


def _now_iso() -> str:
    return datetime.now().isoformat()


def _due_date_from(dt: datetime) -> str:
    return (dt + timedelta(days=28)).isoformat()


def load_requests() -> Dict[str, Any]:
    if REQUESTS_JSON.exists():
        return json.loads(REQUESTS_JSON.read_text())
    return {}


def save_requests(requests: Dict[str, Any]) -> None:
    REQUESTS_JSON.write_text(json.dumps(requests, indent=2))


def new_request(name: str, email: str, text: str, organisation: str | None,
                preferred_fmt: str) -> Dict[str, Any]:
    rid = str(uuid4())
    ref = f"FOI-{datetime.now():%Y%m%d}-{str(uuid4())[:6].upper()}"
    received = _now_iso()
    due = _due_date_from(datetime.now())
    return {
        "id": rid,
        "reference": ref,
        "name": name,
        "email": email,
        "organization": organisation,
        "request_text": text,
        "preferred_format": preferred_fmt,
        "received_date": received,
        "due_date": due,
        "status": "New",
        "response": None,
    }