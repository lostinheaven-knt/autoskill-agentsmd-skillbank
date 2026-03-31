#!/usr/bin/env python3
"""LEGACY: historical pipeline script.

This file is retained for reference only and is not part of the current governance-first recommended workflow. Prefer the governance helpers under scripts/ and scripts/skillbank/.
"""

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
- Preferred (OpenAI-compatible):
  - OPENAI_API_KEY (or DEEPSEEK_API_KEY)
  - OPENAI_BASE_URL (or DEEPSEEK_BASE_URL)
  - OPENAI_MODEL (or DEEPSEEK_MODEL)

Notes about providers
- DeepSeek exposes an OpenAI-compatible Chat Completions endpoint.
  This script uses chat.completions + JSON output to maximize compatibility.

Usage
  # Option A: export env vars in shell
  python scripts/llm_fill_drafts.py --apply

  # Option B: load from an env file (KEY=VALUE lines)
  python scripts/llm_fill_drafts.py --env-file ~/.openclaw/workspace_tester/.secrets.env --apply

  # Target one skill
  python scripts/llm_fill_drafts.py --env-file ~/.openclaw/workspace_tester/.secrets.env \
    --only openclaw-agents-skills/social-content-generator-0.1.0 --apply
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


def load_env_file(path: str) -> None:
    p = Path(path).expanduser()
    if not p.exists():
        raise SystemExit(f"env file not found: {p}")
    for raw in p.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        if k and k not in os.environ:
            os.environ[k] = v


def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def write_text(p: Path, s: str) -> None:
    p.write_text(s, encoding="utf-8")


def extract_title(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip() or "Untitled Skill"
    return "Untitled Skill"


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


def _env_first(*names: str) -> Optional[str]:
    for n in names:
        v = os.getenv(n)
        if v:
            return v
    return None


def mk_client() -> OpenAI:
    api_key = _env_first("OPENAI_API_KEY", "DEEPSEEK_API_KEY")
    if not api_key:
        raise SystemExit("Missing OPENAI_API_KEY/DEEPSEEK_API_KEY; cannot run LLM fill")

    base_url = _env_first("OPENAI_BASE_URL", "DEEPSEEK_BASE_URL")
    if base_url:
        return OpenAI(api_key=api_key, base_url=base_url)
    return OpenAI(api_key=api_key)


def pick_model() -> str:
    m = _env_first("OPENAI_MODEL", "DEEPSEEK_MODEL")
    if m:
        return m
    if os.getenv("DEEPSEEK_API_KEY") or os.getenv("DEEPSEEK_BASE_URL"):
        return "deepseek-chat"
    return "gpt-4o-mini"


def call_llm(client: OpenAI, model: str, title: str, draft_text: str, original: Optional[str]) -> Dict[str, str]:
    """Return dict(section->body) with NO TODO placeholders.

    Provider note:
    - Some OpenAI-compatible providers may return lists/dicts even in json_object mode.
      We normalize those into markdown-ish strings.
    """

    system = (
        "You are an expert skill author.\n"
        "Fill a SkillBank SKILL.md template with concrete, checkable content.\n"
        "Hard rules:\n"
        "- Output MUST be valid JSON object (no markdown, no code fences).\n"
        "- Keys MUST be exactly: " + ", ".join([f'\"{k}\"' for k in SECTION_ORDER]) + "\n"
        "- Do NOT include the word 'TODO' anywhere.\n"
        "- Do NOT claim you have access to tools/APIs/integrations.\n"
        "- Procedure: 3-7 numbered steps (you may return a list).\n"
        "- Checks and Failure modes: at least 2 bullets each (you may return a list).\n"
        "- Prefer extracting from original draft if provided; otherwise keep content conservative.\n"
    )

    user = {
        "title": title,
        "draft_template": draft_text,
        "original_draft": original or "",
        "output": "Return ONLY the JSON object.",
    }

    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": json.dumps(user, ensure_ascii=False)},
        ],
        response_format={"type": "json_object"},
        temperature=0.2,
    )

    txt = resp.choices[0].message.content
    data = json.loads(txt)

    # validate keys exist
    for k in SECTION_ORDER:
        if k not in data:
            raise ValueError(f"missing key: {k}")
    extra_keys = [k for k in data.keys() if k not in SECTION_ORDER]
    if extra_keys:
        raise ValueError(f"extra keys: {extra_keys}")

    def norm_value(section: str, v) -> str:
        if isinstance(v, str):
            return v.strip("\n")

        if isinstance(v, list):
            items: List[str] = []
            for it in v:
                if it is None:
                    continue
                s = str(it).strip()
                if s:
                    items.append(s)
            if not items:
                return ""
            if section == "Procedure":
                cleaned = []
                for s in items:
                    # avoid double numbering like "1. 1. ..."
                    s2 = re.sub(r"^\s*\d+\.\s+", "", s).strip()
                    cleaned.append(s2 or s)
                return "\n".join([f"{i+1}. {s}" for i, s in enumerate(cleaned)])
            return "\n".join([f"- {s}" for s in items])

        if isinstance(v, dict):
            if section == "Examples":
                out_lines: List[str] = []
                for kk, vv in v.items():
                    kk = str(kk).strip()
                    if not kk:
                        continue
                    out_lines.append(f"### {kk}")
                    if isinstance(vv, dict):
                        for k2, v2 in vv.items():
                            s2 = str(v2).strip()
                            if s2:
                                out_lines.append(f"- {k2}: {s2}")
                    elif isinstance(vv, list):
                        for x in vv:
                            sx = str(x).strip()
                            if sx:
                                out_lines.append(sx)
                    else:
                        s = str(vv).strip()
                        if s:
                            out_lines.append(s)
                    out_lines.append("")
                return "\n".join(out_lines).strip()

            out_lines: List[str] = []
            for kk, vv in v.items():
                kk = str(kk).strip()
                if not kk:
                    continue
                if isinstance(vv, list):
                    out_lines.append(f"- {kk}:")
                    for x in vv:
                        sx = str(x).strip()
                        if sx:
                            out_lines.append(f"  - {sx}")
                else:
                    s = str(vv).strip()
                    if s:
                        out_lines.append(f"- {kk}: {s}")
            return "\n".join(out_lines).strip()

        return str(v).strip()

    out: Dict[str, str] = {}
    for k in SECTION_ORDER:
        out[k] = norm_value(k, data.get(k))

    for k in SECTION_ORDER:
        v = out[k]
        if not isinstance(v, str) or not v.strip():
            raise ValueError(f"empty/invalid value for key: {k}")
        if "todo" in v.lower():
            raise ValueError(f"LLM returned TODO in section {k}")

    return out


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
    ap.add_argument("--env-file", type=str, default="", help="Load env vars from a .env file (KEY=VALUE)")
    args = ap.parse_args()

    if args.env_file:
        load_env_file(args.env_file)

    client = mk_client()
    model = pick_model()

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

        appendix = ""
        m = re.search(r"(<!--\s*ORIGINAL_DRAFT_PRESERVED:START\s*-->.*)$", text, flags=re.DOTALL)
        if m:
            appendix = "\n\n" + m.group(1).rstrip() + "\n"

        new_text = render_skill(title, sections).rstrip() + (appendix or "")
        changed = new_text != text
        if changed and args.apply:
            write_text(p, new_text)

        results.append(FillResult(str(p), changed, [f"filled by LLM ({model})"]))
        n += 1
        if args.limit and n >= args.limit:
            break
        time.sleep(args.sleep)

    changed = sum(1 for r in results if r.changed)
    print(f"processed: {len(results)}")
    print(f"changed: {changed}")


if __name__ == "__main__":
    main()
