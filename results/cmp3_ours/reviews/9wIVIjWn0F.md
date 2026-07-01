Now I have all the calibration data I need. Let me write the final consolidated review.

**Calibration Round 1 (Bracketing):**
- Strong reject band (score < 1.5): Lower-quality papers that are clearly flawed or off-topic (avg 0.5-1.0)
- Low band (1.5-3.5): Papers with limited novelty, minor improvements, poor writing — e.g., Active TPT (2.50), MP-TPT (3.67)
- Mid-low band (3.5-5.5): Papers with solid ideas but significant gaps — e.g., ROSITA (4.67), BAT-CLIP (5.50)
- Mid-high band (5.5-7.5): Borderline accept to accept — ML-TTA (6.25, Accept), RLCF (6.67, Accept), DOTA (6.00, Reject)
- High band (7.5-8.5): Strong clear accepts

RTA sits in the 4-6 range. It's better than MP-TPT (3.67) and Active TPT (2.50) — these had limited novelty or poor execution. But RTA has more significant structural issues than ML-TTA (6.25) and RLCF (6.67), which were accepted with presentation-level concerns. RTA's weaknesses (pseudo-LCE target mismatch, missing key ablations, unexplained multi-label extension) are methodological gaps, not presentation issues. This puts it closer to BAT-CLIP (5.50, Reject) which also had structural concerns, albeit different ones.

**Narrowing:** The paper's core idea (regression-based view selection) is genuinely novel and the evaluation breadth is impressive. However, the three major weaknesses — particularly the disconnection between the motivating LCE ceiling and the actual pseudo-LCE regression, and the complete lack of multi-label method specification — are significant enough to place it at the boundary.

**Final: Score 5.0, Reject.**

## Summary

This paper proposes Regression-based Test-Time Adaptation (RTA), which trains a lightweight LightGBM regressor on pseudo-labeled data to predict view quality (as cross-entropy loss), then selects test-time augmented views with the lowest predicted loss. The method is motivated by a "Ceiling TTA" analysis showing that ground-truth label cross-entropy (LCE) for view selection far outperforms entropy-based selection. Experiments span 5 ImageNet variants, 10 cross-domain datasets, and 3 multi-label datasets, with consistent improvements over prior TTA methods.

## Strengths

1. **Informative ceiling analysis (Section 4.1, Tables 1-2).** The LCE ceiling quantifies the headroom available in view selection — e.g., 64.3% → 90.2% on ImageNet-A with ViT-B/16. This is a clear, honest upper bound that the research community can build on.

2. **Broad and consistent empirical evaluation.** RTA is tested on two backbones (RN50, ViT-B/16) across 5 ImageNet variants, 10 cross-domain datasets, and 3 multi-label datasets. Across nearly all conditions, RTA achieves the best or tied result with directionally consistent improvements. The cross-domain results (Table 4) are particularly valuable for demonstrating generalization.

3. **Computational efficiency.** The regression model is a shallow LightGBM tree (depth 5, 16 leaves), trained once offline on 1,000 samples and applied without updates at test time. This adds negligible overhead compared to methods requiring per-instance prompt tuning, diffusion inference, or memory banks.

## Weaknesses

### Major

1. **The regression target (pseudo-LCE) does not match the motivating analysis (true LCE), and this gap is unaddressed.** The paper's core motivation (Section 4.1) uses ground-truth LCE to establish a dramatic ceiling. However, the actual regression model is trained on **pseudo-LCE** (Eq. 4): `-log(p(ŷ|x))` where ŷ is CLIP's argmax prediction on samples where CLIP's confidence ≥ 0.8. This is fundamentally a function of CLIP's own self-confidence, not of prediction correctness — a sample where CLIP confidently predicts the wrong class gets the same pseudo-LCE as one where it correctly predicts the right class. The paper never acknowledges this disconnect, nor analyzes why RTA captures only a small fraction of the LCE ceiling's headroom (e.g., 65.65% vs. 90.2% on ImageNet-A). The reader cannot tell whether the gap stems from the pseudo-labeling bottleneck, the regression approximation error, or a more fundamental issue.

2. **No ablation against simple confidence-based view selection.** Pseudo-LCE (`-log(p_max)`) is a monotonic function of CLIP's maximum softmax probability. The paper does not compare RTA against a baseline that simply selects views by `p_max`, nor against a version of RTA that uses entropy as the regression target. Without these ablations, it is impossible to determine whether the regression model provides a genuinely better view-quality metric, or whether the observed gains largely stem from the broader training data (ImageVal-12k). The claim that RTA "eliminates complex algorithmic designs" (Contribution 2) is undercut if a simple confidence threshold would perform similarly.

3. **Multi-label extension is completely unspecified.** Multi-label results are presented as a contribution (Tables 5-6, outperforming ML-TTA on MSCOCO, VOC2007, NUSWIDE). However, the entire method description (Section 4.1-4.3, Algorithms 1-2) is written for single-label classification: Eq. (4) defines cross-entropy with respect to a single class index, and Algorithm 1 assumes a single pseudo-label per sample. How the regression target, pseudo-label generation, and view selection are adapted for per-class binary predictions is never explained. This undermines the credibility of the multi-label results entirely.

### Minor

4. **No variance reporting.** The paper does not report standard deviations or confidence intervals for any experiment. TTA methods involve stochastic augmentations; many ViT-B/16 improvements are small (IN-1k: +0.24%, IN-V2: +0.32%, IN-R: +0.23%). Without variance estimates, these marginal gains are uninterpretable.

