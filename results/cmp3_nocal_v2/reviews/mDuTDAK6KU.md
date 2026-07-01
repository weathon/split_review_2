## Summary

KOALA proposes a reactive adversarial detector based on a simple but principled idea: two complementary similarity metrics (KL divergence and an L₀-based distance) should agree on clean inputs but disagree under attack. The method requires only clean-image fine-tuning (no adversarial training, no architectural changes) and comes with a formal theorem specifying conditions under which detection is guaranteed. Experiments on ResNet/CIFAR-10 and CLIP/Tiny-ImageNet show perfect detection on the subset of samples satisfying the theorem's conditions, with degraded but non-trivial performance on the remainder.

## Strengths

1. **Well-motivated complementarity with formal backing.** The observation that energy-bounded perturbations are either dense/low-amplitude (naturally captured by KL divergence) or sparse/high-impact (naturally captured by an L₀-based metric) is clear and intuitive (Section 3.1, Figure 1). This gives the method conceptual coherence, and unlike nearly all prior detection methods (NIC, feature squeezing, LID, MagNet, Mahalanobis, CADet, Bayesian uncertainty — Section 2), KOALA attempts to provide a theorem specifying when detection is guaranteed.

2. **The theorem-compliant subset results are striking.** On samples satisfying Theorem 1's conditions, Table 1 reports accuracy, precision, recall, and F1 of 1.0 across both datasets and perturbation budgets (e.g., 3345/5000 ResNet/CIFAR-10 samples at ε=2/255). These results directly validate the theoretical claim for the applicable subset.

3. **Lightweight, plug-and-play training.** The method requires only fine-tuning a backbone encoder on clean images with a composite loss — no adversarial training, no architectural changes, no attack-specific priors. This practical advantage is real and clearly communicated (Section 3.3).

## Weaknesses

### Fatal

None.

### Major

1. **Non-standard confusion matrix definitions make overall metrics uninterpretable and non-comparable.**  
   The paper defines (Section 4.2, line 188):  
   - TP: attacked input (a=1) that is *either* flagged (â=1) *or* correctly classified without being flagged (â=0, ŷ=y*).  
   - FP: clean input (a=0) that is *either* falsely flagged (â=1) *or* misclassified by the model without being flagged (â=0, ŷ=-y*).  
   - FN: attacked input that is *both* undetected *and* misclassified.

   **Problem A (TP inflation):** An undetected attack counts as a true positive if the classifier happens to be robust enough to still predict correctly. This conflates detection with classification robustness — on trivial attacks that barely change the classifier's output but the detector never fires, recall would still be 1.0.  
   **Problem B (FP inflation):** A clean input counts as a false positive even when the detector correctly does not flag it, as long as the model misclassifies it. This deflates precision based on the classifier's clean accuracy rather than the detector's false-positive rate.

   *Why this is Major rather than Fatal:* The core theoretical contribution and the theorem-compliant subset results (1.0 across all metrics) are unaffected — under standard definitions, clean compliant samples would still be TN and attacked compliant samples would still be TP because the theorem guarantees disagreement (â=1). The non-standard framing primarily distorts the overall/comparative numbers (precision 0.94, recall 0.81 in the abstract). However, these numbers are advertised in the abstract as detection metrics, which is misleading without a caveat about the non-standard definitions. The authors should report standard detection metrics (TP: â=1|a=1; FP: â=1|a=0; TN: â=0|a=0; FN: â=0|a=1) as primary results and explain the rationale for any alternative framing separately.

2. **No baselines against any prior detection method.**  
   The paper compares KOALA only against ablations of its own metric combinations (KL+L₀ vs. L₀+Cosine vs. KL+Cosine vs. KL+L₀+Cosine, Table 2). There is zero comparison to any existing method from the extensive literature cited in Section 2 — no confidence-threshold baseline, no NIC, feature squeezing, LID, MagNet, Mahalanobis, CADet, or Bayesian uncertainty detector. Without these, a reader cannot assess whether KOALA advances the state of the art. On CLIP/Tiny-ImageNet, the overall precision is 0.66 and recall 0.85 (Table 2) — but there is no frame of reference for whether these numbers are good. A simple softmax-confidence baseline might achieve comparable results, and the paper provides no way to rule this out. Adding at least one standard detection baseline (e.g., a threshold-based detector or a Mahalanobis detector) on the same setup is essential for calibrating the results.

3. **Detection results are only shown for PGD attacks.**  
   Table 1 (the main detection evaluation) is explicitly labeled "evaluated under PGD" (line 212). Section 4.1 lists CW and AutoAttack as attacks used, but these appear only in Tables 3 and 4, which report *adversarial accuracy* (classification), not detection metrics. Since the theoretical guarantee is attack-agnostic — it depends only on the perturbation budget and prototype separation, not the attack algorithm — detection performance should be verified across the full attack suite. The absence of CW and AutoAttack detection results is a significant evidential gap.

### Minor

