Now I have all the information I need. Let me compile the final review with calibrated score.

**Round-1 bracket analysis:** The paper sits between reject-range anchors (4.00-4.50 for SFDA-TAD and PrAViC) and accept-range anchors (5.67-6.00 for CLDyB, EgoVideo, and continual anomaly detection). The paper is stronger than the 4.00-4.50 anchors (which have severe novelty/evaluation problems) and weaker than the 6.00 EgoVideo anchor (which has SOTA performance and stronger method validation).

**Final score: 5.5** — The task formulation and dataset are genuine contributions with high model-assigned weights (9.14, 8.40, 8.04, 7.85). The insufficient baselines (-3.21) are the main drag, but this is less severe than the -5.34 weakness in the 5.71-scored continual anomaly detection paper. The paper is transparent and its ablation is honest. It belongs in the borderline-accept range.

---

## Summary

This paper introduces **Continuous Online Action Detection (COAD)**, a new task formulation where OAD models not only detect actions in real time from streaming video but also continuously adapt via single-pass training without storing data. It also contributes **Ego-OAD**, a large-scale egocentric OAD benchmark (263 hours, 22,991 instances, 87 classes) curated from Ego4D. The proposed method combines orthogonal gradient projection, non-uniform loss weighting, and state continuity to balance adaptation to individual users with generalization to unseen environments.

## Strengths

- **Well-motivated task formulation.** COAD addresses a genuine gap: existing OAD models are trained offline and cannot adapt to individual users or environments after deployment. The connection to wearable/egocentric devices is concrete and well-argued (Section 1). [weight=7.85]
- **Substantial dataset contribution.** Ego-OAD (Section 3) fills a real void — the first large-scale egocentric OAD benchmark. At 263 hours, 22,991 labeled instances, 87 classes, drawn from Ego4D's diverse scenarios, it is substantially larger and more diverse than any prior egocentric OAD resource. The curation procedure is reasonable and documented. [weight=9.14]
- **Clean evaluation protocol.** The three-way split into pretraining / in-stream / out-of-stream sets (following Carreira et al. 2024a) cleanly separates adaptation to the current stream from generalization to unseen data. The IID training upper bound in Fig. 4 provides useful context. [weight=8.40]
- **Honest ablation study.** Table 3 fully ablates the three COAD components and reports all combinations, including the revealing result that non-uniform loss (adapted from prior work) contributes the most. The paper does not hide which components drive the results. [weight=8.04]

## Weaknesses

### Fatal
None.

### Major

1. **Insufficient baselines for method validation.** [weight=-3.21] The method is compared against only two baselines: a frozen pretrained model and naive single-pass SGD without any regularization ("w/o COAD"). Neither is a serious continual learning baseline — w/o COAD is essentially continuous SGD without stabilization, which is known to cause catastrophic forgetting. There are no comparisons to standard continual learning methods (e.g., EWC, online EWC, LwF, small replay buffer) or other OAD architectures (LSTR, TeSTra, GateHub) adapted to the streaming setting. Since the core claim is that COAD's specific ingredients provide effective online adaptation, the experimental design does not allow readers to assess whether comparably simple continual learning strategies would match or exceed these numbers. The task formulation and dataset are valuable independently, but the method evaluation is incomplete.

### Minor

2. **No variance or statistical significance information.** [weight=5.54] Every result in Tables 1–4 and all figures appears to come from a single run. Without variance estimates, the reliability of reported differences (e.g., COAD 26.0 vs. w/o COAD 25.5 mAP on out-of-stream with Ego pretraining) is unclear. In several settings the margins between COAD and w/o COAD are small, making this a meaningful omission even though single-run evaluation is common in large-scale CV benchmarks.

### Trivial
None.

## Nice-to-Haves

