---
name: feishu-doc
description: Read, write, append, structure, and update Feishu documents/docx pages. Use when the user mentions Feishu docs, docx links, editing cloud docs, inserting tables/images/files, or reading structured document content.
---

# Feishu Doc

Use this skill for Feishu **document content operations**.

## When to use

Trigger when the user wants to:
- read a Feishu doc/docx
- edit or rewrite a doc
- append content to a doc
- inspect structured content like tables/images/blocks
- create a new doc
- insert tables, images, or file attachments into a doc

Do **not** use this skill for:
- folder / drive management → use `feishu-drive`
- wiki navigation / moving wiki nodes → use `feishu-wiki`
- sharing / collaborator permissions → use `feishu-perm`

## Core workflow

1. Extract `doc_token` from a `/docx/` URL if the user gives a link.
2. If the task is content inspection, start with `read`.
3. If the response hints that structured content exists, use `list_blocks`.
4. For edits, choose the narrowest safe write:
   - full rewrite → `write`
   - append → `append`
   - targeted block change → `update_block`
   - table/image/file insertion → dedicated actions
5. After mutation, summarize what changed.

## Recommended task patterns

- **Read document text** → `read`
- **Read table/image-heavy document** → `read`, then `list_blocks`
- **Replace whole document** → `write`
- **Add content to end** → `append`
- **Edit one known block** → `get_block` / `update_block`
- **Insert a table** → `create_table` or `create_table_with_values`
- **Upload image/file** → `upload_image` / `upload_file`

## Gotchas

- Markdown tables are **not** supported by `write`; use docx table actions instead.
- `read` is best for plain text inspection; it may not fully expose tables/images/layout.
- If blocks matter, use `list_blocks`.
- Prefer the smallest write that solves the task. Avoid `write` when the user asked for a local edit.
- If creating a new document for the requesting user, ensure the requester gets edit access when your environment/tooling expects that.

## Verification

After edits:
- re-read the doc with `read` for text changes
- use `list_blocks` when validating tables/images/block structure
- mention any limitation if formatting cannot be perfectly verified via plain text

## References

Read as needed:
- `references/actions.md` — action cheat sheet and parameter patterns
- `references/gotchas.md` — common failure points and safe defaults
- `references/recipes.md` — common end-to-end workflows
