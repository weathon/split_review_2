## Summary
# Final Review Report

## Summary

This paper presents KOALA, an adversarial input detector for neural networks that operates by comparing predictions from two complementary nearest-prototype classifiers: one using KL-divergence and one using an L0-based metric. The detector flags an input as attacked when the two classifiers disagree on the predicted class. The authors provide a formal theorem stating that under certain conditions (normalized embeddings, bounded perturbation, sufficient class prototype separation), no norm-bounded perturbation can simultaneously fool both classifiers, guaranteeing detection. The method requires only fine-tuning the backbone encoder on clean images with a composite loss that aligns embeddings with both metrics.

The paper addresses an important problem—lack of formal guarantees in adversarial detection—and proposes an elegant conceptual approach with theoretical backing. The experiments on ResNet-18/CIFAR-10 and CLIP/Tiny-ImageNet validate that when the theorem's conditions are met, detection accuracy reaches 1.0. On the full test sets, KOALA achieves precision 0.94 and recall 0.81 on ResNet/CIFAR-10.

However, the paper has several significant weaknesses. (1) The evaluation metrics for detection are unconventional and may inflate reported performance. (2) The central theoretical guarantee relies on a threshold Γ_i(ε) that is never instantiated in the main text, and the operationalization of "theorem-compliant" vs "non-compliant" splits in experiments is not described. (3) The CLIP/Tiny-ImageNet results directly contradict the paper's core claim: on CLIP, the proposed KL+L0 combination performs substantially worse than L0-only or KL-only fine-tuning, exposing architecture-dependent behavior that undermines generality claims. (4) No variance or statistical significance is reported for any experimental results, making it impossible to assess whether observed advantages are robust. (5) The L0 metric definition has a circular threshold dependency that may disconnect the theoretical analysis from the implementation.

These weaknesses are fixable with targeted revisions, but in their current form, they prevent the paper from fully delivering on its claimed contributions.

## Strengths
**S1. Clear conceptual contribution with formal theory.** The core idea—using disagreement between KL-divergence and L0-based predictions as an adversarial detection signal—is conceptually novel and well-motivated. The observation that norm-bounded perturbations affect the embedding space in complementary ways (dense low-amplitude vs. sparse high-impact) provides an intuitive rationale for the dual-metric design. The attempt to provide formal detection conditions (Theorem 1) is a genuine strength, as most prior detection methods (feature squeezing, LID, Mahalanobis, MagNet) are purely empirical with no provable guarantees. The proof sketch, while needing refinement, correctly identifies the key mechanism: the energy budget of a perturbation cannot simultaneously satisfy the conditions needed to flip both KL and L0 nearest-prototype predictions.

**S2. Lightweight training without adversarial examples.** KOALA requires only fine-tuning a pre-trained backbone on clean images with a composite BCE loss. This is a practical advantage over adversarial training-based defenses that require generating adversarial examples during training (which is computationally expensive and attack-model dependent). The fine-tuning preserves clean accuracy (Table 3: all ResNet variants within ~0.5-1% of baseline), showing that detection capability is added without degrading core classification performance.

**S3. Strong performance on the theorem-compliant subset.** Experiment 1 (Table 1) shows that on the subset of test examples satisfying the theorem's conditions, KOALA achieves perfect detection (accuracy, precision, recall, F1 = 1.0). This empirically validates that the theoretical guarantee translates to actual performance when assumptions are met. The sharp contrast with non-compliant subset results (e.g., ResNet acc 0.63-0.66, recall 0.42-0.45) confirms that successful detection depends on sufficient inter-class prototype separation, consistent with the theory.

**S4. Thorough ablation study across metric combinations.** Experiment 2 systematically compares seven different fine-tuning objectives (KL+L0, L0+Cosine, KL+Cosine, L0+KL+Cosine, plus single-metric controls). This comprehensive ablation allows readers to assess the marginal benefit of each metric. The finding that adding Cosine similarity degrades robustness on ResNet (Table 3) is a non-obvious insight that demonstrates the authors' careful experimental design.

**S5. Reproducibility infrastructure.** The paper provides detailed hyperparameters, model architectures, attack configurations, and loss formulations. The availability of anonymous code and the open commitment to release models are positive for reproducibility.

## Weaknesses
**W1. CLIP/Tiny-ImageNet results contradict the central claim (Severity: Major, Fixable: Yes).**

