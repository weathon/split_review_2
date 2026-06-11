## Summary
# Final Review Report

## Summary

This paper addresses modality imbalance in multimodal learning — a phenomenon where faster-converging modalities dominate the shared classifier and suppress weaker ones. The authors propose Classifier-Constrained Alternating Training (CCAT), a two-stage framework that: (1) pre-trains a shared classifier with a regularization term that penalizes large disparities in modality contributions; (2) freezes this classifier during alternating-modal training while using modality-specific Low-Rank Adaptation (LoRA) modules to adapt features; and (3) applies sample-level secondary updates for severely imbalanced instances. Experiments on CREMA-D, Kinetic-Sound, and MVSA datasets show accuracy improvements over existing methods.

The paper identifies a genuine and important problem — that alternating training alone cannot prevent classifier-level bias toward dominant modalities. The proposed solution (freezing a pre-trained unbiased classifier) is conceptually well-motivated. However, several significant issues weaken the contribution: a numerical inconsistency in the abstract's reported gain on CREMA-D (+1.35% claimed vs +2.27% shown in Table 1), overstated claims about a "theoretical isomorphism" between class and modality imbalance that does not hold mathematically, a misnamed "mutual information" estimator that does not match standard MI definitions, missing variance bars on main results, and absence of a limitations discussion. Novelty assessment is deferred due to external literature search being unavailable in this run.

## Strengths
**S1. Well-motivated problem and conceptually clear solution.** The paper identifies a genuine limitation of existing alternating training methods — that they address encoder-level gradient conflicts but overlook classifier-level structural bias. The diagnosis that "encoder-level interventions alone are insufficient to resolve structural preference in classifiers" (Page 1 - Introduction) is a valid and non-trivial observation. The proposed remedy of freezing a pre-trained unbiased classifier is a clean conceptual response to this diagnosis.

**S2. Comprehensive ablation study.** Table 2 systematically ablates four components (classifier freezing, alternating training, secondary updates, LoRA modules) across all three datasets. This allows readers to assess the contribution of each component. The ablation shows that each component contributes positively, with the full configuration achieving the best results, and that the gains are generally consistent across datasets.

**S3. Good benchmark coverage.** The evaluation spans three diverse datasets covering different modality pairs (audio-visual: CREMA-D, Kinetic-Sound; image-text: MVSA), different task types (emotion recognition, action recognition, sentiment analysis), and different scales (up to 30,000+ samples). The inclusion of per-modality performance alongside multimodal accuracy provides useful diagnostic information about modality balance.

**S4. Clear empirical improvements.** The reported accuracy gains on Kinetic-Sound (+6.76% over LFM) and MVSA (+1.92% over MMPareto) are practically significant. The consistent improvement across all three datasets (even after accounting for the CREMA-D numerical discrepancy) suggests the framework has genuine benefits beyond what existing methods achieve.

**S5. Thoughtful use of LoRA for modality-specific adaptation.** Integrating lightweight LoRA modules into the frozen classifier to enable modality-specific adaptation without modifying the shared decision boundaries is an elegant engineering choice that balances flexibility with constraint. The rank grid search (r=1,2,4,8,16) in Table 3 provides useful sensitivity analysis.

## Weaknesses
### W1. Numerical inconsistency in abstract (Critical)

The abstract claims accuracy gains of "+1.35% on CREMA-D" over state-of-the-art methods. However, Table 1 shows the best prior method on CREMA-D is LFM at 83.62%, and CCAT achieves 85.89%, yielding a difference of +2.27 percentage points (not +1.35%). This is a clear numerical inconsistency between the abstract and the main results table. Even accounting for potential rounding or comparison against a different baseline, no entry in Table 1 supports a +1.35% gain on CREMA-D. This error undermines trust in the reported numbers.

**Required action**: Correct the abstract to read "+2.27%" or clarify which baseline is being compared against. All numerical claims should be cross-checked against Table 1 before resubmission.

### W2. Overstated theoretical contribution (Major)

The paper claims (Contribution i) to provide "a new theoretical framework for understanding multimodal imbalance" and Section 3.1 asserts "a profound theoretical isomorphism between class imbalance and modality imbalance at the gradient optimization level." However, the mathematical analysis reveals significant differences that are glossed over:

