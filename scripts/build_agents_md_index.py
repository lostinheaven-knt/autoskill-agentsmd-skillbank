"""Build a deterministic SkillBank DocIndex block for AGENTS.md.

Governance-first version:
- root: ./SkillBank/skills
- A leaf is any directory containing SKILL.md
- Index lines are one leaf path per line
- Only production leaves are indexed
"""

from __future__ import annotations

import argparse
from pathlib import Path

from skillbank.indexer import build_index_text, find_leaf_paths, inject_index


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
        updated, had_markers = inject_index(agents, index_text)
        agents.write_text(updated, encoding="utf-8")
        if had_markers:
            print(f"Updated index in {agents}")
        else:
            print(f"Appended index block to {agents} (markers were missing)")


if __name__ == "__main__":
    main()
