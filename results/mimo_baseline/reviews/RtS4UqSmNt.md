## Summary
This paper introduces a novel framework for controlled sequential social learning, where an information-mediating planner (e.g., an LLM) dynamically chooses the precision of private signals for a sequence of Bayesian agents who also learn from observing predecessors' actions. The paper characterizes optimal policies for both altruistic and biased planners, proves convexity of the value function, and validates the theoretical predictions through LLM-based simulations where LLMs serve as both planner and agents.

## Strengths
- **Novel and well-motivated framework.** The paper convincingly combines dynamic information control with sequential social learning, filling a genuine gap between the information design and social learning literatures. The positioning relative to prior work (Wei & Anastasopoulos, 2022; Smith et al., 2021; Arieli et al., 2022; Wu et al., 2025) is clear and the distinctions are substantive—no two-way communication, agents retain action control, and the planner makes dynamic (not one-shot) precision choices.

- **Rigorous and non-trivial theoretical results.** The convexity proof of the altruistic value function (Theorem 2) is described as novel and technically challenging due to the dependence of agent actions on the public belief. The full characterization of optimal policies for both planner types (Theorems 1–5) reveals rich structure: the altruistic policy has three distinct phases, and the biased policy has five phases including intentional signal obfuscation—a counterintuitive and interesting finding. The existence of regions where the biased planner deliberately decreases precision below baseline to prevent unfavorable signal realizations is a genuinely insightful result.

- **Thoughtful LLM-based empirical validation.** The three-role simulation design (Planner, Agent, Oracle) is clean and well-structured. The paper identifies specific non-Bayesian behaviors in LLM agents (underreaction to confirming signals, overreaction to disconfirming signals) that mirror documented human cognitive biases, and demonstrates that the LLM planner's emergent strategy adapts to these biases while remaining structurally close to the Bayesian-optimal policy. The comparison across analytical, LLM, and hybrid settings (Figure 2c) provides meaningful insight into the cost of model misspecification.

- **Clear practical relevance.** The paper directly addresses a pressing real-world concern: LLMs deployed as information mediators at scale can significantly influence social welfare, even under stringent transparency constraints. The finding that a biased planner can decrease social welfare by 40–50% is striking and policy-relevant.

## Weaknesses
### Fatal
None.

### Major
- **Highly restrictive model assumptions.** The model assumes a binary state space, binary symmetric signals, 0-1 loss, and full observability of the planner's precision choices. While the paper acknowledges these limitations, the gap to realistic settings is substantial. The paper conjectures that qualitative results will generalize but provides no partial results toward this. The convexity result (Theorem 2), which is foundational for the entire analysis, is noted to be the main obstacle for generalization to richer signal structures—this is a significant limitation for a paper whose primary contribution is theoretical.

- **Limited experimental scope.** The LLM experiments use a single scenario (car buying), and the paper does not clearly specify which LLM model(s) are used (this may be a parsing issue). The welfare analysis in Section 6.3 is based on a single parameter configuration with the true state fixed to B. The robustness of the findings across different scenarios, model families, and parameter settings is not established. The claim that LLM planners exhibit "emergent strategic behavior" that "broadly mirrors" theoretical predictions is supported by one example policy (Figure 2a) and a histogram of deviations (Figure 2b), but a more systematic comparison across parameter sweeps would strengthen the claims considerably.

### Minor
- **The oracle design introduces a confound.** The Oracle generates tailored messages of desired precision, but the mapping from precision to message content is itself an LLM generation process with its own biases. The paper validates the oracle in Appendix E.3, but the interaction between oracle biases and agent non-Bayesian reasoning could create artifacts that are difficult to disentangle from the phenomena of interest.

- **The biased planner's non-existence result (Theorem 4(D), Theorem 5(E))** is handled via ε-optimal policies, which is standard but means the optimal policy is not well-defined in certain belief regions. The practical implications of this for the LLM simulation are not discussed.

### Trivial
None.

## Nice-to-Haves
- A sensitivity analysis of the LLM planner's policy across different cost parameters and discount factors would substantially strengthen the empirical claims.
- Discussion of how the framework could be extended to settings where the planner has richer information than agents (violating Assumption 1 in Remark 2), as this is common in practice.
- Analysis of whether the non-Bayesian behaviors identified in LLM agents are stable across different prompt framings and model versions.

## Novel Insights
The paper's most novel insight is that a biased information mediator operating under strict transparency constraints (no lying, no cherry-picking, full observability) can still dramatically shift social welfare by strategically modulating signal precision. The characterization reveals that the optimal biased planner operates in qualitatively different regimes depending on the public belief—sometimes investing heavily to escape unfavorable cascades, sometimes deliberately obfuscating signals to prevent unfavorable private information from reaching agents, and sometimes free-riding on favorable public opinion. This nuanced strategic landscape, combined with the finding that LLM planners naturally discover strategies approximating these theoretically optimal policies even when facing non-Bayesian agents, provides a compelling and somewhat alarming picture of the power of algorithmic information mediation.

## Suggestions
- Expand the experimental evaluation to include multiple LLM families (e.g., GPT-4, Claude, Llama) and multiple scenario types to assess generalizability.
- Provide a more systematic parameter sweep in the welfare analysis rather than a single configuration.
- Consider adding a brief discussion of potential regulatory mechanisms or alignment strategies that could mitigate the welfare losses from biased planners, as this is raised as a future direction but could be foreshadowed with preliminary analysis.

## Score and Decision
The paper makes a genuine and novel theoretical contribution by introducing a well-motivated model of controlled social learning and providing rigorous characterizations of optimal policies. The convexity proof and the multi-phase policy structure for the biased planner are non-trivial results. The LLM experiments, while limited in scope, provide meaningful validation and reveal interesting emergent behavior. The main limitations are the restrictive model assumptions and the limited experimental breadth, but these are acknowledged and do not invalidate the core contributions. The paper is timely, well-written, and opens a new research direction at the intersection of information design, social learning, and AI safety.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: Accept