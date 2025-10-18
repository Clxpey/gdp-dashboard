from __future__ import annotations
from pathlib import Path
from typing import List, Tuple
import base64

from google.oauth2.credentials import Credentials  # type: ignore
from google_auth_oauthlib.flow import InstalledAppFlow  # type: ignore
from googleapiclient.discovery import build  # type: ignore
from googleapiclient.errors import HttpError  # type: ignore

from .config import GOOGLE_CLIENT_SECRET_FILE, GOOGLE_TOKEN_FILE, GMAIL_USER_ID, GMAIL_DIR

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
]


def ensure_gmail_credentials() -> bool:
    try:
        if GOOGLE_TOKEN_FILE.exists():
            return True
        if not GOOGLE_CLIENT_SECRET_FILE.exists():
            return False
        flow = InstalledAppFlow.from_client_secrets_file(str(GOOGLE_CLIENT_SECRET_FILE), SCOPES)
        creds = flow.run_local_server(port=0)
        GOOGLE_TOKEN_FILE.write_text(creds.to_json())
        return True
    except Exception:
        return False


def list_attachments(max_messages: int = 50) -> List[Tuple[str, str, bytes]]:
    """Return list of tuples (filename, mimeType, data_bytes)."""
    if not GOOGLE_TOKEN_FILE.exists():
        return []
    creds = Credentials.from_authorized_user_file(str(GOOGLE_TOKEN_FILE), SCOPES)
    service = build("gmail", "v1", credentials=creds)

    results: List[Tuple[str, str, bytes]] = []
    try:
        msgs = service.users().messages().list(userId=GMAIL_USER_ID, maxResults=max_messages, q="has:attachment").execute()
        for m in msgs.get("messages", []):
            msg = service.users().messages().get(userId=GMAIL_USER_ID, id=m["id"]).execute()
            parts = msg.get("payload", {}).get("parts", [])
            for p in parts:
                if p.get("filename") and p.get("body", {}).get("attachmentId"):
                    att_id = p["body"]["attachmentId"]
                    att = service.users().messages().attachments().get(userId=GMAIL_USER_ID, messageId=m["id"], id=att_id).execute()
                    data = base64.urlsafe_b64decode(att.get("data", ""))
                    filename = p.get("filename")
                    mime = p.get("mimeType", "application/octet-stream")
                    results.append((filename, mime, data))
    except HttpError:
        return []
    return results


def save_attachments_to_dir() -> List[Path]:
    saved: List[Path] = []
    for filename, _mime, data in list_attachments():
        path = GMAIL_DIR / filename
        path.write_bytes(data)
        saved.append(path)
    return saved
