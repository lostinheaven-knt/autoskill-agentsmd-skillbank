"""Install this repo's DocIndex + SkillBank layout into an OpenClaw workspace.

Design goals:
- Minimal OpenClaw core embedding: operate at the workspace filesystem layer.
- Token efficiency: avoid loading the original workspace skills by default.
- Safety first: explicit --workspace required; support --dry-run.

Actions performed:
1) Seed/archive existing skills into this repo under skill-seeds/ (read-only store)
2) Ensure target workspace skills/ is empty (curated-only by default)
3) Write/update target workspace AGENTS.md with this repo's SkillBank index

NOTE
- This script does NOT modify OpenClaw core.
- This script does NOT alter your production workspace unless you point --workspace to it.
"""

from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path
from typing import List

REPO_ROOT = Path(__file__).resolve().parents[1]

INDEX_START = "<!-- SKILLBANK_INDEX:START -->"
INDEX_END = "<!-- SKILLBANK_INDEX:END -->"


def eprint(msg: str) -> None:
    print(msg)


def run_plan(plan: List[str], dry_run: bool) -> None:
    for line in plan:
        eprint(line)
    if dry_run:
        eprint("\n[dry-run] No changes were made.")


def ensure_dir(p: Path, dry_run: bool, plan: List[str]) -> None:
    if p.exists():
        return
    plan.append(f"mkdir -p {p}")
    if not dry_run:
        p.mkdir(parents=True, exist_ok=True)


def clear_dir(p: Path, dry_run: bool, plan: List[str]) -> None:
    if not p.exists():
        return
    # Remove contents but keep directory
    for child in p.iterdir():
        plan.append(f"rm -rf {child}")
        if not dry_run:
            if child.is_dir() and not child.is_symlink():
                shutil.rmtree(child)
            else:
                child.unlink(missing_ok=True)


def copy_tree(src: Path, dst: Path, dry_run: bool, plan: List[str]) -> None:
    plan.append(f"copy {src} -> {dst}")
    if dry_run:
        return
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst, symlinks=True)


def build_index_text(skills_root: Path) -> str:
    """Build a compressed index text (same format as scripts/build_agents_md_index.py v0.2).

    Format:
      |<section_path>:{<leaf1>,<leaf2>,...}

    where each leaf is a directory containing SKILL.md and leaf1 is the last path
    segment under the section.
    """
    leaf_paths = set()
    if skills_root.exists():
        for p in skills_root.rglob("SKILL.md"):
            if p.is_file():
                rel = p.parent.relative_to(skills_root).as_posix()
                leaf_paths.add(rel)

    # compress leaf paths -> section:{leaf,...}
    groups = {}
    for lp in sorted(leaf_paths):
        parts = [x for x in lp.split("/") if x]
        if not parts:
            continue
        if len(parts) == 1:
            section, leaf = "root", parts[0]
        else:
            section, leaf = "/".join(parts[:-1]), parts[-1]
        groups.setdefault(section, set()).add(leaf)

    lines = [
        "[SkillBank Index]|root: ./SkillBank/skills",
        "|IMPORTANT: Prefer retrieval-led reasoning over pre-training-led reasoning",
        "|Workflow: Explore this index -> choose a path -> open the leaf doc (SKILL.md) -> follow it. Index is navigation only.",
    ]
    for section in sorted(groups.keys()):
        leaves = ",".join(sorted(groups[section]))
        lines.append(f"|{section}:{{{leaves}}}")
    return "\n".join(lines) + "\n"


def inject_agents_md(agents_md_path: Path, index_text: str, dry_run: bool, plan: List[str]) -> None:
    content = agents_md_path.read_text(encoding="utf-8") if agents_md_path.exists() else ""

    if INDEX_START in content and INDEX_END in content:
        pre, rest = content.split(INDEX_START, 1)
        _, post = rest.split(INDEX_END, 1)
        new_content = pre + INDEX_START + "\n" + index_text + INDEX_END + post
    else:
        # minimal header
        header = (
            "# AGENTS.md\n\n"
            "IMPORTANT: Prefer retrieval-led reasoning over pre-training-led reasoning.\n\n"
            "Workflow (strict):\n"
            "1) Explore the SkillBank Index below.\n"
            "2) Choose the most relevant leaf path.\n"
            "3) Expand the leaf by opening: `./SkillBank/skills/<leaf_path>/SKILL.md`\n"
            "4) Follow the leaf doc. The index is navigation only.\n\n"
        )
        base = content.strip() + "\n\n" if content.strip() else header
        new_content = base + INDEX_START + "\n" + index_text + INDEX_END + "\n"

    plan.append(f"write {agents_md_path} (inject DocIndex)")
    if not dry_run:
        agents_md_path.write_text(new_content, encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", required=True, help="Target OpenClaw workspace path (e.g. ~/.openclaw/workspace_tester)")
    ap.add_argument("--seeds-from", required=True, help="Source skills directory to archive into skill-seeds (e.g. ~/.openclaw/workspace/skills)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    workspace = Path(os.path.expanduser(args.workspace)).resolve()
    seeds_from = Path(os.path.expanduser(args.seeds_from)).resolve()

    # Safety checks
    if not seeds_from.exists() or not seeds_from.is_dir():
        raise SystemExit(f"--seeds-from must be an existing directory: {seeds_from}")

    # Explicitly discourage using production workspace by name
    if workspace.as_posix().endswith("/workspace"):
        eprint("ERROR: Refusing to run on a workspace path ending with '/workspace'. Use a dedicated test workspace.")
        raise SystemExit(2)

    plan: List[str] = []

    # 1) Ensure workspace structure
    ensure_dir(workspace, args.dry_run, plan)
    ensure_dir(workspace / "skills", args.dry_run, plan)

    # 2) Archive seeds into repo
    seeds_dst = REPO_ROOT / "skill-seeds" / "openclaw-workspace-skills"
    ensure_dir(seeds_dst.parent, args.dry_run, plan)
    copy_tree(seeds_from, seeds_dst, args.dry_run, plan)

    # 3) Empty runtime skills in target workspace
    plan.append(f"clear {workspace / 'skills'} (token-saving; curated-only)")
    if not args.dry_run:
        clear_dir(workspace / "skills", False, [])

    # 4) Prepare SkillBank in target workspace by copying this repo's SkillBank (optional but practical)
    src_skillbank = REPO_ROOT / "SkillBank"
    dst_skillbank = workspace / "SkillBank"
    copy_tree(src_skillbank, dst_skillbank, args.dry_run, plan)

    # 5) Inject AGENTS.md index (based on target workspace SkillBank)
    index_text = build_index_text(dst_skillbank / "skills")
    inject_agents_md(workspace / "AGENTS.md", index_text, args.dry_run, plan)

    run_plan(plan, args.dry_run)


if __name__ == "__main__":
    main()
