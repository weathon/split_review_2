## Summary
This paper presents KOALA, an adversarial detection method that flags attacks when class predictions from two complementary similarity metrics—KL divergence and an L0-based metric—disagree. The method operates as a nearest-prototype classifier on normalized embeddings, requires only fine-tuning on clean images, and is accompanied by a formal theorem claiming that under certain conditions, adversarial perturbations cannot simultaneously fool both metrics, guaranteeing detection. Experiments on ResNet/CIFAR-10 and CLIP/Tiny-ImageNet show that on a subset of examples satisfying the theorem's conditions, detection is perfect, while overall detection performance is moderate.

## Strengths
- **Novel detection principle**: The idea of using disagreement between KL and L0-based nearest-prototype predictions as an adversarial detector is creative and well-motivated by the observation that attacks can be either dense/low-amplitude or sparse/high-impact.
- **Theoretical ambition**: The paper attempts to provide a formal proof of correctness for an adversarial detector, which is rare in the detection literature and could be valuable if the proof is sound.
- **Lightweight training**: The method requires only clean-image fine-tuning, avoiding adversarial training or architectural modifications, making it practical as a plug-in component.

## Weaknesses

### Fatal
- **The theoretical proof is not actually provided in the paper.** The paper states "A complete proof of Theorem 1 is provided in the appendix B" and gives a "Proof Sketch," but the appendix is stripped from the provided content. Without the full proof, it is impossible to verify the central claim of the paper—that detection is guaranteed under stated conditions. The proof sketch is too vague to assess correctness: it mentions "necessary conditions" and "incompatibility" but does not derive any concrete thresholds, show how the L0 threshold τ is chosen, or demonstrate that the required "coordinate gap" condition is achievable or non-vacuous. This is a fatal issue because the paper's main selling point is its formal guarantee.

- **The theorem's conditions are not verified or enforced in practice.** The paper partitions test sets into "Theorem-Compliant" and "Non-Compliant" samples based on inter-class prototype separation, but it never specifies how this separation is measured, what threshold Γ_i(ε) is used, or whether the fine-tuning procedure actually ensures the conditions hold. The fact that only a minority of samples are "compliant" (e.g., 510 out of 5000 for CLIP/Tiny-ImageNet) suggests the conditions are restrictive and rarely met. The paper does not report what fraction of clean or attacked samples satisfy the conditions, nor does it provide a practical way to check them at inference time.

- **The evaluation conflates detection with classification in a problematic way.** The confusion matrix definitions in Section 4.2 are unusual and potentially misleading. A true positive is defined as an attacked input where either the detector flags it OR the detector correctly classifies it (even if not flagged). This means that a detector that never flags any attack but always guesses the correct class would achieve perfect recall. The paper's reported "perfect" recall of 1.0 on theorem-compliant samples could be driven by correct classification rather than actual detection. The standard evaluation for a detector should treat detection (flagging) as the primary task, with separate reporting of classification accuracy.

### Major
- **The L0 metric definition is problematic and not well-justified.** Equation (2) defines L0 distance as counting dimensions where |c_i - p_i| exceeds τ·μ(c,p), where μ is the mean absolute difference. This means the threshold is data-dependent and varies per sample. The paper does not explain why this particular formulation is chosen, how τ is selected (beyond stating τ=0.75), or whether the metric is even a valid distance (it is not symmetric, and the threshold depends on both vectors). The differentiable surrogate in Section 3.3 uses a different formulation (sigmoid of the same quantity), but the relationship between the hard L0 count and the surrogate is not analyzed.

- **The ablation study results are contradictory and undermine the core claim.** On CLIP/Tiny-ImageNet, the KL+L0+Cosine combination outperforms the proposed KL+L0 combination on all detection metrics. The paper dismisses this by saying the three-metric model "breaks the underlying classification," but this is precisely the point: if adding Cosine improves detection, then the claim that KL and L0 are the "right" complementary metrics is weakened. The paper needs to explain why the proposed combination is preferable when it is not the best performer.

- **The experimental setup is incomplete.** The paper only evaluates on PGD attacks in the main detection experiments (Tables 1 and 2). The adversarial accuracy tables (3 and 4) include CW and AutoAttack, but these are not linked to detection performance. A detector that works only against PGD but fails against stronger attacks like AutoAttack is not practically useful. The paper should report detection metrics (precision, recall, F1) for all attack types.

- **No comparison to existing detection methods.** The paper discusses related work extensively but never compares KOALA's performance to any baseline detector (e.g., Mahalanobis, LID, feature squeezing, NIC). Without such comparisons, it is impossible to assess whether KOALA offers any practical advantage over existing approaches.

### Minor
- The paper claims KOALA is "semantics-free" but uses class prototypes derived from class labels, which is a form of semantic information. The distinction from "semantics-driven" methods is not clearly drawn.
- The fine-tuning procedure uses binary cross-entropy on positive/negative pairs, but the paper does not specify how negative pairs are sampled or whether class imbalance is handled.
- The hyperparameters (τ=0.75, φ=0.5, ω_L0=0.9, ω_KL=0.1) are presented without any sensitivity analysis.

### Trivial
- The paper states "All finetuning was done using clean images only" in tables, which is redundant with the method description.
- Figure 1 and its caption are duplicated in the text.

## Nice-to-Haves
- A sensitivity analysis for the key hyperparameters (τ, φ, loss weights) would strengthen the empirical evaluation.
- Reporting detection performance separately for each attack type (PGD, CW, AutoAttack) rather than aggregating would be more informative.
- A comparison to at least one simple baseline (e.g., thresholding on softmax confidence or entropy) would help contextualize the results.

## Novel Insights
None beyond the paper's own contributions. The idea of using metric disagreement for detection is novel, but the theoretical and empirical support is insufficient to establish it as a reliable method.

## Suggestions
1. Provide the full proof of Theorem 1 in the main paper or a clearly accessible appendix, and verify its correctness. The proof sketch is too vague to be evaluated.
2. Clarify the confusion matrix definitions and report detection metrics in the standard way: treat flagging (â=1) as the positive detection event, independent of whether the classification is correct.
3. Report the fraction of test samples that satisfy the theorem's conditions, and explain how practitioners can check these conditions at inference time.
4. Compare KOALA to at least 2-3 existing detection methods (e.g., Mahalanobis, LID, feature squeezing) on the same datasets and attacks.
5. Report detection metrics (precision, recall, F1) separately for each attack type, not just PGD.

## Score and Decision
The paper presents a novel and interesting idea, but the central theoretical claim cannot be evaluated due to the missing proof, the evaluation methodology is flawed (unusual confusion matrix definitions that may inflate results), and the experimental validation is incomplete (no baseline comparisons, limited attack types for detection metrics). These issues are fatal to the paper's contribution as presented.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>