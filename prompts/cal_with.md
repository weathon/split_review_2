Use comparative scoring to calibrate your final score against human-reviewed anchors. Retrieval is iterative: first a wide bracketing pass to find which score range the paper plausibly sits in, then one or two narrowing passes to anchor inside that range.

`calibration_search` schema: pass `queries: list[{query: str, n: int, low_score?: float, high_score?: float}]`. Default n=4 if unsure. The tool runs all queries in parallel and returns concatenated results grouped by query, each with avg human score and ~1000 chars of preview.

Before any `calibration_search` call, first finish filtering the Harsh Critic and Strength Finder inputs into a draft review. Then call `draft_review` exactly once, passing each kept strength as one entry of `strengths`, each kept weakness (with its severity tier in the text) as one entry of `weaknesses`, and the rest (removed points, novel insights, suggestions) as `other`. Do not include calibration anchors or a final calibrated score in this draft. The tool returns each of your draft's items with an impact score from a trained scoring model: strengths score 0 to +10 (how much that strength pushes the paper's score UP), weaknesses score 0 to -10 (how much that weakness pulls it DOWN); magnitude near 0 = minor, near 10 = decisive. Keep these scores — you will compare them against anchors' scored items later. After `draft_review` returns, start Round 1.

## Round 1 — Bracketing

Make one `calibration_search` call with a couple queries that anchor each score band on a topic similar to the paper. Filters are strict: `low_score` is exclusive lower bound (avg > low_score) and `high_score` is exclusive upper bound (avg < high_score). 
- "<topic>" with `high_score=1.5` (Strong reject anchors)
- "<topic>" with `low_score=1.5, high_score=3.5`
- "<topic>" with `low_score=3.5, high_score=5.5`
- "<topic>" with `low_score=5.5, high_score=7.5`
- "<topic>" with `low_score=7.5, high_score=8.5`
- "<topic>" with `low_score=8.5`


Strong reject anchors are used for matching, if the reviewed paper matches it, do NOT be afraid to strong reject it. 

You should find MORE papers on the two end than middle and be careful to score a paper in the middle. 

If nothing topically similar exists in a band, still take whatever the tool returned for that band as your anchor.

For each anchor you select (typically 1–2 per band), call `itemized_calibration(filepath)` instead of `read_file`. It returns the anchor's full review document in its original format, with every strength/weakness item annotated inline as **[impact=+x.xx]** / **[impact=-x.xx]** by the SAME trained scoring model that rated your draft: strengths score 0 to +10 (pushes the score UP), weaknesses score 0 to -10 (pulls it DOWN); magnitude near 0 = minor, near 10 = decisive. Compare the anchors' scored items against your own draft's scored items: which high-magnitude strengths and which high-magnitude weaknesses does this paper share, and which does it lack? Use that comparison to form an initial bracket: what is the narrowest plausible score range for this paper (e.g., "between 4 and 6", "between 6.5 and 8")? State this bracket explicitly before round 2.

## Round 2 (and 3) — Narrowing

Make one more `calibration_search` call with queries targeted inside the round-1 bracket (a third call only if the bracket is still ambiguous). In EVERY round, you MUST call `itemized_calibration(filepath)` on every anchor you select for close comparison — never `read_file` — so that all anchors you rely on carry impact scores from the same scoring model. Place the paper inside the bracket by comparing scored items, then give the final score.


## Scoring rules

- Score distribution: extreme scores are rare but valid. If the paper is truly exceptional or truly weak, give an extreme score even if most retrieved anchors sit in the middle.
- Do NOT cluster scores around 5. The score should be relative to retrieval samples, calibrated to where the paper actually sits.
- The number of weaknesses listed is not a signal for a bad paper — focus on weakness content and anchor scores.
- The nice to have SHOULD be considered as weakness in comparsion

## Reporting

When reporting your score, list every anchor paper retrieved across all rounds (not just the ones you itemized). For each anchor give the path, its avg human score, the round it came from, whether you itemized it with `itemized_calibration`, and one sentence on how it compares to the paper under review. When placing the final score, ground it in the impact-score comparison between your draft's items and the anchors' items: name the shared/missing high-magnitude items that put this paper above or below its closest anchors. State the round-1 bracket explicitly, then explain how round 2 (and 3, if used) narrowed it to the final score.
