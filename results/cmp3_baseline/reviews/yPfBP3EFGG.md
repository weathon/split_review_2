## Summary

The paper proposes STNAdam, a stochastic variant of Adam that uses a "two-track" iteration framework combining Nesterov momentum and adaptive learning rates. The method is designed for nonconvex + weakly-convex composite optimization and claims almost-sure convergence to stationary points under the Kurdyka-Łojasiewicz property, with convergence rate results. Experiments on low-light image enhancement (LIE) report improved PSNR, SSIM, and LPIPS over existing optimizers and specialized LIE methods.

## Strengths

- The idea of maintaining two interleaved iteration trajectories (extrapolation track and regular update track) is a novel algorithmic ingredient that could, in principle, allow a larger update neighborhood and better exploration.
- The theoretical framework allows the use of various variance-reduced gradient estimators (SVRG, SAGA, SARAH) and provides adaptive update rules for some hyperparameters, which is a principled step beyond manual tuning.
- The experimental results on the LIE task show noticeable quantitative improvements over the compared baselines (SGD, Adam, SNAdam, and several specialized LIE methods), especially for STNAdam-SARAH.

## Weaknesses

### Fatal

1. **Theoretical convergence analysis is not verifiable.** The entire proof (the energy function (9) with unspecified parameters \(M, H, Z, D\), Lemma 2 with \(A_i > 0\) whose explicit conditions are deferred to an appendix that is not present, the KL-inequality treatment, and the step numbering that jumps from Step 3 to Step 5) is presented only as a sketch. Without the appendix, the reader cannot assess the correctness, the necessary conditions, or whether the claimed "almost sure" convergence (which the main body reframes as "convergence in expectation") is actually established. This renders the paper's core theoretical contribution unsubstantiated.

2. **Experimental results contain implausible numbers.** The reported runtime values in Tables 2 and 3 are on the order of \(10^{-5}\) seconds per image (e.g., STNAdam-SARAH: 2.64e-05 s, Retinex-Net: 7.63e-05 s). For any realistic LIE pipeline involving patch extraction, optimization loops, and image reconstruction, such times are orders of magnitude below what is possible. This suggests either a unit error (e.g., seconds per iteration rather than per image) or a reporting mistake, and it casts doubt on the reliability of the entire experimental evaluation.

3. **Key claims are contradicted or unsupported.** The paper claims to "remove hand-tuning" by dynamically scheduling hyperparameters within iterate-dependent intervals, but the intervals themselves (6)–(8) depend on constants \(V_1, V_\Upsilon, \rho, M, s, \tau, L\) that must be specified or estimated a priori. The method still requires selecting \(\mu, \nu, \alpha, \varepsilon\) plus the estimator choice and the interval bounds. This is not a removal of hand-tuning. Furthermore, the convergence results require the KL property and Assumption 1, but no verification that the target LIE model satisfies these conditions is provided.

### Major

1. **Limited experimental scope and missing comparisons.** The experiments are restricted to one application (LIE) and one dataset (LOL). No ablation study isolates the effect of the two-track mechanism vs. the variance-reduced estimator vs. the adaptive parameter rules. No comparison is made with recent widely-used optimizers (e.g., AdamW, Lion, AdaBelief) that are standard in deep learning. The paper does not report variance or statistical significance across multiple runs, so the observed improvements may not be reproducible.

2. **Clarity and completeness of the algorithmic description are poor.** The two-track update in Algorithm 1 uses the proximal operator \(\mathcal{P}_g\), but the definition and the relationship to the stochastic gradient estimates \(\tilde{\varpi}^{k+1}\) and the adaptive step sizes are not explained intuitively. The notation \(\widehat{m}_i^{k+1}\) appears without definition (it seems to be the full-gradient counterpart, but the text is confusing). The paper frequently cites "Lemma A.1 in Appendix" for essential details that are missing.

### Minor

1. The paper uses "TNAdam" for the deterministic version and "STNAdam" for the stochastic version, but the abstract and title only mention "STNAdam". The relationship between the two is not clearly delineated.
2. Some references appear unusual (e.g., "Damek (2016)" is listed but is not a standard reference in the optimization literature) and the citation of Robbins & Siegmund (1971) for a desingularization function is historically inaccurate—that work is about martingale convergence, not desingularization for KL inequalities.
3. The paper claims the two-track framework "promotes the formation of a larger update neighborhood," but this statement is not formally defined or empirically quantified.

### Trivial

- The figure captions are repeated almost verbatim in the text, an artifact of the extraction process but not a substantive issue.

## Nice-to-Haves

- Provide a complete, self-contained convergence proof in the main paper or a publicly available appendix.
- Include an ablation study that isolates the two-track mechanism from the variance reduction and adaptive learning rate components.
- Verify the validity of the KL property for the LIE objective (14) or at least discuss the conditions under which it holds.
- Use proper units for runtime and explain whether the reported times refer to per-image or per-iteration costs.
- Compare against modern optimizers (AdamW, Lion, etc.) on standard deep learning benchmarks (e.g., CIFAR, ImageNet classification) to demonstrate generalizability.

## Novel Insights

None beyond the paper's own contributions. The two-track iteration idea is the main novelty, but the paper does not provide a clear theoretical or empirical analysis that reveals *why* it works better than standard single-track methods.

## Suggestions

1. Present the complete convergence proof (energy function decrement, positivity of A_i, KL argument) in the main text, or at least ensure the appendix is available for review. Without it, the theoretical claims cannot be evaluated.
2. Fix the runtime reporting: clarify units and ensure the numbers are physically plausible; if there is an error, correct it.
3. Add an ablation study: compare STNAdam with a variant that uses the two-track update but without the variance-reduced estimator, and with a single-track version that uses the same estimator, to attribute performance gains.
4. Discuss the practical choice of the many hyperparameters and provide default values or tuning guidelines.
5. Improve the clarity of Algorithm 1: define the notation for \(\widehat{m}_i^{k+1}\), show the full gradient counterpart explicitly, and give an intuitive explanation of the two-track idea.

## Score and Decision

**Score:** 3 — Reject. The paper proposes a novel algorithmic idea, but the core theoretical contribution is unverifiable due to missing proofs and the experimental evaluation contains an implausible runtime that undermines the reported results. The overall presentation lacks rigor and completeness, making the paper unsuitable for acceptance at this venue.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>