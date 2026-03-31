# autoskill-agentsmd-skillbank

A governance-first reference repository for retrieval-led SkillBank usage.

This repo demonstrates how to:

- keep a small, deterministic DocIndex in `AGENTS.md`
- separate production skills from seed/source material
- validate and review skills before promotion
- retire bad examples without losing traceability

It is **not** positioned as a bulk auto-promotion pipeline for turning arbitrary seeds into production skills.
Legacy pipeline scripts are retained only under `scripts/_legacy/` for historical reference.

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
```

## Current governance direction

- Do not treat seeds as production by default
- Do not keep large private/workspace-specific skill archives in the routing surface
- Do not auto-merge or auto-promote aggressively
- Prefer inventory, validation, sanitization, and reviewed promotion

## Generate / inject DocIndex

```bash
python scripts/build_agents_md_index.py --write
```

Print index only:

```bash
python scripts/build_agents_md_index.py --print
```

## Inventory report

```bash
python scripts/review_inventory.py --write
```

## Validate production tree

```bash
python scripts/validate_production_skills.py
```

## Validate seed status

```bash
python scripts/validate_seed_status.py
```

## Prune seed examples

```bash
python scripts/prune_seed_examples.py --dry-run
python scripts/prune_seed_examples.py --apply
```

## Tests

```bash
pytest -q
```

## Notes

- Only `SkillBank/skills/` is indexed into `AGENTS.md`
- Seed material is retained only as small, governed source material
- This repo intentionally favors filesystem retrieval over embedding-based retrieval
