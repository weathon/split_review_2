## Summary

This paper formalizes the problem of assessing dataset reliability when ground truth is unobserved but auxiliary data from an unknown experiment are available. It introduces ground-truth-based reliability orderings (exact-match, Blackwell, Hamming/dist), proves impossibility results charting what no score can preserve, and proposes the Gram determinant score, which factorizes as Γ(PQ) = det(P^T P) det(Q)². The score is shown to be experiment-agnostic and, up to scaling, unique in this property. Experiments on synthetic data, CIFAR-10 embeddings, and employment data illustrate the score's behavior.

## Strengths

- **Elegant theoretical framework and impossibility results (Sections 2–3).** The formalization of reliability scoring with ground-truth-based orderings (exact-match, Blackwell, Hamming/dist) is well-motivated and clean. Proposition 3.1's impossibility results—showing, e.g., that no score preserves Hamming ordering even under linearly independent experiments and diagonally dominant misreports—provide a principled characterization of what is and is not achievable, making the subsequent restrictions feel motivated rather than ad-hoc.

- **Experiment agnosticism and uniqueness (Proposition 4.3).** The Gram determinant score's ranking is independent of which experiment generated the observations (since Γ(PQ) ∝ det(Q)² when comparing under the same P). The further result that the score is unique up to scaling in having this property is striking and provides a strong theoretical anchor for the proposal.

- **Clean decoupling via determinant factorization (Equation 4).** The factorization Γ(PQ) = det(PᵀP) det(Q)² separates the quality of the experiment (which the analyst cannot control) from the degree of misreport (which is what the analyst wants to measure). This explains why the score can be experiment-agnostic and why it preserves multiple orderings—essentially, the score operates on Q directly, and the experiment contributes only a multiplicative constant.

## Weaknesses

### Fatal

None.

### Major

- **No baselines in any main-text experiment (Section 5).** Every experiment evaluates the Gram determinant score in isolation against ground-truth metrics (corruption level p, Hamming distance). While the paper mentions a comparison with Kong (2024) and alternative candidates deferred to the appendix, the main experiments include no alternative scoring methods. Any reasonable statistic that covaries with corruption (e.g., trace of the empirical confusion matrix, entropy of conditional label distributions, mutual information) would also decrease with p. Without baselines, the experiments cannot distinguish between "the Gram determinant score captures data quality" and "any statistic correlated with corruption captures data quality." The core theoretical claims do not depend on these experiments, so this does not invalidate the paper, but it makes the empirical support substantially weaker than what the abstract and conclusion suggest.

- **Experiments do not directly test the strongest theoretical claim (Blackwell ordering preservation).** Theorem 4.2 proves that the score preserves Blackwell ordering under P_indep and Q_reg, yet the corruption policies used in the experiments (uniform random, asymmetric neighbor, merge, etc.) are not designed to produce Q matrices satisfying the invertibility and diagonal-maximality conditions under which Blackwell ordering is defined. The experiments instead evaluate correlation with Hamming distance and p—the ordering for which the score has the weakest theoretical guarantee (the scaled dist-ordering with restrictive conditions). The ranking recovery experiment (Fig 2d) provides indirect validation, but the paper's core claim about Blackwell ordering preservation is never tested directly.

### Minor

- **The dist-ordering guarantee is theoretically very narrow (Theorem 4.2, part 3).** The conditions require δ ≤ 1/(64L²d²) and the ordering preserved is only a scaled (1/(4LΔ))-dist ordering. For d=5, L=1, this permits at most N/1600 misreports on the Hamming bound, and one dataset must have less than 1/4 the Hamming distance of the other. The theorem states the conditions explicitly, but the body could be more forthright about how restrictive this window is. (The experiments show good behavior far beyond these conditions, which is encouraging but the guarantee itself is limited.)

- **Computational cost of the plug-in estimator is not discussed.** The plug-in estimator (Definition 4.4) requires O(N²) pairwise comparisons. For N=4000 this is ~16M comparisons; for the CIFAR-10 experiment (N=10000), ~100M per trial. This cost is not acknowledged anywhere in the paper. The stratified matching estimator in the appendix may mitigate this, but the main text should at minimum mention the issue.

