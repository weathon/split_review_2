Now I have all the information needed. Let me write the final consolidated review.

## Summary

This paper identifies and addresses three methodological misconceptions in the emerging online-map-based motion prediction protocol: (1) inappropriate data splits causing a train-val gap, (2) a mismatch between the perception range of online mapping models and the requirements of motion prediction, and (3) non-discriminative metrics that evaluate only the ego vehicle and include static agents. The authors propose **OMMP-Bench**, featuring a spatially-disjoint three-way split (map train / motion train / motion val), refined metrics (non-ego, moving-only, close/far stratification), and a boundary-free image-feature baseline to compensate for missing map information beyond the perception range. Experiments with MapTR/MapTRv2-CL and HiVT/DenseTNT are conducted to validate the proposed corrections.

## Strengths

1. **The train-val gap diagnosis is well-evidenced and consequential.** The paper clearly demonstrates that under the existing two-stage protocol, the map model infers on its *training* set to produce maps for motion model training, but on a *different* set during evaluation — creating a distribution shift. Figure 3 shows the mAP of input maps dropping from 87.6 to 50.3, and Table 1 confirms the default split underperforms the proposed split despite having more training data (minADE 0.6839 vs. 0.6308). This finding calls into question whether prior work's conclusions about which map representations benefit motion prediction are reliable.

2. **The range-misalignment problem is cleanly diagnosed.** Table 2 shows MapTR's mAP collapsing from 0.124 to 0.014 when extending the perception range from 30×60m to 100×100m. Table 3 shows that if perfect (GT) long-range maps were available, motion prediction would improve — but since online models cannot produce them, the existing protocol obscures the problem by only evaluating the ego vehicle.

3. **The metrics reform is principled and well-justified.** Table 6 demonstrates that static agents achieve minADE of 0.002 (near-perfect), so including them dilutes the metric; far agents are substantially harder to predict than close agents. The proposed stratification (moving non-ego close/far) reveals performance differences that a single aggregate number would hide, and is consistent with conventions from Argoverse and Waymo.

## Weaknesses

### Fatal
None.

### Major

1. **The image-feature ("img") baseline is not directly comparable to map-only methods, yet it is presented as the leading result without qualification.** The img baseline injects multi-scale backbone features (via Deformable Attention) that contain strictly richer information than the vectorized map output used by map-only methods. The paper repeatedly shows img outperforming base/unc/bev methods in Tables 4 and 7 and states it "achieves SOTA performance" (line 198). While the paper is transparent about what the method does, it does not explicitly acknowledge that this is an apples-to-oranges comparison within a benchmark framed as "online map based motion prediction." The benchmark should either (a) separate the leaderboard into map-only and map+image categories, or (b) include a clear caveat when reporting the "SOTA" result. This is a presentation/framing issue rather than a methodological flaw, but it is significant because the headline result conflates two different problems.

2. **No variance or statistical significance is reported anywhere in the paper.** Motion prediction metrics are known to be sensitive to random seeds, and many comparisons in Tables 1, 4, and 7 involve differences as small as 0.01–0.05 minADE (e.g., the 0.0531 gap between Split 1 at 0.6308 and Split 3 Default at 0.6839 in Table 1, or the 0.0109 minADE gap between base and img for HiVT+MapTR close agents). Without standard deviations over multiple runs, the reader cannot assess whether these differences are robust signal or noise. For a benchmark paper that aims to set the standard for evaluation in this area, this is a significant gap in experimental rigor.

### Minor

3. **The range-misalignment claim is tested on only two mapping models from the same architecture family.** Table 2 tests only MapTR and MapTRv2-CL. The paper generalizes that "current online map prediction models cannot fully meet the perception range requirements of downstream motion prediction tasks" (line 151). While the claim is reasonable for the tested models (which are the ones used in the existing protocol), a benchmark positioning itself as a permanent reference should characterize this phenomenon across a broader set of mapping models — e.g., StreamMapNet (which uses temporal information and may have a different range profile) — to strengthen the generality of the conclusion.

4. **The new split uses only 367 scenes for map model training** (roughly half of the available nuScenes training data). The paper does not discuss whether this reduced training set might limit the map model's quality and interact with the comparison — a map model trained on more data might yield a smaller train-val gap. This should be acknowledged as a limitation.

5. **The image-feature baseline is described with insufficient detail for reproducibility.** Section 3.3 provides Equation (1) and a high-level description, but critical details are omitted: how agent feature A_i is obtained from the projected image coordinates, Deformable Attention hyperparameters (number of heads, sampling points, feature dimensions), and how the resulting features are fused with map features in the motion prediction model (HiVT/DenseTNT). For a method claimed to achieve SOTA, this level of detail is insufficient.

### Trivial

6. **The paper does not clarify what happens to the nuScenes test set** (150 scenes with private labels) in the new split, which uses 367+397+86 = 850 scenes from the 700-train + 150-val pool.

7. **No computational cost comparison** is provided between the img baseline and map-only methods, though Deformable Attention on multi-scale multi-view features may be substantially more expensive.

## Removed Points

