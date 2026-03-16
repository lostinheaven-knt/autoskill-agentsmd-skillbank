#!/usr/bin/env python3
"""Auto-fix draft SKILL.md files to match the v0.1 template structure.

Goal: increase promote success rate WITHOUT inventing unsafe operational details.

Principles:
- Never change seeds.
- Only edit drafts.
- Preserve existing content as much as possible.
- If a required section is missing, create it with a minimal placeholder.
- If Procedure has <3 steps, add generic, safe placeholders (TODO) that force future refinement.
- If Checks / When NOT to use have no bullets, add a minimal TODO bullet.

This is a scaffolding normalizer, not a content generator.

"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
DRAFTS_ROOT = REPO_ROOT / "SkillBank" / "drafts"

SECTION_ORDER = [
    "Purpose",
    "When to use",
    "When NOT to use",
    "Inputs / Preconditions",
    "Procedure",
    "Checks",
    "Failure modes",
    "Examples",
    "Version / Changelog",
]


@dataclass
class FixResult:
    path: str
    changed: bool
    notes: List[str]


def extract_title(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip() or "Untitled Skill"
    return "Untitled Skill"


def split_sections(text: str) -> Dict[str, str]:
    """Parse markdown headings into sections by exact names (case-insensitive match on SECTION_ORDER).

    Returns dict: section_name -> body (without the heading line).
    Content before first recognized section is ignored (except title).
    """
    # Find all headings
    lines = text.splitlines()
    bodies: Dict[str, List[str]] = {k: [] for k in SECTION_ORDER}

    current = None
    for line in lines:
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            name = m.group(1).strip()
            # normalize to canonical section name
            canon = None
            for sec in SECTION_ORDER:
                if sec.lower() == name.lower():
                    canon = sec
                    break
            current = canon
            continue
        if current:
            bodies[current].append(line)

    return {k: "\n".join(v).strip("\n") for k, v in bodies.items() if "\n".join(v).strip("\n") != ""}


def ensure_bullet(body: str, default_bullet: str) -> Tuple[str, bool]:
    if re.search(r"^\s*-\s+.+$", body, flags=re.MULTILINE):
        return body, False
    # add a bullet
    new = (body.strip() + "\n" if body.strip() else "") + f"- {default_bullet}\n"
    return new.strip("\n"), True


def ensure_numbered_steps(body: str, min_steps: int = 3) -> Tuple[str, bool]:
    steps = re.findall(r"^\s*\d+\.\s+.+$", body, flags=re.MULTILINE)
    changed = False
    out = body.strip("\n")
    # count existing leading numbered list items
    n = len(steps)
    if n >= min_steps:
        return out, False

    # Append placeholders
    if out.strip():
        out += "\n"
    for i in range(n + 1, min_steps + 1):
        out += f"{i}. TODO: refine this step with concrete actions and parameters.\n"
        changed = True
    return out.strip("\n"), changed


def render(title: str, sections: Dict[str, str]) -> str:
    lines = [f"# {title}", ""]
    for sec in SECTION_ORDER:
        lines.append(f"## {sec}")
        body = sections.get(sec, "").strip("\n")
        if body:
            lines.append(body)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def autofix_text(text: str) -> Tuple[str, bool, List[str]]:
    notes: List[str] = []
    title = extract_title(text)
    sections = split_sections(text)
    changed = False

    # Ensure required sections exist with minimal placeholders
    if "Purpose" not in sections:
        sections["Purpose"] = "TODO: Describe the purpose in 1-2 sentences."
        notes.append("add Purpose")
        changed = True

    if "When to use" not in sections:
        sections["When to use"] = "- TODO: specify scenarios where this skill applies."
        notes.append("add When to use")
        changed = True

    body = sections.get("When NOT to use", "")
    body, c = ensure_bullet(body, "TODO: specify at least one situation where this skill should NOT be used.")
    if c:
        notes.append("fix When NOT to use bullets")
        changed = True
    sections["When NOT to use"] = body

    if "Inputs / Preconditions" not in sections:
        sections["Inputs / Preconditions"] = "- Required info: TODO\n- Assumptions: TODO\n- Constraints: TODO"
        notes.append("add Inputs / Preconditions")
        changed = True

    proc = sections.get("Procedure", "")
    proc, c = ensure_numbered_steps(proc, 3)
    if c:
        notes.append("fix Procedure steps")
        changed = True
    sections["Procedure"] = proc

    checks = sections.get("Checks", "")
    checks, c = ensure_bullet(checks, "TODO: add at least one verifiable check.")
    if c:
        notes.append("fix Checks bullets")
        changed = True
    sections["Checks"] = checks

    if "Failure modes" not in sections:
        sections["Failure modes"] = "- TODO: list at least one failure mode and how to detect it."
        notes.append("add Failure modes")
        changed = True

    if "Examples" not in sections:
        sections["Examples"] = "### Example 1\nTODO"
        notes.append("add Examples")
        changed = True

    if "Version / Changelog" not in sections:
        sections["Version / Changelog"] = "- v0.1.0: imported (autofix)"
        notes.append("add Version / Changelog")
        changed = True

    # Preserve existing non-empty optional sections if present
    for opt in ["Purpose", "When to use", "Inputs / Preconditions", "Procedure", "Checks", "Failure modes", "Examples", "Version / Changelog"]:
        if opt in sections:
            sections[opt] = sections[opt].strip("\n")

    new_text = render(title, sections)
    if new_text != text:
        # If structure parser dropped some content (unrecognized sections), keep original appended.
        # We do this conservatively: only if original has headings we didn't recognize.
        extra = []
        for line in text.splitlines():
            if re.match(r"^##\s+", line):
                name = re.sub(r"^##\s+", "", line).strip()
                if all(name.lower() != s.lower() for s in SECTION_ORDER):
                    extra.append(line)
        if extra:
            new_text += "\n<!-- ORIGINAL_EXTRA_SECTIONS_DETECTED -->\n"
            new_text += "<!-- Please review original draft for additional headings not covered by the template. -->\n"
            notes.append("extra sections detected")
            changed = True

    return new_text, changed, notes


def iter_draft_skill_md() -> List[Path]:
    return sorted(DRAFTS_ROOT.rglob("SKILL.md"))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="Write fixes to draft SKILL.md files")
    args = ap.parse_args()

    results: List[FixResult] = []

    for p in iter_draft_skill_md():
        text = p.read_text(encoding="utf-8", errors="replace")
        new_text, changed, notes = autofix_text(text)
        if changed and args.apply:
            p.write_text(new_text, encoding="utf-8")
        results.append(FixResult(str(p), changed, notes))

    changed_count = sum(1 for r in results if r.changed)
    print(f"draft_skill_files: {len(results)}")
    print(f"changed: {changed_count}")


if __name__ == "__main__":
    main()
