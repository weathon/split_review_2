Now I have all the information needed. Let me produce the final review.

## Summary

This paper identifies and fixes three methodological problems in the emerging two-stage online-map-based motion prediction protocol: (1) a train-val gap caused by the map model being evaluated on its own training set, (2) spatial overlap between nuScenes train/val sets that inflates generalization estimates, and (3) non-discriminative metrics that evaluate only the ego vehicle and include trivial static-agent cases. The authors propose OMMP-Bench, a benchmark with a spatially-disjoint three-way split (map train / motion train / motion val), refined metrics evaluating moving non-ego agents partitioned by distance, and a boundary-free baseline using image features for out-of-range agents.

## Strengths

- **Train-val gap is correctly identified and convincingly demonstrated.** Figure 3 shows a stark contrast: under the default protocol, the map model achieves 87.6 mAP on the motion model's training set but only 50.3 mAP on the validation set. The proposed three-way split eliminates this discrepancy (48.9 vs. 50.3 mAP), and Table 1 shows this correction yields 7.8% better minADE (0.6308 vs. 0.6839). This is the paper's strongest contribution and is directly supported by the data.

- **The spatial overlap issue is correctly raised and fixed.** Citing Yuan et al. (2024), the paper reports that 87% of validation data spatially overlaps with training data (Figure 4). The proposed new split reduces this overlap to 5%, a principled fix for better generalization evaluation.

- **Metric refinements are sensible and empirically justified.** Table 6 shows static agents have near-perfect minADE of 0.002, justifying their exclusion. The close/far partition in Table 7 reveals meaningful variation (e.g., 25% worse minADE for far vs. close agents with HiVT+MapTR) that is masked under the ego-only protocol. This makes the evaluation more informative.

- **Comprehensive evaluation across 16 settings.** Table 7 systematically covers 2 map models × 2 motion models × 4 methods, enabling meaningful comparisons across multiple dimensions.

## Weaknesses

### Fatal
None.

### Major

- **The boundary-free baseline — listed as a core contribution — is insufficiently described.** The main text devotes roughly 15 lines plus Equation (1) to this method. Critical details are absent: the image feature backbone is not specified (only "CNN" appears in Figure 7), the feature dimensionality D is stated but never assigned a value, how the aggregated features Â_i are fused into the motion prediction model is not explained, and whether the deformable attention module is trained end-to-end with the motion model is not stated. While the appendix (stripped by the parser) may contain additional pipeline details, the main-text description is too sparse to evaluate or reproduce this claimed contribution. Since the paper presents this as Contribution 3, readers should be able to understand its mechanism from the paper itself.

### Minor

- **No variance estimates reported.** No standard deviations, confidence intervals, or multiple-seed results are provided for any experimental finding. The headline improvements from the proposed baseline are modest (3.3% relative on overall minADE, 9.7% on far agents). While single-run evaluation is common practice in this field, the absence of variance information makes it impossible to assess whether these differences are statistically reliable. This would significantly strengthen the paper if addressed.

- **The framing overstates the novelty.** The paper describes the identified issues as "long-standing" "misconceptions" and "misunderstandings" of the field. However, the protocol emerged only in 2024, and the fixes (disjoint train/test sets, excluding trivial cases from metrics, evaluating relevant agents) are straightforward applications of standard ML methodology. The contribution is real and valuable — it is a methodological cleanup of a hastily-designed protocol — but the framing inflates the apparent conceptual depth beyond what is delivered.

- **The "close" vs. "far" threshold is not precisely specified.** The paper states it is "decided by whether within the perception range of online mapping models" (30×60m area centered on the ego vehicle), but does not specify whether this is based on the agent's current position, the centroid of its trajectory over the observation horizon, or some other criterion. This needs precise specification for benchmark reproducibility.

- **The boundary-free baseline lacks ablation studies.** Key ablations are missing: (1) providing image features to all agents (close and far) vs. only far agents, (2) comparing against a simpler signal such as agent distance-to-map-edge, or (3) padding missing map regions with zeros. Without these, it is unclear whether the specific deformable-attention-on-image-features mechanism is responsible for the gains or whether any additional signal for far agents would produce similar improvements.

### Trivial
None.

## Nice-to-Haves

- An analysis of failure cases would add depth: when does the image-feature baseline fail to help, and are there systematic patterns (occluded agents, agents at extreme image boundaries)?
- A discussion of whether the specific 30×60m perception range is fundamental or whether other architectures with more capacity could successfully learn a longer-range map model.

## Removed Points

These points are flagged to be removed; treat them with caution.

