# Image Read Gotchas

## 1. Endpoint mismatch

This workflow expects the coding-plan base URL noted by the original integration. Using the wrong endpoint may fail or degrade behavior.

## 2. Reachability matters

The image URL must be reachable from the runtime environment.

## 3. Precision depends on the question

`Describe this image` and `What is the logo text in the far background?` are not equally reliable asks.
Ask visually realistic questions.

## 4. OCR is not guaranteed

If the real task is text extraction from an image/document, a dedicated OCR/document route may be better.

## 5. Confidence should match visibility

Do not sound certain about tiny, blurry, occluded, or identity-sensitive details.
