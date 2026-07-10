Now let me write the final review.

## Summary

This paper introduces Dig-DEC, a new model-free decision-estimation coefficient that removes the optimism principle from prior work (FGQ+23) and replaces it with KL regularization plus an information-gain term. This conceptual advance enables handling adversarial/hybrid MDPs where optimism-based methods fail because they require explicit reward estimators. The paper obtains the first model-free regret bounds for hybrid MDPs with bandit feedback (under linear reward and general transition structures), improves regret bounds in stochastic settings, and demonstrates through a separation example (3-armed bandit) that Dig-DEC can be arbitrarily smaller than optimistic DEC.

## Strengths

- **Clean conceptual innovation**: Dig-DEC replaces the optimism principle (the V\_φ(π\_φ) term in Eq. 9 of FGQ+23) with KL regularization plus an information-gain term (Eq. 2 and Eq. 7). This is a principled modification that enables handling adversarial/hybrid settings where optimism-based methods require explicit reward estimators and fail in the bandit-feedback case.

- **More flexible and simpler analysis**: The new analysis (Section 4) connects to standard mirror-descent analysis and avoids the restrictive "constructive minimax theorem" of XZ23 and LWZ25, which only works for strictly convex divergences. As stated on lines 153–154, Algorithm 1 can handle a general divergence D, a genuine technical simplification.

- **Theorem 14 (3-armed bandit separation)**: This clean example shows Dig-DEC can be arbitrarily better than optimistic DEC (Ω(√T) vs O(1)), demonstrating that the KL information-gain term yields strict improvement over prior work in a simple yet illuminating setting.

- **Resolution of an open problem**: The paper obtains the first model-free regret bounds for hybrid MDPs with bandit feedback under linear reward and general transition structures (bilinear classes, Bellman-complete coverable MDPs). This directly addresses the open question left by LWZ25.

## Weaknesses

### Fatal
None.

### Major

- **Internal inconsistency in numerical claims about regret exponents**: The abstract (line 13) states that for average estimation error minimization, regret improves from T^{3/4} to T^{3/5} (on-policy) and from T^{5/6} to T^{7/8} (off-policy). However, Table 1 shows T^{2/3} for both on-policy and off-policy in the average estimation error (non-completeness) cases. Moreover, the off-policy claim T^{5/6}→T^{7/8} corresponds to T^{0.833}→T^{0.875}, which is a worsening rather than an improvement. These mutually contradictory claims undermine reader trust in the paper's quantitative contributions. The authors must reconcile the abstract, introduction, and tables to present a single coherent set of exponents before the paper can be accepted.

### Minor

- **Algorithmic tractability is not discussed**: Algorithm 1 requires solving a minimax optimization over Δ(Π) × Δ(Ψ) (Eq. 3) at each round. The paper correctly notes (line 37) that "model-free" does not imply computational tractability, but this disclaimer is easy to miss. A brief discussion of computational challenges and when the meta-algorithm is implementable would strengthen the paper's self-awareness.

- **The "open problem resolution" framing is slightly broader than warranted**: The paper resolves the open problem under Assumptions 2–4 (linear reward with known feature, specific partition structure). The paper acknowledges (line 115) that Assumption 3 does not capture all learnable hybrid MDPs (e.g., low-rank MDPs with unknown reward feature). The abstract and introduction would benefit from more precisely scoping which classes of hybrid MDPs are covered and which are not, rather than the broad claim that the problem is "resolved."

### Trivial
None.

## Nice-to-Haves

- The paper would benefit from a simple example showing where the strict improvement over o-DEC manifests in a non-toy setting (beyond the 3-armed bandit of Theorem 14). While Theorem 14 demonstrates the separation exists, it would strengthen the paper to connect it to the canonical settings (bilinear, BE, coverable) where the framework is ultimately applied.

## Removed Points

These points are flagged to be removed, treat them with caution:

1. **Numerical inconsistency between abstract and introduction's T^{3/2}**: The harsh critic claimed the introduction's parsed T^{3/2} is inconsistent with the abstract. The fraction T^{3/2}=T^{1.5} is almost certainly a parser artifact for what was T^{2/3} in the original submission (the table correctly shows T^{2/3}). This is a formatting artifact and not attributable to the authors.

