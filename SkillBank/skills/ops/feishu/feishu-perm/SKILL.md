---
name: feishu-perm
description: Manage Feishu document, folder, file, wiki, and sheet permissions. Use when the user asks to share something, add/remove collaborators, inspect who has access, or change view/edit/full-access permissions.
---

# Feishu Perm

Use this skill for Feishu **sharing and collaborator permission management**.

## When to use

Trigger when the user wants to:
- see who has access to a Feishu doc/folder/file/wiki object
- add a collaborator
- remove a collaborator
- change or grant view/edit/full access
- share a file or folder with a person, group, or department

Do **not** use this skill for:
- editing document content → `feishu-doc`
- browsing/moving wiki nodes → `feishu-wiki`
- drive file/folder organization → `feishu-drive`

## Safety rule

Permission changes are sensitive.

Before any write action (`add` / `remove`), make sure you know:
- the exact target object
- the object type
- the member identity type
- the intended permission level

If the request is ambiguous, ask or inspect first.

## Core workflow

1. Identify the target object token and its type.
2. Start with `list` when you need current collaborators.
3. Confirm the member identity format:
   - `email`
   - `openid`
   - `userid`
   - `unionid`
   - `openchat`
   - `opendepartmentid`
4. Apply the narrow change:
   - add collaborator → `add`
   - remove collaborator → `remove`
5. Re-list collaborators to verify the final state.

## Recommended task patterns

- **See who can access a doc/folder** → `list`
- **Share with one person** → inspect/list, then `add`
- **Share with a group chat** → `add` with `openchat`
- **Remove access** → `remove`, then `list`

## Gotchas

- Token type matters: `docx`, `folder`, `wiki`, `file`, etc. Don’t mix them.
- Member ID type matters just as much as the member ID value.
- `openid` / `userid` / `unionid` are not interchangeable.
- For sensitive objects, inspect current collaborators first instead of blindly modifying access.
- `full_access` is powerful; don’t grant it casually if the user only asked for edit/view.

## Verification

After any permission mutation:
- call `list` again
- confirm the expected member appears/disappears
- confirm the final permission level matches the request

## References

Read as needed:
- `references/actions.md` — collaborator actions and parameter patterns
- `references/gotchas.md` — token/member-id pitfalls and safety checks
- `references/recipes.md` — safe share/remove workflows
