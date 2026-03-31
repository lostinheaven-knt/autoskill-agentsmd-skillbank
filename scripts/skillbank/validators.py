from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from skillbank.detectors import scan_file


@dataclass
class ValidationIssue:
    level: str
    code: str
    message: str


@dataclass
class ValidationResult:
    ok: bool
    issues: list[ValidationIssue]


def _read_seed_status(skill_dir: Path) -> str:
    sidecar = skill_dir / "SEED_STATUS.md"
    if sidecar.exists():
        return sidecar.read_text(encoding="utf-8", errors="replace")
    skill_md = skill_dir / "SKILL.md"
    if skill_md.exists():
        return skill_md.read_text(encoding="utf-8", errors="replace")
    return ""


def validate_production_skill(skill_dir: Path) -> ValidationResult:
    issues: list[ValidationIssue] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        issues.append(ValidationIssue("error", "missing_skill_md", "SKILL.md not found"))
        return ValidationResult(False, issues)
    text = skill_md.read_text(encoding="utf-8", errors="replace")
    if "TODO" in text:
        issues.append(ValidationIssue("warn", "todo_present", "TODO placeholder present"))
    findings = scan_file(skill_md)
    if findings:
        issues.append(ValidationIssue("warn", "sensitive_signals", f"sensitive-like signals: {', '.join(sorted({f.kind for f in findings}))}"))
    rel = skill_dir.as_posix()
    bad_markers = ["/imported/", "/superpowers-raw/", "genstore-operation", "/426345955d8e/"]
    if any(marker in rel for marker in bad_markers):
        issues.append(ValidationIssue("error", "bad_path_pattern", f"path looks like bad demo pattern: {rel}"))
    return ValidationResult(not any(i.level == 'error' for i in issues), issues)


def validate_seed_skill(skill_dir: Path) -> ValidationResult:
    issues: list[ValidationIssue] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        issues.append(ValidationIssue("error", "missing_skill_md", "SKILL.md not found"))
        return ValidationResult(False, issues)
    text = _read_seed_status(skill_dir)
    if "SEED STATUS:" not in text:
        issues.append(ValidationIssue("error", "missing_seed_status", "SEED STATUS label not found"))
    findings = scan_file(skill_md)
    if findings and "SEED STATUS: SENSITIVE" not in text:
        issues.append(ValidationIssue("warn", "sensitive_unlabeled", "sensitive-like signals found but seed is not labeled SENSITIVE"))
    return ValidationResult(not any(i.level == 'error' for i in issues), issues)
