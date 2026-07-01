Now I have all the verification I need. Here is the final consolidated review.

---

## Summary

This paper proposes AC-DC, a three-stage score-based denoiser (auto-correction via additive Gaussian noise, directional correction via conditional Langevin dynamics, and score-based denoising) designed for integration into ADMM-PnP frameworks. The method addresses the "manifold mismatch" between score functions trained on Gaussian-perturbed data and the distribution of ADMM iterates (especially those affected by dual variables). The paper provides convergence analysis showing weakly nonexpansive operator properties (ball convergence) under constant step sizes with strongly convex losses, and convergence under adaptive step sizes without convexity. Experiments across seven inverse problems on FFHQ and ImageNet demonstrate competitive empirical performance.

## Strengths

1. **Well-motivated problem framing (Sections 1–3).** The paper clearly articulates a genuine technical issue: ADMM iterates, particularly those affected by dual variables, do not lie on the Gaussian-perturbed manifolds where score functions are trained, causing direct score-based denoising to be ineffective. The AC-DC three-stage design (noise injection → Langevin correction → Tweedie/ODE denoising) is a principled architecture-level response to this problem.

2. **Non-trivial extension of ADMM-PnP convergence theory (Theorems 1–3, Section 4).** The analysis extends prior ADMM-PnP convergence results (Ryu et al. 2019; Chan et al. 2016) to score-based denoisers. Theorem 1 generalizes fixed-point convergence to δ-ball convergence by relaxing strict contractiveness to weak non-expansiveness with a slack δ. Theorem 3 relaxes the strong convexity assumption on ℓ using adaptive step sizes. These are genuine theoretical extensions to a setting (score-based denoisers in primal-dual algorithms) not previously covered.

3. **Broad experimental scope.** Experiments cover seven inverse problems (super-resolution, Gaussian deblur, motion deblur, random inpainting, box inpainting, phase retrieval) on two datasets (FFHQ, ImageNet) with comparisons against eight baselines (DPS, DAPS, DDRM, DiffPIR, RED-diff, DPIR, DCDP, PMC). The scale is reasonably comprehensive for a new-method paper.

4. **Candid limitations section (Section 7).** The paper openly acknowledges that its adaptive step-size results are less practically appealing, that the theory ensures stability rather than recovery quality, and that noise schedules are heuristic.

## Weaknesses

### Major

1. **Disconnect between convergence theory assumptions and experimental configuration.** This is the paper's most significant weakness. (a) Theorems 2–3 assume that the DC Langevin dynamics "reaches the stationary distribution for each k" (lines 183, 205); experiments use only J = 10 Langevin steps in a 256×256 (≈196k-dimensional) space, which is far from mixing. A footnote (line 207) references "counterparts removing this assumption" in Appendix E.2, but the main-text theory is stated under the stationarity assumption and the paper never verifies that J = 10 approximately satisfies the required conditions. (b) Theorem 3(b) requires lim_{k→∞} σ^{(k)} = 0 and lim_{k→∞} σ_{s^{(k)}} = 0 (line 215); the implemented schedule clips σ^{(k)} at a floor of 0.1 (line 297) and σ_{s^{(k)}} = 0.1/√(σ^{(k)}) also fails to approach zero. (c) The ball radius r (Theorem 1) is expressed in terms of uninstantiated constants (δ, ε̄, etc.) and is never estimated empirically, so the convergence guarantee remains existential. The theory and experiments operate under different regimes without a quantitative bridge between them.

2. **Missing the most informative ablation: ADMM with naive score-based denoising (without AC-DC).** The paper's central claim is that AC-DC is necessary because direct score-based denoising fails in ADMM due to manifold mismatch. Yet no experiment directly tests this by comparing "ADMM + vanilla Tweedie denoising" (no AC, no DC) against "ADMM + AC-DC" within the same framework. All comparisons are against different inference frameworks (DPS, DDRM, DiffPIR, etc.), which conflate denoiser design with algorithmic choices. The ablation in Fig. 5 varies J (DC steps) only, with AC fixed, and only on phase retrieval. Without the direct within-ADMM comparison, the evidence for the AC-DC design's necessity is incomplete.

3. **RED-diff baseline results are anomalously low.** RED-diff reports PSNR values of 16.83 (FFHQ super-resolution), 16.82 (Gaussian deblur), and 15.10 (ImageNet Gaussian deblur) in Table 1. These are substantially below typical reported performance for this method on similar tasks, strongly suggesting the baseline was used with incompatible settings or suboptimal tuning. When a strong baseline performs at near-random level, the claimed margins over it are unreliable. The authors should either verify and report properly configured RED-diff numbers or explain the discrepancy.

### Minor

4. **No variance or statistical significance information.** All results are point estimates averaged over 100 images (line 269). No standard deviations, confidence intervals, or significance tests are reported. Given the stochastic components (Langevin noise injection, random masking), variance could be non-negligible. Reported improvements over DAPS (often 0.5–1.5 PSNR) cannot be assessed for reliability.

