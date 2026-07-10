Now I have all the anchors. Let me compile the final review.

**Round 1 Bracket**: Based on comparison with HOI-Diff (5.25, Reject), 3D Interacting Hands Diffusion Model (5.50, Reject), and InterMask (6.00, Accept), the plausible bracket for TOUCH is [6.0, 7.0]. The paper has clearer novelty than InterMask (which was criticized for "innovation not well-defined" at -10.00) and stronger contributions than HOI-Diff (5.25). Its weaknesses are fixable and don't undermine core claims.

**Narrowing**: TOUCH shares with InterMask (6.00→Accept) the pattern of strong results but missing error bars. However, TOUCH has stronger innovation clarity (+9.97 for task formulation) while InterMask had -10.00 for "innovation not well-defined." Both have small user studies. TOUCH's baseline ambiguity (-7.48) and P-FID specification (-7.63) are moderate-impact weaknesses, well below the decisive -10.00 weaknesses that pulled down HOI-Diff and IHDiff. Final score: **6.5**.

---

## Summary

This paper introduces Free-Form HOI Generation, a task that moves beyond the grasp-centric paradigm to generate diverse hand-object interactions (pushing, poking, rotating, tipping) conditioned on fine-grained text. The authors construct WildO2, a dataset of 4.4k 3D interaction samples from internet videos across 92 intents and 610 object categories, and propose TOUCH, a three-stage framework (contact map CVAE → multi-level conditioned diffusion → physical refinement). Results show substantial improvements over adapted baselines on contact accuracy, physical plausibility, diversity, and semantic consistency metrics.

## Strengths

- **Novel and well-motivated task formulation.** The paper correctly identifies that HOI generation is locked into grasping and makes a compelling case for expanding to non-grasping interactions. This reframing is the paper's most significant conceptual contribution (Sec. 1). **[impact=+9.97]**

- **WildO2 dataset fills a genuine gap.** It provides 4.4k interactions with multi-level annotations (contact maps, 17-part hand segmentation, SSCs, DSCs). The O2HOI frame-pairing strategy for handling occlusion during reconstruction is clever and enables automated scaling (Sec. 3.1). **[impact=+9.34]**

- **Architecturally coherent three-stage method.** The coarse-to-fine conditioning design (global SSC + object geometry in early diffusion blocks, fine-grained DSC + local contact features in later blocks) is cleanly implemented. The cycle-consistency loss (Eq. 7) for contact refinement is a nice idea for reducing ambiguity in bidirectional mapping (Sec. 4). **[impact=+9.98]**

- **Strong quantitative results.** In Table 1, TOUCH substantially outperforms ContactGen and Text2HOI across all metrics with large margins (MPVPE: 2.97 vs 4.69/5.46; P-FID: 4.13 vs 15.72/6.08). The ablation study (Table 2) convincingly demonstrates each component's contribution. **[impact=+10.00]**

## Weaknesses

### Major

- **Ambiguous baseline training protocol.** The paper states that baselines are "adapted for our setting" and augmented with post-processing (Sec. 5.2), but never clarifies whether ContactGen and Text2HOI were retrained on WildO2 training data or simply run with pre-trained weights. Since Table 1 is the only quantitative comparison, this ambiguity determines whether the comparison is a fair head-to-head or an apples-to-oranges evaluation. The authors must clarify this. **[impact=-7.48]**

- **No error bars or variance reporting.** Tables 1 and 2 report single numbers without standard deviations, confidence intervals, or significance tests. With a test set of 677 samples, a 2% P-IoU gap (0.728 vs 0.713 when switching text encoders) could be within noise. The user study reports only the mean from 10 users with no standard deviation, demographics, or inter-rater agreement (Sec. 5.1). **[impact=-9.99]**

- **P-FID metric is underspecified.** The paper cites Nichol et al. (2022) for "point cloud-based FID" but does not state what 3D feature extractor is used, how the reference distribution is constructed, or whether the metric has been validated for HOI. Text2HOI's anomalously high P-FID (15.72 vs 4.13–6.08 for others) may reflect hand-drift rather than semantic mismatch, undermining interpretability (Sec. 5.1). **[impact=-7.63]**

### Minor

- **Evaluation only on the paper's own dataset.** All experiments are on WildO2, with no evaluation on established benchmarks (GRAB, OakInk) where ground-truth 3D data is available. Since WildO2's ground truth is produced by a reconstruction pipeline, there is a risk the method exploits pipeline-specific artifacts. A validation experiment (reconstructing a subset of an existing benchmark with the same pipeline) would strengthen confidence. **[impact=-0.49]**

