from __future__ import annotations

from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def skillbank_root() -> Path:
    return repo_root() / "SkillBank"


def skills_root() -> Path:
    return skillbank_root() / "skills"


def seed_root() -> Path:
    return skillbank_root() / "seed_openclaw_skills"


def drafts_root() -> Path:
    return skillbank_root() / "drafts"


def trash_root() -> Path:
    return skillbank_root() / ".trash"


def meta_root() -> Path:
    return skillbank_root() / "meta"


def reports_root() -> Path:
    return repo_root() / "reports"
