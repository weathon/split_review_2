Now I have a thorough understanding of the paper and all the reviewer claims. Let me produce the final consolidated review.

## Summary

KOALA proposes an adversarial detector based on disagreement between two complementary similarity metrics — KL divergence (sensitive to dense, low-amplitude perturbations) and an L0-based score (sensitive to sparse, high-impact changes). The paper provides Theorem 1, a formal proof that under mild assumptions and sufficient class separation, no single norm-bounded perturbation can simultaneously flip both metrics' predictions, forcing a disagreement that signals an attack. Training requires only clean-image fine-tuning of the encoder. Experiments on ResNet/CIFAR-10 and CLIP/Tiny-ImageNet validate the theorem on a compliant subset and compare metric combinations.

## Strengths

- **Novel detection principle with formal grounding.** The core insight — detecting attacks via forced disagreement between two geometrically complementary metrics — is original. Section 3.2 provides a proof sketch (Theorem 1) showing conditions under which a single perturbation cannot simultaneously flip both metrics' predictions, which is a genuine theoretical advance over purely empirical detectors. The proof is grounded in explicit assumptions (A1–A4) and a well-defined incompatibility argument (Proposition 4).

- **Clean-image-only training.** The fine-tuning procedure (Section 3.3) uses only clean images and avoids adversarial training, making KOALA lightweight and applicable to existing pre-trained encoders without requiring knowledge of specific attack types.

- **Honest ablation and subset analysis.** Experiment 2 (Table 2) systematically compares KL+L0 against three other metric combinations across both model/dataset pairs, and the paper transparently discusses when and why KL+L0+Cosine outperforms the proposed method on CLIP/Tiny-ImageNet (Section 4.3). Experiment 1 (Table 1) explicitly partitions data into theorem-compliant and non-compliant subsets, reporting perfect scores on the compliant subset as the theory predicts, and does not hide the small compliant fraction on CLIP/Tiny-ImageNet.

## Weaknesses

### Fatal
None.

### Major

1. **Non-standard confusion matrix conflates detection with robust classification, making the reported precision/recall uninterpretable as standard detection metrics.** The paper defines (Section 4.2, line 188):

   ```
   TP := [a = 1] ∧ [ (â, ŷ) = (1, ⟂) ∨ (â, ŷ) = (0, y*) ]
   FN := [a = 1] ∧ [ (â, ŷ) = (0, -y*) ]
   ```

   Under this definition, an attacked input (a=1) counts as **true positive** even when the detector misses the attack (â=0), as long as the classifier's prediction happens to be correct (ŷ = y*). A false negative occurs only when the attack both evades detection *and* causes a misclassification. This means a detector that never fires would score well on any dataset where the underlying classifier is robust. The reported numbers — "precision of 0.94 and recall of 0.81" in the abstract (from Table 2) — therefore measure a compound of detection and classifier robustness, not detection alone. The definitions are explicitly stated, which is transparent, but the labels "TP," "FN," "Precision," and "Recall" carry standard meanings in the detection literature that differ from what the paper measures. This is not a fatal error (the paper can redefine metrics, and the core theory is unaffected), but it undermines the paper's central empirical claim of providing a verifiable "adversarial detector."

2. **No evaluation against adaptive attacks — a critical gap for a paper claiming a formal guarantee.** The paper explicitly positions itself as providing guarantees that prior methods lack: prior "methods are generally empirical and lack formal *proof-of-correctness* guarantees against adaptive adversaries" (Section 2, line 48). However, the experiments test only standard attacks (PGD, CW, AutoAttack) that target the classifier, not the detector. An adaptive adversary aware of the dual-metric criterion could attempt to craft a perturbation that fools both metrics simultaneously — and the differentiable smooth L0 surrogate used in training (Section 3.3, line 153) provides a potential optimization pathway. Theorem 1's proof, if correct, should hold against any adversary under its assumptions, but without empirical evaluation against an adaptive adversary, the practical relevance of the guarantee is unverified.

