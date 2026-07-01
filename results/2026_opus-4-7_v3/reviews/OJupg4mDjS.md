Now let me read the rest of the paper to check any remaining details:Now I have a thorough understanding of the paper. Let me draft the review.Now let me do Round 1 calibration — bracketing across score bands:Let me read some of the most relevant anchor papers to calibrate:Now let me form my bracket and finalize the review. Based on the calibration:

**Round 1 Bracket Assessment:**

- **Strong reject (<1.5)**: Non-contributions — paper far above these.
- **Reject (1.5-3.5)**: Papers with fundamental contribution/correctness issues (Grassmannian 3.0, MKRRR 3.0, unbalanced OT 2.6). Our paper is substantially stronger.
- **Borderline reject (3.5-5.5)**: Papers like "Intrinsic Riemannian Classifiers on SPD" (5.0), "Relative-Translation Invariant Wasserstein" (3.8). These have decent ideas but significant experimental or novelty gaps.
- **Borderline accept (5.5-7.5)**: "Wasserstein Flow Matching" (6.33, rejected), "OT Barycenter" (6.20, rejected), "Probabilistic GPCA" (7.33, accepted). Solid math but varying experimental strength.
- **Accept (7.5-8.5)**: "Flow Matching on General Geometries" (8.0, accepted), "Comparing noisy neural populations" (8.0, accepted). Strong theory + comprehensive quantitative experiments.
- **Strong accept (>8.5)**: No results returned.

**Initial bracket: 5.0–6.5.** The paper's mathematical framework is comparable to borderline-accept work but GPCAGEN's entirely qualitative evaluation and the limited practical advantage shown for the Gaussian case push it toward the lower end. The "Wasserstein Flow Matching" paper (6.33, rejected) had similar issues (Wasserstein geometry + neural networks, limited experimental evidence beyond Gaussians) and was rejected. "Probabilistic GPCA" (7.33, accepted) had similar scope but included quantitative experiments.

Now let me write the final consolidated review:

---

## Summary
This paper proposes two algorithms for Geodesic PCA (GPCA) in the Wasserstein space of probability measures. For centered Gaussian distributions, it leverages the Bures-Wasserstein fiber bundle to lift computations to GL_d, replacing geodesic search with horizontal line-segment search in the Frobenius norm. For general absolutely continuous (a.c.) measures, it uses Otto's formulation with MLP-parametrized geodesics (GPCAGEN), avoiding convexity constraints needed by McCann's formulation. Theoretical contributions include explicit projection formulas (Proposition 3), a TPCA distortion quantification (Proposition 4), and a 1D equivalence result (Proposition 5).

## Strengths
- **Elegant lifting construction (Proposition 3, Section 3):** The fiber-bundle lift from S_d^{++} to GL_d replaces BW_2 distance with Frobenius norm and geodesic search with horizontal line-segment search, yielding a structurally tractable optimization. The explicit projection-time formula and clipping mechanism are carefully worked out.
- **Otto's parametrization avoids convexity constraints (Section 4, eq. 9 vs eq. 10):** The paper clearly shows that f in Otto's geodesic formula (eq. 9) need not be convex, unlike McCann's formulation (eq. 10). This eliminates the need for input-convex neural networks and is a genuine practical contribution for the community working on Wasserstein geometry with neural networks.
- **Proposition 4 — concrete distortion formula (eq. 14):** The explicit quantification showing TPCA distortion scales with (a−b)²/(a+b)² and cos²θ provides a verifiable, previously unavailable characterization of when linearization fails, with clear geometric interpretation (proximity to SPD cone boundary).
- **Proposition 5 — 1D Gaussian equivalence:** A clean theoretical result showing GPCA restricted to Gaussians equals GPCA in the full a.c. space for univariate distributions, with honest acknowledgment that the higher-dimensional case remains open (line 150).
- **Clear mathematical exposition:** The paper is well-written, with the fiber-bundle diagrams (Figures 1–2) effectively conveying geometric intuition, and the parallel between Bures-Wasserstein and Otto-Wasserstein geometries drawn clearly.

## Weaknesses

### Fatal
None

### Major
- **GPCAGEN evaluation is entirely qualitative (Section 5.2).** This is the paper's main algorithmic contribution, yet no quantitative metric is reported for any GPCAGEN experiment. The MNIST experiment (Figure 5) has synthetic ground-truth geodesics available but reports no recovery error — no Wasserstein distance between recovered and true geodesics, no objective value (eq. 1 or 15). The 3D point cloud experiments (Figure 6, top/middle) and landscape experiment (Figure 6, bottom) are described purely in interpretive terms ("first component captures the distinction between hanging lamps and standing lamps"). The paper acknowledges that "a direct numerical comparison" with TPCA "is therefore not meaningful" (line 264), but the GPCA objective value (eq. 1) itself is a common currency that both methods can be evaluated against. Not reporting it for any experiment leaves the reader unable to assess whether GPCAGEN actually produces good solutions.

