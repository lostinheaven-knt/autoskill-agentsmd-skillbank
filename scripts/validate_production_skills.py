#!/usr/bin/env python3
from __future__ import annotations

from skillbank.paths import skills_root
from skillbank.validators import validate_production_skill


def main() -> int:
    root = skills_root()
    errors = 0
    warnings = 0
    for skill_md in sorted(root.rglob("SKILL.md")):
        skill_dir = skill_md.parent
        result = validate_production_skill(skill_dir)
        rel = skill_dir.relative_to(root).as_posix()
        if result.issues:
            print(f"[{rel}]")
            for issue in result.issues:
                print(f"  - {issue.level}: {issue.code}: {issue.message}")
                if issue.level == "error":
                    errors += 1
                elif issue.level == "warn":
                    warnings += 1
    if errors == 0 and warnings == 0:
        print("production validation passed")
    else:
        print(f"production validation finished: {errors} error(s), {warnings} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
