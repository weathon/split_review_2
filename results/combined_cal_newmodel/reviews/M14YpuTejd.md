Now I have all the information I need. Let me write the final consolidated review.

## Summary

This paper identifies and addresses several methodological issues in the emerging "online map based motion prediction" protocol (a 2024 CVPR best-paper-finalist line of work). It demonstrates that (1) the default nuScenes train/val split creates a train-validation gap because the motion model trains on high-quality inferred maps (from the map model's training set) but evaluates on lower-quality maps, (2) the perception range of online mapping models (~30×60m) is mismatched to the range needed for motion prediction (>100m), a problem obscured by evaluating only the ego vehicle, and (3) existing metrics include many static agents, making them non-discriminative. The paper proposes OMMP-Bench with spatially-disjoint train/val splits, refined metrics (evaluating moving non-ego agents, separately for close/far agents), and an image-feature baseline to supplement map information for out-of-range agents.

## Strengths

- **The train-val gap problem is correctly identified and cleanly demonstrated.** Section 3.2 and Figure 3 articulate the distribution-shift mechanism clearly. Table 1 provides compelling within-set controls: Row 4 (nuScenes Train split into two disjoint halves, evaluated on nuScenes Val) yields 0.6373 minADE vs Row 3 (default overlapping protocol) at 0.6839 minADE on the **same** evaluation set (nuScenes Val), confirming the gap is real and harmful. The within-set comparison on the proposed Motion Val (Row 1 vs Row 2) independently confirms this.

- **The range mismatch is well-documented.** Tables 2 and 3 together make a compelling case: online mapping models collapse at extended ranges (MapTR drops from 0.124 to 0.014 mAP from 30×60m to 100×100m), but long-range map information benefits motion prediction (0.6154 → 0.6003 minADE with GT maps). This directly supports the paper's recommendations.

- **Metric refinements are sensible and overdue.** Excluding static agents (minADE ≈ 0.002, near-perfect, confirming they add metric noise), evaluating moving non-ego agents, and reporting separately for close vs far agents (Table 6) are clear improvements over existing practice.

- **The finding about ego vs non-ego prediction divergence (Section 4.2, Table 7) is an important insight.** Methods that improve ego prediction can degrade far-agent prediction (e.g., MapUncertaintyPrediction with MapTRv2-CL+DenseTNT: far-agent minADE increases from 2.2742 to 2.3666). This suggests the two-stage protocol as practiced may optimize for the wrong quantity.

- **The map element type analysis (Table 5)** provides useful information about the relative importance of different semantic types, with centerlines emerging as the most informative single element.

## Weaknesses

### Fatal
None.

### Major

- **The headline claim that the proposed split "leads to an explicit performance enhancement compared to the default split" (line 145) relies on an invalid cross-set comparison.** The specific comparison is Row 1 (proposed split: 0.6308 on Motion Val, 86 scenes) vs Row 3 (default split: 0.6839 on nuScenes Val, ~150 scenes). These are different validation sets with different scene distributions and difficulty levels; the difference could simply reflect Motion Val being easier. The paper's own valid within-set comparisons (Row 1 vs Row 2 on Motion Val; Row 3 vs Row 4 on nuScenes Val) correctly demonstrate the train-val gap exists and is harmful. The paper should reframe the contribution as providing a more *realistic* (not better-performing) evaluation protocol and drop the cross-set comparison. This is a material weakness in how the paper presents its central contribution — it does not invalidate the benchmark's value but requires correction.

### Minor

- **The "SOTA" claim for the image-feature baseline is overstated.** Table 4 compares against only two prior methods within the same narrow protocol (MapUncertaintyPrediction, MapBEVPrediction), with modest gains (~2–3% relative). No comparison is made to broader motion prediction or end-to-end methods, and the approach is a straightforward application of deformable attention. The paper should scope this claim appropriately.

- **The paper does not analyze what information the image features contribute.** While Table 7 shows the "img" method improves both close and far agents (with disproportionately larger gains for far agents), the paper does not ablate whether the benefit comes from resolving the map deficiency vs. simply providing a richer feature set, nor does it analyze what information (lane structure vs. texture cues) the features encode.

- **Several experimental tables lack a clear split specification.** Table 4 ("Comparison of Online Map Based Motion Prediction") and Table 6 ("Performance of Different Groups of Agents") do not state which data split they use. Only Table 7 explicitly states it uses OMMP-Bench.

- **The "boundary-free baseline" name is somewhat misleading.** Image features also have limitations (occluded regions, resolution limits, projection errors for distant agents). The name oversells the approach.

- **Table 5 has a likely formatting issue.** Rows 2 and 3 both show the same configuration (✗ ✓ ✗ ✗, Boundary only) with different values (0.6829 vs 0.6558). This needs clarification.

### Trivial
None.

## Nice-to-Haves

- Include error bars or confidence intervals for key benchmark results, especially given the Motion Val set has only 86 scenes where variance could be substantial.
- Clarify how the spatially-disjoint sets were algorithmically created for reproducibility.
- Explain what happened to the test-set scenes (367+397+86 = 850; nuScenes has 1000 scenes; the remaining ~150 are the test set with no public labels).
- Characterize how scene difficulty/density varies between Motion Val and nuScenes Val.

## Removed Points

- **"No error bars"**: Standard practice in this field (single-run large-benchmark evaluation). Downgraded to Nice-to-Have.
- **Metric label inconsistency (minDE vs minFDE, L subscript)**: Parser artifact, not author error.
- **Claims about prior work tone being too harsh**: Stylistic preference, not a substantive weakness. The paper's critical framing is part of its contribution.
- **Missing related works**: Cannot confirm existence of unreviewed references.
- **Purported missing scenes explanation**: The unaccounted ~150 scenes are the nuScenes test set, which lacks public labels — a standard exclusion. Downgraded to Nice-to-Have.
- **Missing split creation methodology details**: Partially described in Section 3.2 ("manually check the whole dataset"). Downgraded to Nice-to-Have.

## Novel Insights

The observation that methods improving ego-vehicle motion prediction can simultaneously degrade non-ego-agent prediction (Section 4.2, Table 7) is a genuinely non-obvious finding that emerges from the proposed multi-agent evaluation. This finding — that MapUncertaintyPrediction and MapBEVPrediction methods help ego but can hurt far agents — suggests that the community should not assume that improvements on the original protocol generalize to the full prediction task. This insight alone warrants attention from researchers working on this protocol.

## Suggestions

1. **Reframe the split comparison.** Drop the invalid cross-set "explicit performance enhancement" claim. The paper's real finding — demonstrated by valid within-set controls — is that the train-val gap exists and eliminating it gives a more realistic assessment of generalization. The new split's value is realism, not better numbers.
2. **Add an ablation for the image features.** Analyze whether the benefit is disproportionately larger for far agents (who lack map context) vs close agents. Consider analyzing what type of information the features encode.
3. **Label every experimental table with its data split.** Ensure Tables 4 and 6 are explicit about which split is used.
4. **Fix Table 5's formatting issue** (duplicate configurations with different values).
5. **Drop the "SOTA" claim** for the baseline and scope it as "competitive performance among existing online map-based methods."

## Score and Decision

**Calibration summary:**

Anchors retrieved across all rounds:

| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| ZPCBcR7Drg | Driving by the Rules (HD map benchmark) | 5.0 | R1 | Yes | Similar benchmark-domain paper, rejected for limited ablation/diversity. Our paper has stronger diagnostic evidence. |
| k3y0oyK7sn | BEV Uncertainty Benchmark | 5.4 | R1 | Yes | Accepted benchmark paper with stronger novelty (novel loss). Our paper has comparable depth of analysis but thinner technical contribution. |
| cvGdPXaydP | nuPlan critique + City-Driver | 4.25 | R1 | Yes | Most similar genre (critiquing existing benchmark). Rejected for narrow scope. Our paper has more extensive evaluation. |
| 72MSbSZtHv | RedMotion (motion prediction method) | 5.33 | R1 | Yes | Method paper, less comparable. |
| ga1IraEqTE | A2Perf benchmark | 4.75 | R2 | Yes | Rejected for limited novelty/narrow evaluation. Our paper's within-set control experiments are stronger. |
| 9rtlfjWMXI | PADetBench (physical attack benchmark) | 4.75 | R2 | Yes | Rejected for lack of comparisons and limited analytical depth. |

**Round 1 bracket:** Between ~4.5 (cvGdPXaydP-level, rejected) and ~5.5 (k3y0oyK7sn-level, accepted). Our paper has stronger evidence than the 4.25-5.0 rejected anchors but thinner technical novelty than the 5.4 accepted anchor.

**Narrowing comparison:** Our paper's weaknesses have favorability ranging from -1.36 to 1.85, with the most negative being the image feature analysis gap (-1.36). The rejected anchors had weaknesses reaching -2.96 (A2Perf), -3.38 (PADetBench), and -2.35 (nuPlan critique). Our weakness profile is milder, closer to k3y0oyK7sn (accepted at 5.4) which had weaknesses around -2.88. The key distinguishing factor is that our paper's central diagnostic contributions (train-val gap, range mismatch, metric refinements) are solid and well-evidenced, while the main issues (overclaiming, analysis gaps) are fixable through revision.

**Final score: 5.5**

The paper makes a worthwhile contribution to an emerging protocol by identifying genuine evaluation flaws and providing a corrected framework. The main weaknesses are presentation overclaims (cross-set comparison, SOTA label) and insufficient depth in the image-feature analysis — none fatal, all fixable. The core benchmark contributions (spatially-disjoint split, refined metrics, multi-agent evaluation, the ego/non-ego divergence finding) are valuable to the community. I recommend acceptance with major revisions to tighten the central claims.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>