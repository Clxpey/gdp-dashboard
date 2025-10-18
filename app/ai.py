from __future__ import annotations
import os
import re
from typing import Any, Dict, List, Optional, Tuple

from .config import OPENAI_API_KEY, OPENAI_MODEL

try:
    from openai import OpenAI  # type: ignore
except Exception:  # pragma: no cover
    OpenAI = None  # type: ignore


def has_openai() -> bool:
    return bool(OPENAI_API_KEY and OpenAI is not None)


def summarize_text(text: str, max_words: int = 120) -> str:
    """Summarize text using OpenAI if available; fall back to extractive lead summary."""
    text = text.strip()
    if not text:
        return ""

    if has_openai():
        try:
            client = OpenAI(api_key=OPENAI_API_KEY)
            prompt = (
                "Summarize the following document for a manager. "
                f"Limit to about {max_words} words.\n\n" + text[:12000]
            )
            resp = client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a concise business document summarizer."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
            )
            return resp.choices[0].message.content or ""
        except Exception:
            pass  # gracefully fall back

    # Fallback: simple lead-based summary (first sentences)
    sentences = re.split(r"(?<=[.!?])\s+", text)
    summary: List[str] = []
    word_count = 0
    for s in sentences:
        words = len(s.split())
        if word_count + words > max_words and summary:
            break
        summary.append(s)
        word_count += words
        if word_count >= max_words:
            break
    return " ".join(summary).strip()


# Intent parsing for natural language commands for the document assistant
# Supported actions: move, rename, tag, archive, summarize, search

Action = str


def parse_intent(command: str) -> Dict[str, Any]:
    cmd = command.strip().lower()

    # Move: "move all client x files to folder y"
    m = re.search(r"move (?:all )?(?P<what>.+?) to (?:folder|dir|directory) (?P<dest>.+)$", cmd)
    if m:
        return {"action": "move", "what": m.group("what").strip(), "dest": m.group("dest").strip()}

    # Rename: "rename file abc to xyz.pdf"
    m = re.search(r"rename (?:file )?(?P<what>.+?) to (?P<dest>.+)$", cmd)
    if m:
        return {"action": "rename", "what": m.group("what").strip(), "dest": m.group("dest").strip()}

    # Tag: "tag invoices as urgent" / "tag client x files as contracts"
    m = re.search(r"tag (?P<what>.+?) as (?P<tag>.+)$", cmd)
    if m:
        return {"action": "tag", "what": m.group("what").strip(), "tag": m.group("tag").strip()}

    # Archive: "archive client x invoices"
    m = re.search(r"archive (?P<what>.+)$", cmd)
    if m:
        return {"action": "archive", "what": m.group("what").strip()}

    # Summarize: "summarize the document abc" / "summarize this"
    if cmd.startswith("summarize"):
        w = cmd.replace("summarize", "", 1).strip() or "this"
        return {"action": "summarize", "what": w}

    # Search default: treat as search query (smart search)
    return {"action": "search", "query": command.strip()}


def llm_structured_intent(command: str) -> Dict[str, Any]:
    if not has_openai():
        return parse_intent(command)

    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        sys_prompt = (
            "You convert a user's natural command into a structured JSON intent for document management. "
            "Actions: move, rename, tag, archive, summarize, search. "
            "JSON keys for actions: "
            "- move: action, what, dest\n"
            "- rename: action, what, dest\n"
            "- tag: action, what, tag\n"
            "- archive: action, what\n"
            "- summarize: action, what\n"
            "- search: action, query\n"
            "Always return a single JSON object."
        )
        resp = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": command},
            ],
            temperature=0,
        )
        content = resp.choices[0].message.content or ""
        import json
        # try to extract JSON
        start = content.find("{")
        end = content.rfind("}")
        if start != -1 and end != -1:
            return json.loads(content[start : end + 1])
    except Exception:
        pass

    return parse_intent(command)