- **Employment data experiment lacks uncertainty quantification (Experiment 3).** With N=209 and d=4 (~52 data points per bucket on average), the plug-in estimator operates in a regime where the asymptotic justification (Proposition 4.5) is weakest. No confidence intervals or standard errors are reported for Figure 3d, even though the score is intended for decision-making contexts.

- **The |Y| < d case is not acknowledged as a limitation.** The factorization Γ(PQ) = det(PᵀP) det(Q)² requires PᵀP to be full rank, which implicitly assumes |Y| ≥ d. The kernel extension in Section 4.3 partially addresses continuous Y, but the paper does not acknowledge that the basic score breaks down when the observation space has fewer dimensions than the label space.

### Trivial

None.

## Nice-to-Haves

- Restructure experiments to directly test Blackwell ordering preservation by constructing Q matrices satisfying the Q_reg conditions and verifying ranking under multiple experiments.
- Include at least one baseline (e.g., trace(Q), entropy-based measures) in the main experiments to anchor the empirical contribution.
- Add confidence intervals or bootstrap estimates for the employment data experiment.
- Acknowledge the O(N²) cost of the plug-in estimator and briefly discuss when the stratified matching estimator is preferable.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **"Score increases monotonically with p (line 258)"**: Reviewer flagged as likely typo ("decreases" intended). Per hard rules, this is a typo-level issue; removed.
- **Conclusion overstates finite-sample guarantees**: The reviewer notes the main text only has asymptotic guarantees (Proposition 4.5). However, the finite-sample guarantees are in the appendix (stripped by parser); per hard rules, removed.
- **No comparison with Kong (2024) in main text**: The paper states the comparison is deferred to the appendix. Per hard rules about missing appendix content, removed.
- **Blackwell ordering defined only for restricted class (Q_reg)**: The paper explicitly acknowledges this restriction on line 88 ("Blackwell dominant ordering is intentionally defined for a subset of misreport matrices"). This is the paper's own transparency, not a weakness to criticize.
- **Impossibility results prose is compressed**: This is a presentation suggestion, not a concrete weakness. Moved to Nice-to-Haves implicitly.

## Novel Insights

The most penetrating observation emerging from the reviews is the **mismatch between what the theory guarantees strongly (Blackwell ordering preservation under Q_reg) and what the experiments test (correlation with Hamming distance under unrestricted corruption policies)**. This gap weakens the paper's otherwise well-structured narrative. A second insight: the dist-ordering guarantee, while mathematically valid, operates in conditions so restrictive (≤ N/1600 misreports for d=5, L=1) that its practical relevance is limited; the score's actual usefulness in broader corruption regimes is supported empirically but lacks theoretical backing.

## Suggestions

- Add at least one baseline comparison to the main experiments. The simplest would be the trace of the empirical confusion matrix (which corresponds to 1 − Hamming error) or the determinant mutual information from Kong (2024), which the paper explicitly builds upon.
- Construct experiments that directly validate the Blackwell ordering claim: generate Q, Q' ∈ Q_reg where Q ≻_Blackwell Q', generate data under multiple experiments P ∈ P_indep, and verify that the Gram determinant score ranks them correctly. This would directly validate Theorem 4.2 part 2.
- Acknowledge the O(N²) computational cost of the plug-in estimator and discuss trade-offs with the stratified matching estimator.

## Score and Decision

The paper makes genuine theoretical contributions: a clean formalization of reliability scoring, impossibility results that usefully delineate the feasible region, and the Gram determinant score with its experiment-agnosticism and uniqueness properties. The decoupling factorization is elegant. However, the experimental validation has significant gaps (no baselines, does not test the core ordering claims) that weaken the overall presentation. The theory stands on its own, but the empirical section does not meet the standard needed to claim the score is a *useful* measure—only that it has nice mathematical properties. This is a solid theoretical paper with weak empirical support; for ICLR, it sits at the borderline.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>