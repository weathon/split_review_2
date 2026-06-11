## Summary
# Final Review Report

## Summary

This paper presents SPS (Summarize-Privatize-Synthesize) and its enhanced variant SPS+, which are differentially private dataset distillation algorithms. The core idea is to generate a synthetic version of a sensitive dataset that satisfies differential privacy guarantees, allowing unlimited downstream use (model training, ensembling, federated learning, continual learning) without further privacy cost. The method builds on the D3S dataset distillation framework by (1) replacing the privately-trained model with a public pretrained model, (2) privatizing intermediate activation statistics via the Gaussian mechanism, and (3) synthesizing images that match these privatized statistics.

On CIFAR-10/100 at ε=1, SPS+ achieves 96.2%/76.6% accuracy, competitive with or exceeding DP-SGD (94.8%/70.3%). Beyond accuracy, SPS+ demonstrates practical advantages: support for model ensembling without additional composition, asynchronous federated learning across disjoint data partitions, and class-incremental continual learning without extra privacy cost.

**Overall assessment:** The paper introduces a genuinely useful paradigm shift for private deep learning—privatizing the dataset once instead of the training process. The technical approach is well-motivated and the empirical results are promising. However, several issues need attention: the abstract overclaims superiority without scope boundaries, Theorem 4.1 contains a notational error in the privacy guarantee formula, the dimensionality formula in Section 3.2.2 appears inconsistent, the grouped pseudo-classes mechanism lacks mechanistic explanation, and several experimental comparisons need more careful framing. Novelty claims cannot be fully verified in this run due to disabled external retrieval; manual literature verification is required to confirm SPS+ is indeed the first generation-based method to match DP-SGD accuracy. score placeholder: Final Score: 7/10.

## Strengths
**1. Novel paradigm with practical value.** The paper introduces a conceptually clean approach to DP deep learning: instead of privatizing the training process (as in DP-SGD), privatize the dataset once and unlock unlimited downstream usage. This paradigm shift has genuine practical advantages for model ensembling, cross-silo aggregation, and continual learning—all of which are demonstrated experimentally. The ability to train multiple models, apply any optimizer including SAM, and perform data-attribution analysis on the same DP dataset without additional privacy cost is a meaningful contribution.

**2. Well-engineered technical adaptation.** The adaptation from D3S to the DP setting is technically sound. Removing the reliance on a privately-trained model by using public pretrained models and class-conditional statistics is a natural and effective solution. The noise redistribution trick (Section 3.2.4) that balances sensitivity between global and per-class statistics is clever and demonstrably improves performance. Multistage clipping and grouped pseudo-classes address genuine challenges in the high-privacy regime.

**3. Strong empirical results under strict privacy budgets.** At ε=1 on CIFAR-10/100, SPS+ achieves 96.2%/76.6% accuracy, outperforming DP-SGD (94.8%/70.3%). These are the strongest reported results for a generation-based DP method on these benchmarks. The CAMELYON17 OOD experiment (92.6% at ε=8 vs. DP-SGD 90.5% at ε=10) further demonstrates robustness to domain mismatch between public pretraining and private data.

**4. Comprehensive experimental exploration.** The paper goes beyond standard accuracy comparisons to evaluate compression ratios (10% synthetic data retains near-full performance), oversized datasets (larger-than-original synthetic data yields further gains), federated learning with up to 5 parties, and continual learning across 10 subsets. These experiments convincingly demonstrate the flexibility advantage of dataset-based privacy.

**5. Reproducibility-conscious.** The paper provides pseudocode (Appendix A.1) and mentions code in supplementary material. The algorithm description, while dense, is sufficiently detailed for reproduction by a skilled practitioner in the field.

## Weaknesses
### Major Weaknesses

**W1. Theorem 4.1 contains a notational error in the RDP privacy guarantee.**
The theorem states ε = Mα/(2δ²) for (α, ε)-RDP, with δ appearing without definition. In standard RDP for the Gaussian mechanism, ε(α) = α/(2σ²) where σ is the noise scale. The manuscript's δ is undefined: if it refers to the DP δ parameter (e.g., 10⁻⁵), the formula is incorrect because RDP does not use δ; if it refers to the noise multiplier b₀ scaled by sensitivity, the derivation is missing. This error could propagate into the privacy accounting used for all experimental comparisons. **Fix:** Replace with ε(α) = Mα/(2b₀²) where b₀ is the noise multiplier from eq. (4), then add separate conversion to (ε, δ)-DP.

**W2. Dimensionality formula in Section 3.2.2 appears inconsistent.**
The term D_G^{layer} = D_G + D_C(D_G+1)/2 mixes the global dimension D_G with the class dimension D_C in the covariance term. The covariance dimension should match the mean dimension: D_G^{layer} = D_G + D_G(D_G+1)/2 for global statistics, and D_C^{layer} = D_C + D_C(D_C+1)/2 for class statistics. This directly affects the clipping bound ‖v‖_max and the noise calibration, so the error could cascade into the privacy guarantee. **Fix:** Correct both formulas and verify that the clipping bound derivation remains consistent.

