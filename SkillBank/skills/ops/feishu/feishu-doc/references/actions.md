# Feishu Doc Actions

## Token extraction

From:
- `https://xxx.feishu.cn/docx/ABC123def`

Extract:
- `doc_token = ABC123def`

## Core actions

### Read document

```json
{ "action": "read", "doc_token": "ABC123def" }
```

Use first when you need plain text content, title, and a quick sense of document structure.

### Replace whole document

```json
{ "action": "write", "doc_token": "ABC123def", "content": "# Title\n\nMarkdown content..." }
```

Use only when the user wants a full rewrite or when targeted mutation would be more error-prone.

### Append to end

```json
{ "action": "append", "doc_token": "ABC123def", "content": "Additional content" }
```

### Create document

```json
{ "action": "create", "title": "New Document" }
```

Optional folder placement:

```json
{ "action": "create", "title": "New Document", "folder_token": "fldcnXXX" }
```

### List blocks

```json
{ "action": "list_blocks", "doc_token": "ABC123def" }
```

Use when tables/images/structured content matter.

### Get block

```json
{ "action": "get_block", "doc_token": "ABC123def", "block_id": "doxcnXXX" }
```

### Update block text

```json
{
  "action": "update_block",
  "doc_token": "ABC123def",
  "block_id": "doxcnXXX",
  "content": "New text"
}
```

### Delete block

```json
{ "action": "delete_block", "doc_token": "ABC123def", "block_id": "doxcnXXX" }
```

### Create table

```json
{
  "action": "create_table",
  "doc_token": "ABC123def",
  "row_size": 2,
  "column_size": 2,
  "column_width": [200, 200]
}
```

### Write table cells

```json
{
  "action": "write_table_cells",
  "doc_token": "ABC123def",
  "table_block_id": "doxcnTABLE",
  "values": [
    ["A1", "B1"],
    ["A2", "B2"]
  ]
}
```

### Create table with values

```json
{
  "action": "create_table_with_values",
  "doc_token": "ABC123def",
  "row_size": 2,
  "column_size": 2,
  "column_width": [200, 200],
  "values": [
    ["A1", "B1"],
    ["A2", "B2"]
  ]
}
```

### Upload image

```json
{ "action": "upload_image", "doc_token": "ABC123def", "url": "https://example.com/image.png" }
```

or

```json
{ "action": "upload_image", "doc_token": "ABC123def", "file_path": "/tmp/image.png" }
```

### Upload file attachment

```json
{ "action": "upload_file", "doc_token": "ABC123def", "url": "https://example.com/report.pdf" }
```

or

```json
{ "action": "upload_file", "doc_token": "ABC123def", "file_path": "/tmp/report.pdf", "filename": "report.pdf" }
```
