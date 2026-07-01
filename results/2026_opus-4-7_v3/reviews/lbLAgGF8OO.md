Now let me read the remaining sections more carefully, including Tables and the comparison section.Now I have a thorough understanding of the paper. Let me verify a few more specific claims about the exponents and Section 4.2.1.Good. I've confirmed the systematic parsing artifacts (e.g., line 213: "improves their rate of Est from √T to T^{1/2}" — identical expressions, clearly a parser error). Now let me submit the draft review before calibration.Now let me do Round 1 calibration — bracketing the score range with anchor papers on similar topics.Let me read a few relevant anchor papers to narrow the bracket.Now let me do a Round 2 narrowing search within my initial bracket of 6.0-8.0.Now I have sufficient calibration. Let me synthesize the final review.

**Round 1 bracket: 6.0 – 8.0**

Key anchor comparisons:
- The paper is clearly stronger than the 6.0 anchors (horizon-free adversarial RL, contextual bandit second-order bounds) — it has more contributions and resolves an open problem.
- It is comparable to the 7.0 model-based RL minimalist paper, which also makes a clean conceptual point with solid theory.
- It falls short of 8.0 due to the niche audience of the DEC framework and the loose (possibly vacuous) hybrid setting rates.

**Narrowed bracket after Round 2: 6.5 – 7.5**, centering at 7.0.

Now let me write the final consolidated review.

---

## Summary
This paper introduces Dig-DEC (dual information gain DEC), a model-free complexity measure for reinforcement learning that replaces the optimism principle in prior DEC frameworks with a dual information-gain divergence. The key insight is decomposing the KL term into a regularization component (which removes the need for optimism) and an information-gain component (which enables strict improvement). The approach yields improved regret bounds for stochastic MDPs—matching √T rates for Bellman-complete settings for the first time within the DEC framework—and delivers the first model-free regret bounds for hybrid MDPs with bandit feedback under linear reward and general transition structures, resolving the main open problem from [LWZ25].

## Strengths
- **Conceptual clarity and novelty of Dig-DEC (Section 4.1, Eq. 8; Section 6).** The replacement of optimism with dual information gain is a genuine conceptual contribution. The decomposition of the KL divergence into regularization (KL(ν_φ, ρ)) and information-gain (KL(ν_φ(·|π,o), ν_φ)) terms is clearly explained in Section 6 and reveals that optimism in [FGQ⁺23] was serving as a proxy for regularization—a perspective not previously articulated in the DEC literature. This is the paper's most lasting contribution.

- **Resolution of [LWZ25]'s open problem (Section 5.2, Table 2).** The paper delivers the first model-free regret bounds for hybrid MDPs with bandit feedback under linear reward and several general transition structures. The solution arises naturally from the framework (removing optimism avoids the need for explicit reward estimators, which was precisely the barrier in [LWZ25]). This is a concrete, well-defined advance.

- **√T regret for Bellman-complete MDPs (Theorem 11, Table 1 rows 6, 8, 10).** Achieving Est ≲ log²|Φ| (constant in T) under Bellman completeness is a substantial technical improvement over [FGQ⁺23]'s T-dependent bound, and for the first time matches optimism-based approaches [JLM21, XFB⁺23] within the DEC framework.

- **Clean formal dominance and separation (Theorems 13–14).** Theorem 13 (dig-dec ≤ o-dec + η) establishes that Dig-DEC is always at least as good as optimistic DEC. Theorem 14 provides a decisive separation: a 3-armed bandit where the prior approach incurs Ω(√T) regret while the new approach achieves O(1). This shows the improvement can be arbitrarily large, not merely asymptotic refinement.

- **Modular framework (Section 4, Eqs. 5–6).** The Bregman-divergence-based analysis is more flexible than the "constructive minimax theorem" approach of [XZ23] and [LWZ25], and the framework's ability to recover prior results (Appendix C) while handling both stochastic and hybrid settings with the same algorithmic principle is a real generalization.

- **Improved average estimation error via split-sample estimator (Section 4.2.1).** The unbiased split-sample estimator (using products of two independent half-sample means) is a technically clean improvement over [FGQ⁺23]'s biased squared-mean estimator.

## Weaknesses

### Fatal
None

### Major
None

