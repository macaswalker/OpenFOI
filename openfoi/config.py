"""Central configuration & constants."""
from pathlib import Path
import os

ROOT_DIR = Path(__file__).resolve().parent.parent  # project root
DATA_DIR = ROOT_DIR / "data"
REQUESTS_JSON = DATA_DIR / "requests.json"
DOCUMENTS_DIR = DATA_DIR / "documents"
RESPONSES_DIR = DATA_DIR / "responses"

# Ensure folders exist at import time
for p in [DATA_DIR, DOCUMENTS_DIR, RESPONSES_DIR]:
    p.mkdir(parents=True, exist_ok=True)

FOI_EXEMPTIONS = {
    "S21": "Information accessible by other means",
    "S22": "Information intended for future publication",
    "S23": "Security matters",
    "S24": "National security",
    "S26": "Defence",
    "S27": "International relations",
    "S28": "Relations within the UK",
    "S29": "The economy",
    "S30": "Investigations and proceedings",
    "S31": "Law enforcement",
    "S32": "Court records",
    "S33": "Audit functions",
    "S35": "Formulation of government policy",
    "S36": "Prejudice to the effective conduct of public affairs",
    "S37": "Communications with Her Majesty and honours",
    "S38": "Health and safety",
    "S40": "Personal information",
    "S41": "Information provided in confidence",
    "S42": "Legal professional privilege",
    "S43": "Commercial interests",
    "S44": "Prohibitions on disclosure",
}