5. **Missing key hyperparameter: W (decay window).** The noise schedule uses σ^{(k)} = max(0.1, 10 − (10 − 0.1)·k/W) and total iterations K = W + 10 (line 297). The numerical value of W is never given, hindering reproducibility.

6. **PMC baseline results are incomplete.** PMC has blank entries for several tasks (random inpainting, Gaussian blur, box inpainting) in Table 1 with no explanation.

7. **The DC step's theoretical motivation has a residual logical gap.** The DC Langevin dynamics uses the score function s_θ(w, σ^{(k)}) as the gradient of the log-prior. But the paper's core motivation is that the score function is unreliable off the trained manifolds M_{σ(t)}. While the AC step is designed to bring points "closer" to these manifolds, no quantitative measure of closeness or validation that the score function is reliable at the resulting points is provided. The Gaussian approximation to the conditional likelihood (Section 3, lines 131–135) relies on conditions (e.g., Var(s^{(k)})^{1/2} ≪ σ^{(k)}) stated without empirical verification.

### Trivial

None.

## Nice-to-Haves

- A runtime or NFE (number of score function evaluations) comparison. The inner x-subproblem uses up to 1000 Adam iterations per ADMM outer loop, placing the method in a different computational budget class from single-pass posterior sampling methods (DPS, DDRM). Reporting total NFEs or wall-clock time per method would enable fair cost-benefit assessment.
- Experiments at higher measurement noise levels (σ_n > 0.05) would strengthen robustness claims.
- An ablation varying whether the AC step is included would complement the existing DC-step ablation.
- The notation in Eq. (9) around the decomposition of s^{(k)} is confusing and could be clarified.

## Removed Points

These points were raised in the input review but are removed after cross-checking against the paper:

1. **"Abstract claims convergence but does not mention ball convergence caveats."** — The abstract on line 9 explicitly says "fixed-point *ball convergence*." The caveat is present. REMOVED (factually incorrect).

2. **"DPIR is listed as a baseline but never appears in any results table."** — DPIR results appear in Table 1 as "DiPIR" (parser-garbled rendering of "DPIR"). The results are present. REMOVED (factually incorrect).

3. **"Self-referential notation in Eq. (9) — s^(k) = √2σ^(k)n_2 + s^(k) is self-referential and does not make sense."** — This is likely a parser artifact (the tilde/accent on the first s^{(k)} was stripped). The mathematical intent is decipherable from surrounding context. REMOVED (parser artifact).

4. **"The section could benefit from a more precise statement about why the dual variable in ADMM makes the geometry worse compared to primal methods."** — This is a presentation suggestion, not a weakness. MOVED to Removed Points.

5. **Generic speculation about confounders and proxies (e.g., "could the metric be measuring a proxy?").** — These are area-of-concern framings from the harsh review template without concrete anchors in the paper. REMOVED (speculative framing, not a specific identified problem).

6. **Strengths removed:** "The paper addressed an important problem" (generic), "The paper targeted an interesting question" (generic). REMOVED (generic/superficial).

## Novel Insights

The most penetrating observation across the reviews is the structural disconnect between the theory's conditions (Langevin stationarity, noise decaying to zero) and the practical method (finite Langevin steps, noise-floor clipping). This is not a shallow "theory is abstract" complaint — the paper's own theory provides the language (δ-ball radius, ε_k, δ_k) that could be used to quantify this gap, but the paper never instantiates these quantities. The second key insight is that the paper's motivating rationale (manifold mismatch makes naive score denoising fail in ADMM) is the one comparison the experiments do not directly test. Together, these observations identify that the paper's three contributions (motivation, algorithm, theory) are individually interesting but lack the evidential connectors that would make them a coherent whole.

## Suggestions

1. **Add a within-ADMM ablation** comparing "ADMM + vanilla Tweedie denoising" vs. "ADMM + AC-DC" on at least 2–3 tasks. This directly tests the paper's central claim about the AC-DC design.
2. **Diagnose the theory-practice gap:** On a small-scale problem where Langevin can mix to stationarity, verify that Assumption 1 (weak non-expansiveness) holds with small δ. Separately, run the method with unclipped σ^{(k)} → 0 and many Langevin steps, and compare to the practical (clipped, J=10) version. Report whether the ball radius r is small enough to be meaningful.
3. **Verify RED-diff baseline configuration** or replace the numbers with properly tuned values.
4. **Report standard deviations or confidence intervals** for the main quantitative results, and provide the numerical value of W.

## Score and Decision

The paper addresses a genuine problem with a reasonable algorithmic proposal and non-trivial theoretical extensions. However, the evidence connecting the theory to the experiments is structurally incomplete (Major weakness 1), the central algorithmic claim is not directly tested (Major weakness 2), and a key baseline has suspect numbers (Major weakness 3). These gaps prevent the paper from being a fully convincing contribution in its current form.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>