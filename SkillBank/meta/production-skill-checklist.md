# Production Skill Checklist

Use this checklist before promoting a skill from `seed_openclaw_skills/` into `skills/`.

## 1. Trigger quality

- [ ] Has valid frontmatter with `name` and `description`
- [ ] `name` is stable and preferably lowercase hyphen-case
- [ ] `description` clearly says what the skill does and when to use it
- [ ] Trigger boundary is clear enough to avoid accidental activation
- [ ] Non-trigger boundary is also explicit (what this skill should not handle)

## 2. Responsibility and scope

- [ ] The skill has a single clear responsibility
- [ ] It is not mixing unrelated jobs (e.g. tutorial + deploy + debugging + ops)
- [ ] If it covers multiple variants, the variants are either clearly selected in `SKILL.md` or split into references/other skills

## 3. Workflow quality

- [ ] `SKILL.md` contains a concise core workflow
- [ ] The workflow starts with a safe discovery/read step when appropriate
- [ ] The workflow prefers the narrowest safe mutation over the broadest one
- [ ] The workflow tells the agent what to verify after changes

## 4. Gotchas / guardrails

- [ ] There is a `Gotchas` or equivalent guardrail section
- [ ] It captures realistic failure modes, not generic filler
- [ ] Sensitive or destructive operations include safety guidance
- [ ] The skill helps the agent avoid default-but-wrong behavior

## 5. Progressive disclosure

- [ ] `SKILL.md` is concise and not overloaded with parameter encyclopedias
- [ ] Large details are moved into `references/` where appropriate
- [ ] `SKILL.md` explicitly points to those references
- [ ] `scripts/` are used only when determinism or reuse justifies them

## 6. Content hygiene

- [ ] No TODO placeholders remain
- [ ] No personal notes or debugging diary is mixed into the production workflow
- [ ] No secrets, passwords, personal identifiers, or environment-specific sensitive values are embedded
- [ ] Examples are realistic but sanitized

## 7. Verification quality

- [ ] There is at least one clear verification path
- [ ] Verification uses the right tool for the task (not a weak proxy when a stronger check exists)
- [ ] Limitations are acknowledged if verification is partial

## 8. Promotion decision

A skill is usually ready for `skills/` only when:

- [ ] it is trustworthy enough to be auto-routed to
- [ ] it is short enough to be context-efficient
- [ ] it is opinionated enough to prevent common mistakes
- [ ] it is structured enough that future edits stay clean

## Practical rule

If a skill is informative but not yet trustworthy, keep it in `seed_openclaw_skills/`.
If it is sharp, bounded, and verified, promote it to `skills/`.
