Now I have verified all claims against the paper. Let me construct the final review.

**Key verifications:**
- Table 1 confirmed: Setting 1 (proposed) = 0.6308, Setting 4 (50/50 split) = 0.6373, Setting 3 (default) = 0.6839.
- No FLOPs, latency, or parameter counts reported anywhere in the paper.
- No variance or statistical significance reported for any metric.
- Validation set = 86 scenes (line 275).
- Single-dataset limitation explicitly acknowledged (line 96).
- The "metric" changes are evaluation protocol refinements (which agents, how to group), not new metric definitions.

---

## Summary

This paper identifies problems in the emerging online map-based motion prediction protocol: (1) a train-validation gap arises because the map model's training-set predictions are unrealistically accurate for the downstream motion model, (2) the perception range of online map models (e.g., 30×60m) is too small for motion prediction's needs, and (3) evaluating only the ego vehicle and including static agents inflates metrics. The authors propose OMMP-Bench, with a spatially disjoint data split, refined evaluation (non-ego moving agents, close/far subgroups), and a baseline that uses image features via deformable attention to provide context for far-range agents.

## Strengths

1. **Clear identification of the train-val gap in two-stage training (Section 3.2, Figure 3, Table 1).** The paper demonstrates concretely that the existing protocol (map model evaluated on its own training set → unrealistically accurate maps → motion model learns to rely on those accurate maps → performance collapses at validation) is a genuine and non-obvious problem. This diagnosis is well-supported and the field will benefit from recognizing it.

2. **Clean demonstration of the perception range mismatch (Section 3.3, Tables 2–3).** Table 2 shows MapTR's mAP dropping from 0.124 (30×60m) to 0.014 (100×100m), while Table 3 confirms that broader GT maps provide only modest help (minADE 0.6154 → 0.6003) — yet the online model cannot deliver even that. The evidence is sufficient and the diagnosis is sound.

3. **Careful spatially disjoint split design (Figure 4).** The paper manually verifies and reduces spatial overlap from 87% to 5%, producing a cleaner evaluation protocol that future work can adopt. This is a careful piece of dataset curation.

4. **Non-obvious finding about existing methods (Section 4.2, lines 311–312).** The paper notes that MapUncertaintyPrediction and MapBEVPrediction improve ego-vehicle prediction but can *hurt* prediction of nearby non-ego agents — a nuanced result that would be missed under the old protocol.

## Weaknesses

### Fatal
None.

### Major

1. **The claimed benefit of the spatial split is not clearly separated from a simpler confounding factor (Table 1).** Setting 4 — a straightforward 50/50 split of nuScenes train into separate map and motion training sets, without any spatial overlap curation — achieves minADE 0.6373, nearly matching the proposed split (Setting 1, 0.6308). The difference (≈1% relative) is tiny, especially given the absence of variance estimates. This strongly suggests that the main driver of improvement is simply *not training the motion model on the map model's own training-set outputs* (which Setting 4 partially avoids), rather than the paper's careful spatial overlap reduction. However, the paper does not discuss Setting 4 in the text — it appears only in the table — and the narrative around the split as a key contribution implicitly attributes the benefit to the spatial curation. The paper should either provide evidence that spatial overlap matters beyond what Setting 4 captures, or recalibrate its claims to acknowledge that the simpler fix accounts for most of the improvement.

2. **The metrics "contribution" is an evaluation protocol refinement, not a metric innovation (Section 3.4).** The paper's intervention is to change *which agents are evaluated* (non-ego moving agents, disaggregated by distance) and to filter out static agents. These are sensible and useful decisions for the evaluation protocol, but the paper frames them under the heading "Non-discriminative Metrics" and presents them as a major contribution in the introduction. The standard metrics (minADE, minFDE, MR) remain unchanged. This overstates the nature of the contribution.

### Minor

1. **No computational cost comparison.** The main results (Table 7) compare "base", "unc", "bew", and "img" methods without reporting FLOPs, latency, or parameter counts. Since "img" uses raw image features via deformable attention while "bew" uses BEV features, the two methods have different computational profiles. Without cost data, it is impossible to assess whether "img"'s advantage is methodological or simply reflects different compute allocation. (This does not invalidate the paper's results, but a benchmark should report cost for informed practitioner trade-offs.)

2. **No variance or statistical significance reported.** All metrics are point estimates. With a validation set of only 86 scenes, the differences between some methods or conditions could easily fall within run-to-run noise. This is especially relevant for the split comparison (Setting 1 vs. Setting 4, Δ≈0.0065 minADE) and several Table 7 entries where methods differ by under 1%.

3. **Implementation details of the proposed baseline are sparse (Section 3.3, Eq. 1).** The paper does not specify which backbone produces the image features, whether it is shared with the map model, or how the deformable attention module is initialized and trained. These details affect reproducibility, though the promised code release partially mitigates this concern.

### Trivial
None.

## Nice-to-Haves

- Report variance (e.g., standard deviation over multiple seeds) for all metrics, especially given the small validation set.
- Include FLOPs, latency, or parameter counts for all evaluated methods.
- Discuss the relationship between Setting 4 and Setting 1 explicitly: both avoid training the motion model on the map model's training-set outputs, and the near-identical results suggest the spatial curation is less impactful than the paper implies. Deepening this discussion would strengthen the diagnostic contribution.

## Removed Points

These points were raised in the input review but removed under the filtering rules:

- **"The benchmark is limited to a single dataset"** — The paper explicitly acknowledges this (line 96) as an inherent constraint of the sub-field. Not a genuine weakness; it is the paper being transparent about scope.
- **"The boundary-free baseline is straightforward / technically trivial"** — The paper presents it as "straightforward" and "simple yet effective"; it does not claim technical novelty in the module design. This is not a weakness.
- **"Related work is thin"** — Subjective and not actionable. The related work covers the necessary context.
- **Speculation that "img" uses more compute than "bew"** — Unsupported by evidence in the review or the paper. The *absence* of compute reporting is a valid weakness (included above), but the claim that the comparison is *unfair* because one method necessarily uses more compute is speculative.
- **Missed opportunities for discussion about Setting 4** — Already captured in Major weakness #1 above.

## Novel Insights

None beyond the paper's own contributions. The input review does not surface a novel perspective that the paper itself missed; it primarily sharpens the calibration of the paper's claims.

## Suggestions

- Add a dedicated discussion paragraph about Setting 4: acknowledge that it achieves similar results to the proposed split, explain why, and separate the effects of "train-val gap avoidance" vs. "spatial overlap reduction."
- Replace "new metrics" framing in the introduction and Section 3.4 with "refined evaluation protocol" or similar language that accurately reflects the contribution.
- Add a computational cost table (FLOPs, latency, or parameters) for all four method variants (base, unc, bew, img) across both motion models.
- Report variance for at least the main results (Tables 1 and 7).
- Provide clearer implementation details for the baseline (backbone specification, shared vs. separate weights, training procedure for the deformable attention module).

## Score and Decision

This paper makes genuinely useful diagnostic contributions — the train-val gap analysis and the range-mismatch demonstration are solid and will inform future work in this sub-area. The split curation is careful, and the non-obvious finding about existing methods sometimes hurting non-ego prediction is valuable. However, the paper overstates its contributions in two significant ways (the split benefit conflated with a simpler confound, and the metrics framed as an innovation), and the missing variance and compute reporting weaken the empirical contribution. The paper needs non-trivial revisions to recalibrate claims and add missing analysis. With those revisions it could be a strong paper.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>