- **"Exact" framing is partially misleading (abstract, Section 1, Section 4).** The paper defines "exact" at line 28 as "not rely[ing] on a linearization of the Wasserstein space," and the parametrization class does contain true geodesics — this is a valid contribution. However, the optimization introduces multiple approximation layers: Sinkhorn divergence S_ε replacing W_2² (line 168, Algorithm 1 line 7), finite-capacity MLPs approximating φ and f, and stochastic gradient descent on a non-convex landscape. None of these approximation errors are quantified. The distinction from Seguy & Cuturi (2015)'s "approximate" approach is therefore blurred: both contain approximations, just at different stages. The paper would benefit from explicitly acknowledging the optimization is approximate while the parametrization is exact.

### Minor
- **Soft enforcement of geometric constraints without residual reporting (Section 4, eq. for second component).** The orthogonality and intersection constraints for higher GPCA components are enforced via penalty terms with λ_I = λ_O = 1.0. The paper states this "ensures the algorithm works as expected in all experiments" (line 256) but never reports constraint violation magnitudes (||ξ₁(t_inter¹) − ξ₂(t_inter²)||² or the orthogonality inner product). For a method emphasizing geometric fidelity, reporting these residuals would directly demonstrate that computed components satisfy GPCA's defining properties.

- **Gaussian experiments show limited practical advantage (Section 5.1).** The paper honestly reports that for randomly generated covariance matrices, "GPCA reduces the objective in equation 11 of less than 1% w.r.t. TPCA, on average for 100 trials" (line 208). In the one regime where they differ substantially (same eigenvalues, different orientations), the paper acknowledges "undesirable effects" where "some of the Gaussian distributions will project onto the first geodesic component boundaries, yielding a poor separation" (line 232). While the honesty is commendable, this creates a narrative tension: the practical case for the Gaussian algorithm is weaker than the theoretical motivation suggests.

- **No computational cost discussion.** Wall-clock times and scaling behavior with respect to n (distributions), d (ambient dimension), or m (samples) are never reported. The method involves repeated computation of d×d Hessian eigenvalues at m sample points per iteration (line 168); for high-dimensional problems, this cost could be prohibitive, but the reader cannot assess feasibility.

### Trivial
None

## Nice-to-Haves
- Convergence diagnostics (training curves, sensitivity to initialization) for the non-convex GPCAGEN optimization would help assess reliability.
- Discussion of the Sinkhorn regularization parameter ε and its effect on approximation quality.
- The observation that Otto's parametrization "opens new directions for parametrising convex functions without imposing hard architectural constraints" (Section 6) is interesting but undeveloped — even a brief example would strengthen this byproduct contribution.
- Quantitative evaluation of GPCA components for the Weather dataset experiment (line 234), which is described too briefly.

## Removed Points
*These points are flagged to be removed; treat them with caution.*
- **Reference measure ρ as standard Gaussian (not compactly supported) vs. Prob(Ω) setup:** The reviewer noted tension between Section 2's compact Ω and Section 4's use of the standard Gaussian as reference measure (line 156). This is standard practice in optimal transport computation, and the paper notes the choice explicitly. Not a substantive issue.
- **Dismissal of embedding+PCA baseline:** The reviewer criticized the paper for dismissing this baseline without evidence, but the paper explicitly points to Appendix A.2 for supporting evidence (line 268). The main text summary is a space decision, not an evasion.
- **Reproducibility details deferred to appendices:** The reviewer noted implementation details are in appendices. This is standard for a 9-page paper with mathematical content and does not constitute a weakness.

## Novel Insights
The paper's central novel insight is that Otto's fiber-bundle formulation transforms GPCA from a constrained geodesic search into an optimization over straight lines in a flat space, and that the non-convexity of f in Otto's parametrization (eq. 9) — which initially appears as a nuisance compared to McCann's convex formulation (eq. 10) — is actually an advantage because it frees the neural network parametrization from input-convexity constraints. The distortion formula (Proposition 4) connecting TPCA error to the geometry of the SPD cone boundary is a concrete, previously unavailable result. Proposition 5's 1D equivalence result opens a clean open question in higher dimensions.

## Suggestions
1. Report the GPCA objective value (eq. 1 or 15) for all GPCAGEN experiments, including the MNIST experiment where ground truth is available. This is the single highest-leverage improvement.
2. For the MNIST experiment, report pointwise Wasserstein distances between recovered and ground-truth geodesics at matched time points.
3. Report constraint violation magnitudes (intersection distance, orthogonality inner product) for all second-component experiments.
4. Add at least order-of-magnitude runtime information and note how the cost of Hessian eigenvalue computation scales with dimension.
5. Qualify the "exact" language: explicitly state that the parametrization is exact while the optimization is approximate, and discuss how this differs from prior approximations.

