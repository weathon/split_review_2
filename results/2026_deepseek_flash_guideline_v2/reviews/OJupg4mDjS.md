## Summary

The paper proposes two algorithms for Geodesic Principal Component Analysis (GPCA) in Wasserstein space: one for centered Gaussian distributions using the Bures-Wasserstein lift to $GL_d$ (Section 3), and one for general absolutely continuous measures (GPCAGEN, Section 4) using Otto's fiber-bundle geometry with neural-network parametrization. The Gaussian formulation is theoretically sound and includes a quantitative characterization of when the linearized approximation (TPCA) distorts. GPCAGEN offers a novel parametrization of Wasserstein geodesics via MLPs that avoids input-convex architectural constraints. The paper demonstrates results on real data (3D point clouds, images) but the evaluation of GPCAGEN is almost entirely qualitative.

## Strengths

- **First exact (non-linearized) GPCA formulation for $\mathbb{R}^d$-valued probability measures beyond 1D.** Section 3 lifts the GPCA problem to $GL_d$ with explicit horizontal constraints (Proposition 3). The paper correctly identifies that prior work (Seguy & Cuturi, 2015) solves only an approximate version via generalized geodesics, filling a gap noted in the literature.

- **Proposition 4 gives a closed-form expression** (equation 14) for the distortion ratio between exact and linearized Bures-Wasserstein distance for same-eigenvalue covariance matrices at different orientations. The experimental validation (Figure 4, right) confirms the predicted ~35% improvement near the cone boundary. This is a concrete, testable theoretical result.

- **Proposition 5** proves that univariate GPCA stays within the Gaussian family, with the higher-dimensional case honestly flagged as open (line 150). This is a clean consistency result.

- **Otto's parametrization avoids input-convex neural networks (ICNNs).** The key insight (line 92) is that $f$ need not be convex in equation 9 — only $\text{id} + t\nabla f$ must be a diffeomorphism, enforced by monitoring Hessian eigenvalues (line 162). This is a genuine methodological advantage over the standard McCann parametrization.

- **Qualitative results on real data are interpretable.** The ModelNet40 experiments (Figure 6) show semantically meaningful decompositions (e.g., first component separating hanging vs. standing lamps, second capturing stem thickness) learned without labels.

## Weaknesses

### Fatal
None.

### Major

1. **GPCAGEN lacks quantitative validation.** The paper states (line 238) that it "conduct[s] a preliminary experiment on a synthetic dataset with known geodesics to verify that our algorithm… accurately recovers the two first principal components," but **never reports any results from this experiment** — no error metrics, recovery scores, or comparison to ground truth appear in the main text. The MNIST experiment (Figure 5, line 258) is also purely qualitative: the claim that GPCAGEN "successfully recovers" orthogonal geodesics rests on visual inspection alone. The paper then declines quantitative comparison with TPCA, arguing it is "not meaningful" (line 264). This creates a significant evidential gap: one of the paper's two main contributions has no quantitative support for the claim that it actually minimizes equation 1. This is fixable (the synthetic experiment presumably has results that can be reported), but in the current submission the contribution of Section 4 is not empirically substantiated.

2. **No quantitative comparison with Seguy & Cuturi (2015).** This prior work on approximate GPCA via generalized geodesics is cited in the related work (line 26) but never empirically compared on a common setting. Even a single synthetic experiment comparing the GPCA costs achieved by both methods would help position GPCAGEN relative to the closest prior approach.

### Minor

1. **"Exact" framing needs sharper qualification for GPCAGEN.** The abstract says the methods are "exact in the sense that they do not rely on a linearization of the Wasserstein space." This is technically true of the formulation, but GPCAGEN's implementation uses: (a) the Sinkhorn divergence $S_\varepsilon$ as an approximation to $W_2^2$, (b) finite-sample minibatch approximation, (c) empirical estimation of Hessian eigenvalues over a finite sample, and (d) MLPs that are not guaranteed to be diffeomorphisms. The paper should more clearly distinguish the exactness of the mathematical formulation from the approximations inherent in the algorithm.

