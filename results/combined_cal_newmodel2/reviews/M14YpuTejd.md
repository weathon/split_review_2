Now I have all the data. Let me write the final consolidated review.

## Summary

This paper identifies three real, consequential problems in the emerging online-map-based motion prediction evaluation protocol: (1) a train-validation gap caused by the map model inferring on its training set during motion model training but on unseen data during evaluation, (2) a range mismatch where online mapping models' limited perception range leaves many agents without map context, and (3) non-discriminative metrics that evaluate only the ego vehicle and include trivial static-agent predictions. The paper proposes OMMP-Bench, a benchmark with a new spatially-disjoint data split, refined per-agent metrics, and an image-feature baseline to compensate for out-of-range agents. The diagnostic analyses are the paper's strongest contribution; the proposed solutions have several significant issues.

## Strengths

- **The train-validation gap diagnosis (Section 3.2) identifies a genuine and previously overlooked problem.** The paper clearly demonstrates that under the existing protocol (Gu et al., 2024a), the motion prediction model trains on maps with ~87.6 mAP but evaluates on maps at ~50.3 mAP — a severe distribution shift that makes prior evaluations systematically unreliable. Figure 3 and the accompanying explanation are clear and well-supported.

- **The range-misalignment finding (Section 3.3) is convincingly demonstrated with concrete evidence.** Table 2 shows that extending MapTR from 30×60m to 100×100m collapses its mAP from 0.124 to 0.014, and Table 3 shows that even when GT maps are available at longer range, performance improves only marginally (minADE 0.6154→0.6003). This reveals a genuine tension: the map model cannot serve the motion model's range requirements without sacrificing quality.

- **The metric critique (Section 3.4) is the paper's strongest contribution.** Table 6 shows that static agents achieve minADE of 0.002 (nearly perfect prediction), meaning their inclusion inflates aggregate metrics and obscures real prediction difficulty. The close/far distinction based on map perception range is a sensible operationalization. The finding (line 311) that methods improving ego prediction do not necessarily improve prediction for other vehicles is a non-obvious insight with real implications for how this field evaluates progress.

## Weaknesses

### Major

- **The proposed split resolves the train-val gap at a steep, undiscussed cost.** The map model trains on only 367 scenes (~50% of the available training data). The paper frames this as an unqualified improvement, but Table 1 shows that Split 4 (a random 50% subset of nuScenes train) achieves minADE of 0.6373, nearly matching Split 1 (Ours) at 0.6308 — a ~1% difference that is well within noise range. This suggests the benefit comes primarily from reduced training data, not spatial disjointness. The paper claims "explicit performance enhancement" (line 145) without acknowledging this confound.

- **Statistical uncertainty is absent from all comparisons.** No standard deviations, confidence intervals, or multi-seed results are reported anywhere. Given that the key comparison in Table 1 (Split 1 vs. Split 4 at 0.6308 vs. 0.6373) hinges on a 0.0065 minADE difference, single-run point estimates are insufficient to distinguish signal from noise. This undermines the paper's strongest claimed benefit of the new split.

- **The claimed 12.7% minADE reduction for the image-feature baseline (line 313) is inconsistent with Table 7.** For MapTRv2-CL+HiVT on Far Non-Ego agents (the most relevant category for the out-of-range problem): base=0.6999, img=0.6274, relative improvement = (0.6999−0.6274)/0.6999 ≈ 10.4%, not 12.7%. No subgroup in Table 7 yields 12.7%. This factual error needs correction or clarification.

### Minor

- **The image-feature baseline (Section 3.3) is under-specified and over-claimed.** The technical description occupies roughly half a page with a single equation (Eq. 1). There is no description of how agent features \(A_i\) are initialized, how the output fuses with the motion prediction pipeline, whether image features are frozen or fine-tuned, or any ablation of design choices. Despite this, the paper states it "achieves SOTA performance" (line 198) when the only comparisons are variants from the same research group (Gu et al., 2024a,b) — no external SOTA methods are compared. This claim is disproportionate to the development level.

### Trivial

- **Table 5 has two rows with identical input configurations** (Boundary only, ✓) but different minADE values (0.6829 vs. 0.6558). This appears to be a formatting or data error that should be corrected.

## Nice-to-Haves

