#!/usr/bin/env python3
"""LEGACY: historical pipeline script.

This file is retained for reference only and is not part of the current governance-first recommended workflow. Prefer the governance helpers under scripts/ and scripts/skillbank/.
"""

"""Promote draft skills into curated SkillBank/skills with reports.

This is the Phase-B step of the pipeline:
  drafts -> skills (curated)

It is designed to run in bulk:
- scans all drafts
- applies a lightweight quality gate
- suggests a target path
- promotes passing candidates
- generates reports for failures and collisions

Important constraints:
- We do NOT modify seed stores.
- We keep curated tree small and high-quality.

Quality gate (v0.1, lightweight):
- SKILL.md exists
- Contains required sections (case-insensitive, markdown headings):
    Purpose
    When to use
    When NOT to use
    Procedure
    Checks
    Failure modes
- Procedure has >= 3 numbered steps ("1.")
- When NOT to use has >= 1 bullet ("- ")
- Checks has >= 1 bullet
- NEW: Reject placeholder-only drafts (TODO ratio/threshold), so TODO scaffolds never pollute curated tree.
  NOTE: TODO lines are fine in small amounts; we only block when they dominate.

Target path heuristic (deterministic):
- Use existing leaf path if the draft already sits under a goal tree that matches our naming rules.
- Else fallback to: imported/<seed_name>/<slug>

Collisions:
- If target leaf already exists, we do not overwrite.
  We record a merge candidate in MERGE_QUEUE.md.

Outputs:
- SkillBank/meta/drafts_report.json
- SkillBank/drafts/REPORT.md
- SkillBank/drafts/MERGE_QUEUE.md

Usage:
  python scripts/promote_drafts.py --apply
  python scripts/promote_drafts.py --print

"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
DRAFTS_ROOT = REPO_ROOT / "SkillBank" / "drafts"
CURATED_ROOT = REPO_ROOT / "SkillBank" / "skills"
META_ROOT = REPO_ROOT / "SkillBank" / "meta"


REQUIRED_SECTIONS = [
    "purpose",
    "when to use",
    "when not to use",
    "procedure",
    "checks",
    "failure modes",
]

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

# Placeholder blocking (tuneable, conservative)
# - If TODO lines are >= this absolute number, block.
# - Or if TODO ratio among content-like lines exceeds ratio, block.
TODO_MAX_LINES = 10
TODO_MAX_RATIO = 0.25


@dataclass
class GateResult:
    ok: bool
    reasons: List[str]


def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def has_required_sections(text: str) -> Tuple[bool, List[str]]:
    low = text.lower()
    missing = []
    for sec in REQUIRED_SECTIONS:
        if re.search(r"^#+\s+" + re.escape(sec) + r"\s*$", low, flags=re.MULTILINE) is None:
            missing.append(f"missing section: {sec}")
    return (len(missing) == 0, missing)


def count_numbered_steps(text: str) -> int:
    return len(re.findall(r"^\s*\d+\.\s+.+$", text, flags=re.MULTILINE))


def section_body(text: str, section: str) -> str:
    pattern = re.compile(r"^#+\s+" + re.escape(section) + r"\s*$", re.IGNORECASE | re.MULTILINE)
    m = pattern.search(text)
    if not m:
        return ""
    start = m.end()
    m2 = re.search(r"^#+\s+.+$", text[start:], flags=re.MULTILINE)
    end = start + (m2.start() if m2 else len(text[start:]))
    return text[start:end]


def count_bullets(body: str) -> int:
    return len(re.findall(r"^\s*-\s+.+$", body, flags=re.MULTILINE))


def placeholder_gate(text: str) -> Tuple[bool, List[str]]:
    """Block placeholder-heavy drafts.

    We count TODO lines only in the main body (anything inside code fences is ignored),
    and only for content-like lines (skip headings/empty/comments).
    """

    lines = text.splitlines()
    in_fence = False
    todo = 0
    content = 0

    for ln in lines:
        if ln.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        s = ln.strip()
        if not s:
            continue
        if s.startswith("<!--"):
            continue
        if s.startswith("#"):
            continue

        # content-like
        content += 1
        if "todo" in s.lower():
            todo += 1

    if content == 0:
        return False, ["empty content"]

    ratio = todo / max(1, content)
    reasons = []
    if todo >= TODO_MAX_LINES:
        reasons.append(f"too many TODO lines ({todo} >= {TODO_MAX_LINES})")
    if ratio > TODO_MAX_RATIO:
        reasons.append(f"TODO ratio too high ({ratio:.0%} > {TODO_MAX_RATIO:.0%})")

    return (len(reasons) == 0), reasons


def quality_gate(skill_md: Path) -> GateResult:
    if not skill_md.exists():
        return GateResult(False, ["SKILL.md not found"])

    text = read_text(skill_md)
    ok, missing = has_required_sections(text)
    reasons = list(missing)

    steps = count_numbered_steps(section_body(text, "Procedure"))
    if steps < 3:
        reasons.append(f"procedure steps < 3 (found {steps})")

    not_use_bullets = count_bullets(section_body(text, "When NOT to use"))
    if not_use_bullets < 1:
        reasons.append("When NOT to use bullets < 1")

    checks_bullets = count_bullets(section_body(text, "Checks"))
    if checks_bullets < 1:
        reasons.append("Checks bullets < 1")

    ok2, reasons2 = placeholder_gate(text)
    if not ok2:
        reasons.extend(reasons2)

    return GateResult(len(reasons) == 0, reasons)


def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9\-_/]+", "-", s)
    s = re.sub(r"-+", "-", s)
    s = s.strip("-")
    return s or "skill"


def valid_path_parts(parts: List[str]) -> bool:
    return all(NAME_RE.match(p) for p in parts if p)


def propose_target_leaf(draft_dir: Path) -> str:
    rel = draft_dir.relative_to(DRAFTS_ROOT)
    parts = list(rel.parts)
    seed_name = parts[0]
    orig_parts = parts[1:]

    if orig_parts and valid_path_parts(orig_parts):
        return "/".join(orig_parts)

    return f"imported/{slugify(seed_name)}/{slugify('/'.join(orig_parts) or draft_dir.name)}"


def iter_draft_skill_dirs() -> List[Path]:
    dirs = set()
    for f in DRAFTS_ROOT.rglob("SKILL.md"):
        dirs.add(f.parent)
    return sorted(dirs)


def copy_leaf_to_curated(draft_dir: Path, target_leaf: str, apply: bool) -> Tuple[bool, str]:
    """Copy a draft leaf into curated tree.

    Collision policy (upgrade-safe):
    - Default: do not overwrite existing curated leaves.
    - Exception: if the existing curated SKILL.md is clearly placeholder-heavy (TODO gate fails)
      AND the draft passes the quality gate, we allow an in-place upgrade.
      We first move the old curated leaf to SkillBank/drafts/_replaced/<timestamp>/<target_leaf>/ for traceability.
    """

    dst_dir = CURATED_ROOT / target_leaf
    if dst_dir.exists():
        # Decide whether to upgrade
        dst_skill = dst_dir / "SKILL.md"
        src_skill = draft_dir / "SKILL.md"

        # If existing curated fails placeholder gate but new draft passes full quality gate, upgrade.
        if dst_skill.exists() and src_skill.exists():
            dst_text = read_text(dst_skill)
            src_text = read_text(src_skill)

            ok_dst, _reasons_dst = placeholder_gate(dst_text)
            ok_src, _reasons_src = placeholder_gate(src_text)

            if (not ok_dst) and ok_src:
                msg = f"upgrade: replacing placeholder-heavy curated leaf {dst_dir}"
                if apply:
                    import time

                    stamp = time.strftime("%Y%m%d-%H%M%S")
                    backup = (DRAFTS_ROOT / "_replaced" / stamp / target_leaf).resolve()
                    backup.parent.mkdir(parents=True, exist_ok=True)
                    if backup.exists():
                        shutil.rmtree(backup)
                    shutil.copytree(dst_dir, backup, symlinks=True)

                    # Replace in place
                    shutil.rmtree(dst_dir)
                    dst_dir.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copytree(draft_dir, dst_dir, symlinks=True)
                return True, msg

        return False, f"collision: {dst_dir}"

    if apply:
        dst_dir.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(draft_dir, dst_dir, symlinks=True)
    return True, f"promoted: {dst_dir}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="Actually promote into SkillBank/skills")
    ap.add_argument("--print", action="store_true", help="Print summary (default)")
    args = ap.parse_args()

    META_ROOT.mkdir(parents=True, exist_ok=True)

    report: Dict[str, dict] = {
        "promoted": [],
        "failed": [],
        "collisions": [],
        "stats": {},
    }

    merge_queue_lines = ["# MERGE QUEUE", "", "Collisions where a draft leaf maps to an existing curated leaf.", ""]
    fail_lines = ["# DRAFT REPORT", "", "Drafts that failed the quality gate (not promoted).", ""]

    promoted = 0
    failed = 0
    collisions = 0

    for d in iter_draft_skill_dirs():
        skill_md = d / "SKILL.md"
        gate = quality_gate(skill_md)
        target = propose_target_leaf(d)

        if not gate.ok:
            failed += 1
            item = {"draft": str(d), "target": target, "reasons": gate.reasons}
            report["failed"].append(item)
            fail_lines.append(f"- {target}  (from {d})")
            for r in gate.reasons:
                fail_lines.append(f"  - {r}")
            continue

        ok, msg = copy_leaf_to_curated(d, target, apply=args.apply)
        if ok:
            promoted += 1
            report["promoted"].append({"draft": str(d), "target": target})
        else:
            collisions += 1
            report["collisions"].append({"draft": str(d), "target": target, "reason": msg})
            merge_queue_lines.append(f"- {target}  (draft: {d})")

    report["stats"] = {"promoted": promoted, "failed": failed, "collisions": collisions}

    (META_ROOT / "drafts_report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    (DRAFTS_ROOT / "REPORT.md").write_text("\n".join(fail_lines) + "\n", encoding="utf-8")
    (DRAFTS_ROOT / "MERGE_QUEUE.md").write_text("\n".join(merge_queue_lines) + "\n", encoding="utf-8")

    if args.print or True:
        print(json.dumps(report["stats"], indent=2))
        print(f"meta report: {META_ROOT / 'drafts_report.json'}")
        print(f"human report: {DRAFTS_ROOT / 'REPORT.md'}")
        print(f"merge queue: {DRAFTS_ROOT / 'MERGE_QUEUE.md'}")


if __name__ == "__main__":
    main()