- Criticism about "no comparison to alternative approaches to the out-of-range problem (expanding BEV range, separate map model, extrapolation)": The paper already compares against extending the map range (Table 2 shows mAP collapses from 0.124 to 0.014 when extending MapTR to 100×100m). Exhaustive comparison against every conceivable alternative is beyond the scope of a benchmark paper.
- Criticism about "single dataset (nuScenes)": The paper explicitly explains that nuScenes is the only dataset providing raw camera data, HD maps, and agent trajectories simultaneously. This is a data-availability constraint, not an oversight. Removed as scope-creep.
- Criticism about "benchmark scope is narrow": Same as above.
- Claim about Table 5 having identical rows: This is likely a parser artifact; removed per hard rules about formatting artifacts.
- Claim about Table 1 column headers ("minADE <sub>L</sub>"): Parser artifact. Removed.
- Criticism about "the paper does not analyze failure cases": Reasonable but speculative; moved to nice-to-have.
- Several generic strengths from the input review removed (e.g., "motivation is clearly communicated", "Figure 1's overview is helpful").

## Novel Insights

None beyond the paper's own contributions. The review's main insights reinforce what the paper already demonstrates: the train-val gap and spatial overlap issues are genuine and the proposed fixes are methodologically sound.

## Suggestions

1. Provide full architectural and training details for the boundary-free baseline in the main paper or a clearly referenced appendix — including the backbone architecture, the fusion mechanism, end-to-end training setup, and key hyperparameters (attention heads, sampling points, learning rates).
2. Add variance estimates (at least 3 seeds with standard deviations) for the main experimental results to establish statistical reliability.
3. Precisely specify the close/far threshold criterion (e.g., "agents whose current position falls within the 30×60m region centered on the ego vehicle").
4. Add at least one ablation of the boundary-free baseline (e.g., providing image features to all agents vs. far-only; comparing against a simpler signal such as distance-to-map-edge).

## Score and Decision

**Calibration Report:**

All anchors retrieved across all rounds:

| Anchor | Path | Avg Score | Round | Itemized? | Comparison to this paper |
|--------|------|-----------|-------|-----------|-------------------------|
| TSF Benchmark Fix | X8aFMdXk3N.md | 4.25 | Round 1 | Yes | Very similar type (identifying dataset/eval issues), but our paper has stronger evidence, broader evaluation (16 vs. 3 settings), and lighter negative-weighted criticisms. |
| Inductive KGC Benchmark | npBAHV5BJI.md | 7.00 | Round 1 | Yes | Similar in identifying benchmark flaws and proposing fixes, but executed more cleanly with deeper analysis. Our paper has a heavier weakness (baseline underspecification). |
| Training on Test Task | jOmk0uS1hl.md | 8.00 | Round 1 | Yes | Higher-quality paper with novel methodology and broad implications. Our paper is not at this level. |
| Redefining Bioactivity | S8gbnkCgxZ.md | 7.00 | Round 1 | Yes | Redefines a task with new dataset and protocol; larger scale and deeper analysis. |
| ESDMotion | sEJYPiVEt4.md | 5.25 | Round 2 | No | Motion prediction paper, different contribution type. |
| RedMotion | 72MSbSZtHv.md | 5.33 | Round 2 | No | Motion prediction model paper, different type. |
| SmartPretrain | Bmzv2Gch9v.md | 6.75 | Round 2 | No | Motion prediction representation learning, different type. |
| ITPNet | mDIXfHvoqH.md | 6.75 | Round 2 | No | Instantaneous trajectory prediction, different type. |

**Round 1 bracket:** [5.0, 6.5], established by comparing the paper's weighted-item profile against the closest methodology-match anchor (X8aFMdXk3N, 4.25 — lighter negative tail, stronger evidence) and the higher-quality benchmark-fix anchor (npBAHV5BJI, 7.00 — less polished, heavier single weakness).

**Weighted-item comparison:** The paper's strongest positive (+4.78 for train-val gap evidence) exceeds any positive in the 4.25 anchor and is comparable to the highest positives in the 7.00 anchor (~+5.00). Its strongest negative (-6.62 for baseline underspecification) is lighter than the 4.25 anchor's worst negatives (-10.35, -9.15, -8.83) but heavier than most negatives in the 7.00 anchor (whose worst is -6.96). The paper's other negatives (-2.52, -1.73, -1.55, -1.10) are substantially lighter than the 4.25 anchor's midweight criticisms. This places the paper clearly above 4.25 but below 7.00 — within the 5.0–6.5 bracket.

**Final score:** 6.0 — borderline accept. The core benchmark contributions (train-val gap, spatial overlap fix, metric refinements) are genuine, well-supported, and would benefit the community. However, the underspecified baseline — listed as a core contribution — and the lack of variance estimates prevent a stronger score. The paper needs revision on the baseline description and variance reporting, but the methodological contributions are solid.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>