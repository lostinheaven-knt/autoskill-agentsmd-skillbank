# Dispatching Parallel Agents

## Purpose
TODO: Describe the purpose in 1-2 sentences.

## When to use
```dot
digraph when_to_use {
    "Multiple failures?" [shape=diamond];
    "Are they independent?" [shape=diamond];
    "Single agent investigates all" [shape=box];
    "One agent per problem domain" [shape=box];
    "Can they work in parallel?" [shape=diamond];
    "Sequential agents" [shape=box];
    "Parallel dispatch" [shape=box];

    "Multiple failures?" -> "Are they independent?" [label="yes"];
    "Are they independent?" -> "Single agent investigates all" [label="no - related"];
    "Are they independent?" -> "Can they work in parallel?" [label="yes"];
    "Can they work in parallel?" -> "Parallel dispatch" [label="yes"];
    "Can they work in parallel?" -> "Sequential agents" [label="no - shared state"];
}
```

**Use when:**
- 3+ test files failing with different root causes
- Multiple subsystems broken independently
- Each problem can be understood without context from others
- No shared state between investigations

**Don't use when:**
- Failures are related (fix one might fix others)
- Need to understand full system state
- Agents would interfere with each other

## When NOT to use
**Related failures:** Fixing one might fix others - investigate together first
**Need full context:** Understanding requires seeing entire system
**Exploratory debugging:** You don't know what's broken yet
**Shared state:** Agents would interfere (editing same files, using same resources)
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
