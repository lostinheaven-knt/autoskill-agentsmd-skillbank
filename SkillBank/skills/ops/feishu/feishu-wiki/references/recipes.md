# Feishu Wiki Recipes

## Read a wiki page from a link

1. Extract the wiki `token` from the URL.
2. Call `get`.
3. Check `obj_type`.
4. If it is doc-backed (for example `docx`), call `feishu-doc read` using `obj_token` as `doc_token`.

## Browse the tree under a wiki parent

1. Identify `space_id` and optionally `parent_node_token`.
2. Call `nodes`.
3. Use returned node metadata for next-step navigation or edits.

## Create a new page in a wiki section

1. Identify `space_id` and target parent node.
2. Call `create` with `title`, optional `obj_type`, and optional `parent_node_token`.
3. Verify by listing nodes under the parent.

## Rename a page

1. Get the node metadata if needed.
2. Call `rename` with `space_id`, `node_token`, and new title.
3. Verify with `get`.

## Move a page

1. Confirm source node, source space, destination space, and destination parent.
2. Call `move`.
3. Verify by listing destination parent and/or re-running `get`.
