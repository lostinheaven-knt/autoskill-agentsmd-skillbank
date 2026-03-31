from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Finding:
    path: Path
    kind: str
    line_no: int
    excerpt: str
    severity: str


PATTERNS: list[tuple[str, re.Pattern[str], str]] = [
    ("email", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"), "warn"),
    ("admin_url", re.compile(r"https?://[^\s]*admin[^\s]*", re.IGNORECASE), "high"),
    ("private_domain", re.compile(r"https?://[^\s]*(genstore|genmystore|internal|corp)[^\s]*", re.IGNORECASE), "high"),
    # Only treat token/password-like text as sensitive when it looks like a secret-bearing variable/assignment,
    # not when a doc is merely discussing a normal parameter such as folder_token or wiki token.
    ("secret_assignment", re.compile(r"(?i)\b([A-Z][A-Z0-9_]*(PASSWORD|SECRET|TOKEN|API_KEY)|password|secret|api[_-]?key)\b\s*[:=]"), "high"),
    ("env_secret_name", re.compile(r"\b[A-Z][A-Z0-9_]*(PASSWORD|SECRET|TOKEN|API_KEY)\b"), "warn"),
    ("diary_signal", re.compile(r"(成功经验|记录人|来源人|下次忘记|经验来源)"), "warn"),
]

SAFE_TOKEN_CONTEXT = [
    "doc token",
    "doc_token",
    "wiki token",
    "folder token",
    "folder_token",
    "file token",
    "obj_token",
    "node_token",
    "token type",
    "member-id",
    "member id",
]


def _is_safe_context(kind: str, line: str) -> bool:
    low = line.lower()
    if kind in {"secret_assignment", "env_secret_name"}:
        return any(ctx in low for ctx in SAFE_TOKEN_CONTEXT)
    return False


def scan_text(text: str, path: Path) -> list[Finding]:
    findings: list[Finding] = []
    for idx, line in enumerate(text.splitlines(), start=1):
        for kind, pattern, severity in PATTERNS:
            if pattern.search(line):
                if _is_safe_context(kind, line):
                    continue
                findings.append(Finding(path=path, kind=kind, line_no=idx, excerpt=line.strip()[:200], severity=severity))
    return findings


def scan_file(path: Path) -> list[Finding]:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return []
    return scan_text(text, path)
