Now I have enough calibration data. Let me finalize the review.

## Summary
This paper develops a random-matrix-theoretic analysis of data pruning for high-dimensional binary classification with squared loss and ridge regularization. It studies oracle-based pruning rules (label-agnostic and label-aware) that retain examples based on difficulty and/or correctness. Theorem 2 identifies a clean phase transition: "keep hard" is optimal when both the data generator and pruning oracle are excellent, while "keep easy" is optimal when the generator is weak but the pruner is excellent. The paper presents synthetic validation, ImageNet experiments, model collapse simulations, and a qualitative discussion connecting to LLM reasoning results.

## Strengths

1. **Clean theoretical setup (Sections 2–3).** The framework is mathematically precise: binary classification with Gaussian features, squared loss, ridge regularization, and proportionate scaling limit. The geometric quantities ρ, ρ₊, ρ₉ cleanly capture generator/oracle quality via cosine similarities, providing a tractable sandbox for formal analysis of data pruning.

2. **Theorem 2 states a crisp phase transition.** The result that the optimal pruning strategy switches from "keep hard" to "keep easy" depending on generator quality (ρ → 1 vs. ρ < 1, given an excellent pruner) is a sharp, interpretable prediction. Within the stated assumptions, this is a non-trivial finding.

3. **Honest acknowledgment that optimal strategy is not universal.** The paper's core message — that the best curation strategy depends on generator quality, oracle quality, and data scale — is a worthwhile corrective to one-size-fits-all pruning heuristics.

## Weaknesses

### Major

1. **Framing overclaims relative to what is actually delivered.** The abstract, introduction, and conclusion present this as a theory that "resolves a central paradox," "provides a principled explanation for LIMO and s1," and "bends classical scaling laws." What the paper actually delivers is an exact analysis of data pruning for a *linear classifier trained with squared loss on isotropic Gaussian features for binary classification*. The LLM discussion (Section 4.2) assigns the LLM labels of "strong generator" or "weak generator" based on the very outcomes it purports to predict, with no independent estimation of ρ or quantitative mapping between the theory's parameters and the LLM setting. The claims about "bending classical scaling laws" (Kaplan et al., Hoffmann et al.) are unsubstantiated: those scaling laws concern compute–model–data relationships for neural networks, while this paper studies test error vs. pruning fraction for ridge regression classifiers. The paper never engages with the technical content of the scaling-law literature beyond name-dropping. This framing mismatch undermines the credibility of the otherwise solid theoretical contribution.

2. **ImageNet experiments are critically underspecified.** The paper claims to "validate these theoretical claims with empirical results on ImageNet" but provides none of the following: (a) the neural architecture used (ResNet? ViT?); (b) the training procedure (optimizer, learning-rate schedule, epochs, batch size); (c) how the pruning oracle wₒ is constructed from a pre-trained model — what does the "pruning direction" mean for an image classifier, and at which layer's features?; (d) how "keep easy" and "keep hard" are operationalized; (e) the effective dimensionality d of the features and how it relates to n. The proportionate scaling limit d/n → φ is central to the theory, but no dimensionality information is reported. Without these details, the experiments are not reproducible and their connection to the theory is unverifiable.

3. **Model collapse experiments (Figure 3) lack essential context.** The paper reports that iterative pseudo-label training on all data degrades from ~30% to ~52% error while curated training stays stable, but provides almost no experimental details: (a) what dataset is used for the iterative procedure; (b) how pseudo-labels are generated at each round; (c) how the pruning oracle is defined at each round and whether it changes; (d) what "hard valid examples" means concretely in this iterative context; (e) the number of rounds and data sizes. This experiment is presented as a black box.

### Minor

4. **LLM reconciliation is post-hoc labeling, not independent prediction.** Section 4.2 classifies the base LLM as a "strong generator" for average AIME problems and a "weak generator" for hard AIME problems, determined entirely by whether the empirical results show "less is more" or "more is more." No independent measurement of ρ from the LLM's characteristics is provided. This is retrofitting observed outcomes with the theory's vocabulary, not a predictive test. The paper would be stronger if it clearly labeled this section as speculative interpretation rather than validation.

5. **Missing dimensionality d in synthetic experiments.** The synthetic validation (Figure 1) reports n = 100 and n = 5000 but never states the dimensionality d. The theory depends on the scaling limit d/n → φ, and knowing d is necessary to assess whether the asymptotic approximation is reasonable. (The good match between theory and simulation partially mitigates this, but the omission should still be fixed.)