4. **The theorem's limited coverage is under-discussed in the framing.**  
   On ResNet/CIFAR-10, only ~67% of test samples satisfy Theorem 1's conditions (3345/5000 at ε=2/255); on CLIP/Tiny-ImageNet, only ~10% do (510/5000 at ε=2/255). On the non-compliant majority, detection degrades substantially: recall drops to 0.42–0.84 and precision to 0.62–0.78 (Table 1). The paper reports these numbers transparently in Table 1, but the abstract and contributions list ("a formal proof of correctness," "extensive experiments confirm our theoretical claims") do not caveat the narrow scope. The guarantee is conditional on a property that does not hold for 33–90% of test samples. The authors should qualify the high-level claims to reflect this limitation.

5. **The L₀ threshold parameter τ is not analyzed for sensitivity.**  
   The L₀ distance (Equation 2) uses τ = 0.75, which determines what counts as a "perturbed" coordinate relative to the mean absolute deviation. Proposition 4 in the proof sketch shows that the theoretical trade-off between KL and L₀ stability bands depends on τ. Yet the paper provides no analysis of how detection performance varies with τ. Showing that results are robust to this choice — or at minimum characterizing the effect — would strengthen the paper.

6. **The proof sketch in the main text is insufficiently precise.**  
   Theorem 1 references a threshold function Γ_i(ε) without specifying its form. The "coordinate gap" condition is described qualitatively. The proof is deferred to the appendix (which is stripped from the submission), so a reader of the main text cannot assess whether the theorem is tight or potentially vacuous (e.g., if Γ_i(ε) is very large, the condition may never be met in practice except on trivially separable data). The empirical breakdown in Table 1 makes this concern concrete. The authors should provide a more precise statement of the theorem's conditions in the main text.

### Trivial

7. **Data splitting description is ambiguous.** Line 171 says "we randomly split the development sets into two equal halves." For CIFAR-10, it is unclear whether this refers to splitting the training set or the test set. Given that standard CIFAR-10 has 50k/10k train/test splits, the sample sizes (~5000) suggest half the test set was used, but this should be stated explicitly.

8. **Centroid update during fine-tuning is not specified.** The paper states centroids are computed from training data (ResNet) or the CLIP text encoder (CLIP), but does not specify whether these centroids are frozen or re-computed during fine-tuning. This is relevant because the fine-tuning changes the embedding space.

## Nice-to-Haves

- **Adaptive attack evaluation.** Since the paper claims a provable detection condition, an adaptive adversary who knows KOALA's mechanism and tries to craft perturbations that keep both KL and L₀ predictions in agreement would be the natural stress test. This is especially relevant for the non-compliant subset where the theorem does not apply.
- **Characterization of theorem-compliance.** Understanding what properties (class difficulty, embedding norm, prototype dispersion) determine whether an input satisfies Theorem 1's conditions would help assess the practical significance of the guarantee, particularly for the CLIP/Tiny-ImageNet setting where only ~10% of samples are compliant.

## Removed Points

*These points were flagged by reviewers but removed during consolidation. Treat them with caution.*

- **"No evaluation on full CIFAR-10 test set (only 5000 of 10000 images)"** — Removed as a minor sample-size nitpick. Using 5000 test samples from a 10k test set is a reasonable evaluation scale for a detection experiment, and the paper explains the split.
- **"CLIP/Tiny-ImageNet class names may not be straightforward nouns"** — Removed as speculative. Tiny-ImageNet classes (goldfish, great white shark, etc.) are standard and compatible with the "a photo of [CLASS]" prompt template.
- **"Reproducibility gaps about centroid recomputation"** — The paper specifies that prototypes are computed as the mean embedding of all training examples (ResNet, line 173) or from the CLIP text encoder (line 177). Whether centroids are frozen during fine-tuning is indeed unspecified but is a standard implementational detail that would be clarified in released code.
- **"The KL(c||p) order is non-standard"** — The paper uses KL(c||p) in Equation 1. While the asymmetry of KL is worth noting, the choice of order depends on the method's design and is not inherently wrong. The paper could briefly justify the choice but this is not a substantive weakness.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Report standard confusion matrix metrics** (TP: â=1|a=1, FP: â=1|a=0, TN: â=0|a=0, FN: â=0|a=1) as primary results. If the alternative framing is retained for any reason, explicitly state how the definitions differ from the standard ones and report both versions so readers can compare with prior work.

2. **Add at least one standard detection baseline** — a confidence-threshold detector, a Mahalanobis-based detector (Lee et al., 2018), or feature squeezing (Xu et al., 2018) — on the same experimental setup. Without this, the practical value of the reported numbers cannot be assessed.

3. **Report detection metrics (Table 1 format) for CW and AutoAttack**, not just PGD. The theoretical claim is attack-agnostic and must be verified across the attack suite the paper itself lists.

4. **Provide a sensitivity analysis for the L₀ threshold τ** (Equation 2), showing detection performance for a range of values (e.g., τ ∈ {0.5, 0.6, 0.7, 0.8, 0.9}) on at least one setting.

5. **Caveat the scope of the guarantee prominently** in the abstract and introduction: the theorem applies to samples with sufficient inter-class prototype separation, which covers ~67% of CIFAR-10 and ~10% of Tiny-ImageNet in the current experiments.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>