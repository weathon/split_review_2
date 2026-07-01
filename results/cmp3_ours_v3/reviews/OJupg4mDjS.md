## Summary

This paper tackles Geodesic PCA (GPCA) in the Wasserstein space of probability measures, proposing two methods: (1) for centered Gaussian distributions using the Bures-Wasserstein geometry lifted to the general linear group GL_d, with a principled optimization formulation and a distortion analysis comparing GPCA to tangent PCA; and (2) GPCAGEN, a neural-network-based method for general absolutely continuous measures using Otto's parametrization of Wasserstein geodesics. The Gaussian part is mathematically well-grounded and quantitatively validated; the general-case method is validated only through qualitative visualizations.

## Strengths

- **Clean Riemannian lifting framework for Gaussian GPCA (Proposition 3).** The formulation converting the curved geodesic optimization in S_d^{++} into a linear optimization in GL_d over horizontal line segments is mathematically elegant and principled. The clipping operator p_{A,X} correctly handles the invertibility constraint, and the orthogonality condition for higher components is consistently derived from the horizontal bundle.

- **Explicit distortion analysis (Proposition 4, Equation 14).** The paper provides a concrete quantitative expression showing how the distortion between TPCA and GPCA scales with the eigenvalue ratio (a−b)/(a+b) and rotation angle θ. This is a genuine theoretical contribution that gives insight into when linearization fails.

- **Intellectual honesty about limitations.** The paper candidly reports that on random covariance matrices GPCA improves upon TPCA by less than 1% on average (line 208), and notes that in the pathological same-eigenvalues case GPCA can behave worse than TPCA by projecting data onto geodesic boundaries (line 232). This candor is uncommon and valuable.

- **Avoiding ICNNs.** Otto's parametrization allows the method to avoid input-convex neural networks (ICNNs), which are architecturally restrictive and harder to train. This is a genuine methodological advantage over alternative parametrizations.

## Weaknesses

### Major

- **GPCAGEN evaluation is almost entirely qualitative, insufficient to validate the core claim.** The synthetic experiment with "known geodesics" is described only in passing (line 238) with no quantitative result — no reconstruction error, cosine similarity, or RMSE between recovered and ground-truth components. For the real-world datasets (ModelNet40, Landscape images), the evidence is purely visual: "the first principal component captures the distinction between hanging lamps and standing lamps" (line 260). The paper explicitly declines to provide a quantitative comparison to the natural baseline TPCA, calling it "not meaningful" (line 264). However, the paper's central claim is that GPCAGEN solves the exact GPCA problem. Without quantitative metrics (e.g., projection reconstruction error, variance explained, held-out evaluation), or at minimum a quantitative synthetic benchmark, the reader cannot assess whether the neural approximations (Sinkhorn divergence, finite-capacity MLPs, Monte Carlo Hessian estimates, regularization) preserve geometric meaning. This is the paper's most significant weakness.

- **Convergence criteria and computational cost are not reported.** Algorithm 1 says "while not converged" but provides no convergence criterion, training iteration count, or wall-clock runtime. The reader cannot assess whether GPCAGEN is practical for datasets of 100 point clouds. This is essential information for a neural method paper.

### Minor

