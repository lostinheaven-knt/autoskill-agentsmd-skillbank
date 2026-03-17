#!/usr/bin/env python3
"""Secret scan gate for SkillBank pipeline.

This script scans the repo tree (or specific roots) for likely secrets / credentials.
It is intended as a *defense-in-depth* check before promoting drafts/skills.

Design goals:
- Prefer false negatives over false positives? No: we prefer catching real leaks, but keep noise reasonable.
- Never print the full secret value (redact matched content where possible).
- Fail fast with a clear report.

Usage:
  python scripts/secret_scan.py
  python scripts/secret_scan.py --roots SkillBank skill-seeds

Exit codes:
- 0: no findings
- 2: findings detected

"""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]

# Patterns: focus on high-signal tokens and private key blocks.
PATTERNS: List[Tuple[str, re.Pattern]] = [
    ("private_key_block", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("aws_access_key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("github_pat", re.compile(r"\bghp_[A-Za-z0-9]{30,}\b")),
    ("openai_key", re.compile(r"\bsk-[A-Za-z0-9]{20,}\b")),
    ("slack_token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b")),

    # High-signal env secrets: fail only when value looks real (not placeholders)
    ("env_secret_real", re.compile(
        r"\b(?:OPENAI_API_KEY|DEEPSEEK_API_KEY|GITHUB_TOKEN|AWS_SECRET_ACCESS_KEY|FEISHU_APP_SECRET)\s*=\s*(?!\.{3})(?!\"\.\.\.\")(?!<)(?!your_)(?!\"your_)([^\s#\"]{12,})"
    )),
    ("env_id_real", re.compile(
        r"\b(?:FEISHU_APP_ID|AWS_ACCESS_KEY_ID)\s*=\s*(?!<)(?!your_)([^\s#\"]{8,})"
    )),

    # JSON secrets: fail only when value looks real (not placeholders like <FEISHU_APP_SECRET>)
    ("json_secret_real", re.compile(
        r"\"(?:app_secret|secret|api_key|access_token)\"\s*:\s*\"(?!<)(?!your_)([^\"]{12,})\""
    )),
]

# Ignore paths that commonly contain vendored or binary content.
IGNORE_DIRS = {
    ".git",
    "node_modules",
    ".venv",
    "dist",
    "build",
    "__pycache__",
}

IGNORE_GLOBS = [
    "**/.secrets.env",
    "**/*.pem",
    "**/*.key",
]


@dataclass
class Finding:
    kind: str
    file: str
    line: int
    snippet: str


def should_ignore_path(p: Path) -> bool:
    parts = set(p.parts)
    if parts & IGNORE_DIRS:
        return True
    for g in IGNORE_GLOBS:
        if p.match(g):
            return True
    return False


def iter_text_files(root: Path) -> Iterable[Path]:
    for p in root.rglob("*"):
        if p.is_dir():
            continue
        if should_ignore_path(p):
            continue
        # crude binary check
        try:
            b = p.read_bytes()
        except Exception:
            continue
        if b"\x00" in b[:4096]:
            continue
        yield p


def redact(s: str) -> str:
    s = s.strip("\n")
    if len(s) <= 12:
        return "<REDACTED>"
    return s[:4] + "…" + s[-4:]


def scan_file(p: Path) -> List[Finding]:
    out: List[Finding] = []
    try:
        lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception:
        return out

    for i, ln in enumerate(lines, start=1):
        for kind, rx in PATTERNS:
            m = rx.search(ln)
            if not m:
                continue

            snippet = ln
            # redact captured secret-like group if present
            if m.lastindex and m.lastindex >= 1:
                secret = m.group(1)
                snippet = ln.replace(secret, redact(secret))
            out.append(Finding(kind, str(p), i, snippet[:300]))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--roots",
        nargs="*",
        default=["."],
        help="Roots to scan (relative to repo root). Default: .",
    )
    args = ap.parse_args()

    findings: List[Finding] = []
    for r in args.roots:
        root = (REPO_ROOT / r).resolve()
        if not root.exists():
            continue
        for f in iter_text_files(root):
            findings.extend(scan_file(f))

    if findings:
        print("Secret scan findings (redacted):")
        for fx in findings:
            rel = str(Path(fx.file).resolve().relative_to(REPO_ROOT)) if str(fx.file).startswith(str(REPO_ROOT)) else fx.file
            print(f"- [{fx.kind}] {rel}:{fx.line}: {fx.snippet}")
        print(f"\nTotal findings: {len(findings)}")
        return 2

    print("Secret scan: OK (no findings)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