- A comparison with a "no-map" baseline for out-of-range agents would strengthen the value proposition of the image-feature approach. The paper could quantify how much the image features recover relative to the ideal (GT maps at full range) and the worst case (no map context).
- The analysis of map element types (Section 3.5) is shallow — it only tests the presence/absence of each type individually. Examining interaction effects or redundant combinations would deepen the insight.

## Removed Points

These points are flagged to be removed, treat them with caution:
- "Only evaluates on nuScenes": Removed per hard rules — the paper acknowledges this field limitation (line 96), and requesting other datasets is scope creep beyond what current benchmarks support.
- "Close/far threshold is model-dependent": Removed — the binary threshold based on map perception range is a reasonable operationalization for the task, and this is inherent to any such grouping.
- Generic "strengths" about the problem being important or timely: Removed — these are generic and lack specific content tied to the paper's execution.

## Novel Insights

The review surfaces a subtle but important concern the paper does not fully address: the proposed split's "fix" for the train-val gap introduces a confound between data quantity and spatial disjointness. Because Split 4 (random 50% subset) achieves nearly identical performance to Split 1 (spatially disjoint), the paper's claim that spatial disjointness drives the improvement is unsupported. This suggests the field may need a different strategy — e.g., training the map model on all available data but evaluating motion prediction on a spatially disjoint subset — rather than the approach taken here.

## Suggestions

1. **Correct the 12.7% claim** to match the data in Table 7, or clarify which metric/subgroup it refers to if it references an appendix section not visible in the main paper.
2. **Add standard deviations or confidence intervals** to Table 1 to support the split comparison, especially given the ~1% difference between Split 1 and Split 4.
3. **Discuss the split tradeoff directly**: acknowledge the ~50% reduction in map training data, compare against Split 4, and either justify the spatial-disjointness choice or consider alternative protocols (e.g., train map on all data, evaluate motion on disjoint subset).
4. **Fix the duplicate-row formatting in Table 5**.
5. **Either substantially develop the image-feature baseline** (architectural details, ablations, failure case analysis) or **frame it modestly as a proof-of-concept** and remove the "SOTA" claim given the limited comparison set.

## Score and Decision

**Calibration anchors (all rounds):**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/sEJYPiVEt4.md` (ESDMotion) | 5.25 | R1 | Yes | Method paper with similar issues (unfair baselines, limited novelty, thin method description). Rejected. Our paper has stronger diagnostics but similar method issues. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/ZPCBcR7Drg.md` (MapDR) | 5.00 | R2 | Yes | Benchmark/dataset paper for traffic rules. Rejected for motivation questions and insufficient comparison. Our diagnostic contributions are more novel. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/9rtlfjWMXI.md` (PADetBench) | 4.75 | R2 | Yes | Benchmark paper identifying evaluation flaws. Rejected for limited novel insights. Our paper has stronger specific findings. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/72MSbSZtHv.md` (RedMotion) | 5.33 | R1 | Yes | Motion prediction method. Mixed reviews, rejected. Our paper's genre (diagnostic benchmark) differs substantially. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Bmzv2Gch9v.md` (SmartPretrain) | 6.75 | R1 | Yes | Pre-training for motion prediction. Accepted with strong empirical support. Well above our paper's empirical rigor. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/efeBC1sQj9.md` (SEPT) | 7.00 | R1 | Yes | Self-supervised scene representation. Accepted with extensive ablations. Much stronger empirical execution. |

**Round 1 bracket:** 4.75–7.00 (between rejected benchmark/analysis papers and accepted method papers)

**Round 2 narrowing:** 5.0–6.0, based on comparison with MapDR (5.00, Reject) and ESDMotion (5.25, Reject). The paper's diagnostic contributions are more valuable than these anchors', but the proposed solutions have analogous issues. The most damaging rated items (method under-specification at -2.52 favorability, no error bars at -0.88) are less severe than MapDR's (-3.04, -3.03) and ESDMotion's (-3.84, -2.38), suggesting a slightly higher position within the 5–6 band.

**Final score:** 5.5. The diagnostic contributions (train-val gap, range misalignment, metric critique) are genuinely valuable and clearly demonstrated. However, the proposed solutions have significant, addressable issues: the split design's tradeoff is undiscussed and confounded with data quantity, a factual error in the claimed 12.7% improvement is present, and the method contribution is overclaimed relative to its development. These prevent acceptance in the current form but point to a clear revision path.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>