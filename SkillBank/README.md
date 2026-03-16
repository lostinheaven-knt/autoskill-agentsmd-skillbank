# SkillBank

This folder stores *leaf skills* as filesystem docs.

- `skills/` contains leaf nodes. Each leaf is a directory containing a single `skill.md`.
- `drafts/` contains candidates that failed the quality gate.
- `meta/` contains machine metadata (versioning, provenance, merge history).

The routing table (DocIndex) is generated and injected into `AGENTS.md` between:

- `<!-- SKILLBANK_INDEX:START -->`
- `<!-- SKILLBANK_INDEX:END -->`
