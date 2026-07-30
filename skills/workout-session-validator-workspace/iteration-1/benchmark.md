# Skill Benchmark: workout-session-validator

**Model**: current Codex session (exact model not reported)
**Date**: 2026-07-29T14:15:21Z
**Evals**: 1, 2, 3 (1 run each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 100% ± 0% | 83% ± 29% | +0.17 |
| Time | Not measured | Not measured | — |
| Tokens | Not measured | Not measured | — |

Timing and token counts were not reported by the executor notifications.

## Notes

- Evals 1 and 2 tied at 4/4 because the structured audit and planted errors made
  the expected findings explicit.
- Eval 2 exposed one false badge warning in the with-skill run. The validator
  and skill instructions were updated to support minimal fixtures and forbid
  guessed error codes.
- Eval 3 separated the configurations: with-skill 4/4 versus baseline 2/4.