5. **Training-test distribution shift in the regression model.** The regression model is trained on logits from **original (non-augmented)** images (Section 4.2: "we only need to learn the regression mapping function based on the original image"), but applied to logits of **augmented views** at test time. Augmented views produced by random crops and color jitter have systematically different logit distributions. The paper does not analyze whether the logit-to-loss mapping is invariant to these augmentations.

6. **Training data overlap with test benchmarks.** The regression data (ImageVal-12k) comes from ImageNet's validation set, and several test benchmarks (IN-V2, IN-R, IN-A, IN-Sketch) share ImageNet's label space. The cross-domain results (Table 4) partially mitigate this, but the claim of "independence from any downstream classification task" (Section 5.1) is overstated given this overlap.

### Trivial

7. The Spearman correlation analysis (Figure 3) does not specify which 10 of the 1,000 logit features are selected, nor whether the same features are consistently predictive across datasets.

## Nice-to-Haves

- An ablation comparing RTA against a simple confidence-threshold-based view selector (using `p_max` directly).
- An ablation using entropy instead of pseudo-LCE as the regression target, to isolate the benefit of the specific regression formulation.
- A scatter plot of predicted pseudo-LCE vs. actual pseudo-LCE (and vs. true LCE on labeled data) to validate regression fit quality.
- An explicit explanation of the multi-label adaptation (pseudo-label generation per class, regression target definition, ensemble strategy).
- An analysis of the pseudo-label confidence threshold (currently 0.8).

## Removed Points
These points from the input review were removed with justification:

- **"RTA captures only a fraction of the LCE ceiling headroom" as a standalone weakness:** The LCE ceiling is an oracle using ground-truth labels; no real method should be expected to match it. This is a non-criticism on its own. However, the deeper concern about the pseudo-LCE vs. true LCE disconnect is retained in Major Weakness 1.
- **"The paper should have a limitations section":** Many papers at comparable venues lack a separate limitations section. Downgraded from the input, as this is a formatting preference rather than a substantive weakness.
- **Missing related work / reference concerns:** Per policy, all cited references are assumed to exist. Removed.
- **Generic presentation and formatting nitpicks:** Parser artifacts and style preferences removed per policy.
- **Speculation about "could the method work on medical images":** The paper explicitly scopes to natural image benchmarks; speculation about out-of-scope domains is removed.

## Novel Insights
None beyond the paper's own contributions. The harsh critic's observation that pseudo-LCE is essentially a function of CLIP's self-confidence (not of true label correctness) is the most substantive concern raised, and it points to a gap between the paper's motivating analysis and its actual operational mechanism.

## Suggestions

1. **Abandon the "predicting cross-entropy loss" framing** and instead honestly characterize the method as "predicting CLIP's self-confidence on pseudo-labeled data." Add a controlled comparison against confidence-based (`p_max`) view selection to validate that the regression model adds value beyond the training data.
2. **Specify the multi-label extension** — including how pseudo-labels are generated per class and how the regression target is defined for per-class binary predictions — or remove the multi-label results.
3. **Report standard deviations** over at least 3 random seeds for the main comparisons, especially where gains are small.
4. **Validate the regression fit** with a correlation analysis (predicted vs. actual values) on held-out data.
5. **Discuss the gap** between the LCE ceiling and RTA's actual performance, and why pseudo-LCE is a reasonable proxy despite the fundamental difference from true LCE.

## Score and Decision

**Calibration Anchors (all rounds):**

| Anchor | Avg Human Score | Round | Comparison |
|--------|--------|-------|------------|
| ML-TTA (75PhjtbBdr) | 6.25 | R1, R2 | Accept. Clear method, mostly presentation-level weaknesses. RTA has a more novel core idea but more structural gaps. |
| RLCF / CLIP Reward (kIP0duasBb) | 6.67 | R1 | Accept. Incremental but clearly explained. RTA has broader evaluation but weaker methodological grounding. |
| DOTA (yD2JMeKumt) | 6.00 | R1, R2 | Reject. Had methodological clarity issues. RTA is comparable in quality but with different weaknesses. |
| BAT-CLIP (z7PhIgVmZU) | 5.50 | R2 | Reject. Had a fatal flaw controversy (label leakage). RTA has no fatal flaw but 3 significant major issues. |
| ROSITA (lF9QXpfNHm) | 4.67 | R1 | Reject. Missing backbones, no error bars. RTA is stronger empirically. |
| MP-TPT (0Xc6o1HKXD) | 3.67 | R1 | Reject. Limited novelty, poor writing. RTA is substantially stronger. |
| Selective Label Enhancement (3Z2flzXzBY) | 6.40 | R2 | Accept. Similar TTA topic, clearer method articulation. |
| Active TPT (pdzHpQbGrn) | 2.50 | R1 | Reject. Minimal improvements, incremental. RTA is clearly better. |

**Round 1 bracket:** 4.0 – 6.0. RTA is stronger than the clearly rejected papers (3-4 range) but has more significant structural issues than the accepted papers (6+ range).

**Narrowing:** The paper's core idea (regression-based view selection) is genuinely novel and the evaluation is admirably broad. However, the three major weaknesses are substantive: the disconnect between the motivating LCE ceiling and the actual pseudo-LCE target is never acknowledged or analyzed; the lack of ablations against confidence-based selection makes the core mechanism's contribution unclear; and the multi-label results are presented without any methodological explanation. These gaps prevent the paper from meeting the bar for acceptance.

**Final Score: 5.0 — Final Decision: Reject**

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>