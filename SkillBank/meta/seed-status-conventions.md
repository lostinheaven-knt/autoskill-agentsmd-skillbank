# Seed Skill Status Conventions

Use these labels inside `seed_openclaw_skills/` to make raw-material status obvious.

## Status labels

### `SEED STATUS: PROMOTED`
Use when a production-grade replacement already exists under `SkillBank/skills/`.

Meaning:
- this seed file is retained as source material / historical reference
- use the production-grade version for active routing and maintenance

Recommended note should include:
- the production path
- a short reminder not to keep editing the seed version unless harvesting material

### `SEED STATUS: INCOMPLETE`
Use when the seed file still contains TODOs, unresolved structure, or unfinished content.

Meaning:
- do not treat this as production-ready
- do not rely on it for routing without further cleanup

### `SEED STATUS: RAW`
Use when the seed is useful source material but has not yet been promoted and is not obviously broken.

Meaning:
- usable as reference material
- not yet production-grade

### `SEED STATUS: SENSITIVE`
Optional extra warning when the seed contains environment-coupled examples, identity-specific defaults, or deployment-specific details that should be sanitized before promotion.

## Practical rule

A seed skill should make it obvious whether it is:
- raw material
- incomplete
- promoted/replaced
- sensitive and needing sanitization

If a reader can mistake seed ore for forged steel, the status label is not prominent enough.
