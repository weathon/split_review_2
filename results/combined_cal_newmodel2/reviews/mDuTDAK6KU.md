Now I have sufficient calibration anchors. Let me compose the final review.

## Summary

This paper introduces KOALA, an adversarial detector that flags inputs when predictions from a KL-divergence-based nearest-prototype classifier and an L₀-based nearest-prototype classifier disagree. The approach is trained using only clean images, requires no adversarial training or architectural modifications, and is supported by a formal theorem specifying conditions under which detection is guaranteed. Experiments are conducted on ResNet-18/CIFAR-10 and CLIP/Tiny-ImageNet.

## Strengths

- **A genuinely novel detection principle (favorability=15.06).** The idea of using disagreement between KL-divergence and L₀-based nearest-prototype classifiers as an adversarial detection signal is creative and well-motivated (Section 3.1). The intuition that dense, low-amplitude perturbations are better captured by KL while sparse, high-impact changes are better captured by L₀ is sound and is not a rehash of existing detectors.

- **Training on clean images only (favorability=11.58).** KOALA requires only clean-image fine-tuning (no adversarial examples, no architectural changes), which is a genuine practical advantage over many prior detectors (Section 3.3). If the approach worked as advertised, this would be a meaningful contribution.

- **Formal theoretical analysis (favorability=10.61).** The paper provides a theorem (Theorem 1) with explicit conditions under which detection is guaranteed. This is more than most empirical detectors offer and provides a principled foundation for the approach.

- **Honest acknowledgment of the CLIP case (favorability=9.02).** The paper openly discusses (Section 4.3) that on CLIP/Tiny-ImageNet, the best detection rate comes from an objective that essentially degrades the model into random guessing — and correctly notes that high detection does not equal robustness. This transparency is welcome.

## Weaknesses

### Fatal
None.

### Major

- **Non-standard confusion matrix definitions conflate detection with classification.** The paper defines TP (for detection) as `[a=1] ∧ [(â,ŷ)=(1,⟂) ∨ (â,ŷ)=(0,y*)]`, where `(â,ŷ)=(0,y*)` means the detector did **not** flag an attack (â=0) but the classifier happened to output the correct class. This counts a failed detection as a "true positive" (Section 4.2, page 6). Conversely, FP includes `[a=0] ∧ [(â,ŷ)=(0,-y*)]` — a clean input that the detector correctly does not flag is counted as a "false positive" if the classifier misclassifies it. This means precision, recall, accuracy, and F1 do not measure pure detection performance; they measure a mixture of detection and classification correctness. Since all headline detection numbers in the abstract and Tables 1–2 use these definitions, the quantitative claims about detection performance are uninterpretable as standard detection metrics.

- **No comparison to any existing adversarial detector.** The paper cites a dozen prior detection methods in Section 2 (NIC, feature squeezing, LID, MagNet, Mahalanobis distance detector, CADet, Bayesian uncertainty detectors, etc.) and frames its contribution as addressing their limitations. Yet the experiments contain zero comparisons to any of them — the ablations only compare metric combinations within KOALA's own framework. Without baselines, it is impossible to assess whether KOALA outperforms, matches, or underperforms existing approaches.

- **The theoretical guarantee is highly conditional and compliance cannot be checked at inference time.** Theorem 1 guarantees detection only when sufficient inter-class prototype separation exists. On CLIP/Tiny-ImageNet, only 510–556 out of 5,000 test samples (~10%) satisfy these conditions (Table 1). The paper never explains how to determine whether a given input satisfies the theorem's conditions at inference time, since doing so requires knowing the true class. The practical relevance of a guarantee that covers only 10% of test samples and cannot be verified during deployment is unclear.

- **Detection evaluation only uses PGD.** Tables 1 and 2 report detection performance only under PGD attacks. CW and AutoAttack are listed in the experimental setup (Section 4.1) but only used for adversarial accuracy (Tables 3–4), not for detection metrics. A detector that works against PGD but fails against stronger attacks would not be practically useful.

### Minor

- **No statistical significance or variance reporting.** All results are point estimates from what appears to be a single run, with no standard deviations, confidence intervals, or significance tests. Given the small sample sizes for the theorem-compliant subset (e.g., 510 samples for CLIP), the perfect 1.0 scores on that subset could be artifacts of a single evaluation.

- **No sensitivity analysis for key hyperparameters.** The L₀ threshold τ=0.75 and smoothness parameter φ=0.5 are stated without discussion of how sensitive the results are to these choices. Similarly, the loss weight ratio ω_{L₀}=0.9, ω_{KL}=0.1 is not ablated.

