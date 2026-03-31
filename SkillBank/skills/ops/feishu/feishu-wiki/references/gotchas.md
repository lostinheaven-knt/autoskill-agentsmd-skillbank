# Feishu Wiki Gotchas

## 1. Wiki token != doc token

A `/wiki/` URL gives a wiki node token.
To read or edit page content, first call `get`, then use the returned `obj_token` with `feishu-doc` if the object is doc-backed.

## 2. `obj_type` must be checked

Not every wiki node is a docx page. It may be a sheet, bitable, file, etc.
Do not blindly route every wiki object into `feishu-doc`.

## 3. Navigation and content are separate concerns

Use:
- `feishu-wiki` for spaces, tree structure, node metadata
- `feishu-doc` for doc page body content

## 4. Cross-space moves need extra care

For moves, verify:
- source `space_id`
- destination `target_space_id`
- destination `target_parent_token`

## 5. Verify after rename/move

A successful mutation should be checked with `get` and often `nodes` on the relevant parent.
