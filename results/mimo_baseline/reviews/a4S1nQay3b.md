## Summary
This paper proposes CorreGen, a generative framework for robust multi-view clustering under noisy correspondence. It formulates cross-view correspondence learning as maximum likelihood estimation with latent variables, solved via an EM algorithm where the E-step uses Gaussian Mixture Model–guided marginals with optimal transport to infer soft category-level correspondences (including virtual samples for unalignable outliers), and the M-step performs a weighted contrastive objective. The authors identify two forms of noisy correspondence—category-level and sample-level mismatch—and show substantial improvements over seven baselines on four datasets.

## Strengths
- **Clear and useful problem taxonomy.** The formalization of category-level mismatch (same-class samples treated as negatives) and sample-level mismatch (alignable mispairs and unalignable outliers) is well-motivated and provides a structured lens for thinking about noisy correspondence in MVC.
- **Elegant EM formulation with a unifying result.** Casting correspondence learning as marginal likelihood maximization and deriving the EM update is clean and principled. Proposition 2 showing InfoNCE as a special case under uniform marginals and deterministic posterior is a nice theoretical connection that grounds the approach in the existing literature.
- **Consistent and often substantial empirical gains.** The method outperforms seven SOTA baselines across all datasets and noise settings. On UMPC-Food101—a naturally noisy web-crawled dataset—CorreGen achieves ~50% ACC vs. ~36% for the next best (DIVIDE) at 0% MR, a ~14 point gap. Gains are maintained even at 80% mismatch ratio (43.00 vs. 27.59 for CANDY on UMPC-Food101).
- **Progressive correspondence discovery is well-visualized.** Figure 3 convincingly shows that the estimated posterior distributions converge toward the ground-truth category-level block structure over training.

## Weaknesses
### Fatal
None.

### Major
- **No ablation results in the accessible paper.** The authors list Q5 ("Are the proposed components crucial for the improvements?") as deferred to Appendix F, which is stripped. The method combines several novel ingredients (GMM-guided marginals, virtual sample mechanism, OT formulation, weighted contrastive M-step) and it is unclear which drives the gains. Without ablation, it is difficult to assess whether a simpler variant—e.g., weighted contrastive loss with uniform marginals and the virtual sample idea—would suffice. This is the single largest gap in the evaluation.
- **Circular dependency in GMM-guided marginals is under-analyzed.** The E-step fits a GMM on the current embedding space to estimate marginals, but the quality of those embeddings depends on prior correspondence estimation. While the paper mentions momentum updates for stability, there is no empirical or theoretical analysis of initialization sensitivity, convergence behavior, or failure modes when initial embeddings are poor (e.g., at high noise ratios). The reliance on a fixed number of GMM components equal to the true number of classes is a strong assumption that is not discussed.
- **Disconnect between category-level mismatch motivation and experiments.** The paper identifies category-level mismatch as a primary motivation, but the synthetic experiments (Tables 1–2) only inject instance-level permutations (MR) and sample corruption (CR). The category-level mismatch is implicitly present in datasets like UMPC-Food101, but the experimental design does not directly evaluate category-level noise robustness (e.g., by explicitly constructing within-class cross-view pair swaps as negatives). The visualization in Figure 3 is suggestive but not quantitative.

### Minor
- **Scalability concerns are unaddressed.** The OT-based E-step operates on (N+1)×(N+1) matrices per view pair. While mini-batch training is standard, the paper provides no runtime analysis, memory requirements, or discussion of scaling to large datasets. The Scaling Algorithm (Proposition 1) involves iterative matrix-vector multiplications of size N, which could become expensive.
- **Limited diversity of experimental settings.** Only four datasets are used, all in image–text or multi-feature settings. The method's effectiveness on other modalities (e.g., video–audio, multi-sensor) or larger-scale settings is unexplored. Two datasets (Scene15, Caltech101) are relatively old benchmarks.
- **The ρ hyperparameter (noise ratio for virtual samples) requires knowing or estimating the noise level.** The paper does not discuss sensitivity to this choice in the main text or how to set it in practice for real-world datasets where the noise ratio is unknown.

### Trivial
- Minor notation inconsistency: summation subscripts in Eq. (3) use v_i, v_1, v_2 inconsistently.

## Nice-to-Haves
- A comparison against methods from related domains (e.g., robust contrastive learning approaches outside MVC, such as Debiased Contrastive Learning) to contextualize gains.
- Analysis of the sensitivity of performance to the number of GMM components, especially when this is mismatched with the true number of clusters.
- Runtime comparison against baselines to establish that the method is computationally competitive.

## Novel Insights
The paper's most novel insight is reframing noisy correspondence in multi-view clustering from a discriminative denoising problem (reweighting/realignment pairs) to a generative correspondence discovery problem via maximum likelihood estimation. The EM-based decomposition cleanly separates the "which samples correspond" question (E-step with GMM-guided OT) from the "how to learn representations" question (M-step with weighted contrastive loss). The observation that InfoNCE is a special case is a satisfying theoretical bridge. However, the individual components (OT for cross-modal alignment, GMM for soft clustering, virtual samples for outlier rejection) are all well-established; the contribution is more in their integration than in any single technique.

## Suggestions
- Include key ablation results in the main paper showing the contribution of GMM-guided marginals vs. uniform marginals, virtual samples vs. no virtual samples, and OT vs. simpler assignment strategies. This is essential for validating that the claimed contributions matter.
- Add a direct experiment on category-level mismatch: synthetically swap cross-view labels within the same class and measure how well each method recovers the correct category-level correspondences.
- Provide a brief discussion of convergence properties and initialization strategy for the EM loop, even if only empirical.
- Discuss the sensitivity to the noise ratio ρ and whether it can be estimated automatically (e.g., via the virtual sample mass after convergence).

## Score and Decision
The paper presents a well-motivated generative framework with a clean mathematical formulation and strong empirical results, particularly on the naturally noisy UMPC-Food101 dataset. The key weakness is the missing ablation analysis (deferred to a stripped appendix) that is essential for validating the contribution of each proposed component. The circular dependency in the GMM-based E-step and the gap between category-level motivation and experimental validation are also concerns. Overall, the contribution is solid but the evaluation gaps prevent a confident acceptance.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>