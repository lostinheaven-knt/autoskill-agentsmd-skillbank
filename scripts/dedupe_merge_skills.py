#!/usr/bin/env python3
"""Deduplicate + merge promoted skills into stronger canonical leaves.

Goal:
- Reduce redundant leaves (same/similar functionality) in SkillBank/skills.
- Auto-merge the best parts into a canonical leaf.
- Do NOT depend on source seed directory priority.
- Do NOT merge TODO placeholders.

Strategy (v0):
- Group leaves by a coarse fingerprint (normalized title + key tokens from Purpose/Procedure).
- Within a group, pick a canonical leaf by a simple quality score.
- Merge in missing bullets/steps/examples from other leaves, de-duplicated.
- Move non-canonical leaves to SkillBank/drafts/_merged/<group_id>/... (for traceability).

This script is deterministic and safe:
- By default: --print only.
- With --apply: writes canonical SKILL.md changes and moves merged leaves.

"""

from __future__ import annotations

import argparse
import hashlib
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO_ROOT / "SkillBank" / "skills"
MERGED_ROOT = REPO_ROOT / "SkillBank" / "drafts" / "_merged"

SECTION_ORDER = [
    "Purpose",
    "When to use",
    "When NOT to use",
    "Inputs / Preconditions",
    "Procedure",
    "Checks",
    "Failure modes",
    "Examples",
    "Version / Changelog",
]

STOPWORDS = {
    "the","a","an","and","or","to","of","in","on","for","with","by","as","is","are","be","this","that",
    "you","your","it","we","our","from","at","into","then","if","else","do","does","did","can","should",
}


def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def write_text(p: Path, text: str) -> None:
    p.write_text(text, encoding="utf-8")


