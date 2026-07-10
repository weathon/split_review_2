Now let me compile everything into the final review.

## Summary

KOALA proposes an adversarial example detector that flags inputs when two complementary nearest-prototype classifiers — one using KL divergence and one using an L0-based similarity — disagree on the predicted class. The paper provides a formal proof showing that under bounded perturbations and sufficient class-prototype separation, no single perturbation can simultaneously fool both metrics, forcing disagreement and enabling guaranteed detection. The method requires only fine-tuning on clean images, with no adversarial training or architectural changes.

## Strengths

- **Novel and well-motivated core idea (Section 3.1, Figure 1).** The observation that bounded adversarial perturbations can be either sparse/high-impact or dense/low-amplitude, and that these regimes are naturally captured by different similarity metrics, is genuinely clever. Using *disagreement* between KL and L0 predictions as a detection signal — rather than requiring knowledge of the true class — is a principled and novel approach that cleanly sidesteps the need for a reference "correct" prediction.

- **Theoretical ambitions (Section 3.2, Theorem 1).** Providing a formal proof of correctness with explicit conditions under which detection is guaranteed is rare in the adversarial detection literature and genuinely distinguishes KOALA from purely empirical detectors (MagNet, LID, Mahalanobis, feature squeezing, etc.). Whether the full proof in the appendix holds up, the attempt at formal guarantees is a meaningful differentiator.

- **Lightweight training requirement.** The method fine-tunes only on clean images, requires no adversarial training, and does not modify the underlying architecture. This makes it computationally practical for deployment on existing models (Sections 3.1, 3.3).

## Weaknesses

### Major

- **Non-standard confusion matrix definition (Section 4.2, lines 188-191).** The paper defines:
  - TP := [a=1] ∧ [(â, ŷ) = (1, ⊥) ∨ (â, ŷ) = (0, y*)]
  - FN := [a=1] ∧ [(â, ŷ) = (0, -y*)]
  
  Under standard detection evaluation, an attacked input (a=1) that is not flagged (â=0) is a **false negative** regardless of whether the classifier happens to predict the correct class. The paper's definition instead counts such cases as true positives. This inflates recall and makes all reported metrics (Tables 1, 2) incomparable with every prior detection method. The paper does not acknowledge this deviation from standard practice or justify it. While the theorem-compliant subset results (where the theory guarantees â=1 for attacked inputs) are likely robust under standard definitions, the overall results (0.94 precision, 0.81 recall on ResNet/CIFAR-10) and non-compliant subset results could be substantially different under standard metrics.

- **No comparison against existing detection methods.** The paper surveys prior detectors in Section 2 (MagNet, feature squeezing, LID, Mahalanobis, CADet, NIC, etc.) but never compares KOALA against a single baseline. Without external baselines, the reader cannot determine whether KOALA's reported performance represents an advance over the state of the art. The ablation study (Table 2) compares metric combinations within the KOALA framework, which is informative but does not substitute for external comparison.

- **Limited threat model evaluation for detection.** The detection experiments (Tables 1 and 2) evaluate only against PGD attacks. CW and AutoAttack are mentioned in Section 4.1 but appear only in Experiment 3 (which measures classification robustness, not detection). No adaptive attacks designed to bypass the specific KL/L0 disagreement criterion are tested — despite the paper noting (Section 2) that prior detectors can degrade under adaptive attacks. Given that the theorem guarantees apply to any norm-bounded perturbation, validating detection against a broader attack suite is essential.

### Minor

- **The "theorem-compliant" partitioning is not operationalized in the main paper.** No threshold Γ_i(ε) is specified, and no description is given of how the sufficient inter-class prototype separation condition is checked. While the appendix may contain these details, the main paper should provide enough information for reproducibility.

- **Unclear relationship between the theory's energy bound and experimental ℓ∞ attacks.** Figure 1 and the proof sketch frame the perturbation bound as an ℓ₂/energy bound (‖δ‖₂ ≤ ε), while Assumption A2 leaves the norm unspecified. All experiments use ℓ∞-bounded attacks. The paper does not discuss how these threat models relate or whether the theorem's conditions are satisfied under the ℓ∞ attacks used.

