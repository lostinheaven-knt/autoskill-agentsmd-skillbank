# Feishu Drive Actions

## Token extraction

Folder URL example:
- `https://xxx.feishu.cn/drive/folder/ABC123`

Extract:
- `folder_token = ABC123`

## Actions

### List folder contents

Root-style listing (if supported in your context):

```json
{ "action": "list" }
```

Specific folder:

```json
{ "action": "list", "folder_token": "fldcnXXX" }
```

### Get file info

```json
{ "action": "info", "file_token": "ABC123", "type": "docx" }
```

Types include:
- `doc`
- `docx`
- `sheet`
- `bitable`
- `folder`
- `file`
- `mindnote`
- `shortcut`

### Create folder

```json
{ "action": "create_folder", "name": "New Folder", "folder_token": "fldcnXXX" }
```

### Move file or folder

```json
{ "action": "move", "file_token": "ABC123", "type": "docx", "folder_token": "fldcnXXX" }
```

### Delete file or folder

```json
{ "action": "delete", "file_token": "ABC123", "type": "docx" }
```
