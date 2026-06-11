## Summary
# Final Review Report

## Summary

This paper introduces a formal model of controlled sequential social learning, where an LLM-powered information mediator (a "planner") strategically chooses the precision of private signals for a sequence of agents who also learn from observing each other's actions. The authors characterize optimal policies for both altruistic planners (maximizing social welfare) and biased planners (inducing a specific action regardless of the true state). Key theoretical results include a convexity proof for the altruistic value function and piecewise characterization of optimal policies with distinct investment regimes. The paper complements theory with LLM-based simulations demonstrating that LLM planners exhibit emergent strategic behavior broadly aligned with the analytical predictions, while adapting to non-Bayesian agents. The framework provides a tractable basis for studying algorithmic information mediation and its societal impact.

## Strengths
1. **Novel problem formulation.** The paper introduces a well-motivated formal model that connects two previously separate literatures — sequential social learning (Banerjee 1992, Bikhchandani et al. 1992) and information design (Kamenica & Gentzkow 2011) — through the lens of an LLM-powered information mediator. The model is clean: binary state, binary symmetric signals, precision as control variable, and Bayesian belief updates. This parsimony makes the analysis tractable while capturing the core tension between private information provision and observational learning.

2. **Rigorous theoretical characterization.** The convexity proof for the altruistic value function (Theorem 2) appears technically sound and addresses a non-trivial challenge arising from the dependence of agents' actions on public belief. The piecewise characterization of optimal policies (Theorems 3 and 5) yields interpretable, multi-phase strategies (no investment, maximum investment, intermediate precision) that align with economic intuition. The analysis of both myopic and forward-looking planners cleanly isolates the role of social learning externalities.

3. **Interesting empirical bridge to LLMs.** The LLM-based simulations are a distinctive contribution, going beyond purely analytical social-learning models by testing whether an LLM planner's emergent behavior matches theoretical predictions. The finding that LLM planners exhibit qualitatively similar strategic patterns — high investment near unfavorable cascades, precision reduction near favorable cascades — despite facing non-Bayesian LLM agents is a nontrivial result that strengthens the practical relevance of the framework.

4. **Clear welfare implications.** The demonstration that even a constrained planner (no lying, no cherry-picking, information parity) can shift social welfare by 40–50% is striking and policy-relevant. The comparison across analytical, LLM, and hybrid settings provides a nuanced picture: optimal policies designed for Bayesian agents are "brittle" under non-Bayesian agents, while LLM-adapted policies perform better — a useful caution for deploying analytical mechanism design in practice.

## Weaknesses
### Major Weaknesses

**W1. LLM empirical evidence for C3 is under-powered and lacks generalizability (major).** 
The third core contribution — empirical validation of strategic LLM behavior — rests entirely on a single scenario (car purchase) with a single LLM model (not named in the main text). The paper reports qualitative similarity between LLM and optimal policies, but does not provide statistical confidence bounds, formal similarity metrics, or bootstrap intervals for the policy deviation histogram (Figure 2b). The three non-Bayesian biases (NB1-NB3) are derived from one model's belief-updating behavior, yet the paper treats them as general LLM properties. Without cross-model validation (e.g., testing on Claude, Llama, Gemini) or additional scenarios (e.g., medical advice, political recommendation), the claim that "LLM planners exhibit sophisticated emergent strategic behavior" remains anecdotal. This significantly limits the strength of C3.
*Required action:* Add bootstrap confidence intervals for policy deviation; test at least one additional domain; specify the LLM model(s) in the main text.

**W2. Social welfare monotonicity claim needs scope boundary (major).**
Section 6.3 states: "As better information never harms an agent's expected utility, social welfare is monotonic in signal precision ... This implies the altruistic planner always increases social welfare relative to the baseline." The monotonicity proof (Appendix C.9) may hold for an individual agent's static decision problem, but social welfare in this model aggregates across a *sequence* of agents where precision choices affect the public belief cascade dynamics. A very informative early signal could theoretically trigger a premature cascade, reducing aggregate welfare. The paper does not explicitly address whether the monotonicity proof accounts for these dynamic informational externalities. This gap affects the validity of the welfare comparison in Figure 2c.
*Required action:* Clarify in the main text whether the monotonicity proof accounts for cascade dynamics, and bound the welfare claim accordingly.

