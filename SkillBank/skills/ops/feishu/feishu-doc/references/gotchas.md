# Feishu Doc Gotchas

## 1. `write` is destructive

`write` replaces the entire document content.
Use it only when the user explicitly wants a full rewrite, or when targeted editing is impractical.

## 2. Markdown tables are not supported

If the user wants a visible table in Feishu docx, use:
- `create_table`
- `write_table_cells`
- `create_table_with_values`

Do not rely on markdown pipe tables in `write`.

## 3. `read` is not enough for structure-heavy docs

`read` is good for plain text, but not a full fidelity structural representation.
If the document includes tables, images, code blocks, or nested blocks, call `list_blocks`.

## 4. Prefer narrow writes

Safer order:
1. `update_block`
2. `append`
3. `write`

## 5. Images may appear visually smaller than expected

Display size depends on image dimensions. If a very small image is uploaded, its rendering may be tiny.

## 6. Re-verify after mutation

After changing a doc, re-read it. For tables/images, validate with `list_blocks`, not only `read`.