- For class imbalance (Eq. 2), the gradient for the correct-class weight is ∂L/∂w_y ≈ -f (class-independent). For a different class j≠y, the gradient is approximately zero.
- For modality imbalance (Eq. 3), the gradient is ∂L/∂w_j ≈ (ŷ_j - 𝟙_{[j=y]}) γ₁ f^{(1)} (class-dependent and modality-specific).

These are qualitatively different gradient structures. The "isomorphism" is at best a high-level analogy (both involve early-dominance-triggered bias), not a formal theoretical equivalence. Calling it a "theoretical framework" and "proof of their underlying similar" (Section 3.1, Page 2) overstates what is actually established.

**Required action**: Replace "theoretical isomorphism" with "high-level optimization analogy" or "shared self-reinforcing bias pathology." Clearly state that the gradient mathematics differ between the two settings, and position the connection as a design inspiration rather than a formal framework.

### W3. Misnamed "Mutual Information" estimator (Major)

Eq. (5) defines what the paper calls mutual information (MI), but the expression does not match any standard definition of MI. Standard MI between two random variables is I(X;Y) = E[log(p(x,y)/p(x)p(y))]. Eq. (5) computes a log-softmax over inner products of normalized features, which is more accurately described as a normalized cross-modal similarity score. The symbol `MI` is misleading and inflates the technical contribution. Additionally:

- The overbar notation (¯f_i, ¯z_i^m) is not defined — are these L2-normalized features? Centered features? 
- The term log(N) appears ad-hoc without justification.
- The resulting "contribution" c_i^m from Eq. (6) measures relative feature alignment to the fused representation, not causal contribution to classification.

**Required action**: Rename to "Modality Contribution Score" or "Cross-Modal Alignment Score." Define all notation explicitly. Justify or remove the log(N) term. Add a caveat that this measures correlation, not causation.

### W4. Missing variance and significance reporting (Major)

Table 1 reports "average test accuracy (%) of three random seeds" but does not report standard deviations, confidence intervals, or significance tests. Several improvements are modest in absolute terms (e.g., CREMA-D: +2.27% over LFM; MVSA: +1.92% over MMPareto). Without variance information, readers cannot determine whether these differences are statistically reliable or within the range of random seed variation.

**Required action**: Report mean ± std over seeds for all entries in Table 1 and Table 2. For the main comparisons, include a paired significance test (e.g., paired t-test or Wilcoxon) against the strongest baseline.

### W5. Missing limitations discussion (Major)

The paper lacks any Limitations section. The Future Work (Section 6) only mentions extending to tri-modal datasets, which is a positive extension but does not acknowledge current weaknesses. Important limitations that should be discussed include: (a) two-stage training increases implementation complexity; (b) hyperparameters (β, r, λ) are dataset-specific and require grid search without theoretical guidance; (c) the contribution estimator is not validated as a reliable measure of modality importance; (d) evaluation covers only three datasets with two modality pair types; (e) no robustness testing (OOD, noise, domain shift) has been performed, despite using the word "robust" in the abstract.

**Required action**: Add a dedicated Limitations subsection that candidly discusses at least 4 concrete limitations with specific suggestions for how they could be addressed in future work.

### W6. Gradient analysis is incomplete (Major)

The gradient analysis in Section 3.1 has two gaps. First, the class-imbalance analysis (Eq. 2) does not distinguish between the correct-class weight (j=y) and other class weights (j≠y). For j≠y and ŷ_j≈0, the gradient is ∂L/∂w_j ≈ (0-0)f = 0, not -f. The text's discussion of "parameter updates become dominated by feature norm f" only applies to w_y, which is a critical distinction. Second, the modality-imbalance analysis (Eq. 3) conflates classifier-weight gradients with encoder learning signals — the chain from "classifier weight gradient is suppressed" to "encoder does not learn" requires unpacking through ∂L/∂f = Σ_j (ŷ_j - 𝟙_{[j=y]}) w_j, which is not discussed.

**Required action**: Revise the gradient analysis to (a) treat w_y and w_{j≠y} separately, (b) clarify the gradient chain from classifier weights to encoder parameters, (c) soften claims about "vicious cycles" that go beyond what the simple gradient formulas can support.