**W3. The "first formal model" claim is not precisely bounded (major).**
The paper claims "the first formal model that integrates a dynamic control problem for a centralized information planner with the mechanism of sequential social learning." The Related Work section itself cites Wei & Anastasopoulos (2022) and Smith et al. (2021) on *control* of social learning, and Arieli et al. (2022) and Wu et al. (2025) on information design in social learning settings. The paper's genuine distinctiveness — no two-way communication, agents retain action control, planner has no informational advantage — is clear but the "first" framing without explicit comparison dimensions invites reviewer skepticism. The authors should adopt a scoped phrasing that acknowledges the closest prior work and pinpoints the precise novel constraint set.
*Required action:* Replace "first formal model" with a bounded statement: "To our knowledge, the first formal model that integrates dynamic precision control by an information mediator with sequential social learning under the constraints that the mediator has no informational advantage and cannot falsify signals."

**W4. Framing tension between "subtle influence" and deliberate obfuscation (major).**
The introduction frames the planner's influence as "subtle: it does not falsify information, but rather decides how much to invest." However, the biased planner's optimal policy (Theorem 5, case E) involves reducing precision below the natural baseline $p$ to $b - \epsilon$, which is a deliberate obfuscation strategy that makes signals *less* informative. This is qualitatively different from "investing less" — it is active signal degradation. The paper should either expand the framing to encompass bidirectional control (enhancement and suppression) or acknowledge that precision reduction constitutes a form of manipulation.
*Required action:* Revise the "subtle influence" framing in the introduction to acknowledge bidirectional precision control (both increasing and decreasing precision), or add a qualification.

**W5. Missing practical interpretation of non-existent optimal policies (major).**
The biased planner analysis (Section 5) correctly identifies that optimal policies do not exist for certain belief ranges, requiring $\epsilon$-optimal policies. The paper describes the mathematical structure but does not explain the practical implication: a system designer operating at those belief thresholds cannot implement a stable deterministic policy without accepting either an arbitrarily small loss or cycling behavior. This is an important design consideration that should be made explicit.
*Required action:* Add a paragraph after Theorem 5 explaining the practical implications of policy non-existence for system implementation.

### Minor Weaknesses

**W6. Introduction narrative buries the core research gap.** The first paragraph catalogs LLM capabilities and only introduces the social learning intersection in the final sentence. A hook-first structure would better engage readers.

**W7. Alignment paragraph is overly convoluted.** The distinction between expected-utility alignment (altruistic planner) and realized-utility alignment (biased planner, conditional on state = G) is a key conceptual point but the prose can be streamlined for clarity.

**W8. Equation (4) derivation is opaque.** The $\min(b_i, 1-b_i, 1-q_i)$ formula elegantly captures three regimes but the main text provides no derivation sketch, forcing readers to reconstruct it from the action rule (Equation 2).

**W9. Conclusion introduces unsubstantiated language.** Phrasing like "take advantage of social learning" goes beyond the evidence, which shows correlation with optimal policy rather than explicit exploitation. The limitations paragraph omits key modeling constraints (binary state space, single LLM model).

**W10. Remark 2 assumption framing is one-sided.** Each assumption is described as "not restrictive" in specific contexts, but the paper would benefit from explicitly stating when each assumption *does* bind (e.g., platforms with proprietary user data violate assumption 1).

**W11. Online persuasion/RL positioning could be sharper.** The paper simultaneously claims its setting is "not an online-learning or RL environment" while modeling it as a discounted MDP. A clarifying sentence about using MDP theory for dynamic programming rather than trial-and-error learning would resolve the tension.

**W12. Myopic vs. optimal comparison lacks economic intuition.** Theorem 3 notes the optimal planner requires stronger public belief, but the mechanism — informational externality — is never explicitly explained in the main text.

## Score
**Final Score: 6/10**

*Rationale:* The paper makes a genuine theoretical contribution by formalizing controlled social learning in a tractable MDP framework, with clean convexity results and interpretable policy characterizations. The theoretical core (C1, C2) is rigorous and well-executed. However, the empirical contribution (C3) — a key differentiator for the paper — is significantly undermined by limited experimental scope (single scenario, single LLM model, no statistical confidence bounds) and overclaimed framing. The welfare monotonicity claim requires tighter scoping. The "first formal model" framing invites unnecessary credibility risk. The paper's strengths lie in its theoretical formulation and the policy-relevant observation that constrained mediators can have outsized welfare effects. The identified weaknesses are fixable with additional experiments, more bounded claims, and improved narrative structure, suggesting the paper could reach 7-8/10 after moderate revision.

**Post-Revision Target: [7, 8]/10**