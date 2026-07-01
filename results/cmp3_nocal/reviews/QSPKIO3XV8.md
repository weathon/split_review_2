## Summary

This paper proposes **Dimension Domain Co-Decomposition (3D)**, a PINN framework that combines two decomposition strategies: (1) a dimension decomposition using a single shared MLP with indexed inputs to produce per-coordinate factors (parameter count independent of input dimensionality), and (2) a Mixture-of-Experts (MoE)-based domain decomposition that automatically partitions the solution space without requiring predefined subdomains or interface conditions. The paper also introduces **Variable Interpretability (VI)**, a metric that quantifies alignment between learned per-dimension factors and ground-truth components. Experiments on Poisson, Wave, Viscous Burgers, and Linear Transport equations demonstrate the framework's effectiveness.

---

## Strengths

1. **Parameter-efficient dimension decomposition (Section 3.1, Table 1).** The shared MLP with indexed inputs `(xⱼ, j-1)` is a clean architectural idea. The parameter count is independent of the input dimensionality — 5,392 parameters regardless of whether the problem is 5d or 10d Poisson. The memory reduction from 50.0% (5d) to 30.4% (10d) versus independent per-dimension networks is a real scaling advantage.

2. **MoE-based automatic domain decomposition produces qualitatively sensible partitions (Figures 4, 5).** For Viscous Burgers, the router identifies the shock at x=0 as the primary partition boundary without manual specification. The ℓ₂ error drops from 0.2108 (K=1) to 0.0011 (K=2), directly demonstrating the value of the MoE component.

3. **Consistency analysis across random seeds (Section 4.3).** Across five random seeds, the same geometric structures (shock at x=0 for Burgers, diagonal stripes for Transport) are consistently recovered, showing the router is responding to the PDE's actual solution structure rather than initialization artifacts.

4. **Dimension fine-tuning capability (Section 4.2, Appendix C).** The separable architecture allows fine-tuning a 5D-trained model on an 8D problem — a non-obvious practical advantage over standard MLP PINNs.

---

## Weaknesses

### Fatal

None.

### Major

1. **Missing experimental comparison against the most relevant baselines: SPINNs and XPINNs/APINNs.** The paper explicitly positions itself as improving upon SPINNs — stating in Section 3.1 that the shared MLP architecture "sav[es] the memory when handling high-dimensional problems" versus SPINNs — and claims advantages over domain-decomposition methods that require manual partitions (Section 2.2). Yet **no experiment compares against SPINNs** for dimension-decomposition benchmarks (Poisson, Wave), and **no experiment compares against XPINNs, APINNs, or any existing domain-decomposition PINN variant** for the Burgers and Transport problems. The "vanilla PINNs" baseline and the "independent MLPs" ablation do not substitute for this. Without these comparisons, the paper's central comparative claims — that the approach improves upon prior decomposition-based methods — are unsubstantiated by experimental evidence. The evaluation demonstrates that the method works and its components contribute, but not whether it is *better* than existing alternatives.

   This is the paper's most significant weakness. It can be addressed by adding SPINNs as a baseline for the dimension-decomposition experiments and XPINNs (or a hand-partitioned PINN) for the domain-decomposition experiments.

### Minor

2. **The VI metric's scope is narrower than claimed.** The paper introduces VI as "a novel, quantitative, scale-invariant metric to evaluate dimension-wise interpretability" (abstract, line 33), but the metric can only be computed when the exact solution is known to factorize as a product of univariate functions. The conclusion acknowledges this limitation (line 208): "*VI* relies on reference solutions that are dimension-separable." However, for non-separable solutions (including the Burgers and Transport equations used elsewhere in the paper), the paper merely suggests constructing "separable approximations, for example using truncated Fourier series" — with no experiment conducted, no method specified, and no analysis of how approximation artifacts would interact with the metric. The paper would benefit from either (a) reframing VI honestly as an alignment check for separable problems (still useful), or (b) demonstrating it on a non-separable problem to show the proposed extension works.

3. **VI as an "interpretability" measure conflates capacity with interpretability.** The results in Table 2 show a monotonic pattern: as the rank *r* increases, VI monotonically approaches 1 for all problems. For the 5d Poisson case, VI jumps from 4.11% (*r*=1) to 99.99% (*r*=4). This pattern is consistent with VI measuring whether the model has sufficient rank to span the ground-truth factor subspace — a capacity/correctness check — rather than measuring whether the internal representations are "interpretable" in the usual sense. The paper could address this by scoping the claim more precisely (e.g., "dimension-component alignment metric" rather than "interpretability metric").