## Score and Decision

**Calibration Anchors (all from Round 1):**

| Paper | Path | Avg Score | Round | Comparison |
|-------|------|-----------|-------|------------|
| Implementation for minimax path | bEgDEyy2Yk | 1.0 | R1 | Non-contribution; far below paper under review |
| Time-dependent discourse UMAP | P49gSPmrvN | 1.0 | R1 | Non-contribution; far below paper under review |
| KL Divergence GFlowNets | Uj0h13lVrR | 1.0 | R1 | Insufficient contribution; far below |
| Fusion over Grassmannian | F5UgXkPgSn | 3.0 | R1 | Riemannian manifold methods with experimental gaps; our paper has stronger math |
| Manifold Kernel Rank Reduced Regression | WVIq7jYIda | 3.0 | R1 | Weak contribution; paper under review is substantially stronger |
| Solving unbalanced OT | Bh4BW69ILq | 2.6 | R1 | OT paper with limited contribution; paper under review is stronger |
| Consistent OT | 9WG1ga39Dq | 3.0 | R1 | OT generalization; paper under review has cleaner theoretical framework |
| Intrinsic Riemannian Classifiers on SPD | EyWKb7Ltcx | 5.0 | R1 | SPD manifold methods with experimental limitations; comparable experimental gaps but paper under review has more novel framework |
| Relative-Translation Invariant Wasserstein | CrOHzVtWmH | 3.8 | R1 | OT distance paper; paper under review has deeper mathematical development |
| Graph Geodesic Distance | OPKBPz6Qnz | 4.4 | R1 | Geodesic distance on graphs; paper under review is more technically sophisticated |
| Dynamic Representation of OT | ueQ6T58ZAK | 4.0 | R1 | OT + dynamical systems; paper under review has cleaner contributions |
| Wasserstein Flow Matching | HB4lr0ykTi | 6.33 | R1 | Very similar profile: Wasserstein geometry + neural networks, solid math but limited quantitative experiments beyond Gaussians. Rejected. Paper under review has comparable theoretical depth but weaker experiments. |
| Probabilistic Geometric PCA | mkDam1xIzW | 7.33 | R1 | Closest thematic analog (PCA on manifolds); accepted with quantitative EM experiments. Paper under review has arguably stronger math but significantly weaker experimental validation. |
| OT Barycenter via minimax | rY8xdjrANt | 6.20 | R1 | Strong algorithmic OT contribution with convergence guarantees; paper under review has comparable theoretical quality but weaker experimental evidence |
| Convergence of Wasserstein Proximal | WPz5e5V85k | 6.0 | R1 | Theoretical OT paper with convergence analysis; paper under review has comparable depth |
| Flow Matching on General Geometries | g7ohDlTITL | 8.0 | R1 | Riemannian generative modeling with comprehensive quantitative experiments; paper under review has weaker experimental support |
| Comparing noisy neural populations via OT | cNmu0hZ4CL | 8.0 | R1 | OT distance for neural data with thorough experiments; paper under review has weaker experiments |
| Residual Deep GPs on Manifolds | JWtrk7mprJ | 7.6 | R1 | Riemannian methods with strong experiments; paper under review has weaker experimental validation |
| DRO with Bias and Variance Reduction | TTrzgEZt9s | 8.0 | R1 | Strong algorithmic contribution with theoretical guarantees and experiments; paper under review lacks comparable experimental rigor |

**Round 1 bracket: 5.0–6.5.** The mathematical framework is genuinely clean and novel, comparable to borderline-accept work. However, the GPCAGEN experiments' entirely qualitative nature and the limited practical advantage shown for the Gaussian case push toward the lower end of this bracket.

**Narrowing:** The closest comparator is "Wasserstein Flow Matching" (6.33, rejected), which had a very similar profile: Wasserstein geometry leveraged with neural networks, solid mathematical framework, but experimental evidence insufficient beyond the Gaussian case. That paper was rejected despite having *some* quantitative results (Table 3). Our paper has *no* quantitative results for GPCAGEN. The second closest is "Probabilistic GPCA" (7.33, accepted), which had comparable scope but included quantitative experiments with an EM algorithm. The paper under review falls below both in experimental support.

The paper's theoretical contributions are solid and above a 5.0-level paper, but the experimental gap for the main contribution (GPCAGEN) is a significant concern at a top venue. The paper presents a promising framework that is incompletely validated.

**Final Score: 5.0** — The mathematical framework is elegant and the theoretical results are solid, but the main algorithmic contribution (GPCAGEN) is not quantitatively validated. The Gaussian case shows limited practical advantage over TPCA in generic settings. The paper would be strengthened substantially by reporting objective values and recovery errors, which are feasible additions. In its current form, the experimental evidence does not sufficiently support the algorithmic claims for a top venue.

**Decision: Reject**

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>