- **Table 5 formatting issues (duplicate row patterns, missing centerline-only row).** The parsed table shows two rows with ✗,✓,✗,✗ but different values (0.6829 vs. 0.6558) and no identifiable ✗,✗,✗,✓ (centerline-only) row. However, the paper text (line 267) states that "centerlines only achieve the second best performance," implying such a row exists. These inconsistencies are consistent with a parser-induced column misalignment artifact. Per the formatting-artifact rule, this criticism is removed. Authors should verify the table renders correctly in the original PDF.

- **Section 1 "tone" criticism about prior work.** The claim that the paper's critique of the existing protocol is "overdrawn" is a stylistic preference, not a substantive weakness.

- **Only evaluating a single data split.** While the split is a single partition of nuScenes, the paper's primary diagnostic claim (train-val gap exists) is independently supported by the mAP drop in Figure 3 (87.6→50.3), which does not depend on the exact split definition.

## Nice-to-Haves

- Test at least one additional online mapping model beyond the MapTR family (e.g., StreamMapNet) to strengthen the generality of the range-misalignment claim.
- Add qualitative visualizations comparing cases where the img baseline succeeds and map-only methods fail.
- Provide standard deviations over at least 3 random seeds for the main comparisons in Tables 1 and 7.
- Include a computational cost comparison between the img baseline and map-only methods.

## Novel Insights

The meta-reviewer observation that sharpens the paper's contribution: the paper's most valuable finding is not any individual result but the demonstration that the existing protocol's evaluation *structure* (the data split, the ego-only metric, the limited perception range) systematically creates an illusion of progress — models can appear to work well because the evaluation artifacts mask the fundamental challenge of imperfect, limited-range online maps. This structural critique is more significant than any single comparison in the tables.

## Suggestions

1. **Disentangle the img baseline from the map-only leaderboard.** Present the img method in a separate section as a complementary approach for out-of-range agents, and clearly distinguish map-only from map+image results. Remove the unqualified "SOTA" claim or append a caveat.

2. **Add variance estimates.** Report standard deviations over multiple seeds for the main comparisons, especially Table 1 (split comparison) and Table 7 (method comparison). This is critical for a benchmark paper.

3. **Acknowledge and discuss the trade-off of using 367 scenes for map model training** in the paper's limitations section.

4. **Provide more implementation details** for the img baseline, including Deformable Attention hyperparameters and fusion mechanism with motion prediction models.

5. **Verify that Table 5 renders correctly** in the original PDF and that a centerline-only row is present.

## Score and Decision

**Calibration anchors retrieved across all rounds:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| sEJYPiVEt4.md (ESDMotion) | 5.25 | R1 | Closest topic (motion prediction without HD maps). Criticized for unfair baselines (using extra SD map info). OMMP has stronger diagnostic contributions. |
| ZPCBcR7Drg.md (MapDR) | 5.00 | R1 | Benchmark paper for traffic rules. Criticized for unclear motivation. OMMP's motivation is clearer and its diagnostic findings are more foundational. |
| 72MSbSZtHv.md (RedMotion) | 5.33 | R1 | Motion prediction method with mixed scores (5,8,3). OMMP's contribution type is different (diagnostic/benchmark vs. method). |
| LsURkIPYR5.md (LaneSegNet) | 6.00 | R1 | Map learning method accepted at ICLR (8,5,5,6). Strong results but novelty concerns. OMMP's conceptual contributions are stronger but evaluation is weaker. |
| efeBC1sQj9.md (SEPT) | 7.00 | R1 | SSL for motion prediction, accepted (8,6,8,6). Strong empirical results on leaderboards. OMMP weaker on evaluation rigor but stronger on diagnostic insights. |
| pzZjyYee6L.md (Steering Wheel) | 2.50 | R1 | Trajectory forecasting. Very different contribution type. |
| LsURkIPYR5.md (LaneSegNet) | 6.00 | R2 | Same as above — used as primary anchor. |

**Bracket:** Round 1 bracketed the paper at 5.0–7.0 based on the similarity to ESDMotion (5.25, Reject) at the low end and SEPT (7.00, Accept) at the high end. LaneSegNet (6.00, Accept) provides the closest anchor: both papers have solid conceptual contributions with evaluation concerns that are fixable rather than fatal.

**Final score rationale:** The paper's core diagnostic contributions (train-val gap, range misalignment, metric issues) are genuinely valuable and well-supported by evidence. These are not incremental improvements but the identification of structural flaws in an emerging protocol — a meta-contribution that should influence how the field designs and evaluates online-map-based motion prediction. However, the evaluation has two notable weaknesses: (1) the img baseline is presented as SOTA without acknowledging that it uses richer information than map-only methods, and (2) no variance estimates are reported, making fine-grained comparisons uninterpretable. Both are fixable. The paper does not have fatal flaws. A score of 6.0 reflects a borderline-accept paper whose diagnostic value outweighs its evaluation shortcomings, with the expectation that the img baseline presentation and variance reporting will be addressed.

**Score:** 6.0

**Decision:** Accept

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>