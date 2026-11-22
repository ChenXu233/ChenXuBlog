"""Plain-text excerpts for article list responses and feeds."""

import re


def make_excerpt(body: str, max_length: int = 160) -> str:
    """Remove common Markdown syntax and bound the returned text size."""
    text = re.sub(r"\x60{3}[\s\S]*?\x60{3}", " ", body)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[#>*_~\x60-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= max_length:
        return text
    return text[:max_length].rstrip() + "…"