- **Out-of-domain generalization is purely qualitative.** The Objaverse results (Fig. 7) show only visual examples with no quantitative metrics (contact accuracy, physical plausibility) reported for these novel objects (Sec. 5.4.2). **[impact=-7.85]**

- **Force-related semantics analysis lacks statistical rigor.** The claim of "22-25% larger average contact area" for firm vs. gentle prompts (Sec. 5.4.3) is reported without sample size, statistical significance, or confidence intervals. **[impact=-7.89]**

- **45% reconstruction failure rate without bias analysis.** Figure 3a shows only 55% of reconstruction attempts succeed, but the paper does not analyze whether failure correlates with interaction type (e.g., whether non-grasping actions fail more often than grasping actions, potentially biasing the dataset toward grasp-like interactions). **[impact=-0.00]**

### Trivial

- **Table 2 row labels are incompletely explained.** The caption does not explicitly spell out abbreviations like "✗ hoc." (removing both hand and object contact maps). **[impact=-5.92]**

## Nice-to-Haves

- Report the CVAE's standalone contact prediction accuracy (P-IoU on held-out data) before feeding into the diffusion model, since errors cascade through the pipeline.
- Consider a softer blending of global and local features across diffusion blocks rather than the hard switch at block 4.
- Quantitatively validate WildO2 reconstruction accuracy against a known-ground-truth dataset (e.g., run the same pipeline on a GRAB subset and report reconstruction error).

## Removed Points

These points are flagged to be removed; treat them with caution:

- **"Overstated novelty regarding fine-grained semantic control"**: The ablation shows DSC contributes a meaningful 0.728→0.698 drop, which is non-trivial. Removed as not a verified weakness.
- **CVAE standalone accuracy / hard switch vs. gradual annealing / two-Transformer-pass question**: These are design-choice questions, not demonstrated flaws. Moved to Nice-to-Haves.
- **Missing validation of reconstruction accuracy against mocap data**: Reasonable suggestion but more of a Nice-to-Have than a weakness, since no ground-truth daily HOI data exists for fair comparison.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Clarify baseline training protocol** explicitly in the paper (retrained on WildO2 vs. used with pre-trained weights).
2. **Add error bars** (3-run standard deviations or bootstrapped CIs) to Tables 1 and 2, and report variance for the user study.
3. **Specify the P-FID feature extractor** and reference distribution construction; optionally validate against human judgments.
4. **Conduct a cross-benchmark validation** by running the WildO2 reconstruction pipeline on a GRAB or OakInk subset and reporting error.
5. **Analyze whether the 45% reconstruction failure correlates** with interaction type (grasping vs. non-grasping).
6. **Report quantitative metrics** for out-of-domain Objaverse generalization.
7. **Provide sample size and significance** for the force-related contact area analysis.

---

### Calibration Anchors

| Path | Avg Score | Round | Itemized? | Comparison to TOUCH |
|------|-----------|-------|-----------|---------------------|
| HOI-Diff (ZYwLfi50GI) | 5.25 | R1 | Yes | Lower: had structural weaknesses (no physical constraints, missing prior work claims). TOUCH has clearer contributions. |
| 3D Interacting Hands Diffusion (nTNElfN4O5) | 5.50 | R2 | Yes | Lower: limited novelty (-10.00), simple baselines outperform on some metrics. TOUCH has stronger innovation. |
| InterMask (ZAyuwJYN8N) | 6.00 | R1 | Yes | Comparable: accepted despite innovation concerns (-10.00). TOUCH has clearer novelty. Both have small user studies. |
| Dynamic Reconst. HOI (J4D5WVoc5g) | 4.50 | R1 | Yes | Lower: major presentation issues (-9.97), unclear contributions. |
| Adversarial HOI Att. (zQXX3ZV2HE) | 3.00 | R1 | Yes | Much lower: writing quality issues, unclear motivation. |

**Round 1 bracket**: [6.0, 7.0] — based on comparison with HOI-Diff (5.25, weaker core contributions) and InterMask (6.00, accepted despite comparable evaluation gaps).

**Narrowing**: TOUCH shares with InterMask (6.00→Accept) strong results but missing variance. However, TOUCH has clearly stronger innovation (+9.97 task formulation strength) vs. InterMask's -10.00 "innovation not well-defined" weakness. TOUCH's weaknesses (baseline ambiguity -7.48, P-FID -7.63, OOD qualitative -7.85) are all fixable in rebuttal and well below the decisive -10.00 weaknesses that pulled down HOI-Diff and IHDiff. The no-error-bars issue (-9.99) is mitigated by the large and consistent margin across all metrics, making noise-based reinterpretation unlikely. Score placed at **6.5**.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>