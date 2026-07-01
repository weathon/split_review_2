## Summary

This paper studies offline change point localization and inference in dynamic multilayer random dot product graphs (D-MRDPGs). It proposes a two-stage algorithm combining seeded binary segmentation with low-rank tensor estimation (TH-PCA), establishes consistency for estimating both the number and locations of change points, and derives limiting distributions of the refined estimators — stated as the first such distributional results in the network change-point literature. A data-driven confidence interval procedure is also developed and evaluated on simulations and real trade network data.

## Strengths

1. **First limiting distributions for change-point estimators in network data.** Theorem 2 derives the limiting distribution of the refined change-point estimator under vanishing jumps, characterized by a two-sided Brownian motion. This goes substantially beyond the high-probability bounds that dominate the existing network change-point literature (Wang et al., 2021; Padilla et al., 2022), and the paper correctly identifies this as a genuine theoretical advance with appropriate qualification.

2. **First treatment of offline change-point detection in dynamic multilayer networks.** The paper fills a clear gap: prior work on multilayer network change points (Wang et al., 2025) is limited to the online setting, and prior offline work focuses on single-layer models. The combination of a low-rank tensor model with seeded binary segmentation is a natural but nontrivial extension carried through fully.

3. **Full theoretical pipeline.** The paper provides consistency (Theorem 1), limiting distributions (Theorem 2), a data-driven procedure for confidence intervals (Section 3.1), and empirical evaluation of the CIs (Table 2). This is a more complete treatment than most papers in this area.

4. **Consistent empirical dominance.** Table 1 shows CPDmrdpg outperforming both gSeg and kerSeg across all four scenarios, including Scenarios 2 and 3 where the assumed model (Model 1) is violated. The improvement is substantial: for Scenario 4 with n=50, CPDmrdpg achieves 99.98% segment coverage while gSeg (nets.) achieves 0%.

5. **Robustness testing beyond model assumptions.** Scenarios 2 and 3 deliberately violate Model 1, and the method still performs well. This demonstrates that the claims are not brittle artifacts of the specific model class.

## Weaknesses

### Fatal

None.

### Major

1. **Sample-splitting gap between theory and practice.** Algorithm 1 requires four mutually independent adjacency tensor sequences {A(t)}, {A'(t)}, {B(t)}, {B'(t)} as input (line 111). Theorem 1 and Theorem 2 both condition on this independence. However, the paper states (line 89): *"The assumption of mutual independence among the four sequences in Algorithm 1 is imposed for theoretical convenience. In practice (and in our numerical experiments in Section 4), Stage I and Stage II are implemented using the same two split tensor sequences via the odd-even splitting approach."*

Odd-even splitting of a single sequence of independent observations produces two independent subsequences, not four. The paper does not explain how the practical implementation (two sequences) maps onto the theoretical requirement (four sequences). The CUSUM statistics and refined scan statistics in Algorithm 1 explicitly use separate sequences for different components to decorrelate the terms; reusing the same two sequences for all four roles may introduce dependencies that the theoretical analysis assumes away. The paper acknowledges the gap but provides no argument — not even a heuristic one — that the guarantees still hold with only two sequences. This creates a genuine disconnect between the theoretical results and the evaluated procedure.

The theoretical results remain valid for the four-sequence version; the issue is that they do not directly apply to the implementation that was actually tested. This should be addressed by either adjusting the theoretical framing to clearly delineate regimes, or providing a principled argument that the two-sequence implementation inherits the guarantees.

### Minor

2. **No ablation studies isolating component contributions.** The paper compares against two generic competitors (gSeg, kerSeg) but provides no ablations to identify which component drives the improvement. Useful ablations would include: (i) Stage I alone (without Stage II refinement), (ii) applying the single-layer method of Wang et al. (2021) independently to each layer, (iii) averaging across layers and applying Wang et al. (2021). Without these, it is difficult to attribute the observed improvement to the multilayer modeling, the tensor estimation, the algorithmic structure, or parameter choices.