### Minor
1. **Some hybrid setting rates appear vacuous (Table 2).** The off-policy bilinear case without completeness shows T^{13/8} ≈ T^{1.625} regret, which is super-linear and thus vacuous for large T. The paper does not discuss lower bounds for the hybrid setting or analyze whether these loose rates are artifacts of the analysis technique or reflect genuine barriers. Since these are the "first results" for model-free hybrid bandit, the absence of any anchor for quality is a gap. A discussion — even informal or conjectural — of where these rates stand relative to optimal would substantially strengthen the contribution. — *This matters because it prevents the reader from assessing whether the Dig-DEC framework captures the "right" complexity for hybrid settings or whether significant slack remains.*

2. **Separation example limited to bandits (Theorem 14).** The 3-armed bandit separation is clean and striking, but a structured MDP example (even H=2) where Dig-DEC strictly improves over optimistic DEC would more convincingly demonstrate that the improvement is relevant in the settings the paper primarily targets (MDPs with complex transition structures). — *This weakens the empirical relevance of the separation claim, though the mathematical result remains valid.*

### Trivial
None

## Nice-to-Haves
- A brief discussion of computational tractability: the minimax optimization in Eq. (3) over Δ(Π) × Δ(Ψ) is potentially intractable. While this is standard for DEC papers and the paper correctly scopes "model-free" to mean regret independence from |M| (Section 1, final paragraph), a paragraph acknowledging the computational gap would be appropriate.
- A comparison table against [FGQ⁺23] and [LWZ25] in the main body (not just Appendix A) showing setting-by-setting rate improvements.
- An MDP-based separation example alongside the bandit one.
- Discussion of whether hybrid rates can be tightened with refined analysis or if structural barriers exist.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

1. **Exponent inconsistencies in abstract/introduction vs. tables.** The reviewer noted apparent inconsistencies (e.g., abstract claims T^{5/6} → T^{7/8} which would be a worsening; Section 4.2.1 line 213 claims Est improves "from √T to T^{1/2}" which are identical). However, the paper's parsed text shows pervasive, systematic parser artifacts with fraction exponents throughout. Per review policy, these are treated as parser errors — the original submission does not have these issues. The tables themselves are internally consistent. **Removed: formatting artifact.**

2. **Theorem 6 imprecision.** The reviewer suggested the theorem statement may have a typo regarding min_ρ max_ν. On inspection, the theorem correctly sums over t with ρ_t fixed by the posterior update, and the min is over p (not ρ). This is consistent with the algorithm and analysis in Eq. (6). **Removed: reviewer misread.**

3. **Computational intractability as a weakness.** This is standard for the entire DEC/E2D literature and the paper explicitly scopes "model-free" to mean independence from |M| in regret bounds (Section 1, final paragraph). **Moved to nice-to-have: not a weakness in the paper's community.**

## Novel Insights
The decomposition of the KL divergence in Dig-DEC into a regularization component (KL(ν_φ, ρ)) and an information-gain component (KL(ν_φ(·|π,o), ν_φ)) is a genuinely novel conceptual contribution. The regularization term removes the need for optimism, while the information-gain term enables strict improvement over optimistic DEC. This reveals that optimism in the prior DEC framework was serving as a proxy for regularization — a structural insight that may extend beyond the specific technical setting. The practical consequence is that removing optimism avoids the need for explicit reward estimators, which is precisely the barrier that prevented prior work from handling hybrid MDPs with bandit feedback. The framework's ability to unify stochastic and adversarial settings through a single information-theoretic principle, rather than requiring separate algorithmic designs, represents a meaningful simplification of the DEC/E2D line of research.

