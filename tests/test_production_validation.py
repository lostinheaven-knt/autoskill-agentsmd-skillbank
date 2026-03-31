from __future__ import annotations

import subprocess
from pathlib import Path

from skillbank.validators import validate_production_skill

ROOT = Path(__file__).resolve().parents[1]


def test_validate_production_cli_passes() -> None:
    result = subprocess.run(
        ["python", "scripts/validate_production_skills.py"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_bad_demo_path_is_error(tmp_path: Path) -> None:
    skill_dir = tmp_path / "imported" / "legacy-skill"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("# Legacy\n", encoding="utf-8")

    result = validate_production_skill(skill_dir)
    assert any(issue.code == "bad_path_pattern" and issue.level == "error" for issue in result.issues)
