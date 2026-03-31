# Technical Spec (governance-first)

> Purpose: keep the repo structure, routing surface, and governance workflow aligned.
>
> Repo: https://github.com/lostinheaven-knt/autoskill-agentsmd-skillbank

## 0) Goals

- **Retrieval-led usage**: agent sees a small DocIndex every turn and must **Explore → Expand**
- **Governance-first curation**: production skills must be intentionally reviewed, not bulk-promoted by default
- **Token efficiency**: only `SkillBank/skills/` participates in routing
- **Filesystem-first design**: keep the source of truth on disk; do not depend on embeddings or core patches
- **Traceable cleanup**: retire bad examples by moving them to `.trash/`, not by silently deleting them

## 1) Repository model

### 1.1 `SkillBank/skills/`
- Role: **production-grade, routeable skills only**
- Only this tree is used for DocIndex generation
- Anything in this tree should be trustworthy enough to auto-route to

### 1.2 `SkillBank/seed_openclaw_skills/`
- Role: **small, generic, sanitized seed/source material**
- Seeds are examples and source material, not production routing targets
- Each seed should carry an explicit status label

### 1.3 `SkillBank/drafts/`
- Role: candidates under active review
- Drafts are not indexed

### 1.4 `SkillBank/.trash/`
- Role: retired or isolated content kept for traceability
- Use this for stopgap removals, private examples, TODO-heavy off-shelf content, and legacy artifacts

### 1.5 root `skill-seeds/`
- Role: legacy import source only
- Not part of the recommended steady-state model
- Keep for migration/reference until the repo fully detaches from the old pipeline

## 2) Leaf convention

- A leaf is any directory under `SkillBank/skills/` containing `SKILL.md`
- Leaf path = relative directory path from `SkillBank/skills/`
- Naming prefers lowercase, hyphen-case, stable taxonomy-aligned paths

## 3) DocIndex in `AGENTS.md`

### 3.1 Markers
`AGENTS.md` must contain:

- `<!-- SKILLBANK_INDEX:START -->`
- `<!-- SKILLBANK_INDEX:END -->`

### 3.2 Header
Inside the block:

1. `[SkillBank Index]|root: ./SkillBank/skills`
2. `|IMPORTANT: Prefer retrieval-led reasoning over pre-training-led reasoning`
3. `|Workflow: Explore this index -> choose a leaf path -> open the leaf doc (SKILL.md) -> follow it. Index is navigation only.`

### 3.3 Index rules
- One leaf per line
- Paths only, no filename
- Deterministic sort
- **Only production leaves are indexed**

## 4) Runtime behavior protocol

- Always: **Explore → Expand**
- Never: implement from the index alone
- Expand one most relevant leaf first, then branch only if needed

## 5) Governance workflow

Recommended path:

1. Capture/import rough material into `seed_openclaw_skills/`
2. Label seed status explicitly
3. Run inventory / validation / sanitization checks
4. Refine into `drafts/` only when active work is happening
5. Promote into `skills/` only after review
6. Rebuild DocIndex

## 6) Explicit non-goals for the current model

The repo should **not** default to:

- bulk seed import into production
- LLM auto-fill as a promotion substitute
- automatic canonical merge of similar skills
- keeping large private/workspace-specific archives in the production surface

Legacy scripts may still exist under `scripts/_legacy/`, but they are reference-only.

## 7) Validation expectations

### 7.1 Production
Production validation should flag:

- bad demo paths (`imported`, `superpowers-raw`, random opaque prefixes, private product-specific paths)
- TODO-heavy content
- sensitive/private signals in routeable content

### 7.2 Seed
Seed validation should flag:

- missing `SEED STATUS`
- sensitive-like content without `SENSITIVE`
- ambiguous raw material that can be mistaken for production

## 8) Definition of Done

A governed state should satisfy:

- `AGENTS.md` indexes only production leaves
- `SkillBank/skills/` remains small and trustworthy
- `SkillBank/seed_openclaw_skills/` remains small and explicitly labeled
- `.trash/` preserves cleanup traceability
- legacy scripts are isolated under `scripts/_legacy/`
- tests cover index determinism and basic governance checks
