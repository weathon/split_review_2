## Summary

This paper proposes an information-theoretic framework for quantifying how distinguishable two competing probabilistic neural coding hypotheses (likelihood coding vs. posterior coding) are under a given experimental design. The core contribution is the "information gap" — the KL divergence between the true posterior and a task-marginalized surrogate posterior under optimal decoding — which provides a theoretical upper bound on decoder performance differences. The paper derives analytic expressions for this gap under both hypotheses, validates via simulations that empirical decoder performance converges to these theoretical values, and demonstrates how evaluating the information gap across parameter grids can guide experimental design. The framework addresses a well-motivated open problem in computational neuroscience.

## Strengths

1. **Well-motivated and clearly framed problem (Section 1).** The paper correctly identifies an unresolved question — whether early sensory populations encode likelihood functions or posterior distributions — and clearly articulates why conventional single-context designs cannot resolve it. The distinction is sharply drawn and the citations are appropriate.

2. **Principled theoretical core (Section 2).** The information gap formalism is sound and well-motivated. The derivation for likelihood coding (Eqs. 1–2) is clean: a decoder trying to extract posterior information from a likelihood-coding population must marginalize over contexts, introducing a systematic bias captured by the KL divergence. The posterior coding derivation (Eqs. 3–5) is more involved but follows from the same logic.

3. **Thorough simulation validation (Section 3, Figs. 3–4).** The validation shows convincing convergence of empirical decoder performance differences to the theoretical information gap across multiple contrast levels, two neural model variants (Poisson and gain-modulated Poisson), and a sweep of task parameters. The scatter plots in Fig. 4 showing points along the diagonal are genuinely compelling evidence that the metric predicts decoder behavior.

4. **Honest transparency about asymmetry (Section 3, line 125).** The paper forthrightly states that posterior-coding information gaps are an order of magnitude smaller than likelihood-coding ones and explains why (the restrictive condition of Eq. 4). This candor is a strength, even though the resulting gap is a concern taken up below.

## Weaknesses

### Fatal

None.

### Major

1. **The claimed "optimization" is a grid scan with hand-picked points, not an optimization procedure (Section 4).** The paper's title and abstract claim a framework for *optimizing* experimental design. What Section 4 actually does is evaluate the information gap on a 2D grid of (prior separation *d*, prior standard deviation *σ*) and manually select "sweet spots" marked by asterisks on contour plots. Three concrete problems follow:

   - **No formal objective.** The paper wants to "balance" the two coding hypotheses but provides no formal objective (maximin, weighted sum, constrained optimization, etc.). The "sweet spots" are identified by a heuristic ("posterior-coding gap approaches its maximum while likelihood-coding maintains sufficient discriminative signal," line 151) with no quantified threshold.
   
   - **No baseline comparison.** The paper never quantifies how much better the recommended designs are compared to intuitive alternatives (maximally separated priors, uniform priors, or random designs). Without this, it is impossible to assess whether the framework adds value over common sense.
   
   - **Imprecise, non-robust output.** The practical recommendation is "*d* ≈ 30° and *σ* ≈ 20°" (line 155). The contour plots in Fig. 5 suggest a smooth landscape, but the sensitivity of the information gap to deviations from these values is not quantified. Is the recommendation robust to ±5° variation?

   The information gap **metric** is the genuine contribution. But the paper consistently frames the framework as enabling *optimization* (title, abstract, line 161: "transforms parameter selection from heuristic search to principled optimization"), and this core claim is not supported by the evidence presented — only grid evaluation and visual inspection are demonstrated.

2. **Posterior coding information gaps are tiny (~0.06 nats), and practical detectability is not addressed (Section 4, Fig. 5).** The paper acknowledges that posterior-coding gaps are an order of magnitude smaller than likelihood-coding gaps (line 125) and mentions "statistical power" (lines 125, 161), but provides no power analysis. With realistic neurophysiology trial counts (hundreds to low thousands), can a difference of ~0.06 nats be reliably detected? The convergence curves in Fig. 3 show non-negligible variance even at 30k trials and 500 neurons. At realistic sample sizes, the variance may easily swamp a 0.06 nat signal. This is a structural concern: if the framework's recommended designs produce predicted effects below the detection threshold of real experiments for one of the two hypotheses, the claim that the framework enables "decisive experiments" (line 194) is only half-supported. The paper should either provide a power analysis showing detectability at feasible sample sizes or explicitly acknowledge that the framework primarily supports ruling out the likelihood-coding hypothesis (where gaps are large) rather than symmetrically distinguishing both.

### Minor

3. **Section 5 (Allen dataset validation) is a weak consistency check, not a test of the framework.** The paper tests a single-context uniform-prior condition, where the theory predicts Δ = 0. Confirming that the empirical difference is not significantly different from zero (p = 0.63) shows that the data are consistent with the modeling assumptions, but it does not validate the framework's predictive power or the optimization procedure. The paper's framing of this as supporting "the necessity of the proposed optimized experimental framework" (line 43–44) is reasonable, but it is not an empirical validation of the framework itself. A stronger test would use multi-context data or predict performance on held-out parameters.