- **"Exact" framing is overstated for the neural method.** The abstract claims the methods are "exact in the sense that they do not rely on a linearization of the Wasserstein space." In the Gaussian case this is defensible (the Bures-Wasserstein distance and geodesics are computed exactly). For GPCAGEN, however, the Wasserstein distance is replaced by the Sinkhorn divergence (which has a known entropic bias), geodesics are parameterized by finite-capacity MLPs, Hessian eigenvalues are estimated from finite Monte Carlo batches, and the overall objective is optimized via SGD in a non-convex landscape. Calling the result a "true geodesic" conflates the exact geometric parametrization (Otto's formula) with the approximate computational implementation. Retracting the "exact" claim for the neural method and characterizing the approximation error would better reflect what the paper actually demonstrates.

- **No ablation studies or sensitivity analysis for key hyperparameters.** GPCAGEN has at least five knobs that could materially affect results: Sinkhorn regularization ε, number of samples m per distribution, regularization coefficients λ_I and λ_O (set to 1.0 without tuning, line 256), and MLP architecture (four hidden layers of size 128, chosen without justification). A minimal sensitivity study on the synthetic benchmark would substantially strengthen the paper.

- **Abstract promises a TPCA comparison that is not delivered for the general case.** The abstract states the paper provides "comparison to classical tangent PCA through various examples," but for GPCAGEN the paper explicitly declines to provide a numerical comparison (line 264).

- **Simplification in orthogonality constraint not analyzed.** The paper imposes intersection in Diff(Ω) (equality of diffeomorphism representatives) rather than only requiring intersection in Prob(Ω), acknowledging this is a stronger condition (lines 196-197). The effect of this approximation on the recovered second component is not characterized.

### Trivial

- None.

## Nice-to-Haves

- A study of how the choice of reference measure ρ (currently fixed to standard Gaussian) affects the quality of learned geodesics.
- Discussion of how the Sinkhorn parameter ε is chosen and whether its bias affects the recovered geodesics.
- A quantitative reconstruction-error benchmark where both GPCAGEN and TPCA project held-out distributions onto components and compare the Wasserstein distance from original to projection.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **"The orthogonality constraint is stronger than necessary" as a separate severe weakness.** The paper acknowledges this design choice and explains it as a computational simplification (computing R* is expensive). The point is kept but demoted to Minor — it is an acknowledged trade-off, not an oversight.
- **Section-by-section notes about the MNIST experiment being qualitative.** This is subsumed by the overarching Major weakness about GPCAGEN evaluation.
- **Criticism about missing appendix content, proofs, or references.** The parser strips these from all papers; they exist in the original submission.
- **Concern about "the optimization landscape in the space of MLP parameters preserving geometric meaning."** This is a generic concern about any neural method applied to a geometric problem and is not specific to this paper's approach.

## Novel Insights

The most striking observation emerges from comparing the two parts of the paper. The Gaussian GPCA section demonstrates that when exact computation is feasible, GPCA and TPCA are nearly identical except in contrived near-degenerate cases — and even then GPCA may produce worse practical behavior (projection onto geodesic boundaries). This implicitly raises the question of whether the considerable complexity of GPCAGEN is justified for real datasets, especially when its benefits cannot be quantitatively demonstrated against TPCA. The paper's own honesty about the Gaussian case thus inadvertently undermines the motivation for the general-case method more than any external critique could.

## Suggestions

1. Provide quantitative validation for GPCAGEN on the synthetic benchmark: report reconstruction error of recovered first and second components against ground truth as a function of sample size m and Sinkhorn parameter ε.
2. Report convergence criteria, training iterations, and wall-clock runtime for all GPCAGEN experiments.
3. Conduct a sensitivity study over λ_I, λ_O ∈ {0.1, 1.0, 10.0} on the synthetic benchmark.
4. Retract or substantially qualify the "exact" claim for the neural method, making clear that the exactness applies to the geometric parametrization, not to the computational solution.

## Score and Decision

**Round 1 bracket:** Plausible score range 4.0–6.0, based on comparison to calibration anchors.

**Anchor papers used for calibration (all rounds):**

| Path | Avg Human Score | Round | Comparison |
|------|----------------|-------|------------|
| EyWKb7Ltcx (SPD classifiers, Reject) | 5.00 | 1 | Similar theoretical depth but rejected for incremental contribution; current paper is more novel theoretically but has weaker evaluation |
| HB4lr0ykTi (Wasserstein Flow Matching, Reject) | 6.33 | 1 | Most methodologically similar (Wasserstein geometry + neural nets); had SOME quantitative eval but was still rejected; current paper has weaker eval for general method but stronger theory |
| mkDam1xIzW (Probabilistic Geometric PCA, Accept) | 7.33 | 1 | Most topically similar (PCA on manifolds); had stronger evaluation with real data benchmarks; current paper has comparable theory but substantially weaker evaluation |
| DWI1xx2sX5 (Neighbor-aware Geodesic Transportation, Reject) | 4.00 | 2 | Weaker theory, more experiments; current paper has stronger theoretical contributions |
| rY8xdjrANt (OT Barycenter, Reject) | 6.20 | 2 | OT theory paper with strong convergence analysis but rejected; current paper is comparable in theory but weaker in evaluation |
| StYc4hQAEi (Sliced Wasserstein, Accept) | 6.50 | 2 | Strong theoretical contribution with thorough evaluation; current paper's Gaussian part is comparable but GPCAGEN evaluation is much weaker |
| WPz5e5V85k (Wasserstein Proximal, Reject) | 6.00 | 1 | Strong convergence theory but rejected; current paper has novel framework but less rigorous analysis |

**Narrowing:** The Wasserstein Flow Matching anchor (6.33, rejected) is the closest methodological match and provides the strongest calibration signal. That paper had *some* quantitative evaluation and was still rejected. The current paper has *no* quantitative evaluation for its general-case method, placing it below WFM. The Gaussian GPCA theory is stronger than WFM's Gaussian contribution, but the paper presents GPCAGEN as its headline contribution. Comparing against the SPD Classifiers anchor (5.00, rejected), the current paper has more theoretical novelty but a larger evaluation gap. The final score is calibrated against these two anchors, settling at 5.0.

The paper has genuine theoretical merit in the Gaussian GPCA section, but the GPCAGEN method — presented as the primary contribution filling the stated gap — lacks quantitative validation. The evaluation is entirely qualitative, the "exact" framing is overstated for the neural method, and key implementation details (convergence, hyperparameter sensitivity) are absent.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>