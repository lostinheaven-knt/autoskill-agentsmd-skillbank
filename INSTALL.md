# Install / Test (workspace_tester)

This repo is designed to be used with **minimal OpenClaw core embedding**.

We enforce a strong constraint for token efficiency and determinism:

- Runtime should rely on **AGENTS.md DocIndex (Explore→Expand)**
- The OpenClaw workspace `skills/` directory should be **empty (or curated-only)**
- All original skills are archived into a **read-only seed store** (`skill-seeds/`) and are **not loaded** by default

> IMPORTANT: **Do NOT run this on your main workspace**.
> Use a dedicated test workspace (recommended: `~/.openclaw/workspace_tester`).

---

## Concepts (3-layer model)

- **skill-seeds/**: read-only archive of original skills (full directories preserved). Never modified by evolution. This also serves as the backup.
- **SkillBank/skills/**: curated leaves used by the agent via DocIndex. This is the evolvable source-of-truth.
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

### 2) Run installer twice (two seed sources)

Initial import must **only copy** from these two sources:

- `~/.openclaw/workspace/skills/`
- `~/.openclaw/workspace/.agents/skills/`

#### 2.1 Archive `~/.openclaw/workspace/skills` into seeds

```bash
python scripts/install_into_openclaw_workspace.py \
  --workspace ~/.openclaw/workspace_tester \
  --seeds-from ~/.openclaw/workspace/skills \
  --seeds-name openclaw-workspace-skills
```

#### 2.2 Archive `~/.openclaw/workspace/.agents/skills` into seeds

```bash
python scripts/install_into_openclaw_workspace.py \
  --workspace ~/.openclaw/workspace_tester \
  --seeds-from ~/.openclaw/workspace/.agents/skills \
  --seeds-name openclaw-agents-skills
```

Each run will also:

- Ensure `<workspace>/skills/` exists and is empty (curated-only by default)
- Copy this repo’s `SkillBank/` into `<workspace>/SkillBank/`
- Write/update `<workspace>/AGENTS.md` and inject the DocIndex block

---

## DocIndex format (v0.1)

- One leaf path per line.
- Filenames are omitted by convention.

Expanding a leaf means opening:

- `./SkillBank/skills/<leaf_path>/SKILL.md`

---

## Rollback

Rollback is simply:

- restore a full `skills/` directory into the target workspace
- remove or ignore the DocIndex block in the workspace `AGENTS.md`

A future version may include `--rollback` automation.

---

## Safety notes

- The installer **requires** `--workspace` and will refuse to run without it.
- Use `--dry-run` first.
- Never point `--workspace` at your production workspace unless you intentionally want to switch it over.
