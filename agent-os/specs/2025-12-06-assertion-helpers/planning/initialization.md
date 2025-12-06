# Spec Initialization: Assertion Helpers

## Date
2025-12-06

## Spec Name
assertion-helpers

## User Description
Next roadmap item on assertion helpers

## Roadmap Item (Item 16)
Assertion helpers — Make dataclass variations of aria-testing queries that can be used in `Story.assertions`. For example `GetByRole` would be passed a `role`. Later, the instance would be passed a `container` and would raise `AssertionError` if not passing. Refactor all `Story` in `src` `examples` `tests` that have assertion functions to instead use these helpers, where appropriate. Update README and docs.

Size: M (Medium)

## Status
Initialized - Ready for requirements gathering
