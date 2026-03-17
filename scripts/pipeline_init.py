#!/usr/bin/env python3
"""Bulk pipeline: seeds -> drafts -> (auto-fix) -> (LLM fill) -> promote -> dedupe/merge -> report -> reindex.

Initialization-oriented batch job:
- ingest seed skills into drafts
- normalize draft SKILL.md structure (autofix)
- fill placeholder-heavy drafts using LLM (llm_fill_drafts)
- promote passing drafts into curated SkillBank/skills
- deduplicate + merge similar curated leaves automatically (keep canonical, move duplicates)
- regenerate AGENTS.md DocIndex

Safety:
- Seeds are never modified.
- Curated leaves are never overwritten by promote.
- Dedupe keeps a canonical leaf and moves duplicates to SkillBank/drafts/_merged/.

"""

from __future__ import annotations

import argparse
import os
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="Apply changes")
    ap.add_argument(
        "--seeds",
        nargs="+",
        default=["openclaw-workspace-skills", "openclaw-agents-skills"],
        help="Seed folders under skill-seeds/ to ingest",
    )
    ap.add_argument("--force-import", action="store_true", help="Overwrite existing drafts during import")
    ap.add_argument("--min-merge-group", type=int, default=2, help="Only merge groups with at least N leaves")
    ap.add_argument(
        "--llm-fill",
        action="store_true",
        help="Run LLM fill step to reduce TODO placeholders before promote (requires API key)",
    )
    ap.add_argument(
        "--env-file",
        type=str,
        default="",
        help="Optional .env file (KEY=VALUE) to load secrets for the LLM fill step",
    )
    ap.add_argument(
        "--llm-limit",
        type=int,
        default=0,
        help="Limit number of draft files processed by LLM fill (0 = no limit)",
    )
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

    # Phase B1.5: LLM fill drafts (optional)
    if args.llm_fill:
        # If secrets are provided as an env file, load them for this process (and child processes will inherit).
        if args.env_file:
            env_path = Path(args.env_file).expanduser()
            if env_path.exists():
                for raw in env_path.read_text(encoding="utf-8", errors="replace").splitlines():
                    line = raw.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    if k and k not in os.environ:
                        os.environ[k] = v

        cmd = ["python", str(REPO_ROOT / "scripts" / "llm_fill_drafts.py")]
        if args.apply:
            cmd.append("--apply")
        if args.llm_limit and args.llm_limit > 0:
            cmd += ["--limit", str(args.llm_limit)]
        if args.env_file:
            cmd += ["--env-file", args.env_file]
        run(cmd)

    # Phase B2: promote
    cmd = ["python", str(REPO_ROOT / "scripts" / "promote_drafts.py")]
    if args.apply:
        cmd.append("--apply")
    run(cmd)

    # Phase C: dedupe/merge curated leaves
    cmd = [
        "python",
        str(REPO_ROOT / "scripts" / "dedupe_merge_skills.py"),
        "--min-group",
        str(args.min_merge_group),
    ]
    if args.apply:
        cmd.append("--apply")
    run(cmd)

    # Reindex
    run(["python", str(REPO_ROOT / "scripts" / "build_agents_md_index.py"), "--write"])

    print("Pipeline done.")


if __name__ == "__main__":
    main()
