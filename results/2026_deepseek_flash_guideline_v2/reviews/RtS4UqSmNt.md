## Summary

This paper introduces a formal model of controlled sequential social learning, where an information-mediating planner (e.g., an LLM) controls the precision of agents' private signals at a cost, while agents also learn from predecessors' actions. The paper proves convexity of the altruistic value function (Theorem 2) and fully characterizes optimal policies for both altruistic and biased planners (Theorems 3, 5), revealing distinct operational phases including an intentional obfuscation regime for biased planners. The theoretical analysis is complemented by LLM-based simulations showing structural similarity between LLM planner policies and the theoretical optima, alongside identification of non-Bayesian biases in LLM agents.

## Strengths

1. **Non-trivial convexity proof (Theorem 2)**: The paper proves that the altruistic value function is convex in public belief—a result the authors correctly note is non-trivial because agents' actions depend on the belief state, contrasting with settings where linearity follows directly (e.g., Nyarko 1994). This convexity is the mathematical foundation for the subsequent optimal policy characterization.

2. **Full characterization of optimal dynamic policies (Theorems 3, 5)**: Prior work on control of social learning assumes two-way communication (Wei & Anastasopoulos 2022) or directly alters agents' choice rules (Smith et al. 2021), while information design in social learning considers one-shot fixed structures (Arieli et al. 2022; Wu et al. 2025). This paper goes further by characterizing the optimal dynamic per-agent precision policy—revealing distinct phases (no investment, maximum investment, belief-dependent precision) for both altruistic and biased planners—under the stricter constraint that the planner only controls precision, has no informational advantage, and cannot falsify signals. The five-phase biased policy with intentional obfuscation (Theorem 5(E)) is a genuinely novel and interesting result.

3. **Identification of specific non-Bayesian biases in LLM agents (NB1–NB3)**: The paper isolates three systematic cognitive biases in LLM agents (underreaction to prior-consistent signals, overreaction to prior-counter signals, higher cascade thresholds) and shows these mirror known human biases. This provides a useful bridge between the Bayesian theory and the empirical simulation setup.

4. **Clean separation of myopic and dynamic cases**: The paper systematically contrasts myopic (δ=0) and forward-looking planners throughout both the theoretical and empirical sections, making it possible to attribute welfare differences specifically to the planner's accounting of information externalities.

5. **Timely and well-motivated problem framing**: The paper is clearly positioned relative to related work in social learning, information design, online persuasion, and LLM research, with honest discussion of how the model differs from each.

## Weaknesses

### Fatal
None.

### Major

1. **Missing quantitative comparison for the central empirical claim.** The paper claims (Section 6.3) that in the hybrid setting (optimal policy applied to LLM agents), the analytically optimal policy is "brittle" and "its performance suffers," while the LLM planner is "better adjusted to non-Bayesian agents." These are the paper's headline empirical findings. However, the paper never reports the actual utility achieved by the LLM planner versus the optimal policy under the same LLM-agent conditions. Figure 2c shows welfare and expenditure changes as percentages of baseline, but the text provides no specific numerical comparison between the LLM planner's utility and the optimal policy's utility under LLM agents. This is the single comparison that would validate whether the observed policy deviations are beneficial strategic adaptations—without it, the "better adjusted" claim is asserted rather than demonstrated.

2. **Social welfare claims lack statistical rigor.** The paper states (Section 6.3) that biased planners "decreased social welfare by 40 to 50% when misaligned" but reports no confidence intervals, no number of independent simulation runs, no information about random seeds or variance across LLM generations, and no statistical tests. Given that LLM outputs are stochastic and prompt-sensitive, the reader cannot assess whether these are robust effects or artifacts of particular configurations. This is especially important since the 40–50% figure is central to the paper's policy-relevance narrative.

### Minor

1. **Interpretation of structural differences as "strategic adaptation" is not disentangled from generic LLM artifacts.** Section 6.2 identifies three structural differences between LLM and optimal policies and interprets each as a strategic response to specific non-Bayesian biases (NB2, NB3). However, the paper provides no control condition or baseline that would distinguish strategic adaptation from generic LLM biases (e.g., central tendency bias, which the paper acknowledges for the first difference). For example, the claim that gradual investment tapering is "a direct response to the agents' resistance to cascades (NB3)" could equally be a function approximation artifact or prompt sensitivity. A control experiment—for instance, asking the LLM planner to produce policies for Bayesian agents and comparing to the theoretical optimum—would help separate genuine strategic reasoning from artifacts.

