from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal

from skillbank.detectors import scan_file
from skillbank.paths import drafts_root, seed_root, skills_root, trash_root

Role = Literal["production", "seed", "draft", "trash", "unknown"]


@dataclass
class SkillEntry:
    rel_path: str
    role: Role
    has_skill_md: bool
    status_label: str | None
    sensitive_hits: list[str]
    suggested_action: str
    title: str | None = None


def classify_role(path: Path) -> Role:
    if path.is_relative_to(skills_root()):
        return "production"
    if path.is_relative_to(seed_root()):
        return "seed"
    if path.is_relative_to(drafts_root()):
        return "draft"
    if path.is_relative_to(trash_root()):
        return "trash"
    return "unknown"


def extract_title(skill_md: Path) -> str | None:
    try:
        for line in skill_md.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.startswith("# "):
                return line[2:].strip() or None
    except Exception:
        return None
    return None


def read_status_label(skill_dir: Path) -> str | None:
    sidecar = skill_dir / "SEED_STATUS.md"
    if sidecar.exists():
        try:
            labels = [line.strip() for line in sidecar.read_text(encoding="utf-8", errors="replace").splitlines() if line.strip().startswith("SEED STATUS:")]
            if labels:
                return "; ".join(labels)
        except Exception:
            return None
    skill_md = skill_dir / "SKILL.md"
    if skill_md.exists():
        try:
            for line in skill_md.read_text(encoding="utf-8", errors="replace").splitlines()[:40]:
                if "SEED STATUS:" in line:
                    return line.strip()
        except Exception:
            return None
    return None


def suggest_action(role: Role, status_label: str | None, sensitive_hits: list[str], rel_path: str) -> str:
    if role == "production":
        if rel_path.startswith("imported/") or rel_path.startswith("superpowers-raw/") or rel_path.startswith("426345955d8e/") or "/genstore-operation" in rel_path:
            return "move-to-trash"
        if sensitive_hits:
            return "review"
        return "keep"
    if role == "seed":
        if sensitive_hits:
            return "sanitize"
        if not status_label:
            return "label-status"
        return "keep"
    if role == "draft":
        return "review"
    return "ignore"


def scan_tree(root: Path) -> list[SkillEntry]:
    entries: list[SkillEntry] = []
    if not root.exists():
        return entries
    for skill_md in sorted(root.rglob("SKILL.md")):
        role = classify_role(skill_md.parent)
        findings = scan_file(skill_md)
        hits = sorted({f.kind for f in findings})
        rel_path = skill_md.parent.relative_to(root).as_posix()
        entry = SkillEntry(
            rel_path=rel_path,
            role=role,
            has_skill_md=True,
            status_label=read_status_label(skill_md.parent),
            sensitive_hits=hits,
            suggested_action=suggest_action(role, read_status_label(skill_md.parent), hits, rel_path),
            title=extract_title(skill_md),
        )
        entries.append(entry)
    return entries


def entries_to_json(entries: list[SkillEntry]) -> dict:
    return {"entries": [asdict(e) for e in entries]}


def entries_to_markdown(entries: list[SkillEntry]) -> str:
    lines = []
    for e in entries:
        hits = ", ".join(e.sensitive_hits) if e.sensitive_hits else "-"
        lines.append(f"- `{e.rel_path}` | role={e.role} | status={e.status_label or '-'} | hits={hits} | action={e.suggested_action}")
    return "\n".join(lines) + ("\n" if lines else "")
