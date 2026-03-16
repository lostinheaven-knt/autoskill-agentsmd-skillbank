# Technical Spec (consolidated)

> Purpose: prevent context loss and spec drift.
>
> Repo: https://github.com/lostinheaven-knt/autoskill-agentsmd-skillbank

## 0) Goals

- **Retrieval-led** usage: agent sees a small DocIndex every turn and must **Explore → Expand**.
- **Token efficiency**: do **not** load the huge original OpenClaw native skills prompt pack.
- **Minimal OpenClaw embedding**: operate at the **workspace filesystem layer**, not by patching OpenClaw core.
- **Evolvable**: AutoSkill pipeline can add/merge/update leaves asynchronously; index is regenerated deterministically.

## 1) Three-layer model (strong constraint)

### 1.1 skill-seeds/ (read-only archive / backup)
- Role: **backup + reference material** for extraction/merge.
- Rule: **never modified by evolution**.
- Source inputs (initial import; COPY ONLY):
  - `~/.openclaw/workspace/skills/`
  - `~/.openclaw/workspace/.agents/skills/`
- Important: seeds are **not indexed** and **not loaded** by OpenClaw runtime by default.

### 1.2 SkillBank/skills/ (curated, evolvable source-of-truth)
- Role: where **curated leaf skills** live and evolve.
- Only this tree is used for DocIndex generation.

### 1.3 OpenClaw workspace `skills/` (runtime loading)
- Role: keep **empty** (or curated-only) to avoid double-loading and token bloat.
- For experiments/testing we use a dedicated workspace:
  - `~/.openclaw/workspace_tester`

## 2) Leaf convention (v0.1)

- A **leaf** is a directory under `SkillBank/skills/`.
- A leaf is discoverable by the presence of **one entry file**:
  - `SKILL.md`
- A leaf path is the classification path:
  - `SkillBank/skills/<goal>/<branch>/<leaf>/SKILL.md`

### Naming
- lowercase a-z0-9, words with `-`, POSIX paths.

## 3) DocIndex in AGENTS.md

### 3.1 Markers
`AGENTS.md` must contain:

- `<!-- SKILLBANK_INDEX:START -->`
- `<!-- SKILLBANK_INDEX:END -->`

Generator replaces content between markers only.

### 3.2 Header (fixed)
Inside the block:

1. `[SkillBank Index]|root: ./SkillBank/skills`
2. `|IMPORTANT: Prefer retrieval-led reasoning over pre-training-led reasoning`
3. `|Workflow: Explore this index -> choose a leaf path -> open the leaf doc (SKILL.md) -> follow it. Index is navigation only.`

### 3.3 Index lines (v0.1)
- **One leaf per line**.
- **Only leaf paths** (no filename, no `{...}`).

Example:

- `|debugging/first-15-min`
- `|coding/refactor/safe-refactor`

### 3.4 Stability
- Deterministic output.
- Sorted lexicographically.

## 4) Runtime behavior protocol (must-follow)

- Always: **Explore → Expand**.
- Never: implement based on index alone.
- Expand strategy: open **one** most relevant leaf first; only expand more on branching.

## 5) Installer contract (tester workspace only)

A Python installer installs into `~/.openclaw/workspace_tester`:

- Copy seeds from the two allowed sources into repo `skill-seeds/`.
- Clear target workspace `skills/` (token-saving).
- Copy repo `SkillBank/` into target workspace `SkillBank/`.
- Inject DocIndex into target workspace `AGENTS.md`.

### Safety
- Must require explicit `--workspace`.
- Must support `--dry-run`.
- Must refuse production-like workspace paths (e.g. ending with `/workspace`).
- Must refuse `--seeds-from` that looks like a workspace/repo tree (contains `AGENTS.md` or `SkillBank/`).
- Must refuse `--seeds-from` inside `--workspace` (avoid self-archiving loops).

## 6) Initialization pipeline (seeds -> drafts -> autofix -> promote -> dedupe/merge)

### 6.1 Why we need a pipeline

Raw seed skills are heterogeneous and often incomplete. The curated SkillBank must be:
- structured (template sections)
- deduplicated (same functionality merged)
- token-efficient (no vendored deps like node_modules)

So initialization is a **batch pipeline**, not manual curation.

### 6.2 Phases

- **Phase A (import):** `skill-seeds/**` → `SkillBank/drafts/` (copy full directories; read-only seeds)
- **Phase B0 (autofix):** normalize `SkillBank/drafts/**/SKILL.md` to match the template (adds minimal TODO placeholders; structure only)
- **Phase B1 (promote):** drafts → curated `SkillBank/skills/` if quality gate passes (after autofix, most drafts should pass)
- **Phase C (dedupe/merge):** automatically merge similar curated leaves:
  - pick the best canonical leaf by a quality score (structure completeness, fewer TODOs, more checks/steps)
  - merge in non-TODO bullets/steps/examples from duplicates
  - move duplicates to `SkillBank/drafts/_merged/<group_id>/...` for traceability

### 6.3 Dedupe/merge rules (current)

- **No seed priority:** canonical selection is based on quality score + deterministic path tiebreak.
- **Never merge TODO:** any bullet/step containing "TODO" is not merged into canonical.
- **More aggressive grouping (v1):**
  1) Tool-domain grouping (github/feishu/pytest/docker/ffmpeg/etc)
  2) Title normalization grouping (strip versions/punctuation; merge near-duplicate titles)

### 6.4 One-command init

```bash
python scripts/pipeline_init.py --apply
```

## 7) Self-check (does DocIndex -> SKILL.md work?)

Run in the target workspace (recommended: `~/.openclaw/workspace_tester`).

### 7.1 Verify every DocIndex leaf path resolves to a real SKILL.md file

```bash
cd ~/.openclaw/workspace_tester
python - <<'PY'
from pathlib import Path

agents = Path('AGENTS.md').read_text(encoding='utf-8').splitlines()
paths=[]
for line in agents:
    if not line.startswith('|'):
        continue
    s=line[1:].strip()
    if not s or s.startswith('IMPORTANT') or s.startswith('Workflow') or s.startswith('[SkillBank Index]'):
        continue
    if '/' in s:
        paths.append(s)

missing=[]
for p in paths:
    f = Path('SkillBank/skills')/p/'SKILL.md'
    if not f.exists():
        missing.append(str(f))

print('leaf_count:', len(paths))
print('missing_count:', len(missing))
if missing:
    print('\n'.join(missing[:50]))
PY
```

Expected:
- `missing_count: 0`

### 7.2 Open a leaf manually

```bash
sed -n '1,80p' SkillBank/skills/github/gh-cli/SKILL.md
```

If both checks pass, the DocIndex routing and leaf expansion path is confirmed working.

## 8) Definition of Done (scaffold)

- Deterministic DocIndex generator.
- Tests covering deterministic output.
- Installer supports `workspace_tester`, `dry-run`, and seed copying from the two sources.
- No vendored dependencies committed (e.g., `node_modules/` under seeds or SkillBank).
