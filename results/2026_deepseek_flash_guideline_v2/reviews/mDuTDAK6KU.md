The calibration search tool is unavailable due to a file system issue, so I will proceed with scoring based on direct analysis of the paper content.

## Final Consolidated Review

## Summary

KOALA proposes an adversarial detector that flags inputs as attacked when two nearest-prototype classifiers — one using KL divergence and one using an L0-based metric — disagree on the predicted class. The paper provides a formal theorem stating that when inter-class prototype separation exceeds a data-dependent threshold, no norm-bounded perturbation can simultaneously flip both metrics' predictions to favor the adversarial class. A lightweight fine-tuning procedure (clean images only, no adversarial training) shapes the embedding space. Experiments on ResNet/CIFAR-10 and CLIP/Tiny-ImageNet evaluate detection and robustness.

## Strengths

1. **Formal theoretical guarantee with explicit, empirically verified conditions.** Unlike most adversarial detectors that rely solely on empirical heuristics, Theorem 1 (Section 3.2) specifies concrete conditions — inter-class prototype separation exceeding a threshold Γ_i(ε) — under which both metrics cannot simultaneously favor the wrong class. Experiment 1 (Table 1) validates this: on the theorem-compliant subset, KOALA achieves perfect scores (Acc=1.0, Prec=1.0, Rec=1.0, F1=1.0) across both datasets and perturbation budgets. This theoretical grounding is a genuine differentiator in the detection literature, where formal guarantees are rare.

2. **Complementary metric design (KL+L₀) supported by ablation on ResNet.** The paper motivates KL+L₀ via the geometry of norm-bounded perturbations (Section 3.1): KL detects dense low-amplitude shifts while L₀ catches sparse high-impact changes. The ablation (Table 2) shows that on ResNet/CIFAR-10, KL+L₀ dominates all alternative pairings (L₀+Cosine, KL+Cosine, KL+L₀+Cosine) across Accuracy, Precision, Recall, and F1 — e.g., Precision 0.94 vs. 0.89–0.92, Recall 0.81 vs. 0.41–0.62.

3. **Substantial adversarial accuracy improvement without adversarial training on ResNet.** Table 3 shows that fine-tuning with the KL+L₀ objective on ResNet/CIFAR-10 raises PGD adversarial accuracy from ~45% to 57.32% (ℓ∞^{2/255}) and from ~32% to 54.60% (ℓ∞^{4/255}) — a gain of 12–22 percentage points — using only clean images. This is notable given that adversarial training is typically required for such improvements.

4. **Semantics-free operation.** The detection mechanism relies purely on representation geometry (disagreement between KL and L₀ distance to class prototypes), not on label text, auxiliary classifiers, or domain-specific priors (Section 3.1). This differentiates it from methods like Zhang et al. (2023) and Zhou et al. (2024) that depend on domain-specific semantics.

## Weaknesses

### Major

1. **Non-standard evaluation metrics conflate detection with classification (Section 4.2, TP/FP definitions).** The confusion matrix counts an attacked input as a True Positive even when the detector says "no attack" (â=0), as long as the classifier happens to predict the correct class (y^*). Conversely, a clean input is counted as a False Positive even when the detector correctly says "no attack" if the classifier misclassifies it. Formally:
   - TP = [a=1] ∧ [(â,ŷ)=(1,⟂) ∨ (â,ŷ)=(0, y^*)]
   - FP = [a=0] ∧ [(â,ŷ)=(1,⟂) ∨ (â,ŷ)=(0, -y^*)]
   
   This means the reported precision (0.94) and recall (0.81) on ResNet/CIFAR-10 conflate the detector's detection accuracy with the classifier's classification accuracy. Under standard detection evaluation (TP = attack correctly flagged, FP = clean input incorrectly flagged), the numbers would be different and likely lower. While the paper is transparent about its definitions, the abstract and headline results state these numbers without caveat, which is misleading to readers who will assume standard definitions.

2. **No evaluation against adaptive attacks.** The detector's decision rule — flag when KL prediction ≠ L₀ prediction — is fully known. An adaptive attacker aware of this rule could design perturbations that cause both metrics to agree on the same (wrong or correct) class, bypassing detection. Despite standard requirements for defense evaluation (Carlini et al., 2019; Athalye et al., 2018; Tramer et al., 2020), the paper only evaluates against generic attacks (PGD, CW, AutoAttack) that do not target the detection mechanism. Theorem 1 guarantees that under its conditions, both metrics cannot simultaneously *favor the wrong class*, but this does not rule out evasion via agreement on the correct class. Without adaptive attacks, the empirical evaluation is incomplete for a defense paper.

3. **Detection metrics are only reported for PGD attacks.** Tables 1 and 2 report detection accuracy, precision, recall, and F1 only under PGD. CW and AutoAttack are described in the experimental setup (Section 4.1) and used in adversarial accuracy evaluation (Tables 3, 4), but no detection metrics are shown for them. A reader cannot assess whether KOALA's detection performance generalizes across different attack types.