**W3. Abstract overclaims by selective reporting.**
The abstract claims SPS+ "outperforms state-of-the-art (SOTA) DP-SGD results (94.8/70.3%)" citing ε=1. However, at ε=8 on CIFAR-100, SPS+ (WRN34-10 Ensemble) achieves 81.6% vs DP-SGD 81.8%, which is lower. The claim of being "the first alternative to DP-SGD that attains higher accuracy on image-classification tasks" is not universally true across the evaluated privacy budget range. **Fix:** Replace with a bounded claim such as "competitive with or exceeding DP-SGD under strict privacy budgets (ε=1) while offering greater flexibility."

**W4. Grouped pseudo-classes mechanism is under-explained.**
Section 4.2 states that the technique "only works due to dynamics of optimizing the loss function, specifically the Σ inversion in the KL-divergence, and the eigenvalue clipping of Σ" but provides zero mechanistic explanation. The reader cannot assess whether the gains come from the grouping strategy itself, the increased effective number of classes P > C, or the interaction with eigenvalue clipping. This is a core innovation of SPS+ and its mechanism should be explained. **Fix:** Add 2-3 sentences explaining how grouping affects the covariance spectrum and how eigenvalue clipping interacts with the grouped statistics.

**W5. Federated learning privacy accounting is incomplete.**
The federated learning section treats the combination of independently privatized datasets as cost-free, which is correct under parallel composition (disjoint data partitions). However, the paper does not mention this composition guarantee or its assumptions, which could mislead readers into thinking arbitrary composition is allowed. **Fix:** Add one sentence citing parallel composition or explaining why the per-party ε guarantees the combined dataset's privacy.

### Minor Weaknesses

**W6. Introduction could be more sharply focused.**
The first introduction paragraph mixes two distinct roles (privacy threat model + DP-SGD limitations) into a single dense paragraph. The BatchNorm incompatibility claim is presented as absolute, while recent work has partially mitigated this issue. The third paragraph mentions DP-KIP's poor performance but does not explain *why* D3S's structure avoids the same pitfalls.

**W7. CAMELYON17 comparison uses different ε across methods.**
SPS at ε=8 (δ=3×10⁻⁶) is compared against DP-Diffusion and DP-SGD at ε=10, and Private Evolution at ε=7.56. SPS operates under a stricter constraint, which actually strengthens the results, but the asymmetry is not acknowledged.

**W8. Continual learning gap understated.**
The 68.1% vs 76.9% (8.8% drop) gap is described as "remains close," which is a significant understatement compared to the non-continual SPS+ ensemble (80.7%, a 12.6% drop).

**W9. Novelty cannot be fully verified in this review run.**
Due to disabled external retrieval (Retrieval-Disabled Mode), the claim of being "the first generation-based method to match gradient-based approaches" cannot be independently verified against the latest literature. The paper cites relevant prior work (DP-KIP at 58.7%, Private Evolution at 89.13%) which supports the claim, but a systematic literature review is needed for confirmation.

**W10. Computational cost mentioned but not contextualized.**
The conclusion mentions "heavy" generation cost but does not compare it to DP-SGD training cost in the same setting. Given that SPS+ generates 50,000 images, the compute budget vs. a single DP-SGD training run should be quantified.

## Score
**Final Score: 7/10**

**Rationale:** The paper presents a novel and well-engineered approach to private deep learning through dataset distillation, with strong empirical results at strict privacy budgets (ε=1) and clear practical advantages for ensembling, federated, and continual learning. However, the score is constrained by: (1) a notational error in Theorem 4.1 that affects the core privacy guarantee presentation, (2) a dimensional inconsistency in the method's core formula, (3) overclaiming in the abstract that does not hold across all evaluated settings, (4) under-explained mechanisms for SPS+'s key innovations, and (5) novelty claims that require external verification which was unavailable in this review run. Major weaknesses W1 and W2 are fixable with targeted corrections and would increase confidence to 8/10. Weakness W3 requires reframing of claims. The remaining weaknesses are minor presentation issues.

**Scoring breakdown:**
- Research value / contribution: 8/10 (genuinely useful paradigm, strong empirical support)
- Novelty: 7/10 (deferred verification needed; prior art in DP-distillation and statistic-matching exists)
- Soundness / validity: 6/10 (formula errors in Theorem 4.1 and dimensionality need correction)
- Reproducibility: 7/10 (algorithm well-described, but formula errors hinder exact reproduction)
- Presentation: 7/10 (clear structure, but abstract overclaims and under-explained mechanisms)