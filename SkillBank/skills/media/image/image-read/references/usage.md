# Image Read Usage

## Basic script usage

```bash
python scripts/image_understand.py "https://example.com/image.jpg"
```

With a custom question:

```bash
python scripts/image_understand.py "https://example.com/image.jpg" "What objects are visible in this image?"
```

## Typical task modes

### 1. General description

Use a broad question such as:
- `Describe this image in detail.`
- `Please describe the scene carefully.`

### 2. Targeted analysis

Use narrow questions such as:
- `What objects are visible?`
- `What is the person doing?`
- `How is the image composed?`
- `What style does this image suggest?`

## Configuration reminders

- Use the required coding-plan base URL for this workflow.
- Provide `ARK_API_KEY` or the required credential source expected by the script.
- Ensure the image URL is reachable from the runtime.
