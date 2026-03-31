---
name: feishu-drive
description: Manage Feishu drive files and folders. Use when the user mentions cloud drive, folders, moving files, creating folders, browsing shared storage, or deleting/moving Feishu files.
---

# Feishu Drive

Use this skill for Feishu **file and folder management**.

## When to use

Trigger when the user wants to:
- list files in a Feishu folder
- inspect file metadata
- create a folder
- move a file/folder into another folder
- delete a file/folder from Feishu drive

Do **not** use this skill for:
- editing document content → `feishu-doc`
- wiki navigation or wiki node operations → `feishu-wiki`
- sharing/collaborator changes → `feishu-perm`

## Core workflow

1. Extract a `folder_token` or file token from a Feishu drive URL when available.
2. For discovery, start with `list`.
3. For a known file, use `info` if you need metadata before moving/deleting it.
4. For mutations, confirm the target folder/object type as needed.
5. After move/create/delete, verify with `list` or `info`.

## Recommended task patterns

- **Browse a folder** → `list`
- **Inspect one file/folder** → `info`
- **Create subfolder** → `create_folder`
- **Move object** → `move`
- **Delete object** → `delete`

## Gotchas

- Feishu bots may not have a usable root drive like a human account does.
- Creating a folder without a valid parent folder token may fail in bot contexts.
- Bots often only see files/folders explicitly shared with them.
- `type` matters for `info`, `move`, and `delete`; don’t guess if you can verify first.
- For destructive actions like delete, prefer confirming the exact target when ambiguity exists.

## Verification

After mutations:
- use `list` on the parent folder to confirm presence/absence
- use `info` when validating a known object
- if a move appears to fail, verify both source and destination folders

## References

Read as needed:
- `references/actions.md` — action patterns and examples
- `references/gotchas.md` — common constraints in bot/shared-drive contexts
- `references/recipes.md` — standard workflows for browse/create/move/delete
