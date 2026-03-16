# Subagent-Driven Development

## Purpose
TODO: Describe the purpose in 1-2 sentences.

## When to use
```dot
digraph when_to_use {
    "Have implementation plan?" [shape=diamond];
    "Tasks mostly independent?" [shape=diamond];
    "Stay in this session?" [shape=diamond];
    "subagent-driven-development" [shape=box];
    "executing-plans" [shape=box];
    "Manual execution or brainstorm first" [shape=box];

    "Have implementation plan?" -> "Tasks mostly independent?" [label="yes"];
    "Have implementation plan?" -> "Manual execution or brainstorm first" [label="no"];
    "Tasks mostly independent?" -> "Stay in this session?" [label="yes"];
    "Tasks mostly independent?" -> "Manual execution or brainstorm first" [label="no - tightly coupled"];
    "Stay in this session?" -> "subagent-driven-development" [label="yes"];
    "Stay in this session?" -> "executing-plans" [label="no - parallel session"];
}
```

**vs. Executing Plans (parallel session):**
- Same session (no context switch)
- Fresh subagent per task (no context pollution)
- Two-stage review after each task: spec compliance first, then code quality
- Faster iteration (no human-in-loop between tasks)

## When NOT to use
- TODO: specify at least one situation where this skill should NOT be used.

## Inputs / Preconditions
- Required info: TODO
- Assumptions: TODO
- Constraints: TODO

## Procedure
1. TODO: refine this step with concrete actions and parameters.
2. TODO: refine this step with concrete actions and parameters.
3. TODO: refine this step with concrete actions and parameters.

## Checks
- TODO: add at least one verifiable check.

## Failure modes
- TODO: list at least one failure mode and how to detect it.

## Examples
### Example 1
TODO

## Version / Changelog
- v0.1.0: imported (autofix)

<!-- ORIGINAL_EXTRA_SECTIONS_DETECTED -->
<!-- Please review original draft for additional headings not covered by the template. -->
