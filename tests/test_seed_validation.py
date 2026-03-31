from __future__ import annotations

from pathlib import Path

from skillbank.validators import validate_seed_skill


def test_seed_without_status_is_error(tmp_path: Path) -> None:
    skill_dir = tmp_path / "seed-skill"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("# Seed\n", encoding="utf-8")

    result = validate_seed_skill(skill_dir)
    assert any(issue.code == "missing_seed_status" and issue.level == "error" for issue in result.issues)


def test_seed_with_status_sidecar_passes(tmp_path: Path) -> None:
    skill_dir = tmp_path / "seed-skill"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("# Seed\n", encoding="utf-8")
    (skill_dir / "SEED_STATUS.md").write_text("SEED STATUS: RAW\n", encoding="utf-8")

    result = validate_seed_skill(skill_dir)
    assert result.ok
