from __future__ import annotations

from pathlib import Path
from typing import Iterable

START = "<!-- SKILLBANK_INDEX:START -->"
END = "<!-- SKILLBANK_INDEX:END -->"

HEADER_LINES = [
    "[SkillBank Index]|root: ./SkillBank/skills",
    "|IMPORTANT: Prefer retrieval-led reasoning over pre-training-led reasoning",
    "|Workflow: Explore this index -> choose a leaf path -> open the leaf doc (SKILL.md) -> follow it. Index is navigation only.",
]


def find_leaf_paths(root: Path) -> list[str]:
    if not root.exists():
        return []
    leaf_dirs = {p.parent.relative_to(root).as_posix() for p in root.rglob("SKILL.md") if p.is_file()}
    return sorted(leaf_dirs)


def build_index_text(leaf_paths: Iterable[str]) -> str:
    lines = list(HEADER_LINES)
    for lp in sorted(set(leaf_paths)):
        lines.append(f"|{lp}")
    return "\n".join(lines) + "\n"


def inject_index(agents_md: Path, index_text: str) -> tuple[str, bool]:
    content = agents_md.read_text(encoding="utf-8")
    if START in content and END in content:
        pre, rest = content.split(START, 1)
        _mid, post = rest.split(END, 1)
        return pre + START + "\n" + index_text + END + post, True
    new_block = f"\n\n{START}\n{index_text}{END}\n"
    return content + new_block, False
