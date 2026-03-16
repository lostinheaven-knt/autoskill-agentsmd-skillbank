#!/usr/bin/env python3
"""Bulk pipeline: seeds -> drafts -> (auto-fix) -> promote -> report -> reindex.

This command is intended for initialization:
- It ingests all seed skills into drafts.
- It attempts to auto-fix draft SKILL.md to match our template (minimal safe edits).
- It promotes passing drafts into curated SkillBank/skills.
- It writes reports for failures/collisions.
- It regenerates AGENTS.md DocIndex.

Safety:
- Seeds are never modified.
- Curated skills are never overwritten.

"""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="Apply changes (default is dry-run/print for substeps where supported)")
    ap.add_argument(
        "--seeds",
        nargs="+",
        default=["openclaw-workspace-skills", "openclaw-agents-skills"],
        help="Seed folders under skill-seeds/ to ingest",
    )
    ap.add_argument("--force-import", action="store_true", help="Overwrite existing drafts during import")
    args = ap.parse_args()

    # Phase A: import
    cmd = ["python", str(REPO_ROOT / "scripts" / "import_seeds_to_drafts.py"), "--seeds", *args.seeds]
    if args.force_import:
        cmd.append("--force")
    run(cmd)

    # Phase B1: auto-fix drafts
    cmd = ["python", str(REPO_ROOT / "scripts" / "autofix_drafts.py")]
    if args.apply:
        cmd.append("--apply")
    run(cmd)

    # Phase B2: promote
    cmd = ["python", str(REPO_ROOT / "scripts" / "promote_drafts.py")]
    if args.apply:
        cmd.append("--apply")
    run(cmd)

    # Reindex
    run(["python", str(REPO_ROOT / "scripts" / "build_agents_md_index.py"), "--write"])

    print("Pipeline done.")


if __name__ == "__main__":
    main()
