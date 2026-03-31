---
name: image-read
description: Understand and describe images using a multimodal vision model. Use when the user asks what is in an image, wants a detailed image description, asks visual questions, or needs scene/object analysis from an image URL.
---

# Image Read

Use this skill for **image understanding and visual question answering**.

## When to use

Trigger when the user wants to:
- know what is in an image
- get a detailed description of an image
- ask a question about visible objects, people, layout, or scene context
- analyze style, composition, or notable visual details

## When NOT to use

Do **not** use this skill for:
- generating new images
- OCR-heavy document extraction when a dedicated OCR/document path is better
- editing or transforming an image
- video understanding

## Core workflow

1. Confirm the image input source, usually a reachable image URL.
2. Decide whether the task is:
   - general description
   - targeted question answering
   - style/composition analysis
3. Use the image understanding script with an explicit question.
4. Return the answer in plain language.
5. If the model output is uncertain, say so instead of overclaiming.

## Recommended task patterns

- **Describe this image** → broad descriptive question
- **What objects/people are visible?** → targeted object question
- **What is happening in the scene?** → action/scene question
- **Analyze style/composition** → visual-design question

## Gotchas

- Use the coding-plan base URL required by this workflow; mismatched endpoints can fail silently or behave differently.
- Vague prompts produce vague descriptions. Ask the model a precise question when precision matters.
- An image URL must be reachable by the script/runtime.
- Vision answers can be uncertain on tiny details, text, identity, or hidden context; don’t overstate confidence.
- This skill is for understanding images, not generating them.

## Verification

After running the script:
- ensure the call succeeded
- ensure the response actually addresses the user’s question
- mention uncertainty on ambiguous visual details

## References

Read as needed:
- `references/usage.md` — script usage and task modes
- `references/questioning.md` — how to ask better visual questions
- `references/gotchas.md` — endpoint/input limitations and confidence rules
- `scripts/image_understand.py` — reusable image understanding script
