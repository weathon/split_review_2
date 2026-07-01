## Summary

This paper proposes algorithms for exact Geodesic PCA (GPCA) in Wasserstein space. For centered Gaussian distributions, it lifts the problem from the SPD cone to GL_d via the Bures-Wasserstein quotient geometry (§3). For general absolutely continuous probability measures (GPCAGEN, §4), it parametrizes geodesics using Otto's formulation with neural networks, avoiding input-convex neural networks. Experiments include synthetic Gaussian comparisons and qualitative demonstrations on MNIST, ModelNet40 point clouds, and landscape images.

## Strengths

1. **Clean theoretical framework for the Gaussian case.** The lifting of GPCA from S_d^{++} to GL_d via Bures-Wasserstein quotient geometry (Proposition 1, Proposition 3) is principled, and the orthogonality constraint between components is handled rigorously via horizontal vectors in the total space. This part is mathematically sound.

2. **Otto parametrization avoids ICNNs.** Using Equation 9 (non-convex f with a diffeomorphism constraint) rather than the McCann parametrization (Equation 10, requiring convex u) is a genuine practical advantage, and the choice is well-motivated (lines 92–96).

3. **Proposition 5 (univariate Gaussians stay Gaussian under GPCA) is a non-trivial theoretical observation** with practical implications: in 1D, practitioners can safely restrict to the Gaussian submanifold and obtain the same result as full-space GPCA.

4. **The paper correctly identifies and frames a real gap** (line 26): existing Wasserstein PCA methods either linearize (TPCA), restrict to 1D, or replace true geodesics with generalized geodesics. The problem of solving exact GPCA in arbitrary dimension is indeed open.

## Weaknesses

### Fatal
None.

### Major

1. **GPCAGEN's experimental validation is almost entirely qualitative, and quantitative comparison against baselines is explicitly declined.** This is the most consequential weakness given that GPCAGEN is the paper's primary contribution.

   - The MNIST "experiment" (line 258) constructs ground-truth geodesics by design and then asserts GPCAGEN "successfully recovers" them, but provides **no error metric** — no Wasserstein distance between recovered and ground-truth geodesics, no reconstruction error, no variance explained. The paper explicitly states it conducts "a preliminary experiment on a synthetic dataset with known geodesics to verify that our algorithm... accurately recovers" components (line 238), yet the verification is entirely visual.
   - The 3D point cloud and landscape image experiments (Figure 6, lines 260–262) are purely visual with post-hoc interpretation ("the first component distinguishes chairs from armchairs"), with no way to verify these correspond to actual modes of variation versus artifacts of the neural network parametrization.
   - The paper states (line 264) that "A direct numerical comparison between the two methods is therefore not meaningful" and only offers a qualitative observation about TPCA artifacts (Figure 16 in appendix), with no indication these artifacts are representative or systematic. Even if the representations differ, one could compare on a common task — e.g., projection residual of held-out distributions onto the learned components.  
     
   For a method paper proposing a new algorithm, the absence of quantitative validation is a structural evidential gap. The reader cannot determine whether GPCAGEN reliably recovers correct geodesic structure, how it compares to alternatives, or where it fails.

2. **Gaussian experiments create a motivational tension that the paper does not resolve.** Line 208: "GPCA reduces the objective... of less than 1% w.r.t. TPCA... This suggests that TPCA is generally a very good approximation of GPCA." Line 232: "In that case GPCA may be seen as worse-behaved as TPCA, as some of the Gaussian distributions will project onto the first geodesic component boundaries, yielding a poor separation." The paper argues exact GPCA is needed because TPCA introduces distortion, but empirically shows TPCA is essentially indistinguishable from exact GPCA in generic random settings, and in the specific setting where they do differ, the exact GPCA solution is *worse-behaved* (geodesics hit the SPD cone boundary). This undermines the practical case for exact GPCA over the simpler TPCA in the Gaussian setting. The paper acknowledges this tension but does not address it.

### Minor

