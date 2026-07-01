Now let me write the final review with all filtering applied and the score calibrated.

## Summary
The paper identifies and systematically addresses three methodological flaws in the emerging "online map based motion prediction" evaluation protocol: (1) spatial overlap between train/val sets creates a train-val gap in the two-stage pipeline, (2) the limited perception range of online mapping models leaves distant agents without map context, and (3) metrics that only evaluate ego-vehicle performance with abundant static agents are non-discriminative. The authors propose OMMP-Bench with a spatially-disjoint three-way split, refined metrics (non-ego, moving, distance-stratified agents), and a simple image-feature baseline to address the out-of-range issue.

## Strengths
- **Train-val gap diagnosis (Sec 3.2, Fig 3, Table 1) is clearly demonstrated with concrete evidence.** The paper shows a dramatic distribution shift in map accuracy (mAP 87.6 on training vs. 50.3 on validation) under the existing two-stage protocol, and the proposed spatially-disjoint split eliminates this gap while producing more realistic generalization estimates. Table 1 provides direct comparisons across four split configurations.
- **Metric refocus onto non-ego, moving, distance-stratified agents (Sec 3.4, Table 6) is well-motivated and practically important.** The paper correctly identifies that evaluating only the ego vehicle sidesteps collision-avoidance with other agents, and that the abundance of static agents in nuScenes inflates metrics. The close/far breakdown (based on the online mapping perception range) usefully disentangles two qualitatively different failure modes.
- **Range misalignment analysis (Sec 3.3, Tables 2–3) yields a non-obvious finding.** Expanding map perception range drastically degrades map quality (MapTR mAP 0.124 → 0.014 from 30×60m to 100×100m), and using a poor long-range map does not improve motion prediction. This insight cleanly motivates the image-feature baseline as an alternative to naive range expansion.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor
- **No variance or statistical significance reported.** All tables report single-point estimates without confidence intervals, standard deviations, or multi-seed runs. The validation set contains only 86 scenes, which is small enough that noise could affect relative rankings. For example, the minADE improvement of the "img" baseline over "base" in Table 4 is 0.6375 → 0.6163 (3.4%); whether this difference is meaningful is unknown without variance estimates. This weakens the quantitative claims, though single-run evaluation is common in this sub-field.
- **Table 5 has a formatting artifact and the text conclusions do not cleanly match the data.** Two rows with identical settings (Boundary only) show different minADE values (0.6829, 0.6558). Interpreting the second row as "Centerlines only" (the only missing combination), the text claims "centerlines are most helpful and centerlines only achieve the second best performance." However, Boundary+Pedestrian crossing (0.6500) outperforms the presumed Centerlines-only (0.6558), so the claim does not follow from the data. The analysis should be corrected.
- **"SOTA" claim for the image feature baseline is over-reaching (line 198).** The baseline is compared against only two prior methods on the same backbone within a newly-defined benchmark where no external results exist. Calling this "SOTA" is self-referential; "performs best among compared methods" would be more precise. The absolute improvement is also small (minADE 0.6163 vs. 0.6272) without variance estimates.
- **Novelty framing overstates the "discovery" of these issues.** The spatial overlap problem is acknowledged as previously identified by StreamMapNet (Yuan et al., 2024), which the paper itself cites. The limited perception range of MapTR is a known design choice documented in the original MapTR work. The paper's genuine contribution is systematically correcting these issues in a unified benchmark, not discovering them for the first time.

### Trivial
- The abstract claims "long-standing mis-usage" but the online map based motion prediction protocol only emerged in 2024 (Gu et al., 2024a).
- The paper does not explicitly discuss the trade-off of reducing the map training set from ~700 to 367 scenes in the proposed split, though Table 1 shows comparable performance between the proposed split and a 50% subsample.

## Nice-to-Haves
- Reporting computational cost (inference speed, parameter counts) for the image feature baseline.
- Discussing what would be needed to extend the protocol to other datasets beyond nuScenes.
- A finer-grained distance breakdown beyond the binary close/far split.

## Removed Points
These points are flagged to be removed; treat them with caution.
1. **Boundary-free baseline is "under-described" (missing Deformable Attention config, heads, sampling points).** The paper states "detailed rules of the pipeline in Appendix A" (line 327). Since the appendix is stripped by the parser, criticisms about missing implementation details that would be in the appendix are not verifiable from the available material. *Removed per rule: parser strips appendix content; details exist in the original submission.*
2. **Formatting/parser artifacts in tables (e.g., "bey"/"bew" for "bev", "minDE" for "minFDE").** These are PDF extraction errors, not paper problems. *Removed per rule: formatting artifacts from PDF parsing are not author errors.*
3. **Strength: "The paper is clearly structured and well-written."** Generic observation without specific concrete content. *Removed per rule: drop strengths that are generic or lack specific citation/content.*

## Novel Insights
None beyond the paper's own contributions. The insight from the harsh critic that methods improving ego prediction sometimes hurt non-ego close prediction (Table 7) is a genuine observation already noted by the paper.

## Suggestions
- Add multi-seed results or confidence intervals to substantiate quantitative comparisons, especially given the 86-scene validation set.
- Fix Table 5 (resolve the duplicate row artifact) and revise the text conclusions to match what the data actually shows.
- Replace the "SOTA" claim with a more precise description (e.g., "performs best among methods compared on this benchmark").
- Acknowledge the reduction in map training data as a trade-off of the proposed split.

## Score and Decision

**Calibration anchors (all rounds):**

| Path | Avg Human Score | Round | Comparison |
|---|---|---|---|
| cvGdPXaydP (nuPlan gym critique) | 4.25 | R1 | Similar critique-of-evaluation paper but had more fundamental issues (ambiguous contributions, limited scope); this paper is stronger. |
| k3y0oyK7sn (BEV uncertainty benchmark) | 5.40 | R1 | Benchmark+method paper, accepted; this paper has cleaner presentation and clearer contributions. |
| LsURkIPYR5 (LaneSegNet) | 6.00 | R2 | Map learning paper for autonomous driving, accepted with scores 8,5,5,6; this paper is comparably strong with less severe weaknesses. |
| mDIXfHvoqH (ITPNet) | 6.75 | R2 | Trajectory prediction method paper, decision Reject despite high avg due to split scores; not directly comparable. |
| Vv76fCYffN (SSR) | 6.40 | R2 | End-to-end driving method paper; different contribution type. |

**Round 1 bracket:** [6.0, 7.0] — determined by comparing against the nuPlan critique (4.25, weaker paper) and the BEV uncertainty benchmark (5.40, accepted with comparable contribution strength).

**Final calibration:** The paper sits above LaneSegNet (6.00) due to cleaner presentation and more clearly valuable benchmark corrections, but below 8.0-level papers that have stronger theoretical or SOTA technical contributions. The weaknesses (no variance, Table 5 artifact, SOTA over-claim) are all minor and addressable.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>