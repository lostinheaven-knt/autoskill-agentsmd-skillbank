# Migration Notes — 2026-03-31

This note records the governance-first rebuild of `autoskill-agentsmd-skillbank` so future maintainers do not have to reverse-engineer intent from a giant diff.

## Why this migration happened

The old repository had drifted into a bad demo state:

- `SkillBank/skills/` mixed production leaves with imported, legacy, private-ish, and TODO-heavy content
- `skill-seeds/` held too many examples, including workspace-specific and potentially sensitive material
- the repo still suggested a pipeline-first worldview: import broadly, auto-fill, auto-promote, auto-merge

That no longer matched the current SkillBank governance direction.

## What changed

### 1) Production routing surface was pruned hard

The routing surface now aims to stay **small and trustworthy**.

Bad demo paths such as these were removed from active production routing and preserved under `.trash/`:

- `imported/...`
- `superpowers-raw/...`
- opaque/random prefixes such as `426345955d8e/...`
- product-specific private material such as `product/genstore/genstore-operation`

Additionally, TODO-heavy pseudo-production leaves were taken off-shelf and moved to `.trash/` instead of being left in `SkillBank/skills/`.

### 2) Seeds were reduced to a small governed sample set

A new directory was established:

- `SkillBank/seed_openclaw_skills/`

This directory is intentionally small. It exists to show what governed seed/source material looks like, not to archive everything.

Each retained seed now carries an explicit `SEED_STATUS` sidecar.

### 3) Governance metadata was added

New files in `SkillBank/meta/` define the new rules of the repo:

- `production-skill-checklist.md`
- `seed-status-conventions.md`
- `retained-seed-allowlist.yml`
- `taxonomy.yml`
- `inventory.schema.json`

These are the reference points for future curation.

### 4) Legacy pipeline scripts were isolated

The previous bulk-pipeline scripts were moved to:

- `scripts/_legacy/`

They are retained for reference only.
They are **not** part of the recommended governance-first workflow.

### 5) Governance helpers and tests were added

New helpers were introduced under:

- `scripts/skillbank/`

And the repo now has baseline governance checks for:

- detectors
- inventory generation
- production validation
- seed validation

## Current intended mental model

Use the repo like this:

- `SkillBank/skills/` = forged steel (small, trusted, routable)
- `SkillBank/seed_openclaw_skills/` = ore (source material with explicit status)
- `SkillBank/drafts/` = current workbench
- `SkillBank/.trash/` = retired/isolated material kept for traceability
- `scripts/_legacy/` = museum, not highway

## What not to do again

Please do **not** drift back into these patterns:

1. bulk-importing external skills directly into `SkillBank/skills/`
2. treating seeds as production by default
3. leaving TODO-heavy scaffolds in the production routing surface
4. mixing private/business-coupled material into demo production leaves
5. restoring legacy pipeline scripts as the default documented workflow

## Rebuilt production leaves kept on purpose

After pruning, a small set of cleaner production leaves was rebuilt intentionally rather than restored blindly.
This includes:

- `ops/feishu/feishu-doc`
- `ops/feishu/feishu-drive`
- `ops/feishu/feishu-perm`
- `ops/feishu/feishu-wiki`
- `media/image/image-read`
- plus existing surviving leaves such as `debugging/first-15-min` and `memory/plugmem-internal`

The idea is simple: start from a small believable surface and expand carefully.

## How to continue from here

Preferred next steps:

1. keep production additions small and reviewed
2. improve validation rules incrementally
3. add tests before broadening the routing surface again
4. prefer moving questionable content to `.trash/` over pretending it is production-ready

## One-line summary

This migration changed the repo from an **auto-promotion experiment** into a **governance-first SkillBank reference**.
