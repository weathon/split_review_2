## Summary

This paper introduces a formal model of controlled sequential social learning, where a planner (e.g., an LLM) strategically chooses the precision of private signals for a sequence of agents who also learn from each other’s actions. The authors characterize optimal policies for an altruistic planner (maximizing social welfare) and a biased planner (inducing a specific action), proving convexity of the value function and identifying distinct policy regimes. LLM-based simulations show emergent strategic behavior that broadly aligns with the theoretical predictions, while also adapting to non-Bayesian agent behavior.

## Strengths

- **Novel integration of control and social learning.** The paper is the first to formulate a dynamic control problem where a planner’s precision choices interact with sequential social learning among agents. This combination is timely and important given the increasing deployment of algorithmic mediators.
- **Rigorous theoretical characterization.** The proof that the altruistic value function is convex (Theorem 2) is nontrivial and forms the basis for the optimal policy structure. The characterizations for both altruistic and biased planners (Theorems 3, 5) reveal intuitive but non-obvious regimes (e.g., where a biased planner intentionally obfuscates signals or where no optimal policy exists and ε-optimal policies are needed).
- **Empirical validation with LLMs.** The simulations using LLMs as both planner and agents provide a concrete test of the theoretical framework. The demonstration that LLM planners adopt policies structurally similar to the analytical optimum—while also deviating in ways that account for non-Bayesian agent biases—suggests the model captures realistic strategic behavior.
- **Clear exposition of real-world relevance.** The paper motivates the model with concrete examples (recommendation systems, political campaigns) and discusses the societal implications of algorithmic information mediation, including the potential for significant welfare decreases even under transparency constraints.

## Weaknesses

### Fatal
- None.

### Major

- **Insufficient empirical rigor.** The main text does not specify which LLM model was used, the number of simulation runs, or any measures of variability (confidence intervals, standard deviations). Figures 1b and 2 appear to show single trajectories or aggregate statistics without quantifying uncertainty. The claims about policy deviation magnitudes and welfare changes lack statistical grounding, making it difficult to assess the reliability of the empirical conclusions.
- **Lack of detail about experimental setup.** The prompts for the planner, agent, and oracle are relegated to the appendix (stripped), and the main text provides only a high-level description. Important operational details—how the LLM agent updates its belief, how the oracle generates a signal of a given precision, how cost functions are implemented—are not described sufficiently to reproduce the experiments. While the missing appendix is a parsing artifact, the main text should still contain enough information to understand the methodology; it does not.

### Minor

- **The planner’s control is highly stylized.** The model assumes binary state, binary symmetric signals, and that the planner can only vary precision (not content or framing). While the paper acknowledges these assumptions (Remark 2), it does not discuss how well they capture real LLM mediators that can tailor content in richer ways. The claim that the planner operates under “stringent transparency constraints” is accurate, but the gap between the model and actual LLM capabilities weakens the direct policy implications drawn.
- **Thresholds are characterized but not computed.** The optimal policies are described in terms of thresholds (e.g., \(d_A, t_A, t_1, t_2\)) whose existence is proven but whose values depend on cost functions and are not given in closed form. The paper could briefly discuss how to compute these thresholds numerically or under special cost structures.

### Trivial
- The title emphasizes “LLM-based control,” but the theoretical framework is general and not LLM-specific; the LLM connection is primarily in the simulation section. This is a minor discrepancy that may mislead readers about the paper’s scope.

## Nice-to-Haves

- A table summarizing the three phases of optimal altruistic policy (no investment, maximum investment, intermediate investment) with the exact belief ranges for a concrete numerical example would improve intuition.
- Including error bars or multiple random seeds in the LLM simulations would greatly strengthen the empirical claims.
- A brief discussion of how the MDP can be solved numerically (e.g., discretized belief grid, value iteration) would enhance practical usability.

## Novel Insights

Beyond the paper’s own contributions, the key insight is that even a planner with severely restricted control (only precision of a binary symmetric signal, no lying, public information parity) can substantially influence social welfare in either direction. The policy regimes—especially the biased planner’s deliberate reduction of precision near unfavorable beliefs, and the absence of an optimal policy (only ε-optimal) in some belief ranges—reveal that the subtlety of control in social-learning settings goes beyond classic Bayesian persuasion or information design. The LLM simulations further suggest that modern language models may naturally learn these strategic trade-offs, which is both a capability and a risk.

## Suggestions

- In the main text, specify the LLM model used in the simulations (e.g., GPT-4, Claude, Gemini) and report the number of runs or seeds. Add confidence intervals or standard errors to Figures 1b and 2.
- Provide a pseudocode or algorithmic description of how the oracle generates signals of a given precision and how the LLM agent updates its belief, so that the experimental method is self-contained.
- Discuss the computational feasibility of computing the optimal policy for a continuous belief state (e.g., via discretization or function approximation), and whether the threshold structure can be exploited algorithmically.

## Score and Decision

**Score: 6** – This is a borderline accept. The theoretical contributions are original, sound, and relevant to an important real-world problem. The empirical validation, while suggestive, lacks sufficient rigor (unknown LLM, no uncertainty quantification, limited experimental detail). If the authors can address the empirical weaknesses, the paper would be stronger. Overall, the paper brings sufficient value to the community by opening a new line of inquiry at the intersection of social learning, information design, and LLM mediators.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>