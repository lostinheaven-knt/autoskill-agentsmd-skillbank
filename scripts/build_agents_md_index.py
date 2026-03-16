"""Build a deterministic SkillBank DocIndex block for AGENTS.md.

Spec v0.1 (consolidated):
- root: ./SkillBank/skills
- A leaf is any directory containing a file named SKILL.md
- Index lines are **one leaf per line** (paths only; no filename / no {...})
- Inject between markers in AGENTS.md:
    <!-- SKILLBANK_INDEX:START -->
    <!-- SKILLBANK_INDEX:END -->

Index format:

    [SkillBank Index]|root: ./SkillBank/skills
    |IMPORTANT: Prefer retrieval-led reasoning over pre-training-led reasoning
    |Workflow: Explore this index -> choose a leaf path -> open the leaf doc (SKILL.md) -> follow it. Index is navigation only.
    |<leaf_path>

Conventions:
- Expanding a leaf means opening:
    <root>/<leaf_path>/SKILL.md
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, List, Set, Tuple

START = "<!-- SKILLBANK_INDEX:START -->"
END = "<!-- SKILLBANK_INDEX:END -->"

HEADER_LINES = [
    "[SkillBank Index]|root: ./SkillBank/skills",
    "|IMPORTANT: Prefer retrieval-led reasoning over pre-training-led reasoning",
    "|Workflow: Explore this index -> choose a leaf path -> open the leaf doc (SKILL.md) -> follow it. Index is navigation only.",
]


def find_leaf_paths(root: Path) -> List[str]:
    """Return leaf paths relative to root, using POSIX separators."""
    if not root.exists():
        return []
    leaf_dirs: Set[str] = set()
    for p in root.rglob("SKILL.md"):
        if p.is_file():
            leaf_dirs.add(p.parent.relative_to(root).as_posix())
    return sorted(leaf_dirs)


def build_index_text(leaf_paths: Iterable[str]) -> str:
    lines = list(HEADER_LINES)
    for lp in sorted(set(leaf_paths)):
        lines.append(f"|{lp}")
    return "\n".join(lines) + "\n"


def inject_into_agents_md(agents_md: Path, index_text: str) -> Tuple[str, bool]:
    """Return updated content and whether markers were found."""
    content = agents_md.read_text(encoding="utf-8")

    if START in content and END in content:
        pre, rest = content.split(START, 1)
        _mid, post = rest.split(END, 1)
        new_content = pre + START + "\n" + index_text + END + post
        return new_content, True

    # If missing markers, append at end.
    new_block = f"\n\n{START}\n{index_text}{END}\n"
    return content + new_block, False


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="SkillBank/skills", help="SkillBank skills root")
    ap.add_argument("--agents", default="AGENTS.md", help="Path to AGENTS.md")
    ap.add_argument("--write", action="store_true", help="Write changes to AGENTS.md")
    ap.add_argument("--print", action="store_true", help="Print generated index to stdout")
    args = ap.parse_args()

    root = Path(args.root)
    agents = Path(args.agents)

    leaf_paths = find_leaf_paths(root)
    index_text = build_index_text(leaf_paths)

    if args.print and not args.write:
        print(index_text, end="")
        return

    if args.write:
        updated, had_markers = inject_into_agents_md(agents, index_text)
        agents.write_text(updated, encoding="utf-8")
        if had_markers:
            print(f"Updated index in {agents}")
        else:
            print(f"Appended index block to {agents} (markers were missing)")


if __name__ == "__main__":
    main()
