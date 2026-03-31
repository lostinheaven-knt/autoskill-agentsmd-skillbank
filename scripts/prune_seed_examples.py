#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from skillbank.detectors import scan_file
from skillbank.paths import meta_root, repo_root, seed_root, trash_root


def load_allowlist(path: Path) -> list[str]:
    items: list[str] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        s = line.strip()
        if s.startswith("- "):
            items.append(s[2:].strip())
    return items


def find_sources(name: str) -> list[Path]:
    candidates = []
    for base in [repo_root() / "skill-seeds" / "openclaw-workspace-skills", repo_root() / "skill-seeds" / "openclaw-agents-skills"]:
        p = base / name
        if p.exists() and p.is_dir():
            candidates.append(p)
    return candidates


def write_seed_status(dst: Path) -> None:
    skill_md = dst / "SKILL.md"
    labels = ["SEED STATUS: RAW"]
    if skill_md.exists() and scan_file(skill_md):
        labels.append("SEED STATUS: SENSITIVE")
    text = "\n".join(labels) + "\n"
    (dst / "SEED_STATUS.md").write_text(text, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="Apply changes")
    ap.add_argument("--dry-run", action="store_true", help="Show planned changes")
    ap.add_argument("--force", action="store_true", help="Overwrite destination if it exists")
    args = ap.parse_args()

    allowlist = load_allowlist(meta_root() / "retained-seed-allowlist.yml")
    dest_root = seed_root()
    trash = trash_root() / "2026-03-31-seed-prune"

    planned_keep: list[tuple[Path, Path]] = []
    missing: list[str] = []
    for name in allowlist:
        sources = find_sources(name)
        if not sources:
            missing.append(name)
            continue
        planned_keep.append((sources[0], dest_root / name))

    print("retain:")
    for src, dst in planned_keep:
        print(f"  - {src} -> {dst}")
    if missing:
        print("missing:")
        for name in missing:
            print(f"  - {name}")

    if not args.apply:
        return 0

    dest_root.mkdir(parents=True, exist_ok=True)
    trash.mkdir(parents=True, exist_ok=True)

    for src, dst in planned_keep:
        if dst.exists():
            if not args.force:
                continue
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        write_seed_status(dst)

    existing = [p for p in dest_root.iterdir() if p.is_dir()]
    retain_names = {dst.name for _src, dst in planned_keep}
    for p in existing:
        if p.name not in retain_names:
            target = trash / p.name
            if target.exists():
                shutil.rmtree(target)
            shutil.move(str(p), str(target))

    print(f"updated seed examples in {dest_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
