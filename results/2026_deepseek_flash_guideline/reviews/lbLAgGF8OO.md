Now let me write the final consolidated review.

## Summary
This paper introduces Dig-DEC (Dual Information Gain Decision-Estimation Coefficient), a new model-free DEC framework that replaces optimism with pure information-gain-driven exploration. The paper makes three main contributions: (1) a generalized AIR framework handling arbitrary convex divergences with connections to mirror descent, which is more flexible and simpler than prior approaches; (2) the first model-free regret bounds for hybrid MDPs (stochastic transitions, adversarial rewards) with bandit feedback under linear rewards, resolving an open problem from [LWZ25]; and (3) improved online function estimation procedures yielding better T-dependence in both average-error and squared-error settings, including the first √T regret for Bellman-complete MDPs by a DEC-based method.

## Strengths

- **Dig-DEC is provably never worse than optimistic DEC and can be arbitrarily better**: Theorem 13 proves $\text{dig-dec} \leq \text{o-dec} + \eta$ for any $\overline{D}$, showing Dig-DEC is always competitive with optimistic DEC. Theorem 14 provides a concrete 3-armed bandit where optimistic DEC suffers $\Omega(\sqrt{T})$ regret while Dig-DEC achieves constant regret ($\leq 1$), demonstrating the improvement can be arbitrarily large.

- **First model-free regret bounds for hybrid MDPs with bandit feedback**: Resolves the main open problem from [LWZ25] by obtaining sublinear regret for hybrid bilinear classes and Bellman-complete coverable MDPs with bandit feedback. The removal of optimism is critical here because it avoids explicit construction of the reward estimator (line 305), which was the barrier in prior work that required full-information feedback.

- **First √T regret for Bellman-complete MDPs by a DEC-based method**: Theorem 11 bounds Est by $O(\log^2|\Phi|)$ — constant in $T$ — for squared estimation error under Bellman completeness. Combined with Dig-DEC bounds in Table 1 (e.g., $H\sqrt{dT}\log|\Phi|$ for coverable MDPs), this yields √T regret, matching optimism-based approaches [JLM21, XFB+23] for the first time in the DEC literature.

- **Elegant generalization of the AIR framework**: The analysis (Section 4) generalizes beyond the KL-based divergence used in [XZ23, LWZ25], connecting to standard mirror descent analysis via Bregman divergences (Eq. 5–6, Lemma 18). The framework recovers [LWZ25]'s two-level algorithm as a special case with simpler analysis, and as noted on lines 171–172, can achieve Est that does not scale with $\log|\Phi|$ where prior work required a more complex approach.

- **Improved estimation procedures**: The unbiased product estimator (Section 4.2.1) using sample-splitting improves over the biased estimator of [FGQ+23] in terms of concentration. The two-timescale posterior update for squared error (Section 4.2.2) achieves a constant-in-$T$ Est bound with a simpler analysis than [FGQ+23].

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Theorem 14's strict improvement is only shown for a 3-armed bandit, not for MDPs**: While the existence proof is valid and shows Dig-DEC can be "arbitrarily better" than optimistic DEC in principle, the demonstration is in a simple bandit setting far removed from the MDPs that motivate the paper. The paper would be materially strengthened by showing — even in a constructed MDP — where the KL information-gain term yields strict improvement over optimistic DEC in a nontrivial sequential decision-making setting.

- **The hybrid setting results rely on assumptions that restrict coverage**: As the paper honestly acknowledges (lines 115–116), Assumption 3 does not capture all learnable hybrid MDPs — for hybrid low-rank MDPs with unknown reward features, $\log|\Phi|$ scales polynomially with the number of feature mappings, whereas [LMWZ24] handles this with only logarithmic dependence. Additionally, Assumption 4 requires linear rewards with *known* features. These are meaningful restrictions on the scope of the hybrid results.

- **Computational tractability is not discussed**: The algorithm requires solving a minimax optimization over $\Delta(\Pi)$ and $\Delta(\Psi)$ at each step (Eq. 3), which is intractable for large policy or model classes. The paper correctly clarifies (line 37) that "model-free" refers to regret dependence on $|\mathcal{M}|$, not computational constraints, but a brief discussion of computational considerations would help set expectations.