2. **No sensitivity analysis for GPCAGEN hyperparameters.** The method has several free parameters (Sinkhorn regularization $\varepsilon$, batch size $m$, regularization coefficients $\lambda_I$ and $\lambda_O$, network architecture, learning rate). The paper claims that "setting the regularization coefficients $\lambda_I$ and $\lambda_O$ to 1.0 ensures the algorithm works as expected in all experiments" (line 256) without any ablation. The Sinkhorn parameter $\varepsilon$ is never specified in the main text.

3. **Gaussian contribution shows limited practical advantage.** The paper honestly reports (line 208) that GPCA and TPCA are "generically very similar" (<1% improvement on average), and the one case where GPCA differs significantly (same eigenvalues, varying orientations) can produce "worse-behaved" results (line 232). While the theoretical formulation is sound, the experiments undercut the practical case for using GPCA over the simpler TPCA in the Gaussian setting.

4. **No computational cost characterization.** No runtime, iteration count, or convergence criteria are reported for GPCAGEN. Since the method involves computing Hessian eigenvalues per iteration, this information is needed to gauge practicality.

### Trivial
None.

## Nice-to-Haves

- Report the synthetic experiment's quantitative results (ground-truth recovery metrics).
- Add an ablation study for the Sinkhorn regularization $\varepsilon$.
- Add a brief note in the main text on how the $SO_d$ optimization in Section 3 is performed (currently deferred to Appendix D).

## Removed Points
These points are flagged to be removed; treat them with caution:
1. **"No comparison with Seguy & Cuturi (2015) discussed beyond the related-work paragraph"** — The paper DOES discuss Seguy & Cuturi (2015) in the related work (line 26). The empirical comparison point is kept as a major weakness above, but the "not discussed" framing is factually wrong.
2. **"Proposition 3 optimization over SO_d not discussed"** — The paper discusses the formulation (lines 106-118); deferring implementation details to an appendix is standard practice. Moved to nice-to-haves.
3. **"GPCAGEN not exact"** — The paper explicitly qualifies what "exact" means. Merged into the minor weakness above with the paper's own qualification acknowledged.
4. **"Typos/formatting nitpicks"** — Parser issues, not author errors. Removed.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions

1. **Report quantitative results from the synthetic dataset experiment** (e.g., relative GPCA cost error compared to the known optimum, angle between learned and true geodesic directions). This single addition would address the most significant weakness.
2. **Add a quantitative comparison with TPCA** on distributions that can be processed by both methods (e.g., by approximating continuous measures with sufficiently many samples), using the Sinkhorn divergence as a shared evaluation metric.
3. **Add sensitivity analysis** for key hyperparameters (Sinkhorn $\varepsilon$, $\lambda_I$, $\lambda_O$) or justify why a single setting suffices beyond a brief statement.
4. **Report computational cost** (runtimes, iterations to convergence) to help readers assess the method's practicality.

## Score and Decision

**Bracket and calibration:** The calibration database had persistent missing-file errors, preventing retrieval of anchor papers. Score is determined by direct assessment against ICLR standards. The paper has one solid, well-executed contribution (Gaussian GPCA, Section 3) with honest reporting of its limitations, and one methodologically interesting but inadequately validated contribution (GPCAGEN, Section 4). The lack of quantitative evidence for GPCAGEN is a significant evidential gap that prevents acceptance in the current form. With the synthetic experiment results and a modest amount of additional evaluation, the paper could be a strong borderline accept (≈6). Without them, the submission is incomplete.

**Score rationale:** The Gaussian GPCA section (theoretically sound, properly evaluated, honest about limitations) would alone be a ~5. The GPCAGEN section (novel formulation, promising approach, but lacking quantitative validation) currently weakens rather than strengthens the submission because its central claim is unsupported. The overall score of 4 reflects that the paper has genuine contributions but a decisive evidential gap for one of its two main pillars.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>