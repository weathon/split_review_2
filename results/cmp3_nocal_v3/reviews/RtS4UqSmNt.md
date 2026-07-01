## Summary

This paper introduces a formal model of controlled sequential social learning in which a planner (e.g., an LLM-based information mediator) strategically chooses the precision of agents' private signals while agents also learn from observing prior agents' actions. The model is analyzed for both altruistic (social-welfare-maximizing) and biased (action-pushing) planners. The authors prove convexity of the altruistic value function (Theorem 2), characterize optimal policies in threshold-form phases for both planner types (Theorems 3 and 5), and complement the theory with LLM-based simulations in which LLMs play the roles of both planner and agents.

## Strengths

1. **Well-posed formal model with clear assumptions (Section 3).** The model captures the core tension between a planner's precision choice and the informational externalities created through social learning. The binary-state, binary-signal, Bayes-rational agent framework is concise, and the constraints on the planner (information parity, no lying or cherry-picking, full observability, Remark 2) are stated explicitly. These restrictions make the positive results about the planner's ability to shift welfare non-trivial.

2. **Rigorous theoretical characterization (Theorems 1–5).** The convexity of the altruistic value function (Theorem 2) is a non-trivial result — the authors correctly note the challenge that agents' action rules depend on public belief, which breaks the linearity that would otherwise directly imply convexity. The characterization of optimal policies in three (altruistic) and five (biased) phases, including the counterintuitive result that a biased planner may intentionally *decrease* signal precision (obfuscation) to lock in a favorable cascade, provides genuine insight. The threshold structure is clearly described and the intuition for each regime is provided.

3. **Novel empirical approach.** Using LLMs as both planner and agents in a three-role architecture (Planner, Agent, Oracle) is a creative methodological bridge between the analytical Bayesian model and real-world deployment settings. The hybrid setting (analytically optimal policy applied to LLM agents) is a sensible way to study model misspecification.

## Weaknesses

### Fatal
None.

### Major

1. **The empirical section lacks basic methodological reporting, substantially weakening the empirical claims (Section 6).** The paper makes strong claims — that LLM planners show "sophisticated emergent strategic behavior," that the analytically optimal policy is "brittle," and that welfare effects are "significant" — but the experimental methodology as reported in the main text is missing several standard elements:

   - **No specific LLM model is named.** The paper refers generically to "LLMs" without identifying the model (GPT-4, Claude, LLaMA, etc.). This is a basic reproducibility requirement; different models have dramatically different reasoning capabilities.
   - **No mention of number of runs, trials, or random seeds.** The results could come from a single run.
   - **No error bars or variance measures.** The welfare bar chart (Figure 2c) shows point estimates only. The policy deviation histogram (Figure 2b) aggregates data without reporting variability.
   - **No statistical testing.** Claims such as "biased planners decreased social welfare by 40 to 50%" are stated as precise quantities with no confidence intervals or significance tests.

   The paper acknowledges in Section 7 that "the fidelity of LLM-human simulators remains contentious" but does not apply corresponding standards of rigor to its own LLM experiments. Because the empirical validation is listed as Contribution 3 in the introduction, these gaps mean the empirical contribution does not meet the evidentiary bar that the paper itself implicitly asserts for it. *The theoretical contribution stands on its own, but the empirical claims as presented are illustrations, not evidence.*

2. **The causal interpretation of LLM policy deviations as "strategic adaptations" to non-Bayesian agents is unsupported (Section 6.2).** The paper observes that the LLM planner's policy avoids extreme precisions, shows gradual taper rather than sharp cutoffs, and continues investing at very low beliefs. It then attributes points (2) and (3) to the planner's "direct response" to agents' non-Bayesian patterns (NB2, NB3). However, the paper provides no controlled experiment to rule out simpler alternatives:

   - **Central tendency bias** — the paper acknowledges point (1) as "consistent with a known central tendency bias" but then attributes the same general pattern in points (2) and (3) to strategic adaptation without disentangling the two.
   - **Approximation error** — the LLM may not be able to compute or represent the optimal policy precisely.
   - **Prompting effects** — the way precision choice is communicated to the LLM may naturally produce smoother or more conservative responses.

   To support the strategic-adaptation claim, the paper would need a control condition — e.g., showing that the same LLM planner facing Bayesian (simulated) agents chooses a policy closer to the analytical optimum, or that deviations increase systematically when agent non-Bayesianness is amplified. Neither is provided.

### Minor

3. **The "brittleness" of the optimal policy is overstated due to an asymmetric comparison (Section 6.3).** The hybrid setting compares the analytical optimal policy (designed for Bayesian agents) applied to LLM agents against the LLM policy developed through interaction with LLM agents. Finding that a policy optimal under one model is suboptimal under a different model is an expected consequence of model misspecification, not evidence of "brittleness" in any distinctive sense. A symmetric comparison (evaluating how the LLM policy performs when applied to Bayesian agents) is missing, making the claim one-sided.

