# SkillBank

SkillBank is the governed skill surface for this repository.

It is **not** a dump of everything the repo has ever seen.
If something is uncertain, private-ish, TODO-heavy, or historically interesting but not routing-worthy, it belongs in `seed_openclaw_skills/`, `drafts/`, or `.trash/` — not in `skills/`.

## Directory roles

- `skills/` — **production-grade skills**
  - Actively maintained, trigger-ready, routing-worthy leaves only.
  - Each skill should have a focused responsibility, clean frontmatter, clear workflow, and minimal ambiguity.

- `seed_openclaw_skills/` — **raw seed skills / source material**
  - Small intake area for imported, drafted, or partially adapted skills.
  - Useful as source material, but not automatically treated as production quality.
  - Keep this set small, generic, and sanitized.

- `drafts/` — candidates under active review
- `meta/` — governance metadata, conventions, validation inputs
- `.trash/` — retired or isolated material kept for traceability

## Production skill standard

A production-grade skill should usually include:

1. frontmatter with a strong `name` and `description`
2. clear trigger boundary
3. a concise core workflow
4. a `Gotchas` or equivalent guardrail section
5. references/scripts/assets only when they add real value
6. a verification path where applicable

For the detailed promotion bar, see:

- `meta/production-skill-checklist.md`

For seed labeling rules, see:

- `meta/seed-status-conventions.md`

## Recommended workflow

1. Capture/import rough material into `seed_openclaw_skills/`
2. Audit and refine the skill
3. Split large detail into `references/` or `scripts/`
4. Promote the cleaned version into `skills/`
5. Keep the production directory small, sharp, and trustworthy

## Indexing

The routing table (DocIndex) is generated and injected into `AGENTS.md` between:

- `<!-- SKILLBANK_INDEX:START -->`
- `<!-- SKILLBANK_INDEX:END -->`

Only `skills/` participates in active routing.

## Practical rule

Treat `seed_openclaw_skills/` as the ore mine.
Treat `skills/` as the forged steel.
Don’t confuse the rocks with the sword.