### Trivial

6. **"Random" baseline terminology is imprecise.** The footnote describes the "random" strategy as using an orthogonal pruner (ρ₊ = ρ₉ = 0), which is a reasonable "uninformative pruner" baseline within the paper's oracle-based framework. However, calling it "random" is imprecise — true random subsampling (Bernoulli(p) independent of features) is a distinct baseline. The paper should clarify this.

## Nice-to-Haves
- An intuitive explanation of *why* Theorem 2 holds (the mechanism by which hard examples help a strong generator but hurt a weak one) would significantly improve readability.
- A true random subsampling baseline in the synthetic experiments would sharpen the comparison.

## Removed Points
- **Theorem 1 formula not interpretable from main text** — The criticism about m, \tilde{m}, and r being deferred to the appendix reflects standard practice for theory papers. Removed per hard rule on appendix content.
- **Label-aware curation (Theorem 3) lacks optimal strategy analysis** — The paper states that corollaries and implications are in the appendix, which is stripped by the parser. Cannot verify the gap; removed per hard rule.
- **Missing comparison to Sorscher et al. (2022) theory** — Removed per hard rule on missing related works.
- **Theorem 2's data-rich regime vs. n=100 experiments** — The simulations show good agreement with theory even at small n, which actually strengthens the paper. Not a genuine weakness.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Reframe the abstract and introduction to accurately scope the contribution: a theory of data pruning for high-dimensional linear models. Present the LLM discussion as qualitative speculation/future work, not validation.
2. Provide full experimental details for the ImageNet experiments (architecture, training procedure, pruning-oracle construction) or remove the section — underspecified experiments weaken the paper.
3. Provide full details for the model collapse experiments (dataset, pseudo-labeling procedure, pruning protocol across rounds).
4. State the dimensionality d used in the synthetic experiments.
5. Clarify the "random" baseline terminology and consider adding a true random subsampling baseline.

## Score and Decision

### Calibration Anchors

| Anchor | Avg Score | Round | Itemized | Comparison |
|--------|-----------|-------|----------|------------|
| EOPLy80bBm — "Disentangling the Roles of Representation and Selection in Data Pruning" | 3.00 | 1 | Yes | Rejected for flawed theoretical analysis and unfair comparisons; our paper's theory is cleaner and sounder. |
| e2F0mJJeN0 — "Geometric Median Matching for Robust Data Pruning" | 3.00 | 1 | Yes | Rejected for limited novelty and insufficient experiments; our paper has stronger theoretical novelty. |
| Bk13Qfu8Ru — "Severing Spurious Correlations with Data Pruning" | 7.00 (but listed 3.80 in tool) | 1,2 | Yes | Accepted despite lacking theoretical formulation; our paper has stronger theory but weaker experiments and framing. |
| 9ccZzuix2D — "Distilling the Knowledge in Data Pruning" | 5.33 | 1,2 | Yes | Rejected for limited novelty and experiments misaligned with theory; our paper has stronger theory but similar experimental shortcomings. |
| et5l9qPUhm — "Strong Model Collapse" | 8.00 | 1 | Yes | Accepted for strong theory + well-aligned experiments; our paper has comparable theoretical ambition but far weaker experimental execution. |

**Round-1 bracket:** 3.0–5.5, narrowing to 3.5–5.0.

**Final placement rationale:** The paper sits above the 3.0 anchors (EOPLy80bBm, e2F0mJJeN0) because its theoretical contribution is genuinely novel and mathematically sound — unlike those papers' flawed or shallow theory. It sits below the 5.33–5.67 anchors because those papers at least provide fully specified, reproducible experiments, whereas this paper's ImageNet and model collapse experiments are critically underspecified. The overclaimed framing (LLM explanation, scaling-law bending) is an additional negative that the 5-range anchors did not share. The strongest comparable anchor is 9ccZzuix2D (5.33), but that paper was rejected primarily for insufficient novelty, whereas this paper has genuine novelty undercut by presentation problems — a slightly lower score is warranted.

**Score:** 4.0 (borderline reject). The core theoretical result (Theorem 2) is a genuine contribution, but the paper's current form is undermined by systematic overclaiming and underspecified empirical support. A substantially rewritten version with honest framing and properly detailed experiments could merit a higher score.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>