## Suggestions
- Discuss whether the T^{13/8} rate (and other loose hybrid rates) are fundamental to the hybrid setting or artifacts of the current analysis. Even a paragraph stating known lower bounds or conjectures would greatly strengthen Table 2's impact.
- Consider adding a structured MDP separation example (even a simple tabular MDP with H=2) to complement Theorem 14's bandit construction.
- Add a concise main-body comparison table showing prior vs. new rates across all settings, to help readers immediately see the advance without consulting Appendix A.
- In the conclusion, briefly acknowledge the computational tractability gap, since the paper's title and framing ("applications in adversarial MDPs") may create expectations about practical deployment.

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison |
|-------|------|-----------|-------|------------|
| KL Divergence for GFlowNets | Uj0h13lVrR | 1.0 | 1 | Fundamentally weak; no relation to our paper's quality |
| Balancing Discriminative Knowledge | 5lUdTogEL3 | 1.0 | 1 | Not relevant; far below our paper |
| All Pairs Minimax Path | bEgDEyy2Yk | 1.0 | 1 | Implementation paper; not comparable |
| UMAP Scientific Discourse | P49gSPmrvN | 1.0 | 1 | Visualization paper; not comparable |
| Variable Forward Regularization | lFzUHGebeb | 2.0 | 1 | Online learning theory but limited contributions |
| Actor-Critic Sample Complexity | A1WwYw5u8m | 3.0 | 1 | RL theory but incremental; weaker than our paper |
| Guided RL with Roll-Back | 5s1qpjrNvZ | 3.0 | 1 | Empirical RL; different category |
| Robust MDPs | Zi1QNJKXAD | 3.2 | 1 | RL theory but limited novelty |
| Value-Biased MLE for Linear MDPs | 2h3m61LFWL | 4.25 | 1 | Rejected for insufficient novelty vs prior work; our paper is clearly stronger |
| BPI in Online CMDPs | w8Zo7jACq7 | 5.2 | 1 | Model-free RL theory but strong assumptions and partial novelty; our paper is stronger |
| Analysis of Deep RL Premises | R6klub5OXr | 5.25 | 1 | Empirical analysis; different type |
| Double Descent in RL | 9RIbNmx984 | 5.25 | 1 | Theoretical but different topic |
| **Horizon-free Adversarial RL** | **aPNwsJgnZJ** | **6.0** | **1** | **Most relevant anchor. Also "first result" for adversarial RL setting, accepted with uniform 6s. Our paper has more contributions (new complexity measure + open problem resolution + separation + √T matching) and is clearly stronger.** |
| IRL Hardness | S24zdyiWDT | 6.0 | 1 | RL theory, first results in IRL settings |
| Adversarial Counterfactual RL | eUEMjwh5wK | 6.0 | 1 | Adversarial RL but more empirical |
| MaxInfoRL | R4q3cY3kQf | 6.75 | 1 | Information gain exploration framework; more empirical |
| Linear System Parameters | 5t57omGVMw | 8.0 | 1 | Bandit/online learning; strong but different niche |
| Multi-Agent RL via Behavioral Economics | stUKwWBuBm | 8.0 | 1 | Strong cross-disciplinary contribution |
| Hidden Cost of Waiting | A3YUPeJTNR | 8.0 | 1 | Prediction/allocation theory |
| Dynamic Discounted CFR | 6PbvbLyqT6 | 8.0 | 1 | Game solving; different domain |
| Misspecified Q-Learning | nIEjY4a2Lf | 6.0 | 2 | RL theory with function approximation; comparable scope but narrower contribution |
| Reward Function Optimization Perils | OmFlDvsvc3 | 6.0 | 2 | Theoretical analysis of reward learning |
| **Second-order Bounds Contextual Bandits** | **h6ktwCPYxE** | **6.0** | **2** | **Related theory (eluder dimension, second-order bounds). Mixed reviews. Our paper has stronger conceptual novelty.** |
| **Model-based RL Minimalist** | **txD9llAYn9** | **7.0** | **2** | **Most comparable anchor. Clean theoretical insight (standard MLE suffices for horizon-free bounds). Got 6,8,8,6. Our paper is comparable: both make genuine conceptual contributions to RL theory with comprehensive results. Our paper resolves an open problem; this one simplifies existing understanding.** |
| BAMDP Shaping | tijmpS9Vy2 | 7.0 | 2 | Framework for intrinsic motivation; clean theory |
| Representation Learning from Video | 3mnWvUZIXt | 7.25 | 2 | Theory for representation learning |

**Round 1 bracket:** 6.0 – 8.0
**Round 2 narrowing:** 6.5 – 7.5, centering at 7.0

**Reasoning:** The paper is clearly above the 6.0 anchors — it has more and stronger contributions than the horizon-free adversarial RL paper (which also resolves an open question but contributes primarily one algorithm). It is comparable to the 7.0 model-based RL minimalist paper: both make clean conceptual points backed by comprehensive theoretical results. The paper's weaknesses (loose hybrid rates, bandit-only separation) are minor and do not undermine the core claims. The niche nature of the DEC framework audience prevents it from reaching 8.0, but the contributions are substantial and the framework advances are genuine.

**Final score: 7.0**

This paper makes a genuine conceptual advance in the DEC/E2D line of research — replacing optimism with dual information gain — backed by strong technical results including resolution of an open problem and the first √T regret matching for Bellman-complete MDPs within DEC. The minor weaknesses (loose hybrid rates, bandit-only separation) do not undermine the core contributions. The paper should be accepted.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>