- **L0 training surrogate vs. inference metric mismatch not analyzed.** The paper uses a sigmoid-based differentiable surrogate for L0 during training but the hard L0 metric at inference (Equations 2 vs. the surrogate). The paper does not analyze whether the surrogate faithfully approximates the hard metric or whether optimizing the surrogate reliably leads to good hard-L0 predictions (Section 3.3 vs. Section 3.1).

- **No statistical precision reported.** No error bars, confidence intervals, or multiple-seed results are reported for any table. Given the small sample sizes for some subsets (e.g., only 510 theorem-compliant samples for CLIP/Tiny-ImageNet), single-run results are unreliable.

### Trivial

None.

## Nice-to-Haves

- The paper could strengthen its generality claim by adding a non-image dataset.
- Experiment 1's detection evaluation could be extended to CW and AutoAttack, not just PGD.
- The paper's "theorem-compliant" samples on CLIP/Tiny-ImageNet are only ~10% of the test set; discussing how to improve the method's coverage would strengthen the contribution.

## Removed Points

The following points from the input review were removed after verification against the paper:

- **"Threat model mismatch: ℓ₂ norm of up to ~0.27 for CIFAR-10"** — Removed because the perturbation δ in Assumption A2 is in the feature space, not the input space. The critic's calculation used input-space dimensionality, which is not relevant to the paper's framing. The general point about unclear norm specification is retained in Minor weaknesses.

- **"No non-image modality tested"** — Removed as scope creep. The paper tests two datasets and two architectures; testing additional modalities is beyond reasonable expectation for a single paper.

- **"No comparison against semantics-driven detectors"** — Removed. The paper positions itself as semantics-free; requiring comparison against semantics-driven methods that use fundamentally different (and often domain-specific) information is not a fair expectation.

- **"No statistical significance"** — Demoted from the critic's framing. The critic focused on this as a general weakness; it's retained as a Minor point.

- **"Experiment 2 attack type not specified"** — Removed as a standalone point. Folded into the limited threat model evaluation weakness.

- **Assumption A3 restrictiveness speculation** — The critic's claim about A3 being restrictive for near-zero coordinates is speculative; no experimental evidence or calculation is provided to show the assumption is violated in practice. Removed.

## Novel Insights

None beyond the paper's own contributions. The reviewer's identification of the non-standard confusion matrix definition is the most significant novel observation — it is a genuine methodological oversight in the paper's evaluation design rather than a subtle flaw.

## Suggestions

1. **Fix the confusion matrix definition.** Recompute all detection metrics using the standard definitions (TP = a=1 ∧ â=1, FN = a=1 ∧ â=0). If the authors wish to also report a "system-level" metric that accounts for classification correctness, it should be presented alongside — not as a replacement for — standard detection metrics, and the deviation should be explicitly acknowledged.

2. **Add external baselines.** Compare KOALA against at least 2-3 established detection methods (e.g., Mahalanobis distance detector, LID, feature squeezing) using the same evaluation protocol with standard metrics.

3. **Broaden the attack evaluation for detection.** Report detection performance against AutoAttack and include an adaptive attack designed to defeat the KL/L0 disagreement criterion.

4. **Clarify the theorem conditions and experimental mapping.** Specify how "theorem-compliant" is determined (including numerical thresholds) and discuss how ℓ∞-bounded attacks relate to the proof's energy bound.

5. **Report variance.** Provide results across multiple random seeds with standard deviations, especially for the smaller compliant-sample subsets.

## Score and Decision

The paper's core idea is genuinely novel and the theoretical ambitions are laudable. However, the empirical evaluation has two significant problems that prevent acceptance in the current form: (1) the non-standard confusion matrix definition means the reported detection metrics do not measure what is conventionally understood, and (2) the complete absence of baseline comparisons makes it impossible to assess whether KOALA advances the state of the art. These issues require substantial revision and additional experiments to resolve.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>