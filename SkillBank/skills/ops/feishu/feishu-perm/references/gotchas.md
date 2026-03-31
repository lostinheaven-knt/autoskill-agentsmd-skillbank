# Feishu Perm Gotchas

## 1. Token type and token value are a pair

A valid token with the wrong `type` can still fail.
Always keep token + type aligned.

## 2. Identity type is easy to get wrong

`openid`, `userid`, and `unionid` are different namespaces.
Do not substitute one for another.

## 3. List before mutate when uncertain

If the user says “share this with Alice” but the exact collaborator identity is unclear, inspect first or clarify.

## 4. `full_access` is not the default safe choice

Prefer:
- `view` when read-only is enough
- `edit` when the user wants collaboration
- `full_access` only when permission administration is intended

## 5. Verify after changes

Do not assume the permission mutation succeeded just because the tool call returned success. Re-list collaborators.
