Now let me write the final consolidated review.

## Summary

2-3 sentence summary of the paper's contribution.

## Strengths

- strength 1 with evidence
- strength 2 with evidence
- ...

## Weaknesses

### Fatal

### Major

### Minor

### Trivial

## Nice-to-Haves

## Removed Points

## Novel Insights

## Suggestions

## Score and Decision

Let me produce the review now.

---

Actually, after careful analysis, I want to re-examine whether the non-standard metrics criticism is as severe as the reviewer claims. Let me re-read the confusion matrix carefully.

The paper defines:
- TP = attacked AND (detected as attack OR not detected but correctly classified)
- FP = clean AND (detected as attack OR not detected but misclassified)

This is indeed non-standard. In standard detection evaluation:
- TP = attacked AND detected
- FP = clean AND detected (false alarm)
- TN = clean AND not detected
- FN = attacked AND not detected (missed)

The paper's definition adds:
- An undetected attacked image that is correctly classified counts as TP (normally it would be FN)
- A clean image that is misclassified by the classifier but not flagged by detector counts as FP (normally it would be TN)

This means the metrics are inflated by the classifier's performance. The reviewer is right that this is non-standard and potentially misleading.

However, I should note that KOALA's architecture couples detection with classification (when it doesn't detect an attack, it produces a class prediction). So there's an argument that system-level evaluation makes sense. But standard detection metrics should also be reported.

Let me also check: the reviewer says "A detector that never flags anything but is paired with a robust classifier could appear to have high precision and recall under this scheme." Let me verify: if the detector never flags (always â=0), then for attacked images: TP requires (â, ŷ) = (0, y*), meaning the classifier must correctly classify the attacked image. So all attacked images that are correctly classified count as TP, and all attacked images that are misclassified count as FN. That would mean recall = accuracy of the classifier on attacked images. For clean images: FP requires (â, ŷ) = (0, -y*), meaning the classifier must misclassify the clean image. So clean images correctly classified are TN, clean images misclassified are FP. This is essentially treating the classifier's performance as detection performance.

Yes, the reviewer's concern is valid. A detector that never fires would have detection performance equal to the classifier's accuracy, which inflates the actual detection capability.

Now, let me finalize and write the review.## Summary

This paper proposes KOALA, a reactive adversarial detector that flags inputs when two complementary similarity metrics — KL divergence and an L₀-based distance — disagree on the predicted class in a nearest-prototype classifier. The authors provide a formal proof of correctness establishing conditions under which detection is guaranteed, and validate the method on ResNet/CIFAR-10 and CLIP/Tiny-ImageNet using PGD, CW, and AutoAttack.

## Strengths

1. **Formal theoretical grounding.** The paper provides a theorem with stated assumptions (A1–A4) and a proof sketch showing that, under sufficient inter-class prototype separation, no bounded perturbation can simultaneously flip both the KL-based and L₀-based predictions, forcing a detectable disagreement. This level of theoretical formality is rare in the adversarial detection literature, where most prior methods rely on purely empirical heuristics.

2. **Lightweight training requirement.** KOALA requires only fine-tuning the backbone encoder with clean images using a composite loss; it does not require adversarial training, architectural modifications, or access to attack data during training. This is a genuine practical advantage over methods that must retrain on specific threat models.

3. **Clean empirical validation of the theorem.** On the subset of samples satisfying the theorem's conditions (Table 1), KOALA achieves perfect precision, recall, accuracy, and F1 (all 1.0) across both model/dataset pairs and both perturbation budgets. This cleanly demonstrates that *when the conditions hold, the guarantee works as advertised*.

## Weaknesses

### Major

1. **No empirical comparison to any existing adversarial detector.** The Related Work section (Section 2) surveys a broad landscape of prior detection methods — MagNet, LID, Mahalanobis, Feature Squeezing, NIC, CADet, Bayesian uncertainty, and others — and criticizes them for lacking formal guarantees. Yet every reported experiment (Tables 1–4) compares only among KOALA variants (different metric combinations) or against the raw unmodified backbone. There is no measurement against a single prior detection method. A paper that motivates itself by identifying gaps in prior work must benchmark against that prior work to establish whether its formal guarantees translate into competitive empirical performance. Without this, the experimental contribution is uncalibrated against the literature the paper itself surveys.

2. **Non-standard evaluation metrics conflate detection with classification.** The confusion matrix defined in Section 4.2 treats an attacked input that is *not detected* but *correctly classified* as a True Positive, and a clean input that is *not flagged* but *misclassified* as a False Positive. This is non-standard for adversarial detection, where the standard protocol reports TPR (fraction of attacks flagged) and FPR (fraction of clean inputs falsely flagged) independently of the classifier's accuracy. Under the paper's formulation, a detector that never fires would inherit the classifier's accuracy as its detection metrics, inflating apparent performance. The reported numbers in Tables 1–2 may therefore reflect the robustness of the underlying classifier as much as the detector's actual discriminative ability. Standard detection metrics (TPR, FPR, ROC/AUC for the detector alone) should be reported alongside the current system-level metrics.

### Minor

3. **Theorem's conditions met for a small fraction of test samples on CLIP/Tiny-ImageNet.** From Table 1, only 510–556 out of ~5,000 test samples (≈10–11%) satisfy the theorem's conditions on CLIP/Tiny-ImageNet. On the remaining 89–90% of data — where the theorem does not apply — detection performance is modest: accuracy 0.65–0.67, precision 0.62–0.63 (meaning ≈37–38% of "attack" flags are false alarms). The paper's strongest claim — "detection is not a probabilistic outcome but a mathematical certainty" — applies rigorously only to a small minority of samples in one of the two experimental settings. The paper should be upfront about this scope limitation and discuss when the required conditions are likely to be met in practice.

