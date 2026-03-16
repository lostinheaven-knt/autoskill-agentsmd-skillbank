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
- Source inputs (initial import):
  - `~/.openclaw/workspace/skills/`
  - `~/.openclaw/workspace/.agents/skills/`
- Important: seeds are not indexed and not loaded by OpenClaw runtime by default.

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
- **Only leaf paths** (no filename, no `{...}`):

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

## 6) Definition of Done (scaffold)

- Deterministic DocIndex generator.
- Tests covering deterministic output.
- Installer supports `workspace_tester`, `dry-run`, and seed copying from the two sources.
- No vendored dependencies committed (e.g., `node_modules/` under seeds).