- Add at least 2–3 standard continual learning baselines (EWC, online EWC, or a small replay buffer) to validate whether COAD's specific design choices matter beyond any reasonable online adaptation strategy.
- Report results over multiple seeds (≥3) with mean and std, especially for settings with small margins.
- Include basic computational cost analysis (wall-clock time, relative FLOPs) to substantiate the wearable deployment motivation.
- Reframe the in-stream results more explicitly as an adaptation-generalization trade-off.

## Removed Points

These points were raised by the harsh critic but are removed after filtering:

- "In-stream framing could be more balanced" — The paper transparently reports all numbers and acknowledges the trade-off in Section 5.3. Removed as the model weight (6.09) indicates it is not a weakness.
- "EPIC-KITCHENS results show limited generality" — The paper acknowledges this limitation in Section 5.3. Removed (model weight 2.92).
- "No computational cost analysis" — Valid suggestion but model weight (2.42) indicates not a weakness; moved to nice-to-haves.
- "Orthogonal gradient projection is only local" — Factually correct but transparently described; model weight (2.49) indicates not a weakness.
- "Sparsity benefit claimed but not evaluated" — Model weight (-0.34) is near-neutral.
- "Ego-OAD dataset characterization is limited" — Model weight (2.71) indicates not a weakness.
- "Most novel component contributes modestly" — The honest ablation is a strength, not a weakness.

## Novel Insights

The reviews collectively reveal that this paper's strongest value is in the COAD **task formulation** and the **Ego-OAD dataset**, which are ready for publication. The method evaluation is the weakest link: the baselines are too sparse to validate whether COAD's specific design choices matter beyond any reasonable online adaptation strategy. However, the paper is transparent about its results and ablations, and the task+dataset contributions stand independently of the method's ultimate superiority over all possible alternatives.

## Suggestions

- **Add continual learning baselines** (EWC, online EWC, or a small replay buffer) to the experimental comparison. This is the single highest-leverage change and would address the main weakness.
- **Report multi-seed results** with standard deviations.
- **Include computational cost analysis** (FLOPs, latency, memory) to substantiate the wearable deployment motivation.

## Score and Decision

**Calibration summary:**

| Anchor | Avg Score | Round | Itemized? | Comparison |
|--------|-----------|-------|-----------|------------|
| Y7jJN0VQ4y (continual anomaly detection) | 5.71 | R1 | Yes | Similar structure (new task + method), but our dataset contribution is stronger (9.14 vs 8.68) and our main weakness is less severe (-3.21 vs -5.34). Slightly above this anchor. |
| 1L52bHEL5d (TTA for egocentric) | 6.00 | R1 | Yes | Stronger overall — has repeated trials with std (9.33) and comprehensive baselines. Below this anchor. |
| o8SPZJaJyj (SFDA for TAD) | 4.00 | R1 | Yes | Much weaker — limited novelty (-4.57), not task-specific (-2.93). Our paper is clearly stronger. |
| P6G1Z6jkf3 (EgoVideo) | 6.00 | R2 | Yes | Stronger top items (10.68, 10.04) and less severe weaknesses (-2.15). Our paper is below this anchor. |
| RnxwxGXxex (CLDyB benchmark) | 5.67 | R2 | Yes | Stronger top items (10.35, 9.65). Our paper is slightly below. |
| 7L2bpe7lfm (video continual learning) | 4.50 | R2 | No | Weaker than our paper. |

**Weighted-item comparison:** Our strongest items (dataset 9.14, evaluation 8.40, ablation 8.04) are strong but not as dominant as EgoVideo's top items (10.68, 10.04). Our main drag (-3.21 for baselines) is material but less severe than Y7jJN0VQ4y's worst (-5.34). Comparing to CLDyB (5.67), our paper has similar contribution type (task+data) with a somewhat more significant method evaluation gap.

**Final placement:** Above 5.71 (Y7jJN0VQ4y) due to stronger dataset and less severe weakness, but below 6.00 (EgoVideo, 1L52bHEL5d) due to weaker method validation. The paper's contributions (new task + large benchmark) are publishable, but the method claims need stronger empirical support.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>