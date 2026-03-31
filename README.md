# autoskill-agentsmd-skillbank

A governance-first reference repository for retrieval-led SkillBank usage.

This repo demonstrates how to:

- keep a small, deterministic DocIndex in `AGENTS.md`
- separate production skills from seed/source material
- validate and review skills before promotion
- retire bad examples without losing traceability

It is **not** positioned as a bulk auto-promotion pipeline for turning arbitrary seeds into production skills.
Legacy pipeline scripts are retained only under `scripts/_legacy/` for historical reference.

## Start here

If you only read three things, read these in order:

1. `docs/migration-notes-2026-03-31.md` — what changed and why
2. `SkillBank/README.md` — how to read the current directory model
3. `TECHNICAL_SPEC.md` — the repository rules and routing contract

For the full implementation plan used during the rebuild, see:

- `docs/skillbank-governance-v2-implementation.md`
- `docs/implementation-checklist.md`

## Current state

The repository has already been pruned away from the old pipeline-first model.
The intended steady-state is now:

- `SkillBank/skills/` = small, trusted production routing surface
- `SkillBank/seed_openclaw_skills/` = small, explicit source-material sample set
- `SkillBank/.trash/` = retired and isolated material kept for traceability
- `scripts/_legacy/` = museum, not highway

## Key idea

> Prefer retrieval-led reasoning over pre-training-led reasoning.

Instead of assuming an agent will correctly trigger hidden skills, keep a small routing table always present.
The agent explores the index, opens the most relevant leaf, and follows the leaf doc.

## Repository layout

```text
SkillBank/
  skills/                  # production-grade leaf skills only
  seed_openclaw_skills/    # small, generic, sanitized seed examples
  drafts/                  # candidates under review
  meta/                    # governance metadata and validation inputs
  .trash/                  # retired/isolated content for traceability
  skill.template.md

scripts/
  build_agents_md_index.py
  review_inventory.py
  validate_production_skills.py
  validate_seed_status.py
  prune_seed_examples.py
  skillbank/
  _legacy/                 # historical pipeline scripts; not recommended

tests/
  test_build_agents_md_index.py
  test_detectors.py
  test_inventory.py
  test_production_validation.py
  test_seed_validation.py
```

## Current governance direction

- Do not treat seeds as production by default
- Do not keep large private/workspace-specific skill archives in the routing surface
- Do not auto-merge or auto-promote aggressively
- Prefer inventory, validation, sanitization, and reviewed promotion

## Common commands

Generate / inject DocIndex:

```bash
python scripts/build_agents_md_index.py --write
```

Generate inventory report:

```bash
python scripts/review_inventory.py --write
```

Validate production tree:

```bash
python scripts/validate_production_skills.py
```

Validate seed status:

```bash
python scripts/validate_seed_status.py
```

Prune seed examples:

```bash
python scripts/prune_seed_examples.py --dry-run
python scripts/prune_seed_examples.py --apply
```

Run tests:

```bash
pytest -q
```

## Notes

- Only `SkillBank/skills/` is indexed into `AGENTS.md`
- Seed material is retained only as small, governed source material
- This repo intentionally favors filesystem retrieval over embedding-based retrieval
