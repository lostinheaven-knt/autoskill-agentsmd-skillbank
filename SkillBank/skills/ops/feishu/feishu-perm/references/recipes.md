# Feishu Perm Recipes

## See who has access

1. Identify the target token and type.
2. Call `list`.
3. Use the current collaborator list to decide the next change.

## Share a doc with one user by email

1. Confirm token + type.
2. Decide the correct permission (`view` / `edit`).
3. Call `add` with `member_type: email`.
4. Re-run `list`.

## Share a folder with a group chat

1. Confirm folder token.
2. Use `member_type: openchat`.
3. Grant the intended permission.
4. Re-run `list`.

## Remove access safely

1. Call `list` first if there is ambiguity.
2. Confirm the exact member identity and member type.
3. Call `remove`.
4. Re-run `list` and confirm removal.

## Change effective permission level

If there is no dedicated update action, the safe pattern is often:
1. inspect current permissions
2. remove the old collaborator mapping if needed
3. add the collaborator back with the desired permission
4. verify final state
