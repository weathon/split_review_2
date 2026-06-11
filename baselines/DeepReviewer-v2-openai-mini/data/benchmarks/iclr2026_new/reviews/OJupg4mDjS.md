## Summary
# Final Review Report

## Summary

This paper addresses Geodesic Principal Component Analysis (GPCA) in the Wasserstein space of probability measures — a problem of finding geodesic curves that best capture modes of variation in a dataset of distributions. The authors propose two algorithms for the *exact* GPCA problem (without linearization): one for centered Gaussian distributions using the Bures-Wasserstein quotient geometry (lifting from SPD matrices to GL_d), and one for general absolutely continuous measures called GPCAGEN, which parametrizes geodesics via MLP-parameterized maps and functions under Otto's formulation.

The theoretical framing is sound and builds on established geometric principles (Bures-Wasserstein geometry, Otto's fiber bundle, horizontal lifts). The Gaussian case provides a clean optimization formulation with explicit orthogonality constraints. The general case avoids input-convex neural networks by using Otto's parametrization, with Sinkhorn-based training.

**Overall assessment:** The paper presents a principled geometric contribution with clear mathematical articulation. However, the experimental validation is almost entirely qualitative, relying on visual inspection of interpolations without quantitative baselines, error metrics, convergence analysis, or sensitivity studies. The novelty relative to existing Wasserstein PCA methods (Seguy & Cuturi 2015, Cazelles et al. 2018) cannot be fully assessed because a direct numerical comparison is avoided rather than addressed. Several technical gaps (orthogonality condition typo, second-component geometric validity, Hessian eigenvalue robustness) require attention before the method can be considered fully validated.

## Strengths
1. **Principled geometric formulation.** The paper correctly identifies the GPCA problem in Wasserstein space and builds on rigorous Riemannian geometry foundations (Otto's fiber bundle, Bures-Wasserstein quotient geometry). The lifting of the GPCA objective to the total space GL_d for Gaussians is elegant and mathematically well-motivated.

2. **Avoidance of input-convex neural networks.** GPCAGEN's use of Otto's parametrization (where the geodesic is determined by a function f whose gradient defines the horizontal displacement) avoids the need for input-convex neural networks. This is a practical advantage, as ICNNs can be challenging to train and have limited capacity.

3. **Continuous representation and sampling.** Unlike TPCA which operates on discrete empirical measures, GPCAGEN learns a continuous geodesic from which samples can be drawn at any t. This is a genuine methodological advantage, especially for applications requiring interpolation or density estimation.

4. **Explicit orthogonality and intersection constraints.** The paper provides a concrete optimization framework for the second and higher geodesic components, with explicit regularization for orthogonality (L² inner product of horizontal vector fields) and intersection (matching in diffeomorphism space). This goes beyond prior work that only addressed the first component.

5. **Honest discussion of limitations.** The paper acknowledges that GPCA can yield "undesirable effects" in certain settings (near the SPD cone boundary) and that the relationship between GPCA and TPCA is empirically close in generic cases. This transparency is commendable.

## Weaknesses
### Major Weaknesses

1. **Lack of quantitative experimental validation (P0).** The experiments for GPCAGEN (Section 5.2) are purely qualitative — all claims about successful geodesic recovery are supported only by visual inspection of figures. No numerical metrics (GPCA objective value, reconstruction error, projection variance explained, geodesic recovery error) are reported. The paper explicitly avoids quantitative comparison with TPCA by claiming it is "not meaningful," but a careful side-by-side evaluation on a common discretized task would be feasible and informative. Without quantitative evidence, readers cannot judge whether GPCAGEN correctly minimizes Eq. (1) or whether it merely overfits to the Sinkhorn approximation.

2. **Critical typo in orthogonality condition (P0).** On Page 3 - Otto-Wasserstein geometry, the orthogonality condition reads: "⟨∇f̃ ∘ φ, ∇f̃ ∘ φ⟩_{L²(ρ)} = 0," which is the norm of ∇f̃, not the inner product between ∇f and ∇f̃. The correct expression is "⟨∇f ∘ φ, ∇f̃ ∘ φ⟩_{L²(ρ)} = 0." This is not a surface typo — it defines the fundamental geometric concept of orthogonal geodesics needed for the second GPCA component. If uncorrected, it could propagate into misunderstandings about the 𝒪 regularizer's justification.

3. **Geometric validity of second component orthogonality constraint (P1).** In Section 3, the second component constraint sets A₂ = A₁ + t*X₁ and imposes ⟨X₂, X₁⟩ = 0 with R* = I_d. However, horizontality of X₁ at A₁ does not automatically guarantee horizontality at A₂ = A₁ + t*X₁, because the horizontality condition Eq. (5) depends on A. The paper states "since X₁R* is horizontal at A₂" but does not verify this when R* = I_d. This gap needs either a proof or a corrected constraint formulation.

4. **Hessian eigenvalue robustness in GPCAGEN (P1).** The clipping procedure for t_min, t_max relies on minibatch estimates of Hessian eigenvalues. With finite batch size m (unspecified), there is no guarantee that the sampled eigenvalues capture the true extremal eigenvalues over the full support of the reference distribution. The diffeomorphism condition (I_d + tH_f positive definite) could be violated outside the minibatch, leading to invalid geodesics. The paper provides no diagnostic for this failure mode.

5. **Regularization weight sensitivity (P1).** The second component uses λ_I = λ_O = 1.0 across all experiments without ablation, despite the three loss terms having different units and scales (Sinkhorn divergence, L² intersection cost, and dimensionless orthogonality cosine). Sensitivity to these hyperparameters is unexplored.

### Minor Weaknesses

6. **Related works reads as a list.** The paragraph lists prior work chronologically rather than organizing by comparison axis. A structured taxonomy (linearized methods, 1D exact methods, approximate methods via generalized geodesics) would make the novelty claim stronger and easier to evaluate.

7. **Introduction narrative order delays the gap statement.** The concrete research gap ("a method to solve the exact GPCA problem...is still missing") appears only at the end of the related works paragraph, midway through the introduction. Front-loading the gap would improve readability.

8. **Abstract lacks empirical findings.** The abstract describes what the paper does but not what was found. A reader cannot determine from the abstract whether GPCA outperforms TPCA or under what conditions.

9. **GPCA-TPCA comparison lacks statistical detail.** The claim that GPCA improves by "less than 1%" over TPCA on random data lacks standard deviation, distribution shape, or maximum observed improvement. The 100-trial experiment should be reported with summary statistics.

10. **Discussion of GPCA's undesirable behavior is incomplete.** The paper notes GPCA can be "worse-behaved as TPCA" near the cone boundary but does not explain the mechanism (geodesic clipping, projection non-uniqueness) or provide practical guidance on when to prefer TPCA over GPCA.

## Score
**Final Score: 6/10**

**Rationale:** This score prioritizes research value and novelty as primary dimensions, consistent with the scoring policy.

**Research Value / Contribution (5/10):** The paper introduces a principled geometric framework for exact GPCA that is conceptually well-motivated. However, the contribution is substantially weakened by the lack of quantitative experimental validation. Without numerical evidence that GPCAGEN correctly minimizes the GPCA objective, outperforms baselines, or recovers known structures with measurable accuracy, the practical value of the proposed methods remains unsubstantiated. The Gaussian GPCA formulation (Proposition 3) is the strongest contribution, but its empirical evaluation is limited to a single 2D toy setting.

**Novelty (7/10):** The idea of using Otto's parametrization with MLPs for GPCA, and the lifting of Gaussian GPCA to GL_d with explicit rotation optimization, appears methodologically novel. However, due to Retrieval-Disabled Mode in this review, novelty cannot be fully verified against the literature. Marked as *deferred manual verification*.

**Validity / Soundness (5/10):** The theoretical development is mathematically sound in its core elements (Propositions 1-3), but the paper contains a significant typo in the orthogonality condition (Page 3) that undermines a key geometric definition, and the second-component orthogonality constraint (Section 3) has a geometric gap that is not addressed. The Hessian eigenvalue estimation in GPCAGEN (Algorithm 1) lacks robustness guarantees. These issues reduce confidence in the correctness of the implementation.

**Reproducibility (6/10):** Code is provided, and Algorithms 1 gives a procedural outline. However, key hyperparameters (batch size m, Sinkhorn ε, learning rates, network architectures beyond layer counts) are not fully specified. The minibatch Hessian estimation introduces stochasticity that is not characterized.

**Presentation (7/10):** The paper is well-structured with clear mathematical exposition. However, the abstract lacks empirical conclusions, the introduction delays the gap statement, and the related work is organized as a list rather than a structured comparison.

**Revision path:** Addressing the P0 weaknesses (adding quantitative experiments, fixing the orthogonality typo, verifying the second-component geometry) would substantially strengthen the paper. A target score of 7-8/10 is achievable after these revisions.

**Post-Revision Target:** [7, 8]/10