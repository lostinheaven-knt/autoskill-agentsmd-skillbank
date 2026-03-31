# Feishu Doc Recipes

## Read a doc from URL

1. Extract `doc_token` from the `/docx/` link.
2. Call `read`.
3. If the result hints that tables/images exist, call `list_blocks`.

## Replace the whole doc with a drafted version

1. Confirm that full replacement is intended.
2. Call `write` with markdown content.
3. Re-run `read` to validate the visible text.

## Add a section to the bottom

1. Use `append`.
2. Re-run `read`.

## Insert a table for structured data

1. Decide the shape (rows/columns).
2. Use `create_table_with_values` when values are already known.
3. Otherwise create the table first, then call `write_table_cells`.
4. Validate with `list_blocks`.

## Edit one known block

1. Use `list_blocks` to identify the right block id if needed.
2. Optionally inspect with `get_block`.
3. Call `update_block`.
4. Re-read the document.

## Add an image or file

1. Upload with `upload_image` or `upload_file`.
2. If placement matters, supply `parent_block_id` and optionally `index`.
3. Validate with `list_blocks`.