- **Norm mismatch between theory and experiments.** Assumption A2 specifies a generic norm-bound ∥δ∥ ≤ ε without specifying which norm, while experiments use ℓ∞ perturbations. The paper does not establish the connection between the norm used in the theory and the norm used in experiments, making it unclear how the theorem's conditions relate to the empirical evaluation.

### Trivial
None.

## Nice-to-Haves

- Adaptive attacks are not considered. An adversary aware of KOALA's detection mechanism could potentially craft perturbations that fool both metrics simultaneously. Addressing this would strengthen the practical claims, though it is not a core requirement for a first presentation of the method.
- Reporting the standard false positive rate on clean data (fraction of clean images that trigger â=1) would help interpret the detection results.

## Removed Points

These points are flagged to be removed, treat them with caution:
- "The proof sketch contains a gap in reasoning" → The complete proof is in the appendix (stripped from the reviewed version). Without access to the full proof, this criticism cannot be verified.
- "Section 4.4 conflates detection vs. robust classification" → The paper explicitly states "This experiment moves beyond attack detection metrics to evaluate the overall classification robustness." This is factually incorrect upon verification.
- "KL divergence direction choice not discussed" → Trivial methodological detail; removed per hard rules.
- "Number of fine-tuning epochs not specified" → Removed per hard rules about trivial implementation details.
- "Adaptive attacks not considered" → Moved to Nice-to-Haves.
- "Missing related works" → Removed per hard rules (reviewer could be making things up).
- Formatting/style complaints → These are parser artifacts, not author errors.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Recompute all detection metrics using standard definitions (TP = â=1 ∧ a=1; FP = â=1 ∧ a=0; FN = â=0 ∧ a=1; TN = â=0 ∧ a=0). Compare these to the current numbers to demonstrate the gap.
2. Add comparisons to at least 2–3 representative prior detectors (e.g., Mahalanobis distance detector (Lee et al., 2018), LID (Ma et al., 2018), feature squeezing (Xu et al., 2018)) under the same attack settings.
3. Report detection results against AutoAttack and CW, not just PGD.
4. Clarify how theorem-compliance can be determined at inference time, or explicitly acknowledge this limitation.
5. Add variance estimates (multiple runs or bootstrap confidence intervals) for the main results.
6. Provide sensitivity analysis for τ, φ, and the loss weight ratio.

## Score and Decision

**Calibration Anchors (all rounds):**

| Anchor | Avg Score | Round | Itemized | Comparison |
|--------|-----------|-------|----------|------------|
| kz78RIVL7G (Compressive sensing detection) | 2.60 | Round 1 | Yes | Lower novelty, weaker attacks, no adaptive eval — but at least reported standard metrics. KOALA's core idea is stronger, but evaluation is less sound. |
| KAWlH5pfQu (Detecting Adversarial Examples) | 3.00 | Round 1 | Yes | Had flawed theoretical claims and no adaptive attacks. KOALA has a stronger theory but comparable evaluation gaps. |
| EWP9BVRRbA (NEARSIDE) | 4.00 | Round 2 | Yes | Adversarial detection for VLMs with limited baselines (1 baseline). KOALA has zero baselines — evaluation is worse. |
| J2we1sVd9m (POT OOD) | 4.60 | Round 2 | Yes | Comprehensive baselines (21 methods) but impractical assumptions. KOALA's evaluation is less comprehensive. |
| RzdtpxL0H5 (DDAD) | 6.20 | Round 1 | Yes | Theory + baselines + multiple datasets. KOALA falls well short on evaluation completeness. |

**Round 1 bracket:** 3.0–5.5 (based on similarity to rejected detection papers with evaluation gaps).

**Round 2 narrowing:** Comparing item-level favorability ratings, KOALA's major weaknesses (metric definitions: -1.94, no baselines: -3.22, conditional theory: -3.65, PGD-only: -0.41) are all more negative than the typical weaknesses of the 4.0-range anchor (NEARSIDE, which had only "limited baselines" complaints). The most damaging items are the non-standard metrics and missing baselines — two issues that the 4.0–5.0 anchors did not suffer from simultaneously. This pulls KOALA below DDAD (6.20) and below POT (4.60). The novel core idea provides a floor above the 2–3 range papers.

**Final score:** 4.0 — the core idea is creative and well-motivated, and the theoretical analysis is a genuine contribution, but the evaluation is fundamentally compromised by non-standard metrics that make the headline detection numbers uninterpretable, the absence of any baseline comparisons, and detection results limited to a single attack type. Significant revisions to the evaluation methodology would be required before the paper's claims can be assessed.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>