## Summary

This paper tackles Geodesic PCA (GPCA) in Wasserstein space — finding geodesic curves that best capture variation in a dataset of probability measures. It makes two contributions: (1) an exact GPCA method for centered Gaussian distributions, leveraging the Bures-Wasserstein geometry to lift the problem to the flat space GL\_d, and (2) GPCAGEN, a neural-network-based extension to general absolutely continuous measures using Otto's fiber bundle parametrization. The Gaussian portion is mathematically clean and well-validated; the GPCAGEN portion proposes a novel theoretical framework but lacks quantitative experimental support.

## Strengths

- **Principled theoretical framing via Otto's fiber bundle.** The paper's central insight — lifting GPCA from the curved Wasserstein space to the flat total space of Otto's bundle — is mathematically elegant and correctly unifies the Gaussian and general cases. The exposition of the horizontal/vertical decomposition (Propositions 1 and 2) and the parametrization \(\mu_{\theta,\psi}(t) = (\mathrm{id} + t\nabla f_\psi)_\#(\varphi_\theta\#\rho)\) (Equation 9) that avoids input-convex neural networks is a genuinely novel and well-motivated approach.

- **Clean handling of the Gaussian case (Section 3).** The lifting to GL\_d (Proposition 3), the formulation of orthogonality constraints via horizontal vectors (Equation 13), the distortion quantification (Proposition 4), and the proof that univariate Gaussians stay Gaussian under GPCA (Proposition 5) are all sound and constitute a self-contained contribution.

- **Honest assessment of GPCA vs. TPCA in the Gaussian setting.** The paper openly reports that GPCA and TPCA "generically yield very similar results" (line 208, <1% improvement on average over 100 trials), that GPCA can produce "undesirable effects" near the cone boundary (line 283), and that GPCA "may be seen as worse-behaved as TPCA" in the pathological example (line 232). This candor is valuable even though it creates a tension with the paper's motivating premise.

## Weaknesses

### Fatal
None.

### Major

- **GPCAGEN is evaluated almost entirely qualitatively, with no quantitative evidence that it minimizes the GPCA objective (Equation 1).**  
  The experiments for GPCAGEN (Section 5.2) consist of visual results only:  
  - MNIST "geodesics" (lines 258–259): a constructed dataset where the answer is known by design — a sanity check, not a validation that Equation 1 is minimized.  
  - ModelNet40 3D point clouds and Landscape images (Figure 6): purely qualitative visualizations along learned geodesics, with no reconstruction error, variance explained, or GPCA objective value reported.  

  The paper dismisses quantitative comparison with TPCA as "not meaningful" (line 264–265) because GPCAGEN works on continuous measures while TPCA acts on discrete measures. This dismissal is too hasty: one could discretize GPCAGEN's output at the empirical samples and compute the GPCA objective (Equation 1) for both methods, or compare against the approximate GPCA method of Seguy & Cuturi (2015), or run a synthetic experiment with known ground-truth geodesics and report recovery error. Without any such evidence, the claim that GPCAGEN "solves the exact GPCA problem" (abstract) is unsupported.

### Minor

- **The "exact" qualifier is somewhat misleading for GPCAGEN.** In the Gaussian case, "exact" is mathematically justified (closed-form horizontal lines in GL\_d). For GPCAGEN, the method involves neural network function approximation, Sinkhorn divergence \(S_\varepsilon\) as a proxy for \(W_2^2\), stochastic minibatch optimization, soft regularization constraints (Equation 15 with \(\lambda_I=\lambda_O=1.0\)), and approximate eigenvalue computation — all of which are approximations. The paper does qualify what it means by "exact" ("in the sense that they do not rely on a linearization of the Wasserstein space," abstract), but the phrasing still sets an expectation the method does not meet, and an ablation study isolating how each approximation affects solution quality would be valuable.

- **No analysis of achieved orthogonality for the second GPCAGEN component.** The orthogonality regularizer \(\mathcal{O}(g,h)\) (Equation 15) is defined but its value at convergence is never reported. Since orthogonality is enforced via a soft penalty (\(\lambda_O=1.0\)), the reader cannot assess whether the second component is actually orthogonal to the first.