4. **Main accuracy results lack statistical variance.** The ℓ₂ errors for the 5d Poisson (line 137: 1.8430×10⁻⁴) and 10d Poisson (line 139: 1.25×10⁻³) are reported as single values without variance across seeds. Only the domain decomposition results (Section 4.3) and VI results (Table 2) report variance. Given the consistency analysis shown for domain decomposition, the same rigor should be applied to the main accuracy claims.

5. **The 10d Poisson timing trade-off requires more analysis.** The shared MLP takes 1,579s versus 1,184s for the baseline PINN — a 33% increase. The paper calls this a "moderate runtime trade-off" but does not discuss whether this gap scales with dimensionality, whether it is a one-time cost, or whether it widens with more training steps. Since the abstract claims "improves both computational efficiency and solution accuracy," this timing penalty warrants more careful discussion.

6. **Router parameter overhead is not broken down in Table 1.** The router is a 5-layer MLP with width 64 (line 120-121), which is substantially larger than each expert (2-layer MLP with width 32 or 64). Table 1 reports total parameters for the MoE cases (Burgers: 23,586; Transport: 29,043) but does not separate router parameters from expert parameters. This makes it difficult to assess the true parameter efficiency of the approach in the MoE setting.

### Trivial

7. The dimension fine-tuning experiment (line 141) is fully deferred to Appendix C with no quantitative result in the main text. A brief summary of the accuracy achieved would strengthen the main paper's narrative.

---

## Nice-to-Haves

- A matched-parameter vanilla PINN baseline for the 5d Poisson experiment (currently the vanilla PINN uses a 10-layer MLP with width 64 — roughly 33k parameters — versus the shared MLP's 5,392). The 10d Poisson experiment already does this correctly, and extending the same rigor to the 5d case would strengthen the experimental design.
- A test of whether sparse MoE actually collapses on the Burgers problem, rather than assuming it will (the paper's stated reason for using dense MoE).
- Guidance for detecting *K_optimal* in practice, beyond empirical selection.

---

## Removed Points

These points were raised in the harsh review but are removed after cross-checking against the paper:

- **"Truncated text at lines 80–82"** — This is a parser artifact in the extracted text; the original submission does not have this issue (hard rule: formatting artifacts are parser errors, not author errors).
- **"Independent MLPs is a strawman baseline that inflates the apparent advantage"** — The independent MLPs comparison is a legitimate ablation that isolates the effect of weight sharing. The paper does not claim this is a published state-of-the-art method. The real gap (missing SPINNs comparison) is already captured as a Major weakness.
- **"The paper does not test whether sparse MoE actually collapses"** — While true, this is a reasonable design choice supported by a stated rationale. It does not rise to the level of a weakness worth retaining given the paper's scope.
- **"The normalization in Equation 5 uses an unusual choice that could produce numerical instability"** — This is a marginal technical concern without demonstrated impact on the paper's results.
- **"No guidance is given for how to detect K_optimal"** — The paper states "we select K_optimal as best number of experts" (line 110), which is standard empirical practice and requires no further specification.

---

## Novel Insights

The harsh review's most valuable observation is that the VI metric's monotonic convergence to 1 with increasing rank *r* reveals it to be primarily a capacity-sufficiency diagnostic rather than an interpretability measure in the traditional sense. This insight is not explicitly discussed in the paper and could inform how the authors frame VI going forward. Beyond this, no genuinely novel insight emerges from the reviews beyond the paper's own contributions.

---

## Suggestions

1. **Add SPINNs as a baseline** for the Poisson and Wave experiments (dimension decomposition), and **add XPINNs or a manually-partitioned PINN** for the Burgers and Transport experiments (domain decomposition). This single change would address the paper's most significant weakness and transform the evaluation from demonstrating that the method works to demonstrating that it improves upon the state of the art.

2. **Reframe the VI contribution** more precisely as a "dimension-component subspace alignment metric for separable solutions" rather than a general "interpretability metric." This would align the claims with the metric's actual scope and avoid overclaiming.

3. **Report ℓ₂ errors with standard deviations** across multiple seeds for all main accuracy results, not just for domain decomposition.

4. **Provide a router/expert parameter breakdown** in Table 1 for the MoE cases to enable transparent assessment of parameter efficiency.

---

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Accept</decision>