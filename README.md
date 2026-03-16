# autoskill-agentsmd-skillbank

A minimal, production-oriented blueprint for the “third way”:

- **AutoSkill** handles **skill extraction → maintenance (add/merge/discard) → versioning** (asynchronous, offline).
- **AGENTS.md-style DocIndex** handles **usage**: *Explore index → Expand leaf docs*.

This repo focuses on the **DocIndex + leaf SkillBank filesystem layout** (no embeddings, no vector DB).

## Key idea
> **Prefer retrieval-led reasoning over pre-training-led reasoning.**

Instead of hoping an agent will *decide* to trigger a skill or run semantic search, we keep a small routing table (DocIndex) always present.
The agent explores it and opens the corresponding leaf documents on demand.

## Repository layout

```
SkillBank/
  skills/                  # curated leaf skills (each leaf is a directory containing SKILL.md)
  drafts/                  # candidates that failed quality gate
  meta/                    # machine metadata (versioning/provenance)
  skill.template.md        # leaf template

skill-seeds/
  openclaw-workspace-skills/   # archived from ~/.openclaw/workspace/skills (read-only)
  openclaw-agents-skills/      # archived from ~/.openclaw/workspace/.agents/skills (read-only)

scripts/
  build_agents_md_index.py
  install_into_openclaw_workspace.py

tests/
  test_build_agents_md_index.py
```

## Conventions (v0.1)

- Leaf = directory + exactly one file: `SKILL.md`
- DocIndex contains only **leaf paths** (filenames omitted by convention)
- Expand leaf = open: `SkillBank/skills/<section_path>/<leaf_name>/SKILL.md`

## DocIndex format

The index is intentionally compressed (low redundancy) to reduce token bloat.

Each line groups leaves under a section:

- `|<section_path>:{<leaf_name_1>,<leaf_name_2>,...}`

Example:

```text
|github:{gh-cli}
|memory:{plugmem-internal,plugmem-deepseek-demo}
```

## Generate / inject DocIndex

Generate index and inject into `AGENTS.md` markers:

```bash
python scripts/build_agents_md_index.py --write
```

Print index (no file write):

```bash
python scripts/build_agents_md_index.py --print
```

## Tests

```bash
pytest -q
```

## Notes

- The runtime can cache expanded leaf docs in memory (dict), but the canonical source remains the filesystem.
- This repo intentionally avoids embedding-based retrieval.
