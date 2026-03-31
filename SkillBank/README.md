# SkillBank

SkillBank is the governed workspace skill library.

## Directory roles

- `skills/` — **production-grade skills**
  - Use this for actively maintained, trigger-ready skills.
  - Each skill should have a focused responsibility, clean frontmatter, clear workflow, and minimal ambiguity.

- `seed_openclaw_skills/` — **raw seed skills / source material**
  - Use this as the small intake area for imported, drafted, or partially adapted skills.
  - These entries may be useful, but they are not automatically treated as production quality.
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

## Practical rule

Treat `seed_openclaw_skills/` as the ore mine.
Treat `skills/` as the forged steel.
Don’t confuse the rocks with the sword.