3. **Multiple layers of approximation in GPCAGEN are not validated against any exact computation.** The paper claims the method is "exact in the sense that they do not rely on a linearization" (line 28), but GPCAGEN relies on: (i) Sinkhorn divergence S_ε as a proxy for W_2² (line 168), (ii) minibatch sampling of both ρ and ν_i (Algorithm 1), (iii) eigenvalue estimates of H_{f_ψ} from finite samples (line 168), and (iv) neural network parametrization with finite capacity. None of these approximations are validated against a small-scale exact computation where brute-force optimization is feasible, so their cumulative effect on solution quality is unknown.

4. **No hyperparameter sensitivity analysis.** The regularization coefficients λ_I = λ_O = 1.0 (line 256) and the 4-layer MLP architecture are stated but not justified through ablation. The robustness of results to these choices is unclear.

5. **The intersection constraint simplification (line 196) is acknowledged but its impact is not analyzed.** The paper simplifies from the theoretically more correct approach (involving R^*) to a direct penalty on diffeomorphism representatives, citing computational cost. It does not evaluate whether this restriction introduces errors or limits the set of achievable intersecting geodesics.

6. **No convergence or runtime information.** Algorithm 1 proceeds as stochastic optimization with no discussion of convergence criteria, number of iterations, or wall-clock time, making it difficult to assess GPCAGEN's practicality.

7. **Weather dataset experiment (line 234) only shows projection plots with no external validation.** The claim that clusters "clearly identify different weather behavior" is not substantiated against any known groupings (e.g., geographic regions or climate zones that could serve as ground truth).

### Trivial

8. The alternation between f and f̃ in lines 90–96 is slightly confusing — it would help to state explicitly that the orthogonality condition uses the L²(ρ) inner product of the velocity fields.

## Nice-to-Haves

- Add a quantitative validation of GPCAGEN on a synthetic problem with known ground-truth geodesics (e.g., measures generated along a single geodesic with added noise), reporting an error metric such as the Wasserstein distance between recovered and true geodesic.
- Include an ablation study showing the effect of varying λ_I and λ_O on a simple problem.
- Report training iterations, wall-clock time, and final loss values for at least one experiment.
- Compute and report variance explained per component, a standard PCA evaluation metric.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"Code/data availability statement"**: Removed per Hard Rule 1 — questioning the release status or verifiability of cited entities is not permitted. All models, datasets, and references cited in the paper are assumed to exist.
- **"Batch size m not specified in the main text"**: Removed per Hard Rule 9 — the paper states (line 256) that architecture and hyperparameter details are provided in Appendix E, which is stripped by the parser.
- **Speculative concern about second-component optimization (Equation 13) local minima**: Removed — the paper does not claim this optimization is free of local minima, and no evidence of practical difficulties is provided.
- **Criticisms framed as generic area-of-concern sweeps** (e.g., "could the metric be measuring a proxy?", "are confounders controlled?"): Removed per filtering discipline — these are speculative and not anchored to specific content in the paper.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add at least one quantitative experiment for GPCAGEN where ground-truth principal geodesics are known, reporting an error metric (e.g., Wasserstein distance between recovered and true geodesic, or reconstruction error on held-out data).
2. Include a meaningful comparison with TPCA on a common task — for instance, evaluate the projection residual of held-out distributions onto the learned components from both methods.
3. Ablate the regularization parameters λ_I and λ_O on a simple problem to demonstrate robustness.
4. Report convergence diagnostics (loss curve, number of iterations, wall-clock time) for at least one experiment.
5. Explicitly discuss the gap between "exact GPCA" (solving Equation 1 with true geodesics) and "what GPCAGEN computes" (geodesics approximated by neural networks, trained with Sinkhorn divergences and minibatch sampling) to prevent over-interpretation.

## Score and Decision

This paper has a genuine theoretical contribution — the Gaussian case is clean, and the GPCAGEN framework using Otto's parametrization to avoid ICNNs is well-motivated. However, the experimental validation of GPCAGEN, the paper's main contribution, is almost entirely qualitative with no error metrics, and quantitative comparison against baselines is explicitly declined. The Gaussian experiments simultaneously show that exact GPCA provides negligible benefit over the much simpler TPCA in generic settings. While the core ideas are sound, the empirical evidence is too thin to support the paper's claims. The paper needs substantially stronger evaluation to be acceptable.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>