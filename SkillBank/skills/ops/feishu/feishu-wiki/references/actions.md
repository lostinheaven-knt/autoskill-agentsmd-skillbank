# Feishu Wiki Actions

## Token extraction

From:
- `https://xxx.feishu.cn/wiki/ABC123def`

Extract:
- `token = ABC123def`

## Actions

### List knowledge spaces

```json
{ "action": "spaces" }
```

### List nodes in a space

```json
{ "action": "nodes", "space_id": "7xxx" }
```

With parent filter:

```json
{ "action": "nodes", "space_id": "7xxx", "parent_node_token": "wikcnXXX" }
```

### Get node details

```json
{ "action": "get", "token": "ABC123def" }
```

This often returns identifiers such as:
- `node_token`
- `obj_token`
- `obj_type`
- `space_id`

### Create node

```json
{ "action": "create", "space_id": "7xxx", "title": "New Page" }
```

With parent and object type:

```json
{
  "action": "create",
  "space_id": "7xxx",
  "title": "New Page",
  "obj_type": "docx",
  "parent_node_token": "wikcnXXX"
}
```

### Move node

```json
{ "action": "move", "space_id": "7xxx", "node_token": "wikcnXXX" }
```

To another location:

```json
{
  "action": "move",
  "space_id": "7xxx",
  "node_token": "wikcnXXX",
  "target_space_id": "7yyy",
  "target_parent_token": "wikcnYYY"
}
```

### Rename node

```json
{ "action": "rename", "space_id": "7xxx", "node_token": "wikcnXXX", "title": "New Title" }
```
