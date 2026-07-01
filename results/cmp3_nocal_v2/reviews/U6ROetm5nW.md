Now I have a thorough understanding of the paper. Let me write the consolidated final review.

## Summary

This paper studies Kernel Density Estimation (KDE) in high dimensions and presents the first provable time-space tradeoffs for the problem. By applying the asymmetric LSH of Andoni et al. (2017) within the Charikar et al. (2020) KDE framework, the authors obtain a parametrized family of data structures indexed by $\delta \geq 0$, yielding space exponent $1+\delta$ and query exponent $\xi(\delta)$. The headline numerical results are query exponent $\approx 0.05$ at space exponent $\approx 4.1$–$4.15$, and query exponent $0.1865$ at linear space (exponent $1$). The paper is entirely theoretical, operating at the same level of rigor as the work it extends.

## Strengths

1. **First time-space tradeoffs for KDE.** Theorem 16 provides a parametrized family of data structures that smoothly trade space $(1/\mu)^{1+\delta}$ against query time $(1/\mu)^{\xi(\delta)}$. Prior work (Charikar et al., 2020) had only two discrete operating points (data-independent at $\approx 0.25$, data-dependent at $\approx 0.173$), both with essentially linear space. The tradeoff curve itself (right plot of Figure 1) is novel.

2. **Clear technical insight, honestly scoped.** The paper correctly identifies that the asymmetric LSH of Andoni et al. (2017) — originally designed for ANN — can be plugged into the Charikar et al. (2020) KDE framework in a non-trivial way, because the query-time bottleneck arises at a different distance scale than the space bottleneck. The explanation in Section 1.2 (starting "Our contribution: query time reduction via asymmetric ANN") is specific and well-motivated.

3. **Honest accounting of limitations.** The paper explicitly states that (a) the high-space regime ($1/\mu^{4.15}$) makes the main result less directly comparable to prior work with $1/\mu$ space, (b) the linear-space result ($0.1865$) does not beat the data-dependent Charikar et al. bound ($0.173$), only the data-independent one ($0.25$), and (c) constant query time KDE is provably not achievable with *current* ANN technology (Section 1.2). These are stated rather than buried.

4. **Rigorous extension of an established framework.** The paper operates at the same level of rigor as Charikar et al. (2020): worst-case analysis over the full Charikar-Siminelakis framework, with proper handling of the "nice range" $[c_0 J, (1-c_1)J]$ and the edge cases. The derivation of $\theta(\delta)$ and the piecewise definitions of $\rho_s(\delta, x), \rho_q(\delta, x)$ are explicit.

## Weaknesses

### Fatal
None.

### Major

1. **Headline numerical exponents are not verifiable from the paper.** The paper's main quantitative selling points — query exponent $\approx 0.05$ at space exponent $\approx 4.1$/$4.15$, and query exponent $0.1865$ at space exponent $1$ — are obtained by solving the optimization problem in Equation (10). The paper states these are "computed numerically" (Section 5) and "using numerical methods" (Section 1.2) but provides: (a) no description of the optimization procedure (discretization scheme, solver used, convergence criterion), (b) no error bounds or precision guarantees, and (c) no table of $\xi(\delta)$ values that would allow readers to verify the tradeoff curve numerically. Equation (10) involves a nested min-max optimization over continuous domains; without knowing how it was solved, a reviewer cannot distinguish correct values from artifacts of a coarse grid or a solver that found a local optimum. This is a significant evidential gap because the improved exponents are the paper's most eye-catching results. The *existence* of a tradeoff is established analytically in Theorem 16, so this is not fatal, but the specific numerical values that drive interest in the result are unsupported.

### Minor

2. **Inconsistent space exponent across theorem statements.** Theorem 1 (Informal, p.2) states space $1/\mu^{4.15}$, while Theorem 17 (p.8) gives $\exp_{1/\mu}(4.1 + o(1))$. The Abstract and Section 5 discussion use $4.15$. This inconsistency should be resolved — the two values differ by $\approx 0.05$ in the exponent, which matters when comparing against the claimed improvements.

3. **Framing of the linear-space result underplays the SOTA data-dependent bound.** The Abstract and Introduction prominently feature the improvement from $0.25$ (data-independent) to $0.1865$, which is accurate. However, a reader could easily miss that the SOTA data-dependent bound of $0.173$ (Charikar et al., 2020) remains better. The paper does acknowledge this in Sections 1.1 and 5, but the Abstract's framing — "improving the non-adaptive KDE bound ... and nearly matching the bound of Charikar et al. (2020)" — does not make clear that "the bound of Charikar et al." had two versions and the better one ($0.173$) is not matched. Since the linear-space regime is the most practically relevant comparison point, this framing should be more precise.

### Trivial
None.

## Nice-to-Haves

- **Describe the numerical optimization** used to evaluate Equation (10), even briefly (e.g., discretization scheme, solver, estimated precision). Better: release a short script that computes $\xi(\delta)$ for any $\delta$.
- **Provide a table of $\xi(\delta)$ values** at key $\delta$ points (e.g., $\delta = 0, 0.5, 1, 2, 3, 3.15, \infty$) so readers can inspect the tradeoff numerically rather than only via Figure 1.
- **State the precision** to which the reported exponents ($0.05$, $0.1865$, $4.1$/$4.15$) are accurate.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Definition 10 sampling rate ($p_j = \min(1/2^{J+n}, 1)$) appears erroneous**: The formula as extracted is suspicious — independent of $j$ and astronomically small — but this is likely a PDF parser corruption of something like $2^{J-j}$. Per the rule that parser artifacts are not author errors, this is removed. If the formula is indeed $2^{J+n}$ in the original, it would be a fatal error, but we cannot determine this from the extracted text.
- **Expected size $m_j$ in Definition 10 inconsistent with later usage**: $m_j = 1/(2^J \mu) = 1$ (since $2^J = 1/\mu$) contradicts $m_j = \exp_{1/\mu}(1 - x_j)$ used on p.7. This too may be a parser corruption; removed for the same reason.
- **Section 1.2 "Why constant query KDE is not possible" over-promises**: The reviewer argued the heading over-promises, but the text explicitly qualifies this as "with known ANN results" and "an exciting open problem." The criticism is not justified given the paper's own scoping.
- **Section 4 threshold function presented as black box**: The derivation is deferred to Appendix C, which is standard practice for theory papers. Not a genuine weakness.
- **No experiments**: The reviewer correctly notes this is not a flaw for a theory paper in the tradition of Charikar et al. (2020). Removed.
- **Space blowup understated as "somewhat higher"**: The paper openly acknowledges the $n^{4.15}$ space cost throughout (Abstract, Sections 1.1 and 5), including the explicit caveat that prior work uses $1/\mu$ space. "Somewhat higher" is a qualitative judgment, not an error. Removed as a subjective framing complaint.

## Novel Insights

None beyond the paper's own contributions. The reviews confirm the paper's main claims but do not surface a perspective the paper itself does not already offer.

## Suggestions

1. Resolve the space exponent inconsistency ($4.15$ vs $4.1$) between Theorem 1 and Theorem 17.
2. Provide a brief description of the numerical optimization procedure used to evaluate Equation (10), and ideally release a verification script. This would transform the headline numerical claims from "we ran an unspecified method and got these numbers" to a verifiable contribution.
3. In the Abstract (and prominently in Section 1), when presenting the linear-space result, make explicit that the data-dependent bound of $0.173$ (Charikar et al., 2020) is still better, even while the paper improves over the data-independent bound.

## Score and Decision

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>