### W7. LoRA distribution-mismatch justification is insufficient (Moderate)

Section 3.3 states that the frozen classifier faces a distribution mismatch when processing unimodal features (P(z^m|y) ≠ P(f|y)). The solution is LoRA modules that add low-rank corrections. However, the paper does not explain *why* an additive low-rank correction to features before the frozen classifier is sufficient to bridge this distribution gap, nor does it analyze what rank is needed. The justification for why LoRA is the right tool (rather than, say, fine-tuning the classifier's top layers or adding an MLP adapter) is missing.

**Required action**: Add a paragraph explaining the assumption that the distribution shift from P(f|y) to P(z^m|y) is approximately low-rank, and discuss conditions under which this assumption might fail.

### W8. Insufficient robustness evaluation (Moderate)

The abstract claims "robust multimodal representations," and the paper uses "robust" in several places. However, the evaluation only measures standard accuracy on IID test splits. No experiments test robustness to: input noise or corruption, modality dropout, domain shift, out-of-distribution samples, or adversarial perturbations. A method that improves accuracy on clean data does not necessarily produce robust representations.

**Required action**: Either (a) add robustness experiments (e.g., noise perturbation, modality masking, cross-dataset evaluation) and report results, or (b) replace "robust" with more precise wording such as "effective" or "balanced" that matches the actual evaluation scope.

### W9. SOTA claim is partially unverifiable and overbroad (Moderate)

The paper claims "state-of-the-art performance in most scenarios" (Section 4.2). However: (a) LFM does not report MVSA results (marked "-" in Table 1), so the comparison is incomplete for that dataset; (b) CCAT's video-only accuracy on KS (53.75%) is below LFM (55.62%); (c) without external literature verification (unavailable in this run), the SOTA claim cannot be independently confirmed. The evaluation covers only three datasets, which limits the scope of any global SOTA claim.

**Required action**: Replace global SOTA language with bounded claims: "achieves the best accuracy among evaluated baselines on these three benchmarks." Explicitly note the KS video case where CCAT does not lead.

### W10. Writing quality issues (Minor)

Several writing issues reduce readability:
- Contribution (iii) ends with "faithfully." — appears to be a typo or leftover artifact.
- Observation (iii) in Section 4.2 is grammatically awkward: "we prioritize liberating weak modalities representational potential."
- Figure 1 caption and table are duplicated in the PDF extract.
- The abstract references "over 30,000 samples" in a contribution claim, which is an oddly specific detail for a contribution summary.

**Required action**: Proofread the entire manuscript, fix the "faithfully." typo, rewrite observation (iii) for clarity, and remove sample-count detail from contribution list.

## Score
**Final Score: 6/10**

**Rationale**: The paper addresses a well-motivated problem and proposes a clean, conceptually sound solution. The empirical results show meaningful improvements across multiple benchmarks, and the ablation study is thorough. However, the score is limited by several factors:

1. **Research value**: The core idea (freezing a pre-trained unbiased classifier to prevent modality bias) is practically useful and the paper provides reasonable empirical validation. However, the claimed "theoretical framework" (Contribution i) does not hold up to scrutiny — the gradient analysis is incomplete and the "isomorphism" with class imbalance is overstated. This reduces the scientific contribution below what the paper claims.

2. **Novelty**: Deferred for manual verification due to external literature search being unavailable. The paper's technical components (bidirectional cross-attention, LoRA, contribution regularization, alternating training) are all existing building blocks. The novelty lies in how they are combined and in the specific insight about classifier freezing. A definitive novelty assessment requires literature comparison that could not be performed in this run.

3. **Validity concerns**: The numerical inconsistency in the abstract (W1) is a factual error that must be corrected. The misnamed "mutual information" estimator (W3) inflates the technical contribution. Missing variance bars (W4) make it impossible to assess statistical reliability. These issues collectively reduce confidence in the reported results.

4. **Completeness**: The absence of a limitations section (W5), lack of robustness evaluation (W8), and partial SOTA verification (W9) suggest the paper would benefit from additional development before being publication-ready.

The paper has clear strengths and addresses an important problem. With the identified issues addressed (particularly W1, W3, W4, and W5), the work could reach a score of 7-8/10.