4. **Disconnect between theoretical assumptions and experimental validation.** Assumption A2 bounds the perturbation in *feature space* (∥δ∥ ≤ ε), but all experiments constrain attacks in *input space* using ℓ∞ bounds (ε ∈ {2/255, 4/255}). The paper states this follows from Lipschitz continuity of the backbone encoder, but no Lipschitz constant is estimated or provided. Without quantifying the mapping from input-space to feature-space perturbation bounds, the experimental validation does not directly test the theorem's stated conditions. The paper should either estimate the Lipschitz constant or design experiments that explicitly control feature-space perturbations.

5. **Detection experiments evaluated only under PGD attacks.** The primary detection validation (Table 1) uses only PGD attacks. CW and AutoAttack are used only in the adversarial accuracy experiments (Tables 3–4), not for detection. A paper offering a formal guarantee of detection should demonstrate that detection holds across diverse attack types, including adaptive attacks designed to evade detection. The absence of this evidence limits the generality of the empirical claims.

6. **CLIP results partially undermine universality claims.** On CLIP/Tiny-ImageNet, the three-metric combination KL+L₀+Cosine outperforms the proposed KL+L₀ on detection accuracy (0.75 vs. 0.71), recall (0.94 vs. 0.85), and F1 (0.79 vs. 0.74) in Table 2. The paper explains this as an artifact where "all three metrics are essentially 'randomly guessing'" — a speculative post-hoc explanation not backed by evidence (e.g., examining prediction distributions). Additionally, Table 4 shows that L₀-only and KL-only individually achieve higher adversarial accuracy than KL+L₀ on CLIP across multiple attack types. The paper attributes this to CLIP's pre-training structure, but this means the method's claimed complementarity advantage is architecture-dependent, which should be more explicitly acknowledged and analyzed.

7. **Missing methodological detail on the theorem-compliant subset.** The paper partitions test samples into theorem-compliant and non-compliant groups but does not explain how this partition is operationalized — specifically, how Γ_i(ε) (the threshold in Theorem 1) is computed in practice. This is a critical reproducibility detail that should be stated in the main text.

### Trivial

None.

## Nice-to-Haves

- **Ablation on the L₀ threshold τ** (currently 0.75). This parameter directly controls what the L₀ metric counts as a "perturbed" dimension and therefore affects both classification and detection. Its sensitivity should be explored.
- **Ablation on the loss weights** (ω_L₀ = 0.9, ω_KL = 0.1). The heavy skew toward L₀ could mean the KL metric is undertrained, and the sensitivity of detection to this ratio should be reported.
- **Reporting standard ROC curves** (TPR vs. FPR for the detector alone) would complement the system-level metrics and enable calibration against the broader detection literature.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"L₀ 'distance' is not a proper metric."** The paper defines L₀(·) as a thresholded count, which is a working definition, not a claim of metric axioms. The reviewer's observation is technically correct but does not affect the validity of the method or results.
- **Criticisms about missing appendix content or absent references.** The appendix and reference list are stripped by the parsing process; these exist in the original submission. Per policy, such criticisms are removed.
- **"Related Work functions as contrastive framing rather than meaningful positioning."** This observation is absorbed into Weakness #1 (no baselines), which is the concrete empirical gap. The broader framing complaint adds no actionable information beyond that.
- **Generic reproducibility nitpicks (trivial implementation details, training logs).** These do not constitute substantive weaknesses.
- **Speculative criticisms that depend on information not in the paper** (e.g., "if the normalization were X, the reported values would be impossible"). No such claims survived verification against the paper as written.

## Novel Insights

The harsh review surfaces one insight that goes beyond the paper's own framing: the non-standard confusion matrix means the reported detection numbers are system-level metrics (detector + classifier combined), not detector-only metrics. This distinction matters because the paper's claims are about *detection*, yet the evaluation conflates detection with classification. An unsuspecting reader comparing these numbers to standard detection benchmarks would be misled. The review's identification of this conflation is the most critical observation for the authors to address, above even the missing baselines, because it affects the interpretation of every reported number.

## Suggestions

1. **Add at least 2–3 prior detection baselines** (e.g., Mahalanobis-based detection, LID, Feature Squeezing) on the same models and datasets. This is the single most important addition to establish empirical competitiveness.
2. **Report standard detection metrics** (TPR, FPR for the detector alone, independent of the classifier's label prediction) alongside or instead of the current confusion matrix. A ROC curve would be ideal.
3. **Explicitly state the operational procedure** for partitioning compliant/non-compliant samples, including how Γ_i(ε) is computed.
4. **Extend detection experiments to CW and AutoAttack**, and ideally to an adaptive attack designed to evade KOALA's specific disagreement criterion.
5. **Estimate or bound the Lipschitz constant** of the backbone encoder to connect the input-space ℓ∞ budget to the feature-space ∥δ∥ ≤ ε assumed in the theorem.

## Score and Decision

The paper introduces a well-motivated and theoretically-grounded detection paradigm — the idea of using complementary metric disagreement with formal guarantees is genuinely novel and rare in this space. The lightweight training requirement and clean proof-of-concept on the theorem-compliant subset demonstrate the idea's viability.

However, the paper has two decisive empirical gaps in its current form: (1) no comparison to any existing detection method, rendering the experimental contribution uncalibrated against the literature the paper itself surveys, and (2) a non-standard evaluation protocol that conflates detection with classification, making the reported numbers difficult to interpret or compare. These gaps prevent the paper from establishing that KOALA is competitive with prior approaches, which is necessary for acceptance in this venue. The theoretical framework is a worthwhile contribution, but the empirical validation needs substantial strengthening.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>