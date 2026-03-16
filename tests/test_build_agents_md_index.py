import subprocess
from pathlib import Path


def test_build_index_deterministic(tmp_path: Path):
    # Create a fake SkillBank structure
    root = tmp_path / "SkillBank" / "skills"
    (root / "debugging" / "first-15-min").mkdir(parents=True)
    (root / "coding" / "refactor" / "safe-refactor").mkdir(parents=True)

    (root / "debugging" / "first-15-min" / "SKILL.md").write_text("# a\n", encoding="utf-8")
    (root / "coding" / "refactor" / "safe-refactor" / "SKILL.md").write_text("# b\n", encoding="utf-8")

    script = Path(__file__).resolve().parents[1] / "scripts" / "build_agents_md_index.py"

    def run() -> str:
        r = subprocess.run(
            ["python", str(script), "--root", str(root), "--print"],
            check=True,
            capture_output=True,
            text=True,
        )
        return r.stdout

    out1 = run()
    out2 = run()
    assert out1 == out2
    assert "|coding/refactor/safe-refactor" in out1
    assert "|debugging/first-15-min" in out1