3. **No quantitative comparison to any prior detection method.** The related work (Section 2) lists numerous prior detectors (Mahalanobis, LID, feature squeezing, MagNet, CADet, etc.) and criticizes them for lacking formal guarantees, but provides zero empirical comparison — not a single baseline row in any table. Without baselines, the reader cannot assess whether KOALA's empirical detection performance is competitive or whether the formal guarantee comes at a substantial practical cost.

### Minor

4. **Theorem-compliant fraction is very small on CLIP/Tiny-ImageNet (~10%), limiting practical scope.** Table 1 shows only 510–556 out of 5000 CLIP/Tiny-ImageNet samples satisfy the theorem's conditions. On the remaining ~90% of samples, the F1 score drops to 0.70–0.72. The paper acknowledges this but does not discuss what it means for the method's usefulness — a detector whose formal guarantee applies to 10% of the data is effectively empirical on the other 90%. The theory is sound, but its scope is narrower than the paper's framing suggests.

5. **Train-test mismatch: smooth L0 surrogate during training, hard L0 during inference.** The training loss (Section 3.3, line 153) uses a differentiable sigmoid-based surrogate for the L0 metric, while inference uses the hard, non-differentiable L0 (Equation 2). The surrogate could assign non-zero gradients in regions where the hard L0 is flat, potentially optimizing for a different objective than what is evaluated. This gap is not discussed or ablated.

6. **No AUROC/AUPR or separate false-positive rate on clean data.** The paper reports accuracy/precision/recall/F1, but these depend on the hard agreement/disagreement threshold. The detection literature standardly uses AUROC and AUPR. Additionally, the false positive rate on clean data alone cannot be extracted from the reported metrics, which is critical for deployment scenarios.

7. **No variance or confidence intervals.** All metrics in all tables are point estimates without standard deviations, making it impossible to assess whether differences between configurations are statistically significant.

8. **Key theoretical quantities are not operationalized for practitioners.** The proof sketch for Theorem 1 refers to a "sufficiently large coordinate gap Γ_i(ε)" but does not show how Γ_i is computed on real data or how the threshold τ (Equation 2) affects the condition. Without this, the theorem cannot be applied as a practical diagnostic by other researchers.

### Trivial
- Calling KL divergence a "distance metric" is imprecise (KL is asymmetric and does not satisfy the triangle inequality). Minor terminological imprecision.

## Nice-to-Haves
- Add AUROC/AUPR metrics for compatibility with the detection literature.
- Include a Limitations section discussing the theorem's scope, the lack of adaptive attacks, and the metric definitions.
- Ablate the L0 threshold τ to show sensitivity.
- The unusual train/test split (halving the development sets, Section 4.1) could be changed to the standard CIFAR-10 test split for better comparability.

## Removed Points
These points are flagged to be removed; treat them with caution.
- "Missing appendix / proof not in main text" — The appendix was stripped by the PDF parser; it exists in the original submission and cannot be held against the paper.
- "Ethics and reproducibility statements are generic" / "LLM usage statement not standard" — These are formatting conventions or parser artifacts, not substantive weaknesses.
- "KL direction not justified" — The direction KL(c||p) is a natural choice given that c is the fixed prototype and p is the embedding; this is not a substantive flaw.
- "Speculative-fatal claim about metrics invalidating the paper" — The metric definitions are non-standard but explicitly stated; they affect interpretation but do not invalidate the theoretical contribution.

## Novel Insights
None beyond the paper's own contributions. The reviews converge on the same assessment: the theoretical idea is genuinely interesting, but the empirical evaluation has significant gaps that prevent full assessment of the claimed contribution.

## Suggestions
1. **Redefine the confusion matrix** to use standard detection conventions (TP = a=1 ∧ â=1, FN = a=1 ∧ â=0) and separately report "robust classification rate" (fraction of undetected attacks that still yield correct predictions) as a secondary metric.
2. **Add an adaptive attack evaluation** that explicitly optimizes against the dual-metric agreement criterion using the differentiable smooth L0 surrogate.
3. **Add at least one prior-detection baseline** (e.g., Mahalanobis 2018, LID 2018) to contextualize empirical results.
4. **Operationalize Γ_i(ε)** by showing how the coordinate gap is computed on real data and how τ affects the compliant fraction — this would turn the theoretical condition into a practical diagnostic.

## Score and Decision

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>