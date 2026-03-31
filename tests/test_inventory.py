from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_review_inventory_writes_reports() -> None:
    subprocess.run(["python", "scripts/review_inventory.py", "--write"], cwd=ROOT, check=True)

    report_json = ROOT / "reports" / "skillbank-inventory.json"
    report_md = ROOT / "reports" / "skillbank-inventory.md"

    assert report_json.exists()
    assert report_md.exists()

    data = json.loads(report_json.read_text(encoding="utf-8"))
    entries = data["entries"]

    assert any(e["rel_path"] == "skills/ops/feishu/feishu-doc" and e["role"] == "production" for e in entries)
    assert any(e["rel_path"] == "seed_openclaw_skills/feishu-doc" and e["role"] == "seed" for e in entries)
