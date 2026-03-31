# Feishu Permission Tool

## Purpose
TODO: Describe the purpose in 1-2 sentences.

## When to use
- TODO: specify scenarios where this skill applies.

## When NOT to use
- TODO: specify at least one situation where this skill should NOT be used.

## Inputs / Preconditions
- Required info: TODO
- Assumptions: TODO
- Constraints: TODO

## Procedure
1. TODO: refine this step with concrete actions and parameters.

## Checks
- TODO: add at least one verifiable check.

## Failure modes
- TODO: list at least one failure mode and how to detect it.

## Examples
Share document with email:
```json
{
"action": "add",
"token": "doxcnXXX",
"type": "docx",
"member_type": "email",
"member_id": "alice@company.com",
"perm": "edit"
}
```
Share folder with group:
"token": "fldcnXXX",
"type": "folder",
"member_type": "openchat",
"member_id": "oc_xxx",
"perm": "view"

## Version / Changelog
- v0.1.0: imported (autofix)

<!-- ORIGINAL_EXTRA_SECTIONS_DETECTED -->
<!-- Please review original draft for additional headings not covered by the template. -->
- merged: auto-dedupe merged similar skills