2. **Claim about "improved T-dependence" being overstated**: The critic said "the tables show at most constant-factor improvements in the non-toy settings." This is speculative without concrete baseline numbers for comparison, and the paper's main contribution is enabling *new settings* (hybrid MDPs with bandit feedback) that prior work could not handle at all.

3. **Generic weakness about missing comparison in canonical settings**: The critic asked for improvement demonstration in bilinear/BE/coverable settings. Theorem 14 provides a clean separation result; the paper's primary contribution is enabling the adversarial/hybrid setting, not improving stochastic rates.

4. **Several strengths removed as generic/superficial**: The critic's strengths about "clean conceptual innovation" and "resolution of an open problem" were kept; more generic statements about writing quality or problem importance were dropped.

## Novel Insights

None beyond the paper's own contributions. The core novelty — removing optimism from DEC via KL regularization plus information gain, and extending to hybrid/adversarial settings — is clearly articulated by the authors.

## Suggestions

1. **Reconcile the numerical claims**: Resolve the inconsistency between abstract (T^{3/5}, T^{7/8}), introduction (T^{3/2}/T^{5/6}), and Table 1 (T^{2/3}) for average estimation error. Present a single coherent set of exponents per setting.

2. **Fix the abstract's off-policy direction**: The claim T^{5/6}→T^{7/8} appears to be a reversal; T^{7/8} > T^{5/6}, so this is not an improvement. Correct the direction or the numbers.

3. **Calibrate the "open problem" framing**: Explicitly state in the abstract/introduction which classes of hybrid MDPs are covered (known-feature linear reward with Assumptions 2–3) and which are not (e.g., unknown-feature low-rank MDPs).

4. **Add computational tractability discussion**: A brief paragraph acknowledging when Algorithm 1 is implementable would improve the paper's completeness.

## Score and Decision

Now let me calibrate. My round-1 bracket from the calibration search placed this paper in the 5.5–7.5 range. Let me narrow.

Looking at the anchors:
- **aPNwsJgnZJ (Horizon-free adversarial RL, score 6.00)**: Similar profile — resolves an open problem, solid theory, but limited novelty and strong assumptions. My paper has a genuinely more novel core idea (removing optimism) but also has the numerical inconsistency weakness.
- **0oWGVvC6oq (Bits and Bandits, score 6.50)**: Clean conceptual contribution, both theory and experiments, but some presentation concerns. My paper lacks experiments but has a more concrete algorithmic contribution.
- **txD9llAYn9 (Model-based RL, score 7.00)**: Strong theory with novel results, but reviewers noted significant presentation concerns (one reviewer gave -2.70 favorability on clarity). My paper's numerical inconsistency is more concrete but less severe than the opacity criticized there.
- **8eNLKk5by4 (Constrained MDPs, score 6.00)**: Solid but incremental theoretical contribution. My paper has a stronger conceptual contribution.

Comparing my draft's favorability ratings against the anchors:
- My strengths (9.15–13.13) are competitive with the 6.0–6.5 anchors' strengths.
- My major weakness (favorability=0.34) is notable but not as negative as some weaknesses in the anchors (e.g., -4.14 in aPNwsJgnZJ, -3.98 in 6HfNB34x9I).
- The numerical inconsistency is real but fixable — it doesn't invalidate the core theory.

Placing the paper: The conceptual contribution (removing optimism from DEC) is genuine and the paper handles settings (hybrid MDPs with bandit feedback) that prior work could not. This is meaningfully above the 5.25 paper (DOOMD) which was rejected for limited novelty. It is comparable to the 6.0 papers (Horizon-free adversarial RL, Constrained MDPs with policy optimization) which were accepted. The numerical inconsistency prevents it from reaching 6.5+ territory.

Final score: **6.0** — a solid theoretical contribution with a genuine innovation and resolved open problem, held back by a significant but fixable presentation issue in the abstract's numerical claims.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>