def norm_ws(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def extract_title(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return norm_ws(line[2:]) or "Untitled"
    return "Untitled"


def section_body(text: str, section: str) -> str:
    pat = re.compile(r"^##\s+" + re.escape(section) + r"\s*$", re.IGNORECASE | re.MULTILINE)
    m = pat.search(text)
    if not m:
        return ""
    start = m.end()
    m2 = re.search(r"^##\s+.+$", text[start:], flags=re.MULTILINE)
    end = start + (m2.start() if m2 else len(text[start:]))
    return text[start:end].strip("\n")


def tokenize(s: str) -> List[str]:
    s = s.lower()
    s = re.sub(r"[^a-z0-9\s\-_/]", " ", s)
    toks = [t for t in re.split(r"\s+", s) if t and t not in STOPWORDS]
    return toks


def is_todo_line(line: str) -> bool:
    return "todo" in line.lower()


def bullets(body: str) -> List[str]:
    out = []
    for line in body.splitlines():
        m = re.match(r"^\s*-\s+(.+)$", line)
        if m:
            txt = norm_ws(m.group(1))
            if txt:
                out.append(txt)
    return out


def numbered_steps(body: str) -> List[str]:
    out=[]
    for line in body.splitlines():
        m=re.match(r"^\s*\d+\.\s+(.+)$", line)
        if m:
            txt=norm_ws(m.group(1))
            if txt:
                out.append(txt)
    return out


def dedup_preserve(seq: Iterable[str]) -> List[str]:
    seen=set()
    out=[]
    for x in seq:
        k=x.lower()
        if k in seen:
            continue
        seen.add(k)
        out.append(x)
    return out


def render_section_bullets(items: List[str]) -> str:
    return "\n".join([f"- {x}" for x in items]).strip()


def render_section_steps(items: List[str]) -> str:
    return "\n".join([f"{i+1}. {x}" for i,x in enumerate(items)]).strip()


def render_skill(title: str, sections: Dict[str,str]) -> str:
    lines=[f"# {title}",""]
    for sec in SECTION_ORDER:
        lines.append(f"## {sec}")
        body=sections.get(sec, "").strip("\n")
        if body:
            lines.append(body)
        lines.append("")
    return "\n".join(lines).rstrip()+"\n"


def parse_sections(text: str) -> Dict[str,str]:
    # simplistic: keep bodies for our known sections
    sections={}
    for sec in SECTION_ORDER:
        b=section_body(text, sec)
        if b:
            sections[sec]=b
    return sections


def quality_score(text: str) -> int:
    # higher is better
    score=0
    for sec in SECTION_ORDER:
        if re.search(r"^##\s+"+re.escape(sec)+r"\s*$", text, flags=re.MULTILINE|re.IGNORECASE):
            score += 2
    # fewer TODOs is better
    todos=len([l for l in text.splitlines() if is_todo_line(l)])
    score -= todos
    # more checks and failure modes is better
    score += len(bullets(section_body(text, "Checks")))
    score += len(bullets(section_body(text, "Failure modes")))
    # more concrete steps is better
    score += len(numbered_steps(section_body(text, "Procedure")))
    return score


def fingerprint(text: str) -> str:
    title = extract_title(text).lower()
    toks = tokenize(section_body(text,"Purpose") + "\n" + section_body(text,"Procedure"))
    key = " ".join([title] + toks[:30])
    key = re.sub(r"\s+", " ", key).strip()
    # hash for stable grouping key
    return hashlib.sha1(key.encode("utf-8")).hexdigest()[:12]


def list_leaves() -> List[Path]:
    return sorted({p.parent for p in SKILLS_ROOT.rglob("SKILL.md")})


def merge_into(canon_text: str, other_texts: List[str]) -> Tuple[str, List[str]]:
    notes=[]
    title=extract_title(canon_text)
    sections=parse_sections(canon_text)

    # collect items
    def collect_bullets(sec: str) -> List[str]:
        items = bullets(sections.get(sec, ""))
        for t in other_texts:
            for it in bullets(section_body(t, sec)):
                if is_todo_line(it):
                    continue
                items.append(it)
        items = dedup_preserve(items)
        return items

    def collect_steps() -> List[str]:
        items = numbered_steps(sections.get("Procedure", ""))
        for t in other_texts:
            for it in numbered_steps(section_body(t, "Procedure")):
                if is_todo_line(it):
                    continue
                items.append(it)
        items = dedup_preserve(items)
        return items

    # Merge selected sections
    for sec in ["When to use","When NOT to use","Inputs / Preconditions","Checks","Failure modes"]:
        merged = collect_bullets(sec)
        if merged:
            sections[sec] = render_section_bullets(merged)

    steps = collect_steps()
    if steps:
        sections["Procedure"] = render_section_steps(steps)

    # Examples: treat as bullets to avoid complex headings
    ex_items = []
    ex_body = sections.get("Examples", "")
    if ex_body:
        ex_items.extend([l.strip() for l in ex_body.splitlines() if l.strip()])
    for t in other_texts:
        b = section_body(t, "Examples")
        if b:
            ex_items.extend([l.strip() for l in b.splitlines() if l.strip() and not is_todo_line(l)])
    ex_items = dedup_preserve(ex_items)
    if ex_items:
        sections["Examples"] = "\n".join(ex_items)

    # Changelog: append merged-from note
    v = sections.get("Version / Changelog", "")
    if v:
        v = v.strip() + "\n- merged: auto-dedupe merged similar skills\n"
    else:
        v = "- merged: auto-dedupe merged similar skills"
    sections["Version / Changelog"] = v

    return render_skill(title, sections), notes


def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--min-group", type=int, default=2, help="Only process groups with at least this many leaves")
    args=ap.parse_args()

    leaves=list_leaves()
    groups: Dict[str, List[Path]] = {}
    for d in leaves:
        text=read_text(d/"SKILL.md")
        fp=fingerprint(text)
        groups.setdefault(fp, []).append(d)

    # stable order
    fps = sorted(groups.keys())

    merged_groups=0
    moved=0
    updated=0

    for fp in fps:
        ds = sorted(groups[fp])
        if len(ds) < args.min_group:
            continue

        # choose canonical by quality score, tie-break by path
        scored=[]
        for d in ds:
            t=read_text(d/"SKILL.md")
            scored.append((quality_score(t), d.as_posix(), d))
        scored.sort(reverse=True)
        canon = scored[0][2]
        others = [x[2] for x in scored[1:]]

        canon_text = read_text(canon/"SKILL.md")
        other_texts = [read_text(o/"SKILL.md") for o in others]
        new_text, _ = merge_into(canon_text, other_texts)

        if new_text != canon_text:
            updated += 1
            if args.apply:
                write_text(canon/"SKILL.md", new_text)

        # move others out of curated
        merged_groups += 1
        for o in others:
            rel = o.relative_to(SKILLS_ROOT)
            dst = MERGED_ROOT / fp / rel
            moved += 1
            if args.apply:
                dst.parent.mkdir(parents=True, exist_ok=True)
                if dst.exists():
                    shutil.rmtree(dst)
                shutil.move(str(o), str(dst))

    print({
        "leaves_total": len(leaves),
        "groups_total": len(groups),
        "groups_merged": merged_groups,
        "canon_updated": updated,
        "moved_to_drafts": moved,
    })


if __name__ == "__main__":
    main()