### Trivial
None.

## Nice-to-Haves
- A worked example for at least one hybrid setting showing how the Dig-DEC bound is computed and optimized over $\eta$ would improve readability.
- The $\Phi$ notation (infosets, $\nu_\phi$, $\rho(\phi)$, $f_\phi$) is consistent with prior work but quite heavy; a simple running-example table would help the reader track the entities.

## Removed Points
These points are flagged for removal; treat them with caution:
- Criticisms about "garbled T-exponents in Table 2" and "inconsistent rate claims between abstract/intro" — These concern what are almost certainly PDF-to-text parsing artifacts (inverted fractions like $T^{3/2}$ vs $T^{2/3}$, garbled LaTeX rendering). The rules specify that formatting artifacts from parsing should not be counted against the paper, as the original submission does not have these issues.
- Criticism that "Est improvement from √T to T^{1/2} is vacuous" — This is likewise a parser artifact where distinct values in the original appear identical in plain text. The paper's framing of the improvement is in the estimator structure (biased → unbiased), which is a genuine contribution.
- Criticisms about missing appendix content or unverifiable claims due to parser-stripped sections — The appendix exists in the original submission and was removed by the parser.
- Formatting/style nitpicks and speculative "could the metric be measuring a proxy?" concerns — These are either parser artifacts or area-of-concern generics without concrete anchor in the paper.

## Novel Insights
The most instructive observation from the reviews is that what initially appears to be a fatal weakness (inconsistent numerical claims and superlinear regret exponents in Table 2) is almost entirely a PDF-parsing artifact rather than an actual flaw in the paper. Once parsing issues are set aside, the paper's genuine limitations are modest: the strict improvement over optimistic DEC is demonstrated only for a bandit rather than for MDPs, and the hybrid results require assumptions that exclude some known learnable cases. Neither limitation undermines the paper's core contributions — a novel framework, resolution of an open problem, and analysis tools generalizing prior DEC theory. The paper is a solid theory contribution that advances the state of the art in model-free learning for structured MDPs.

## Suggestions
1. Provide a concrete MDP example (even a toy) where Dig-DEC provably outperforms optimistic DEC, to strengthen the "arbitrarily better" claim beyond the 3-armed bandit setting.
2. Add a brief discussion of computational considerations for the minimax optimization in Eq. (3), noting any conditions under which it becomes tractable.
3. Add a worked example for at least one hybrid setting to illustrate how the Dig-DEC bound is computed and optimized.
4. Ensure the camera-ready version has clearly readable tables with unambiguous fraction rendering to avoid reader confusion.

## Score and Decision

**Score calibration against human-reviewed anchors:**

| Anchor | Score | Round | Comparison |
|--------|-------|-------|-----------|
| Horizon-free RL in Adversarial Linear Mixture MDPs | 6.0 | Q4 | Solves an open problem about horizon-free adversarial RL; cleaner presentation but comparable contribution depth. This paper resolves a different open problem (hybrid model-free bandit) and provides a more general framework. |
| Model-based RL as a Minimalist Approach | 7.0 | Q4 | Achieves horizon-free and second-order bounds with elegant simplicity; cleaner exposition. This paper's framework is more novel but less cleanly presented. |
| Minimax Optimal RL with Quasi-Optimism | 7.0 | Q4 | Strong practical+theoretical contribution with clean results. This paper is purely theoretical with more restricted practical applicability. |
| On Bits and Bandits | 6.5 | Q2 | Information-theoretic regret bounds with experiments; similar-level contribution but in a different sub-area. |

**Bracketing:** Round 1 bracket was [5.5, 7.5]. After inspecting anchors, the paper sits above the 6.0 anchor (resolves an open problem with a novel framework) but below the 7.0 anchors (which have cleaner presentation and fewer scope restrictions).

**Final score rationale:** The paper makes a genuine theoretical contribution: a novel DEC framework that removes optimism, resolves an open problem (first model-free hybrid MDP bounds with bandit feedback), and matches optimism-based approaches in Bellman-complete settings for the first time. The technical approach is elegant and generalizes prior work. The weaknesses are minor (bandit-only demonstration of strict improvement, acknowledged assumption restrictions, undiscussed computational aspects) and do not threaten the core claims.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>