from __future__ import annotations

from pathlib import Path

from skillbank.detectors import scan_text


def test_safe_token_context_is_not_flagged() -> None:
    text = "1. Extract a `folder_token` or file token from a Feishu drive URL when available."
    findings = scan_text(text, Path("doc.md"))
    assert findings == []


def test_secret_assignment_is_flagged() -> None:
    text = "GENSTORE_PASSWORD=lostlostlostlost"
    findings = scan_text(text, Path("env.txt"))
    assert any(f.kind in {"secret_assignment", "env_secret_name"} for f in findings)