2. **Slightly imprecise framing of the myopic case.** Section 4 states that the myopic case (δ=0) "corresponds to disregarding the role of social learning." More precisely, the myopic planner disregards the *future consequences* of social learning; the current agent's action is still shaped by prior social learning. The distinction between ignoring social learning's existence versus ignoring its future value is small but could confuse readers.

### Trivial
None.

## Nice-to-Haves

- Running the LLM planner on a control condition where it produces policies for simulated Bayesian agents (rather than LLM agents) would help distinguish strategic adaptation to non-Bayesian behavior from generic LLM response patterns.
- A direct comparison table reporting LLM planner utility versus optimal policy utility under LLM agents (with variances) would substantially strengthen the empirical contribution.
- Explicitly reporting the number of simulation runs, random seeds, and LLM generation temperature settings for all quantitative results.

## Removed Points

- **"Fundamental disconnect between theoretical and empirical contributions"** (Harsh Critic Point 1): Removed because the paper's claims are more nuanced than the critic suggests. The paper claims *structural similarity* between LLM and optimal policies (which is about qualitative phase structure), not that the optimal policy performs well with non-Bayesian agents. Finding 2 and the "brittle" statement in Section 6.3 are about different objects (policy structure vs. policy performance) and are not contradictory. The legitimate sub-concern about missing performance numbers is already captured in Major weakness #1.

- **"Conflates similarity with validation / LLM planner might be doing pattern-matching"** (Harsh Critic Point 5): Removed because the paper specifies (Section 6) that the planner "observes the history of actions" and selects precision "according to their objective"—it is not given the theory. The details of what information the planner receives (prompts, model parameters) are in the appendix, which is stripped by the parser (per the rules, appendix content exists in the original submission and should not be penalized).

- **"Name the LLM model(s) used"**: Removed because this information is in the appendix (Appendix E), which is stripped by the parser. Per the rules, missing appendix content should not be treated as a weakness.

- **"The paper's central claim that the LLM planner accounts for non-Bayesian agents is unsupported"** (Harsh Critic's stronger framing): Merged into Minor weakness #1 with softened language. The core concern (lack of control distinguishing adaptation from artifact) is valid but the critic's absolute framing was too strong given that the paper's interpretation is presented as plausible rather than proven.

- **Strength Finder's generic strengths about "important problem" and "timely topic"**: Removed as generic/superficial. Only concrete, evidence-grounded strengths are retained.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add the missing quantitative comparison**: Report the actual planner utility (or welfare) achieved by the LLM planner versus the analytically optimal policy when both face LLM agents. If the LLM planner demonstrably outperforms the optimal policy under LLM agents, the "strategic adaptation" narrative becomes evidence-based; if not, the claim should be dialed back.

2. **Report statistical reliability**: For all quantitative welfare results (especially the 40–50% claim), report number of runs, confidence intervals or standard deviations, and the specific LLM configuration(s) used.

3. **Add a control condition**: Run the LLM planner in a setting with simulated Bayesian agents to see whether its policy matches the theoretical optimum when agent behavior matches the model's assumptions. This would help distinguish genuine strategic adaptation from generic LLM response patterns.

4. **Reconsider the framing of the empirical contribution**: The paper currently presents the LLM experiments as a core contribution alongside the theory. Given the gaps identified above, the paper would be more honest (and defensible) if the experiments were framed as an exploratory illustration rather than rigorous validation, while letting the theoretical results stand as the primary contribution.

## Score and Decision

The calibration search was unavailable due to a data access issue. Based on my assessment of the paper's quality relative to ICLR standards:

The theoretical contribution (clean model, non-trivial convexity proof, complete policy characterizations with interpretable phase structures) is genuine and well-executed. The problem is timely and clearly motivated. The empirical work identifies interesting behavioral patterns but falls short of the paper's own claims about validation—the missing quantitative comparison and lack of statistical rigor are meaningful gaps that prevent the empirical section from supporting the weight placed on it.

Taking all factors into account, the paper's theory is strong enough to merit acceptance at a top venue, but the empirical overclaiming is a real issue that should be addressed. The appropriate score reflects a solid borderline accept: the paper makes a real contribution, but one of its three claimed contributions (the empirical validation) is weaker than advertised.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>