### Minor

4. **Table 4 caption directly contradicts its own data.** The caption reads "The KL+L₀ objective demonstrates superior adversarial accuracy, highlighting the complementary nature of these two metrics," but the table shows KL+L₀ achieving 26.50% on PGD (ε=2/255) for CLIP, while L₀-only achieves 53.31% and KL-only achieves 60.02%. The body text (line 274) correctly acknowledges that L₀-only gives the best CLIP results. The caption is a copy-paste error from Table 3 and must be fixed.

5. **Theorem's guarantee is narrower than the paper's framing suggests.** Theorem 1 states that both metrics cannot simultaneously "favor the adversarial class." The paper repeatedly frames this as "guaranteed detection" (Abstract, Section 3.2). However, the theorem does not guarantee that *all* attacks will be detected — an attack too weak to flip either metric's prediction (both agree on the correct class) would evade detection while still being an adversarial perturbation. The guarantee is also conditional on a substantial subset of data satisfying the inter-class separation condition (e.g., only ~510/5000 CLIP samples). The framing should be calibrated to match what the theorem actually guarantees.

6. **No variance estimates or multiple runs reported.** No standard deviations, confidence intervals, or multiple-run statistics are reported for any metric. Single-run evaluations make it impossible to assess the stability of the reported numbers.

7. **Hyperparameter sensitivity not analyzed.** The threshold τ=0.75 and loss weights ω_L₀=0.9, ω_KL=0.1 are fixed without any sensitivity analysis. Since the L₀ metric definition depends on τ and the training objective depends on the weights, it is unclear how robust the results are to these choices.

### Trivial

8. **Fine-tuning epochs are not specified.** The paper states learning rates, batch sizes, and optimizers but not the number of fine-tuning epochs or a convergence criterion.

## Nice-to-Haves

- Include per-attack-type breakdown of detection metrics (CW, AutoAttack) alongside PGD.
- Perform sensitivity analysis for τ (L₀ threshold) and the loss weights ω_L₀, ω_KL.
- Report standard detection metrics (TPR, FPR) alongside the paper's own system-level metrics.

## Removed Points

The following points from the inputs were removed after verification:

1. **"L₀ metric is self-referential" and "KL asymmetry not discussed"**: These are observations about deliberate design choices, not weaknesses. The paper clearly specifies Eq. 2 and Eq. 1 and does not claim standard norm properties.
2. **"Theorem-compliant/non-compliant partitioning unclear"**: The partition depends on Γ_i(ε), which depends on the perturbation budget ε, explaining why counts differ across attack strengths. The paper states this condition clearly.
3. **"L₀+KL+Cosine on CLIP may be inflated by random guessing"**: The paper explicitly discusses and acknowledges this artifact (Section 4.3, lines 216-218), noting it "does so by breaking the underlying classification, rather than by preserving it."
4. **"Could KL+L₀ results on CLIP be similarly inflated?"**: The paper shows clean accuracy is preserved with KL+L₀ (Table 4: 55.88% vs. baseline 57.88%), unlike the three-metric combination, suggesting the detection signal is not spurious.
5. **Generic speculation about missing appendix content, formatting nitpicks, and scope-creep demands**: Removed per filtering rules.

## Novel Insights

The reviews surface an interesting tension not fully explored in the paper: the theorem guarantees that both metrics cannot simultaneously prefer the wrong class, but this does not imply practical security against an adaptive adversary who can search for perturbations that keep both metrics in agreement on the *correct* class (evading detection while still being adversarial). This gap between the theoretical guarantee and the empirical evaluation (which tests no adaptive attacks at all) deserves more explicit discussion. Additionally, the divergent results between ResNet and CLIP — where the optimal metric combination differs entirely — suggest the method's effectiveness is highly dependent on the geometry of the pre-trained embedding space. The paper acknowledges this (Section 4.4 analysis) but does not deeply characterize what properties of the embedding space predict success.

## Suggestions

1. **Fix the evaluation metrics.** Either adopt standard detection definitions (TP = attack correctly flagged, FP = clean flagged as attack) or transparently report both the paper's system-level metrics and standard detection metrics with clear disclaimers.
2. **Design and evaluate adaptive attacks.** An attack optimizing for both (a) misclassification and (b) agreement between KL and L₀ predictions is the most credible test. If the theorem holds, such attacks should provably fail on the compliant subset — this would be strong evidence.
3. **Fix the Table 4 caption.** The last line is a copy-paste error from Table 3.
4. **Report detection metrics for CW and AutoAttack.** Extend Tables 1 and 2 to cover all attack types.
5. **Calibrate the language around the theorem's guarantee.** State precisely what Theorem 1 guarantees (both metrics cannot favor the wrong class) and what it does not (detection of weak perturbations).
6. **Report variance across multiple runs.**
7. **Include the number of fine-tuning epochs** to substantiate the "lightweight" claim.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>