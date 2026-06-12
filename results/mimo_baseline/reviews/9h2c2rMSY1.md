## Summary
This paper addresses the breakdown of conformal prediction (CP) coverage guarantees for time-dependent PDEs, where distribution shift over time violates exchangeability. The authors prove that in function space, solution distributions at different times are mutually singular (TV distance = 1), making CP inapplicable in that setting. They then show that for discretized linear PDEs with Gaussian initial conditions, the exact time-evolved distributions are available in closed form, enabling weighted conformal prediction (WCP) with formal coverage guarantees. Experiments on synthetic PDEs and a real-world thermography dataset demonstrate that WCP maintains target coverage where naive CP and LSCI fail.

## Strengths
- **Fundamental theoretical insight (Theorem 4.1):** The proof that the TV distance between solution measures at any two distinct times equals 1 for the heat equation with Gaussian initial conditions is elegant and important. It shows that the function-space perspective commonly used in neural operator learning is fundamentally incompatible with CP, providing a crisp negative result that clarifies a real conceptual issue in the field.
- **Practical framework with formal guarantees:** By shifting to discretized formulations and exploiting the closed-form Gaussian evolution (Theorem 4.2), the authors derive exact likelihood ratios for weighted CP. This yields a concrete, implementable method with genuine coverage guarantees—the only method among those tested that provides formal guarantees in the time-dependent PDE setting.
- **Honest and well-designed experiments:** The comparison across varying PDE instability parameters (a, b, c) clearly demonstrates that naive CP and LSCI systematically undercover as dynamics become more unstable, while WCP maintains coverage. Crucially, the method honestly reports infinite bands when the distributional shift is too large (rather than providing false confidence), which is the correct behavior for safety-critical applications.
- **Clear exposition and positioning:** The paper is well-written, with a logical flow from problem identification (Figure 2 motivating the issue) through theory to experiments. The related work section honestly characterizes limitations of competing approaches.

## Weaknesses
### Fatal
None.

### Major
- **Linearity and Gaussian assumptions limit scope:** The method requires linear PDEs with Gaussian (or location-scale family) initial conditions. Many important PDEs in scientific ML are nonlinear (Navier-Stokes, wave equations with nonlinear terms, etc.), and initial conditions may not be Gaussian. While Remark 4.3 extends to location-scale families and the authors acknowledge this limitation, it significantly restricts the practical applicability. The paper would be substantially stronger if it discussed concrete strategies or conditions under which the framework could extend to nonlinear settings (e.g., linearization, or local Gaussian approximations).
- **High n_∞ in unstable regimes:** In the most challenging settings (e.g., a = −0.01), the fraction of samples with infinite bands reaches 100% by timestep 15, meaning the method provides no useful prediction intervals for those cases. While this is formally correct (infinite bands trivially cover), it raises questions about practical utility precisely when users need uncertainty quantification most—under strong instability. The paper should more explicitly discuss the practical tradeoff between guaranteed coverage and informative bands.

### Minor
- **Surrogate model choice:** The paper uses a geometry-informed neural operator but states the choice is not important for downstream CP analysis. However, the quality of the base model's residuals affects calibration. A brief ablation or justification with a different surrogate architecture (e.g., FNO, DeepONet) would strengthen the generality claim.
- **Real-world validation is limited:** The thermography example in Appendix A.6 appears to involve a very specific, small-scale setting. A second real-world example with more complex dynamics would strengthen the empirical case.
- **Remark 4.5 on transferring guarantees to continuous space:** This remark is intriguing but vague. The claim that "bands on the discretized solution can be transferred to the original solution by leveraging numerical error guarantees of the scheme" is not formalized. A concrete statement or theorem about the relationship between discretized and continuous-space coverage would be valuable.

### Trivial
None.

## Nice-to-Haves
- A discussion of how sensitive the method is to misspecification of the covariance matrix Σ_t (e.g., if the PDE parameters or initial distribution are estimated from data rather than known exactly).
- An analysis of computational cost comparison in more detail—WCP requires computing matrix exponentials and density ratios, which scales with discretization size n.

## Novel Insights
The paper's most novel insight is the sharp disconnect between function-space and discretized-space perspectives for conformal prediction on PDEs. Theorem 4.1 shows that in infinite-dimensional function space, measures are mutually singular (TV = 1) for any nonzero time difference, while Theorem 4.2 shows that finite-dimensional discretizations of linear PDEs yield tractable Gaussian evolution with bounded (often moderate) distributional shift. This duality—function space is impossible, discretized space is tractable—is a genuinely useful conceptual contribution that clarifies when and why CP can work for physical systems, and it challenges the neural operator community's emphasis on function-space formulations when the downstream task requires distributional guarantees.

## Suggestions
- Formalize Remark 4.5 with a theorem connecting discretized coverage to continuous-space coverage, even if only for specific PDE classes and discretization schemes.
- Include an ablation on the sensitivity to the Gaussian assumption—e.g., what happens when initial conditions are slightly non-Gaussian or when Σ_0 is estimated from finite samples?
- Discuss the regime boundary where infinite bands begin to dominate and whether adaptive time-stepping or multi-resolution calibration could help.
- Consider adding a nonlinear PDE experiment to empirically test the method's behavior (even if formal guarantees don't hold), to better understand the frontier of applicability.

## Score and Decision
The paper presents a clean theoretical contribution (function-space mutual singularity) paired with a practical method (weighted CP via discretized Gaussian distributions) that fills a genuine gap in conformal prediction for scientific ML. The core theory is solid, the experiments clearly demonstrate the claimed advantages, and the paper is well-written. The main limitation—applicability restricted to linear PDEs with Gaussian initial conditions—is significant but well-acknowledged, and the framework still covers a broad class of practically important problems. The honest handling of infinite bands, while limiting in extreme regimes, reflects methodological integrity appropriate for safety-critical domains. This represents a meaningful step forward for uncertainty quantification in physics-informed ML.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: Accept