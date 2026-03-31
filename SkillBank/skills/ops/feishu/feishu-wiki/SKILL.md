---
name: feishu-wiki
description: Navigate and manage Feishu wiki spaces and nodes. Use when the user mentions Feishu wiki/knowledge base links, browsing wiki trees, creating/moving/renaming wiki pages, or reading wiki-backed doc pages.
---

# Feishu Wiki

Use this skill for Feishu **wiki navigation and node management**.

## When to use

Trigger when the user wants to:
- browse knowledge spaces
- inspect wiki nodes/pages
- create wiki pages/nodes
- move or rename wiki nodes
- read a wiki link and then inspect its underlying document

Do **not** use this skill for:
- editing document body content directly → `feishu-doc`
- drive folder/file management → `feishu-drive`
- collaborator/permission changes → `feishu-perm`

## Core workflow

1. Extract the wiki `token` from a `/wiki/` URL if present.
2. If the user starts from a wiki link, call `get`.
3. Use the returned metadata to determine:
   - `node_token`
   - `space_id`
   - `obj_token`
   - `obj_type`
4. If the user wants page content, hand off to `feishu-doc` using `obj_token` as `doc_token` for docx-backed pages.
5. For structural operations, use `nodes`, `create`, `move`, or `rename`.
6. Verify the resulting tree/node state.

## Recommended task patterns

- **Open a wiki link** → `get`
- **List spaces** → `spaces`
- **Browse children under a node** → `nodes`
- **Create new page in a wiki** → `create`
- **Rename a page** → `rename`
- **Move a page** → `move`
- **Read wiki page content** → `get`, then `feishu-doc read` on `obj_token`

## Gotchas

- A wiki token is **not** the same as the underlying doc token.
- For wiki page content, `feishu-wiki` gives you navigation metadata; `feishu-doc` handles the body content.
- `obj_type` may not always be `docx`; verify before assuming document-edit operations apply.
- When moving nodes, verify both target space and target parent.

## Verification

After structural changes:
- re-run `get` for the node
- re-run `nodes` for parent/target parent when needed
- for content reads/edits, verify via `feishu-doc`

## References

Read as needed:
- `references/actions.md` — wiki actions and parameter patterns
- `references/gotchas.md` — token distinctions and cross-tool handoff rules
- `references/recipes.md` — common browse/create/move/read flows
