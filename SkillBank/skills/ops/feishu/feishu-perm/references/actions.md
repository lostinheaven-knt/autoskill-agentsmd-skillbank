# Feishu Perm Actions

## Actions

### List collaborators

```json
{ "action": "list", "token": "ABC123", "type": "docx" }
```

Returns collaborators with fields such as member type, member id, permission, and name.

### Add collaborator

```json
{
  "action": "add",
  "token": "ABC123",
  "type": "docx",
  "member_type": "email",
  "member_id": "user@example.com",
  "perm": "edit"
}
```

### Remove collaborator

```json
{
  "action": "remove",
  "token": "ABC123",
  "type": "docx",
  "member_type": "email",
  "member_id": "user@example.com"
}
```

## Token types

Common values:
- `doc`
- `docx`
- `sheet`
- `bitable`
- `folder`
- `file`
- `wiki`
- `mindnote`

## Member types

Common values:
- `email`
- `openid`
- `userid`
- `unionid`
- `openchat`
- `opendepartmentid`

## Permission levels

- `view`
- `edit`
- `full_access`