4. **Experimental parameter values not reported in the main text.** The paper states it varies \(k\), baseline precision \(p\), and discount factor \(\delta\) (Section 6, line 212), but the specific values tested are not reported. Varying these parameters could substantially change the comparison, and reporting them is needed for reproducibility.

5. **No explanation of how "underreaction" and "overreaction" are measured relative to the Bayesian benchmark (Section 6.1, Figure 1b).** The paper claims LLM agents exhibit NB1 (underreaction to confirmatory signals) and NB2 (overreaction to contradictory signals), but does not explain the measurement methodology. At extreme priors, Bayesian updates are asymmetric by construction (ceiling/floor effects on the prior). The paper needs to demonstrate that LLM deviations exceed what the Bayesian model already predicts, not merely that the curves differ in shape.

### Trivial
None.

## Nice-to-Haves

- **Symmetric misspecification test**: Evaluating how the LLM-planner policy performs when applied to Bayesian agents would strengthen the empirical comparison and is a natural control condition.
- **Clarify how the LLM planner chooses precision**: The paper describes *what* the planner does but not *how* — is the LLM given a mathematical description of precision and costs, or is the task described qualitatively? This matters for interpreting whether the planner is performing "strategic reasoning" in the same sense as the analytical planner.
- **Welfare monotonicity caveat for non-Bayesian agents**: The claim that social welfare is monotonic in signal precision (Section 6.3) is supported by Appendix C.9 for Bayesian agents. When applied to non-Bayesian LLM agents, this property may not transfer; a brief discussion would be helpful.

## Removed Points

- **Notation nitpick about β(p)**: The harsh critic noted "β(p) = 0, p ∈ [0.5, 1)" as confusing and suggested an alternative. The reviewer's suggested fix (β(q) = 0 for q ∈ [0.5, p]) actually changes the meaning of the cost function and is incorrect. Removed as an erroneous suggestion.
- **"First formal model" claim softened by prior works**: The harsh critic noted that the "first formal model" claim is softened by Wei & Anastasopoulos (2022) and Smith et al. (2021). The paper explicitly distinguishes itself from these works in Section 2 on reasonable grounds (no two-way communication, agents retain action control). The scope of the claim is appropriate. Removed.
- **Strength about "significance of the problem"**: Generic praise that could apply to many papers. Removed.
- **Strength about "empirical approach" being "genuinely creative"**: The empirical approach conflicts with verified weaknesses about its lack of rigor. Per rules, when a weakness and strength disagree, the weakness wins. However, the *approach* (three-role architecture) is indeed novel, and this is already captured in Strengths item 3. The praise here was somewhat generic. Kept in spirit but reframed.

## Novel Insights

The harsh critic's most valuable observation is the gap between two competing interpretations of the LLM planner's deviations: the paper simultaneously attributes the same policy patterns to "central tendency bias" (point 1) and to "strategic adaptation to non-Bayesian agents" (points 2 and 3) without providing experimental controls to distinguish them. This is a genuinely useful observation because it identifies a concrete, fixable design flaw — a control condition with Bayesian agents — rather than a vague call for "more rigor." The critic also correctly identifies that the "brittleness" claim rests on an asymmetric comparison that essentially proves misspecification degrades performance, which is true of any misspecified model and not a distinctive finding about the paper's optimal policy.

## Suggestions

1. **Report the specific LLM model, number of runs, and include error bars or variance measures** on all quantitative results. This is the single highest-leverage improvement — it would transform the empirical section from suggestive illustrations into credible evidence.
2. **Run a control experiment where the LLM planner faces Bayesian (simulated) agents** to directly test whether the observed policy deviations are adaptations to non-Bayesian behavior or artifacts of the LLM's own biases/limitations.
3. **Temper the causal language** in Section 6.2 when describing LLM planner deviations. Replace "direct response to" and "reflects an understanding that" with more neutral language such as "consistent with" or "could be explained by."
4. **Add a table of experimental parameters** (values of \(k\), \(p\), \(\delta\) tested) to the main text.
5. **Add a symmetric misspecification test** evaluating LLM policy on Bayesian agents for completeness.

## Score and Decision

The paper's core contribution is the theoretical framework: a well-posed model, a non-trivial convexity proof, and substantive characterizations of optimal policies for both altruistic and biased planners. This theoretical contribution is novel, rigorous, and significant. The empirical section adds a creative methodological idea but is presented with insufficient rigor to support its stronger claims, and the causal attributions in particular are unsupported.

The theory alone merits acceptance; the empirical issues are resolvable through improved reporting and tempered claims, not through a fundamentally flawed approach. On balance, this is a borderline accept.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>