## Summary

The paper introduces "random set stability," a new stability notion for data-dependent random sets (optimization trajectories), and uses it to derive worst-case generalization bounds that involve empirical complexity measures (topological, fractal) without requiring intractable mutual information terms. The theoretical framework recovers classical edge cases and produces bounds with a multiplicative interaction between stability (β\_n) and topological complexity (E^α, PMag). Experiments on ViT and GraphSAGE estimate the bounds' order of magnitude and show correlations between E^1 and the generalization gap.

## Strengths

1. **Novel theoretical synthesis.** The idea of connecting algorithmic stability to topological complexity measures (E^α, PMag) in a mutual-information-free way is genuinely novel. The bounds in Theorem 4.4 (β\_n^{1/3} × √(log C(W))) represent a plausible and non-trivial synthesis of two previously separate lines of work.

2. **Recovers classical edge cases as sanity checks.** Corollary 3.5 (recovering singleton stability bounds with J=1) and Corollary 3.6 (recovering fixed-hypothesis-set Rademacher bounds with J=n, β\_n=0) demonstrate that the framework is coherent with established theory — a meaningful sanity check that not all new frameworks pass.

3. **Honest about limitations.** The paper explicitly acknowledges (Section 4.1, lines 229–235) that its bounds have a slower convergence rate (O(n^{-1/3}) vs O(n^{-1/2})) and are only in expectation rather than high-probability. This candor is commendable and rare.

4. **Correctly identifies a genuine limitation in prior work.** The intractable mutual information (IT) term in topological/fractal generalization bounds (Simsekli et al., 2020; Birdal et al., 2021; Andreeva et al., 2024) is a real obstacle, and the paper's motivation for removing it (Section 1, Equation 5 and surrounding discussion) is well-posed.

## Weaknesses

### Major

1. **Experiments use the 0-1 loss, which violates the Lipschitz assumptions required by the theory.** The paper states "We use the 0-1 loss" (Table 1 caption, line 282). However, Lemma 3.2 requires L-Lipschitz loss to connect uniform argument stability to random set stability, Assumption 4.1 requires Lipschitz continuity on each random set, and Theorems 4.3–4.4 rely on both. The 0-1 loss is non-Lipschitz in the parameters. The paper provides no justification for why its theoretical results should apply in this setting and offers no acknowledgment of this disconnect. This gap casts doubt on whether the experimental results provide any evidence for the paper's theoretical claims.

2. **The experiments do not evaluate the paper's main claimed theoretical results (Theorems 4.3, 4.4).** The numerical bound in Table 1 is computed via Massart's lemma as 2√(2 log(T)/J) + 2Jβ\_n (line 260), which is a simplified proxy that bypasses the topological complexity measures (E^α, PMag) entirely. The correlation experiments (Figures 2, 3) show univariate Pearson correlations between E^1 and the generalization gap — this was already demonstrated in prior work (Andreeva et al., 2024). The paper claims "our experimental results strongly support Theorem 4.4" (line 297), but the experiments do not test the specific multiplicative structure β\_n^{1/3} × √(log E^α) that Theorem 4.4 predicts. Showing that E^1 correlates with the generalization gap does not validate the interaction between stability and topological complexity that is the claimed novelty.

3. **Several computed bounds are vacuous on a [0,1]-bounded loss.** For ViT at η=10^{-4}, the bounds are 104.43% and 105.24% — exceeding 100% provides no information. The paper states "in most experimental settings, the estimated bounds remain below 100% accuracy, hence, provide meaningful guarantees" (line 278), but 2 out of 8 settings violate this, and even the remaining bounds (47–76%) are 5–10× larger than the actual generalization gaps (4.6–12.8%). The paper overstates the informativeness of these results.

### Minor

1. **No comparison against any prior bound.** The experiments do not compare against IT-based topological bounds, classical uniform convergence bounds, or the Foster et al. (2019) bounds. Without such a benchmark, it is impossible to assess whether the new framework yields practically tighter or more informative guarantees.

