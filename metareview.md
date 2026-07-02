# Metareview: weakness self-overlap (final_results, judge=z-ai/glm-5.2)

Measures whether a reviewer method repeats the same *kind* of weakness across
different papers (template-y, low-effort criticism) vs. producing paper-specific
weaknesses. For each of 30 randomly sampled base papers (seed 42), 3 partner
papers were sampled and the judge model (`z-ai/glm-5.2`) matched each weakness
item in the base paper's review against the partner paper's review, item by
item. `overlap_rate` = fraction of the base review's weakness items that have
a same-kind match in the partner review. Lower is better (less templated).
Nice-to-Have items were excluded only where explicitly labeled as such;
suggestions embedded in the weaknesses were left untouched, at the user's
instruction.

Script: `meta/hivemind_final.py` (adapted from `meta/hivemind.py` to read from
`final_results/` and to use `z-ai/glm-5.2` as judge). Run log:
`meta/hivemind_outputs/run_glm52.log`. Raw records:
`meta/hivemind_outputs/overlap_results_final_glm52.jsonl`.

- Sampling: n_base=30, n_partners=3, seed=42 → 90 pairs × 6 methods = 540 judge calls
- Common papers across all 6 methods: 392
- 537/540 calls succeeded; 3 failed after exhausting retries (see Errors below)

## Mean overlap rate (weakness items, review1 → review2)

| Method | Mean overlap rate | n pairs |
|---|---|---|
| baseline_cmp3_baseline_v2 | 0.330 | 90 |
| DeepReviewer_14B | 0.356 | 89 |
| ours_cmp3_ours_v2 | 0.362 | 90 |
| nocal_cmp3_nocal_v3 | 0.362 | 90 |
| DeepReviewer-v2-openai | 0.505 | 89 |
| cspaper | 0.656 | 89 |

(Rows sorted ascending by overlap rate — i.e. best/least-templated first.)

## Errors (3/540, all `LengthFinishReasonError` retries exhausted or malformed parse)

- `DeepReviewer-v2-openai` JEYWpFGzvn/5H8kxW0Efk — `ValidationError` (10 field errors)
- `DeepReviewer_14B` HwyYpLxY0G/SpUXijnBEg — `ValidationError` (3 field errors)
- `cspaper` 4hkMvkzai5/uXecy0nKiJ — `AttributeError: 'NoneType' object has no attribute 'review1_weakness_items'` (parse returned None after retries)

Root cause: `z-ai/glm-5.2` intermittently consumes its full 65536-token
reasoning budget before emitting the structured `OverlapResult` output,
hitting the length cap (`LengthFinishReasonError`) before the response can be
parsed. The existing 5-attempt retry loop recovered most of these (37 retries
observed across the run); these 3 pairs failed on all attempts and were
dropped rather than retried further or silently substituted.

`human_baseline.py` was not run for this pass (skipped per user instruction).
