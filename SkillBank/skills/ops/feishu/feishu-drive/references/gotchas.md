# Feishu Drive Gotchas

## 1. Bot root is not the same as user root

In bot contexts, “root folder” may not behave like a human user’s personal drive.
A bot often only has access to items explicitly shared with it.

## 2. Parent folder token is often required

For reliable folder creation, prefer creating subfolders inside a known shared folder rather than assuming root access.

## 3. File type matters

For `info`, `move`, and `delete`, the `type` field must match the object.
If unsure, list first and reuse the returned type.

## 4. Verify both sides of a move

If a move seems unsuccessful, check:
- source folder still contains the object
- destination folder now contains the object

## 5. Delete is destructive

When names are ambiguous, inspect first. Do not delete based only on a guessed token or fuzzy name.
