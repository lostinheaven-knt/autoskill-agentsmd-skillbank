#!/usr/bin/env python3
"""Import skills from read-only seed stores into SkillBank/drafts.

This is the Phase-A step of the pipeline:
  seeds (read-only) -> drafts (candidates)

Design:
- Preserve full directories (scripts/docs/examples/assets).
- Do NOT modify seeds.
- Deterministic destination paths for traceability.
- Idempotent by default (skip existing drafts) unless --force.

Draft destination layout (recommended):
  SkillBank/drafts/<seed_name>/<relative_path_from_seed_root>/

Where <seed_name> matches the folder under skill-seeds/ (e.g. openclaw-agents-skills).

Usage:
  python scripts/import_seeds_to_drafts.py --seeds openclaw-workspace-skills openclaw-agents-skills

"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from typing import Iterable, List

REPO_ROOT = Path(__file__).resolve().parents[1]
SEEDS_ROOT = REPO_ROOT / "skill-seeds"
DRAFTS_ROOT = REPO_ROOT / "SkillBank" / "drafts"


def find_skill_dirs(seed_root: Path) -> List[Path]:
    """Find candidate skill directories under a seed root.

    Heuristic: any directory that contains SKILL.md.
    """
    skill_dirs = set()
    for f in seed_root.rglob("SKILL.md"):
        if f.is_file():
            skill_dirs.add(f.parent)
    return sorted(skill_dirs)


def safe_copytree(src: Path, dst: Path, force: bool) -> str:
    if dst.exists():
        if force:
            shutil.rmtree(dst)
        else:
            return "skip"
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dst, symlinks=True)
    return "copied"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--seeds",
        nargs="+",
        default=["openclaw-workspace-skills", "openclaw-agents-skills"],
        help="Seed folders under skill-seeds/ to import",
    )
    ap.add_argument("--force", action="store_true", help="Overwrite existing drafts")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    actions = {"copied": 0, "skip": 0}

    for seed_name in args.seeds:
        seed_root = SEEDS_ROOT / seed_name
        if not seed_root.exists():
            raise SystemExit(f"Seed root not found: {seed_root}")

        skill_dirs = find_skill_dirs(seed_root)
        for sd in skill_dirs:
            rel = sd.relative_to(seed_root)
            dst = DRAFTS_ROOT / seed_name / rel

            if args.dry_run:
                print(f"[dry-run] copy {sd} -> {dst}")
                continue

            result = safe_copytree(sd, dst, args.force)
            actions[result] += 1

    if args.dry_run:
        return

    print("Imported to drafts:")
    for k, v in actions.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
