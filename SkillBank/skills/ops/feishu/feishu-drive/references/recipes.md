# Feishu Drive Recipes

## Browse a shared folder

1. Extract `folder_token` from the URL if provided.
2. Call `list` on that folder.
3. Use returned names/tokens/types for follow-up actions.

## Create a subfolder

1. Identify a valid parent `folder_token`.
2. Call `create_folder` with `name` and parent `folder_token`.
3. Re-run `list` on the parent folder.

## Move a document into another folder

1. Confirm the object token and `type`.
2. Confirm the destination `folder_token`.
3. Call `move`.
4. Verify by listing destination, and optionally source.

## Delete a file safely

1. Inspect or list first if there is any ambiguity.
2. Confirm token + type.
3. Call `delete`.
4. Verify absence with `list` or `info` if supported.
