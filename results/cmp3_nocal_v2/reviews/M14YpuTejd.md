Here is the final consolidated review.

---

## Summary

This paper identifies three genuine misconceptions in the two-stage online map-based motion prediction protocol (Gu et al. 2024a): a train-validation gap caused by the map model inferring on its own training set during motion model training, a perception-range mismatch between online mapping (~30×60m) and motion prediction (agents up to 100m away), and non-discriminative metrics that evaluate only ego trajectories while including trivial static-agent predictions. To address these, the authors propose OMMP-Bench with a new spatially-disjoint data split, refined metrics (moving non-ego agents only, split by close/far distance), and a boundary-free baseline that uses image features to supplement map information for out-of-range agents. Experiments with MapTR/MapTRv2-CL and HiVT/DenseTNT validate the proposed fixes.

## Strengths

1. **Train-validation gap diagnosis is clear and actionable.** Section 3.2 and Figure 3 concretely document that under the existing protocol the map model achieves 87.6 mAP on the motion training set (inferring on its own training data) but only 50.3 mAP on the validation set. The proposed split reduces this to 48.9 vs. 50.3 mAP. Table 1 Row 1 vs. Row 2 (both evaluated on the same Motion Val set) shows that eliminating this gap improves minADE from 0.7006 to 0.6308, directly demonstrating the downstream benefit.

2. **Perception-range mismatch is convincingly documented.** Table 2 shows MapTR's mAP collapsing from 0.124 to 0.014 when the range is extended from 30×60m to 100×100m. Table 3 shows that providing a larger ground-truth map improves prediction (minADE 0.6154 → 0.6003), establishing that the bottleneck is map quality at range, not motion model capability.

3. **The image-feature (img) baseline produces meaningful improvements for far-away agents.** Across all four map-model × motion-model combinations in Table 7, the img method reduces Moving Non-Ego Far minADE relative to the base method (e.g., MapTR+HiVT: 0.6997 → 0.6318, −9.7%; MapTRv2-CL+HiVT: 0.6999 → 0.6274, −10.4%; MapTR+DenseTNT: 2.4140 → 2.0702, −14.2%). These are practically significant gains for the most challenging agents.

4. **Metric refinements reveal important patterns hidden by the existing protocol.** Table 6 shows static-agent minADE of 0.002, confirming that including static agents inflates metrics. Table 7 reveals that methods improving ego prediction do not necessarily improve far-agent prediction (e.g., MapTRv2-CL+HiVT+unc improves ego minADE 0.3976→0.3862 but degrades Moving Non-Ego Far from 0.6999→0.7071) — a non-obvious finding enabled by the proposed close/far split.

## Weaknesses

### Fatal
None.

### Major

1. **Table 5 contains a clear data error, and the map-element analysis is not supported by the evidence as presented.** Rows 2 and 3 of Table 5 list identical configurations (Boundary only) but report different minADE values (0.6829 and 0.6558). This is an unambiguous error. Furthermore, the paper claims "centerlines are most helpful and centerlines only achieve the second best performance," yet (a) there is no "centerlines only" row in the table, (b) the closest proxy (Boundary + Centerline, 0.6631) is worse than Boundary + Pedestrian Crossing (0.6500) and one of the duplicate Boundary-only entries (0.6558). The claim about centerlines' importance does not follow from the data. The overall conclusion (use all map elements) is reasonable, but the specific evidence path is compromised and needs correction.

2. **The new data split is not fully specified, limiting independent reproducibility.** The paper states "we manually check the whole dataset and split it into three spatially disjoint sets" (Section 3.2) without providing the procedure, overlap criteria, threshold for spatial separation, or scene IDs. For a benchmark that proposes a new evaluation protocol, this is insufficient detail. The promised code release mitigates this concern but does not eliminate the need for a clear specification in the paper itself.

### Minor

3. **The "explicit performance enhancement" claim (Section 3.2) relies on a confounded comparison.** The paper compares Row 1 (Ours: 367/397/86 scenes, minADE 0.6308) with Row 3 (Default: 700/700/150 scenes, minADE 0.6839) as evidence that the new split improves performance. However, these rows differ in evaluation set size (86 vs. 150 scenes), training set size, and scene composition simultaneously — the improvement could partly reflect an easier evaluation set. The cleaner comparison is Row 1 vs. Row 2 (same Motion Val evaluation, different training protocols), which does support the thesis but is not highlighted as the primary evidence.

