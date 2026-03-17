#!/usr/bin/env python3
"""LLM fill for draft SKILL.md files.

Purpose
- Convert scaffolded drafts (template + TODOs) into minimally-complete, promotable skills.
- Prefer extracting from the preserved original draft appendix when available.
- Avoid inventing unsafe operational details.

Inputs
- Draft files under SkillBank/drafts/**/SKILL.md

Behavior
- If a draft is TODO-heavy, attempt to fill the template sections using:
  A) Appendix: Original draft (verbatim), if present
  B) Otherwise the current content
- Writes back to the same SKILL.md (drafts only) when --apply.
- Keeps the original appendix as-is for traceability.

Configuration (env)
- OPENAI_API_KEY (required)
- OPENAI_BASE_URL (optional)
- OPENAI_MODEL (optional, default gpt-4o-mini)

Safety
- The model is instructed to avoid claiming API integrations or access.
- The output must be concise and concrete (checkable steps, failure modes).

Usage
  python scripts/llm_fill_drafts.py --apply
  python scripts/llm_fill_drafts.py --limit 10 --apply
  python scripts/llm_fill_drafts.py --only openclaw-agents-skills/social-content-generator-0.1.0
"""

from __future__ import annotations

import argparse
import json
import os
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from openai import OpenAI

REPO_ROOT = Path(__file__).resolve().parents[1]
DRAFTS_ROOT = REPO_ROOT / "SkillBank" / "drafts"

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


@dataclass
class FillResult:
    path: str
    changed: bool
    notes: List[str]


def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def write_text(p: Path, s: str) -> None:
    p.write_text(s, encoding="utf-8")


def extract_title(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip() or "Untitled Skill"
    return "Untitled Skill"


def section_body(text: str, section: str) -> str:
    pat = re.compile(r"^##\s+" + re.escape(section) + r"\s*$", re.IGNORECASE | re.MULTILINE)
    m = pat.search(text)
    if not m:
        return ""
    start = m.end()
    m2 = re.search(r"^##\s+.+$", text[start:], flags=re.MULTILINE)
    end = start + (m2.start() if m2 else len(text[start:]))
    return text[start:end].strip("\n")


def parse_sections(text: str) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for sec in SECTION_ORDER:
        b = section_body(text, sec)
        if b:
            out[sec] = b
    return out


def render_skill(title: str, sections: Dict[str, str]) -> str:
    lines = [f"# {title}", ""]
    for sec in SECTION_ORDER:
        lines.append(f"## {sec}")
        body = sections.get(sec, "").strip("\n")
        if body:
            lines.append(body)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def find_original_appendix(text: str) -> Optional[str]:
    m = re.search(
        r"<!--\s*ORIGINAL_DRAFT_PRESERVED:START\s*-->.*?```markdown\n(.*?)\n```.*?<!--\s*ORIGINAL_DRAFT_PRESERVED:END\s*-->",
        text,
        flags=re.DOTALL,
    )
    if not m:
        return None
    return m.group(1).strip("\n")


def todo_metrics(text: str) -> Tuple[int, float, int]:
    """Return (todo_lines, todo_ratio, content_lines) for main body only."""
    in_fence = False
    todo = 0
    content = 0
    for ln in text.splitlines():
        if ln.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        s = ln.strip()
        if not s or s.startswith("#") or s.startswith("<!--"):
            continue
        content += 1
        if "todo" in s.lower():
            todo += 1
    ratio = todo / max(1, content)
    return todo, ratio, content


def needs_fill(text: str) -> bool:
    todo, ratio, _ = todo_metrics(text)
    return todo >= 5 or ratio > 0.15


def mk_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY missing; cannot run LLM fill")
    base_url = os.getenv("OPENAI_BASE_URL")
    if base_url:
        return OpenAI(api_key=api_key, base_url=base_url)
    return OpenAI(api_key=api_key)


def call_llm(client: OpenAI, model: str, title: str, draft_text: str, original: Optional[str]) -> Dict[str, str]:
    """Return dict(section->body) with NO TODO placeholders."""

    schema = {
        "type": "object",
        "properties": {sec: {"type": "string"} for sec in SECTION_ORDER},
        "required": SECTION_ORDER,
        "additionalProperties": False,
    }

    system = (
        "You are an expert skill author.\n"
        "Your job: fill a SkillBank SKILL.md template with concrete, checkable content.\n"
        "Rules:\n"
        "- Do NOT include the word 'TODO' anywhere.\n"
        "- Do NOT claim you have access to tools/APIs/integrations. Write steps as what the assistant should do conversationally.\n"
        "- Keep it short but non-empty: each required section must have meaningful content.\n"
        "- Procedure: 3-7 numbered steps.\n"
        "- Checks / Failure modes: at least 2 bullets each.\n"
        "- If original draft content is provided, prefer extracting and summarizing it rather than inventing.\n"
    )

    user_payload = {
        "title": title,
        "draft_template": draft_text,
        "original_draft": original or "",
        "output_instructions": {
            "format": "json",
            "schema": schema,
        },
    }

    resp = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": system},
            {"role": "user", "content": json.dumps(user_payload, ensure_ascii=False)},
        ],
        response_format={"type": "json_schema", "json_schema": {"name": "skill_sections", "schema": schema}},
    )

    # OpenAI Responses API returns output_text with JSON when using json_schema
    txt = resp.output_text
    data = json.loads(txt)

    # hard guard
    for k, v in data.items():
        if "todo" in v.lower():
            raise ValueError(f"LLM returned TODO in section {k}")

    return {k: data[k].strip("\n") for k in SECTION_ORDER}


def iter_draft_skill_md() -> List[Path]:
    return sorted(DRAFTS_ROOT.rglob("SKILL.md"))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--limit", type=int, default=0, help="Process at most N files (0 = no limit)")
    ap.add_argument(
        "--only",
        type=str,
        default="",
        help="Only process a relative path under SkillBank/drafts (e.g. openclaw-agents-skills/social-content-generator-0.1.0)",
    )
    ap.add_argument("--sleep", type=float, default=0.4, help="Sleep between calls (seconds)")
    args = ap.parse_args()

    client = mk_client()
    model = os.getenv("OPENAI_MODEL") or "gpt-4o-mini"

    files = iter_draft_skill_md()
    if args.only:
        root = (DRAFTS_ROOT / args.only).resolve()
        files = [root / "SKILL.md"]

    n = 0
    results: List[FillResult] = []

    for p in files:
        if not p.exists():
            continue
        text = read_text(p)
        if not needs_fill(text):
            results.append(FillResult(str(p), False, ["skip: already good"]))
            continue

        title = extract_title(text)
        original = find_original_appendix(text)

        sections = call_llm(client, model, title, text, original)

        # preserve appendix (if any) by taking everything from ORIGINAL_DRAFT_PRESERVED:START onwards
        appendix = ""
        m = re.search(r"(<!--\s*ORIGINAL_DRAFT_PRESERVED:START\s*-->.*)$", text, flags=re.DOTALL)
        if m:
            appendix = "\n\n" + m.group(1).rstrip() + "\n"

        new_text = render_skill(title, sections).rstrip() + (appendix or "")
        changed = new_text != text
        if changed and args.apply:
            write_text(p, new_text)

        results.append(FillResult(str(p), changed, ["filled by LLM"]))
        n += 1
        if args.limit and n >= args.limit:
            break
        time.sleep(args.sleep)

    changed = sum(1 for r in results if r.changed)
    print(f"processed: {len(results)}")
    print(f"changed: {changed}")


if __name__ == "__main__":
    main()