3. **Suspiciously narrow confidence intervals warranting diagnostic discussion.** In the real-data analysis (Table 4), the 95% CI for the 1991 change point (T=35, discrete annual data) is (5.97, 6.03) — length 0.06 on a grid of 35 integer time points. In simulations (Table 2), Scenario 1 at n=100 yields average CI length 0.003 with 100% coverage. While strong signal can legitimately produce tight CIs, the near-zero length on discrete integer-valued time points merits discussion. More concerning is the coverage drop in Scenario 3 (76.67% at n=100, 95.33% at n=150), where Model 1 is violated — suggesting calibration may degrade under misspecification. The paper does not comment on either observation.

4. **No experiments varying the time horizon T.** The asymptotic theory requires T → ∞, but simulations fix T = 200 throughout. Adding a T ∈ {100, 200, 400, 800} study would help connect the finite-sample experiments to the asymptotic claims, and is a natural request for a paper whose core contributions are theoretical.

5. **CI results for n = 50 are missing from Table 2.** The simulation section reports CI coverage and lengths only for n ∈ {100, 150}, omitting n = 50 which is used in Table 1 for the localization results. The omission is not explained.

### Trivial

6. **Minor presentation issue:** In Table 4, the 2005 change point (time point 20) has CI (17.97, 18.05) — this asymmetry relative to the detected point could be clarified.

## Nice-to-Haves

- **Varying T in simulations.** A study with T ∈ {100, 200, 400, 800} would better connect the asymptotic theory to finite-sample behavior.
- **Data-driven rank selection guidance.** The paper uses r₁ = r₂ = 15 following Wang et al. (2025) and defers sensitivity analysis to the appendix; some practical guidance in the main text would improve utility.
- **A summary of appendix comparisons** with Wang et al. (2025) and Li et al. (2024) in the main text (space permitting) would strengthen the empirical positioning.

## Removed Points

The following points from the input review are removed with justification:

- "Remark 1's comparison with online methods is not apples-to-apples" — Scope creep. The comparison is labeled as a Remark and compares localization rates, which is standard practice.
- "The post-hoc storytelling in real-data analysis should be acknowledged" — Standard practice in change-point detection; the paper does not claim causal evidence.
- "No discussion of rank selection" — The paper follows prior work (Wang et al., 2025) and mentions sensitivity analysis in the appendix. Moved to Nice-to-Haves.
- "Comparison with Wang et al. (2025) and Li et al. (2024) deferred to appendix" — Space constraint, not a methodological flaw.
- Various formatting/style nitpicks — Parser artifacts, not author errors.

## Novel Insights

The central tension revealed by this review is that the paper makes a genuinely novel theoretical contribution (first limiting distributions for network change-point estimators) while having a non-trivial gap between the conditions under which the theory is proven (four independent data sequences) and those under which the method is evaluated (two sequences via odd-even splitting). This tension is more consequential than the paper acknowledges: the theoretical guarantees are presented alongside the experimental results without clarifying that the experiments do not satisfy all theoretical input requirements. Independently, the CI narrowness in both simulations and real data suggests that the asymptotic approximation's finite-sample behavior merits deeper investigation. These are real but addressable issues that do not undermine the theoretical contribution itself.

## Suggestions

1. **Explicitly delineate the theoretical and experimental settings.** Either prove (or provide a rigorous argument) that the theory goes through with two independent sequences obtained via odd-even splitting, or clearly state that the theoretical results apply to the four-sequence version and the experiments use a heuristic adaptation. Do not let the current ambiguity stand.

2. **Add one key ablation.** The most informative single ablation would be Stage I alone (without tensor-based Stage II refinement). This would quantify the improvement attributable to the low-rank estimation component, which is the paper's main algorithmic novelty.

3. **Diagnose the CI narrowness.** Add a comment explaining why CIs can be narrower than the integer grid resolution, and consider a small simulation where jump sizes and T are varied to examine the coverage-to-length tradeoff.

## Score and Decision

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>