2. **The β\_n^{-2/3} "integer divisor of n" condition is restrictive and unexplained.** Theorems 4.3 and 4.4 (lines 209, 221) require that β\_n^{-2/3} is an integer divisor of n, stated "without loss of generality" but without justification. Since β\_n depends on the algorithm, loss, and data distribution, this couples the stability parameter to the sample size in a specific way that will not hold generically.

3. **Scope of Assumption 3.1 beyond finite trajectories is unclear.** The sufficient condition (Lemma 3.2) covers only finite trajectories via uniform argument stability — which are settings where classical single-iterate bounds already work. For continuous trajectories (Example 1.2, SGD with Brownian motion), Lemma 3.2 does not apply, and the paper does not address how Assumption 3.1 can be satisfied in this case.

4. **No high-probability bounds.** The paper provides only bounds in expectation, while the prior work it builds on (Equation 5) provides high-probability bounds. The paper acknowledges this limitation (Section 6) but does not attempt to close this gap using standard tools (e.g., McDiarmid's inequality).

5. **The optimistic β\_n estimation error is not quantified.** The paper acknowledges that the finite-sample β\_n estimate is optimistic (line 254) but provides no analysis of the approximation gap. If the true β\_n is substantially larger than estimated, the bounds would be even looser.

### Trivial

None.

## Nice-to-Haves

- Replace the 0-1 loss with a Lipschitz surrogate (e.g., cross-entropy) in the experiments, or provide explicit justification for applying the theory to non-Lipschitz losses.
- Compute and report the actual topological bounds from Theorem 4.4 directly, rather than the Massart proxy.
- Include at least one baseline comparison (e.g., a uniform convergence bound or an IT-based topological bound from prior work).
- Discuss how to handle the β\_n^{-2/3} divisor condition in practice, or provide a version of the theorems without this restriction.

## Removed Points

- **Foster et al. framing criticism.** The claim that the paper's criticism of Foster et al. is "slightly inaccurate" is a difference of interpretation, not a factual error. The paper correctly states that Foster et al. do not account for algorithmic randomness U; this is a limitation whether by oversight or by design.
- **Equivalence proof for J-differing datasets.** Speculative; not verifiable from the paper as written.
- **σ and exponent parsing in Corollary 3.3.** Likely a PDF parser artifact. The rule forbids criticizing formatting/parsing issues.
- **Speculation about IT terms being "often bounded by n log|W|".** This is the reviewer's speculation, not content from the paper.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Replace the 0-1 loss with a Lipschitz surrogate in the experiments, or provide a rigorous argument for why the theoretical results should apply to non-Lipschitz losses.
2. Compute and report the actual topological bounds from Theorems 4.3/4.4, even if they are loose — this would validate the paper's central claim of providing "fully computable" topological bounds.
3. Include at least one baseline comparison from prior work (Andreeva et al., 2024, or a simple uniform convergence bound) to demonstrate empirical improvement.
4. Address the β\_n^{-2/3} divisor condition — either justify it or relax it.
5. Provide some quantification of the β\_n estimation error or its impact on the bound.

## Score and Decision

**Round 1 bracket (from calibration):** 3.0–5.5. The paper is clearly not a strong reject (the theory is coherent and novel) and not in the accept range (the experiments fail to validate the claimed contributions). Comparing with anchors: the 5.25-rated "PH generalization on graphs" paper and the 5.25-rated "Stability in Free Adversarial Training" paper have similar profiles — real theory with experiment-theory gaps. The current paper's theory is cleaner than those, but the experimental disconnect (0-1 loss, not testing the claimed bounds) is more severe. The 6.25-rated "Adversarial Training Stability" paper, which was accepted, has better experimental alignment.

**Final score:** 5.0. The theoretical contribution is genuine and the framework is well-motivated, but the experimental validation has significant gaps: the 0-1 loss violates the paper's own Lipschitz assumptions, the experiments test a simplified proxy bound rather than the claimed topological bounds, and some computed bounds are vacuous. Without experimental evidence that actually tests the theoretical results, the paper's central claim of providing "fully computable" topological bounds is not convincingly demonstrated.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>