4. **Limited evaluation scope for a benchmark contribution.** Only 2 motion prediction models (HiVT, DenseTNT) and 2 map models (MapTR, MapTRv2-CL) are evaluated. Stronger models discussed in Related Work (MTR, QCNet, SceneTransformer) are absent. Without results on at least one more modern motion model, it is unclear whether patterns like the close/far gap and image-feature benefits generalize.

5. **The new split conflates two distinct issues.** It simultaneously addresses (a) the train-val inference gap and (b) spatial overlap between nuScenes splits. The paper does not ablate whether the geographic repartitioning is necessary beyond simply splitting the existing training set into map-train and motion-train portions.

### Trivial
None.

## Nice-to-Haves

- **Upper-bound comparison:** Report motion prediction performance using ground-truth maps on the same evaluation split to contextualize the loss from online map errors.
- **Random-split baseline:** Compare against a random three-way split preserving the same per-set scene counts but without geographic separation, to isolate the effect of spatial partitioning from data reduction.
- **Error bars or multiple seeds:** With only 86 validation scenes, results could be sensitive to the specific scene selection.
- **Clarify "boundary-free" terminology:** The baseline supplements online maps with image features rather than eliminating boundaries entirely. Discuss failure cases (occluded agents, agents outside all camera frustums).
- **Implementation details for the image-feature baseline:** The description (backbone choice, feature integration mechanism) is currently minimal and should be self-contained rather than deferring entirely to the appendix.

## Removed Points

These points from the input review are excluded or downgraded with justification:

- **"No procedure is given for the split"** — Kept but listed under Major (point 2), since promised code release partially addresses the concern.
- **"The training data is dramatically reduced"** — Removed. This is a necessary consequence of splitting a fixed dataset into three non-overlapping sets; the sizes are transparently reported. Not a flaw.
- **"Table 1 does not actually demonstrate that the train-val gap is eliminated"** — Partially removed. Figure 3 does demonstrate the gap elimination in map quality (87.6→50.3 vs. 48.9→50.3), and Table 1 Row 1 vs. Row 2 shows downstream benefits. The claim that the gap elimination is "asserted but not measured" overstates what is missing. Folded into Minor point 3.
- **"Section 3.3 method is under-specified"** — Moved to Nice-to-Haves; the appendix (parser-stripped) likely contains details, and code release is promised.
- **"The 'boundary-free' name is underspecified"** — Moved to Nice-to-Haves.
- **"No upper-bound comparison," "No random-split baseline," "No error bars"** — Moved to Nice-to-Haves; these are suggestions, not weaknesses.
- **All "Strengthening the Paper on Its Own Terms" points** — Moved to Nice-to-Haves as constructive suggestions.

## Novel Insights

None beyond the paper's own contributions. The reviewer analysis validates the core contributions (train-val gap, range mismatch, metric issues) while identifying specific gaps in evidence quality for the split design and map-element analysis.

## Suggestions

1. Fix the duplicate row error in Table 5 and revise the claims about centerlines to match what the corrected data supports.
2. Provide the complete split specification (scene IDs, overlap criteria, partitioning algorithm) in the paper or as an immediately available supplement.
3. Add at least one stronger motion prediction model (e.g., MTR or QCNet) to demonstrate that patterns generalize beyond HiVT and DenseTNT.
4. Add a controlled comparison that isolates the train-val gap effect from data-reduction and geographic-partitioning effects.
5. Report results with multiple seeds given the reduced validation set size (86 scenes).

## Score and Decision

The paper identifies genuinely important problems in a young and active field, proposes well-motivated solutions, and provides solid empirical evidence for its core claims. The diagnosis of the train-val gap, perception-range mismatch, and metric flaws is timely and practically useful. The image-feature baseline is a simple but effective fix for out-of-range agents, and the refined metrics clearly reveal important patterns. However, the paper is weakened by a clear data error in Table 5 that undermines the map-element analysis, incomplete specification of the proposed data split, and limited evaluation scope for a benchmark contribution. These issues are addressable with revisions and do not invalidate the core contributions.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>