- **The Gaussian experiments undercut the motivating premise.** The paper motivates GPCA by arguing that TPCA introduces distortion due to curvature (Section 1, Figure 4). Yet Section 5.1 shows that GPCA and TPCA are generically very similar, and the main case where they differ (near the cone boundary) is also where GPCA "can yield undesirable effects" and "may be seen as worse-behaved" than TPCA. This raises the question — *when should one prefer exact GPCA over the cheaper TPCA?* — which the paper does not answer, weakening the practical significance of the Gaussian contribution and, by extension, the motivation for GPCAGEN.

### Trivial

- **Gaussian experiments are restricted to \(d=2\).** While 2D is sufficient to illustrate the geometry, the paper would benefit from at least one example with \(d>2\) to demonstrate that the optimization over rotation matrices \(Q_i \in SO_d\) scales acceptably. Scalability with dimension is not discussed for either method.

## Nice-to-Haves

- **To strengthen the GPCAGEN validation**, the authors could: (a) compute the GPCA objective value (Equation 1) for the learned geodesics on the ModelNet40 and Landscape data, comparing against a baseline (TPCA, or Seguy & Cuturi 2015, evaluated on the same objective); (b) run a synthetic experiment with known ground-truth geodesics and report the Wasserstein recovery error; (c) ablate the approximations: compare exact \(W_2^2\) (via OT solvers) vs. Sinkhorn divergence, and study sensitivity to \(\lambda_I, \lambda_O\) over a range.

- A brief discussion of how the method scales with data dimension \(d\) and number of distributions \(n\) would help readers assess practical applicability.

## Removed Points

These points from the input were removed after cross-checking against the paper:
- **Criticism about missing sensitivity analysis for hyperparameters:** The paper explicitly states that a discussion of regularization coefficients, architecture, and hyperparameters is provided in Appendix E (line 256). Since the parser strips appendices, this criticism cannot be verified against the paper as submitted.
- **"Cherry-picked examples" characterization:** Subjective framing; the paper shows multiple samples along the geodesic for each experiment, not isolated cherry-picked outputs.
- **Wording criticism about the MNIST experiment not being "synthetic":** The paper's description ("a preliminary experiment on a synthetic dataset with known geodesics") is accurate and appropriate.
- **Figure caption repetition note:** This is a PDF-parser artifact, not an author error.
- **Various section-by-section editorial observations:** Subsumed by the higher-level weaknesses above.

## Novel Insights

The harsh review identifies a genuine structural tension that the paper's own framing does not resolve: the paper motivates exact GPCA as a correction to TPCA's curvature-induced distortion, but then shows (honestly) that GPCA and TPCA give nearly identical results in generic settings, and that in the regime where they differ (near the cone boundary), GPCA can behave worse. This creates a credibility gap for the GPCAGEN extension: if exact GPCA offers no clear practical advantage over TPCA even in the tractable Gaussian case, why should the community adopt the more expensive neural approximation for general measures? The paper would be strengthened by explicitly addressing this question — either by identifying realistic regimes where GPCAGEN's continuous geodesic representation yields qualitative benefits that TPCA cannot capture, or by reframing the contribution as a theoretical framework with preliminary illustrations rather than a practical alternative.

## Suggestions

1. Provide at least one quantitative evaluation of GPCAGEN — computing the GPCA objective (Equation 1) for the learned geodesics on existing datasets, and comparing against a reasonable baseline (even a simple one). A synthetic experiment with known ground truth and recovery error would also significantly strengthen the paper.
2. Report the achieved orthogonality \(\mathcal{O}(g,h)\) at convergence for the second component in the GPCAGEN experiments.
3. Either address the "when to prefer GPCA over TPCA" question explicitly in the discussion, or temper the motivating claims to match what the experiments actually show.
4. Include at least one \(d>2\) example for the Gaussian GPCA to demonstrate scalability.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>