4. **Convergence to theoretical values is shown at large sample sizes; the gap at realistic sample sizes is not quantified (Section 3, Fig. 3).** The paper acknowledges (line 61) that empirical decoders underestimate true information content and shows asymptotic convergence (30k trials, 500 neurons). However, the gap between empirical and theoretical values at realistic neurophysiology sample sizes is not quantified. The framework's utility as a *practical* guide depends on the mapping from theoretical Δ to empirical Δ being monotonic and consistent — this is shown for large samples but not for the sample sizes where the recommendations would be applied.

5. **Sensitivity of optimal design parameters is not quantified (Section 4).** The recommended parameters are reported as point values without quantifying the flatness of the landscape around them. The contour plots in Fig. 5 appear smooth, suggesting robustness, but this should be stated explicitly with a quantitative sensitivity measure.

### Trivial

6. **Typo at line 125:** The information gap for likelihood-coding populations is labeled $\Delta_{\text{p}}^{\text{info}}$ (which is the notation used elsewhere for posterior coding). It should be $\Delta_{\text{L}}^{\text{info}}$ or a distinct symbol.

## Nice-to-Haves

- **Formalize the optimization objective.** Replace the grid search + visual inspection with a concrete optimization (e.g., maximize the minimum of the two gaps, or maximize the posterior gap subject to a lower bound on the likelihood gap). Even a simple numerical optimizer would substantially strengthen the "optimization" claim.
- **Compare to baselines.** Show how the recommended design compares to naive alternatives (e.g., maximally separated priors, priors matched to typical V1 experiments) in terms of predicted information gap.
- **Simulate intermediate/mixed coding hypotheses.** The paper discusses mixed hypotheses in Section 6 and Appendix A.5 but does not test whether the framework can detect intermediate representations, which would substantially strengthen the case for practical utility.
- **Apply the framework to multi-context real data,** e.g., by splitting sessions or using natural stimulus statistics as priors, to demonstrate that the information gap predicts decoder performance on real neural data.

## Removed Points

- **"Conflating optimal decoders with neural network decoders"** — the paper explicitly acknowledges this gap (line 61) and shows convergence (Fig. 3). The point about realistic sample sizes is partially merged into Minor #4 above.
- **"Section 4.2 is a negative result that wastes space"** — this is a value judgment. Showing that the framework correctly predicts which priors do not work is a legitimate validation.
- **"No mixed hypotheses simulated"** — the paper discusses this in Section 6 and Appendix A.5 within its stated scope. Moved to Nice-to-Haves.
- **"Theory validated only on data matching assumptions"** — the gain-modulated Poisson model (Fig. 4B) specifically tests a deviation from the modeling assumptions. Generic criticism.
- **"Section 5 is circular"** — the paper frames this section as demonstrating that single-context designs cannot adjudicate the hypotheses, not as a validation of the framework. Not circular, but a weak consistency check (merged into Minor #3).

## Novel Insights

None beyond the paper's own contributions. The harsh review's main novel observations are: (1) the "optimization" in the paper is actually a grid scan, which is a correct but straightforward reading of Section 4; and (2) the tiny posterior coding gaps need a power analysis for the framework's utility claims to hold. Both are important and are already reflected in the weaknesses above.

## Suggestions

1. Reframe the paper's scope to accurately reflect what is demonstrated: an information-theoretic *metric* for quantifying distinguishability whose computation can guide design selection. Either replace "optimization" claims with "evaluation" claims, or add formal optimization with baselines.
2. Add a power analysis showing the sample sizes needed to detect the predicted information gaps at the recommended parameter settings, especially for posterior coding (gaps ~0.06 nats). This single addition would most directly determine whether the framework fulfills its stated purpose.
3. Quantify the sensitivity of the recommended parameters to deviations. If the landscape is flat, state this explicitly with numerical support.
4. Replace the Allen dataset section with a more informative empirical test, or reframe it as a motivation (not validation) for why multi-context designs are needed.

## Score and Decision

The paper's core theoretical contribution — the information gap formalism — is sound, well-motivated, and validated by compelling simulation evidence showing convergence of empirical decoder performance to theoretical predictions. However, the paper systematically overclaims on two fronts: (a) the "optimization" is a grid scan with hand-picked points and no baseline comparison, not a demonstrated optimization procedure, and (b) the practical utility for distinguishing posterior coding is undermined by tiny predicted gaps (~0.06 nats) with no power analysis showing detectability at realistic sample sizes. The real-data validation (Section 5) provides only a weak consistency check. These gaps prevent the paper from meeting the bar for ICLR, where methodological claims should be supported by demonstrated impact.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>