The paper's core contribution is that the KL+L0 combination provides superior detection through metric complementarity. However, Table 4 shows that on CLIP/Tiny-ImageNet, the proposed KL+L0 combination achieves *substantially worse* adversarial accuracy than L0-only or KL-only fine-tuning across all attacks (PGD: 26.50% vs 53.31% for L0-only at ε=2/255; AutoAttack: 16.18% vs 25.43% for L0-only). The paper's post-hoc explanation (CLIP's pre-training creates sparsity-aware structure) is plausible but untested and does not resolve the contradiction with the claimed generality of KL+L0. The title and abstract assert KOALA as a "plug-and-play solution for existing models and various data modalities," but the CLIP results show it can be harmful.

*Required revision:* (a) Revise contribution language to acknowledge architecture-dependent benefits. (b) Add experiments with additional architectures (e.g., VGG, DenseNet, ViT from scratch) to characterize when KL+L0 helps vs. hurts. (c) Add an adaptive mechanism that selects the best metric combination per architecture.

**W2. Unconventional and potentially inflated detection metrics (Severity: Major, Fixable: Yes).**

The TP/FN definitions in Experiment 1 (Page 6-7) deviate from standard detection evaluation. TP is defined as [a=1] ∧ [(â, ŷ) = (1, ⟂) ∨ (â, ŷ) = (0, y^*)], meaning a detected attack is counted as TP even when the detector fails to flag the attack (â=0) as long as it predicts the correct class (ŷ=y^*). This conflates correct classification with attack detection. Similarly, FP includes (â, ŷ) = (0, -y^*), which would standardly be a misclassification, not a false alarm. These unconventional definitions may significantly inflate the reported precision and recall compared to standard evaluation.

*Required revision:* Report results using standard detection definitions (TP: a=1∧â=1; TN: a=0∧â=0; FP: a=0∧â=1; FN: a=1∧â=0) alongside the current metrics. Discuss the discrepancy between the two evaluation schemes.

**W3. Theorem 1's key condition is uninstantiated and the compliant/non-compliant split is not operationalized (Severity: Critical, Fixable: Yes).**

Theorem 1 depends on the condition |c_i^* - ĉ_i| > Γ_i(ε), but Γ_i(ε) is never defined in the main text. The paper states it is "some threshold" without specifying its functional form. More critically, Experiment 1 partitions test examples into "Theorem-Compliant" and "Non-Compliant" subsets, but never describes the decision rule used for this partitioning. The reader cannot verify whether the partitioning correctly reflects the theorem's conditions or whether it introduces selection bias.

*Required revision:* (a) Define Γ_i(ε) explicitly in the main text (at least its functional dependencies). (b) Describe the exact algorithmic procedure for determining whether an input satisfies Theorem 1. (c) Report the threshold value used and the fraction of test samples that are compliant for each model. (d) Verify that the compliant subset is not trivially easy (e.g., samples that are already correctly classified with high confidence).

**W4. No statistical reporting or variance estimates (Severity: Major, Fixable: Yes).**

All experimental results in Tables 1-4 are point estimates without standard deviations, confidence intervals, or significance tests. Many comparisons show modest margins (e.g., KL+L0 vs KL+Cosine on ResNet under PGD ε=2/255: 57.32% vs 55.60%, a 1.72% difference). Without error bars, readers cannot determine if this advantage is reproducible or merely noise. The random split of development sets into halves introduces additional variance that is not accounted for.

*Required revision:* Report all results as mean ± std over at least 3 independent runs (different random seeds for fine-tuning, data partitioning, and attack generation). Add statistical significance tests (e.g., paired t-test) for the key claim that KL+L0 outperforms the next best combination.

**W5. KL divergence direction choice is unexamined (Severity: Major, Fixable: Yes).**

Eq. (1) defines KL(c||p) = Σ c_i log(c_i/p_i)—the forward KL where the prototype is the reference distribution. The paper does not justify this choice over the reverse KL(p||c). The two directions are not symmetric and will produce different nearest-prototype decisions. The forward KL heavily weights coordinates where c_i has mass; the reverse KL emphasizes coordinates where p_i has mass. Which direction is more appropriate for detecting adversarial perturbations is not discussed, and no empirical comparison (KL(c||p) vs KL(p||c) vs symmetric Jensen-Shannon divergence) is provided in the ablation study.

*Required revision:* Add a justification paragraph for the KL direction choice, or include both directions in the ablation study (Experiment 2) to demonstrate empirically that the chosen direction is optimal.

**W6. L0 metric has a circular threshold dependency (Severity: Major, Fixable: Yes).**

The L0 metric in Eq. (2) uses threshold τ·μ(c,p) where μ(c,p) = (1/d) Σ|c_i-p_i| is the mean absolute difference. Since μ depends on the overall perturbation magnitude, a large perturbation affecting many coordinates increases μ, which in turn raises the threshold for counting coordinates as "perturbed." This circularity means the L0 count is a relative rather than absolute sparsity measure. Theorem 1's proof depends on the ability to "always find a threshold τ" that forces incompatibility, but in practice τ is fixed (τ=0.75), and the proof's τ-adjustability claim may not apply to the implemented metric.

*Required revision:* Either (a) decouple the threshold from μ by using a fixed absolute threshold η and analyze sensitivity, or (b) provide explicit bounds showing that the fixed τ=0.75 satisfies the theoretical conditions under the experimental settings, or (c) add τ sensitivity analysis in the ablation study.

**W7. Training loss does not optimize the actual detection metric (Severity: Moderate, Fixable: Yes).**

The BCE-based fine-tuning loss (Eq. 5-6) encourages high absolute similarity for correct pairs and low similarity for incorrect pairs. However, KOALA's detection mechanism depends on the *relative* ranking of distances (nearest-prototype argmin decisions), not absolute similarity values. The BCE loss does not enforce a margin between the correct prototype distance and the nearest incorrect prototype distance—a margin that is essential for Theorem 1's assumption of sufficient class separation.

*Required revision:* Add a margin-based ranking loss (triplet or contrastive) as an alternative in ablation, or demonstrate empirically that the BCE loss produces adequate margins (report distribution of margins between correct and nearest-incorrect prototype distances).

**W8. Non-standard data split reduces comparability (Severity: Minor, Fixable: Yes).**

The paper splits "development sets" into two equal halves for test and validation. For CIFAR-10, this likely means 25k test images instead of the standard 10k, with only 25k for training instead of 50k. This non-standard split prevents direct comparison with the vast literature reporting results on standard CIFAR-10 splits. The impact of reduced training data on fine-tuning quality is not discussed.

*Required revision:* Use the standard train/test split and hold out a smaller validation set (e.g., 5k from training). Report whether results change under the standard split.

**W9. Missing comparison with detection baselines (Severity: Major, Fixable: Partially — requires literature verification).**

The paper compares different metric combinations within KOALA's framework but does not compare against established detection methods (feature squeezing, LID, Mahalanobis, NIC, MagNet) under the same experimental protocol. Without such comparisons, the practical value of KOALA relative to existing approaches cannot be assessed. The related work section criticizes these methods as lacking formal guarantees, but does not provide empirical comparison showing that KOALA achieves comparable or better detection accuracy.

*Required revision (deferred due to Retrieval-Disabled Mode):* Add empirical comparisons with at least 3-4 established detection baselines (e.g., feature squeezing, LID, Mahalanobis) under identical attack settings and datasets. Report detection accuracy, false positive rate, and computational overhead.

**W10. Proof sketch has unresolved gaps (Severity: Moderate, Fixable: Partially — depends on appendix content).**

The proof sketch in Section 3.2 outlines four propositions but leaves key steps unquantified: the energy consumption per flipped L0 dimension is not bounded; the KL flip condition is stated as a first-order inner product condition without considering higher-order KL terms; and the incompatibility condition depends on choosing τ after seeing the attack, while the implementation uses a fixed τ. A complete verification requires reading Appendix B (not available in the provided manuscript excerpt).

*Required revision:* Clarify in the main text whether the proof requires τ to be attack-dependent or fixed, and provide explicit energy bounds for the L0 flip condition. Add a discussion of the gap between the proof's assumptions and the experimental configuration.

## Score
**Final Score: 5/10**

**Scoring Rationale:**

The paper addresses an important problem—provably correct adversarial detection—with an elegant conceptual approach. The core idea (dual-metric disagreement for detection) is interesting and the theoretical framing is ambitious. However, the current version has several unresolved weaknesses that prevent it from fully achieving its claimed contributions:

**Research value (primary scoring dimension):** The idea of using metric disagreement for provable detection is novel and has potential to influence future work on theoretically grounded detection. However, the CLIP results directly undermine the claim that KL+L0 is the right combination, and without statistical validation, the observed advantages on ResNet may not be robust. The paper would benefit significantly from additional experiments, standardized evaluation, and revised claims. Score component: 5/10.

**Novelty (primary scoring dimension):** The concept of using dual complementary metrics for detection is genuinely new to this reviewer's knowledge. However, the novelty is partially diminished by the fact that nearest-prototype classifiers and metric learning are well-established techniques—the contribution lies more in the *combination and disagreement principle* than in the individual components. Score component: 6/10.

**Validity/Soundness:** The theoretical guarantee is not fully connected to the experimental validation (Γ_i(ε) undefined, compliant split not operationalized). The unconventional evaluation metrics raise concerns about performance inflation. The lack of statistical testing weakens confidence in the reported advantages. Score component: 4/10.

**Reproducibility:** Hyperparameters, architectures, and attack settings are well-documented. The anonymous code availability is positive. However, the non-standard data split, missing random seeds, and unconventional evaluation metrics reduce reproducibility. Score component: 5/10.

**Presentation:** The paper is generally well-written and the figures are clear. The proof sketch, while having gaps, is accessible. The main weaknesses in presentation are the overclaiming in the abstract (claiming generality not supported by CLIP results) and the unstructured related work section. Score component: 6/10.

**Overall assessment:** The paper has a promising core idea and the theoretical framework is a step forward for adversarial detection. However, the experiments reveal architecture-dependent behavior that contradicts the claimed generality, the evaluation methodology has issues that may inflate results, and the theory-experiment gap needs bridging. With major revisions including standardized metrics, statistical validation, expanded evaluation, and toned-down claims, this work could become a solid contribution. In its current form, it requires substantial strengthening before being publication-ready.