# Install / Test (workspace_tester)

This repo is designed to be used with **minimal OpenClaw core embedding**.

We enforce a strong constraint for token efficiency and determinism:

- Runtime should rely on **AGENTS.md DocIndex (explore→expand)**
- The original OpenClaw `skills/` directory should be **empty (or curated-only)**
- All original skills are migrated into a **read-only seed store** (`skill-seeds/`) and are **not loaded** by default

> IMPORTANT: **Do NOT run this on your main workspace**.
> Use a dedicated test workspace (recommended: `~/.openclaw/workspace_tester`).

---

## Concepts

- **skill-seeds/**: read-only archive of original skills (full directories preserved). Never modified by evolution.
- **SkillBank/skills/**: curated leaves used by the agent via DocIndex.
- **OpenClaw workspace skills/**: should be empty/curated-only to avoid double-loading and token bloat.

---

## Prerequisites

- Python 3.10+
- OpenClaw installed
- This repository cloned somewhere on disk

---

## Quick start (dry-run)

```bash
python scripts/install_into_openclaw_workspace.py \
  --workspace ~/.openclaw/workspace_tester \
  --seeds-from ~/.openclaw/workspace/skills \
  --dry-run
```

---

## Install into a test workspace

### 1) Create / prepare a dedicated workspace

We recommend:

- `~/.openclaw/workspace_tester`

The installer will create it if missing.

### 2) Run installer (moves skills into seeds; empties runtime skills)

```bash
python scripts/install_into_openclaw_workspace.py \
  --workspace ~/.openclaw/workspace_tester \
  --seeds-from ~/.openclaw/workspace/skills
```

This will:

- Copy `--seeds-from` (full skill directories) into:
  - `<repo>/skill-seeds/openclaw-workspace-skills/`
- Ensure `<workspace>/skills/` exists and is empty (curated-only by default)
- Write/update `<workspace>/AGENTS.md` and inject this repo’s DocIndex block

---

## Rollback

Rollback is simply:

- restore a full `skills/` directory into the target workspace
- remove or ignore the DocIndex block in the workspace AGENTS.md

A future version may include `--rollback` automation.

---

## Safety notes

- The installer **requires** `--workspace` and will refuse to run without it.
- Use `--dry-run` first.
- Never point `--workspace` at your production workspace unless you intentionally want to switch it over.
