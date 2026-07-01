## Summary

This paper validates Goal-Oriented Environment Inference (GOEI), a model-based RL algorithm for minimal state representation, in the competitive card game *Hol’s der Geier*.  The authors show that GOEI reduces the state space to only 2.9% of all possible observations (452 states vs. 15,542) while achieving a reward rate close to the Nash equilibrium.  Through mutual information analysis, they examine which observational features are preserved or lost in the reduced representation, providing insights into the nature of core information for game outcomes.

## Strengths

- **Strong empirical state reduction**: GOEI compresses 15,542 observations to 452 states while maintaining near-Nash performance on a challenging zero-sum game. This 97% reduction is impressive and demonstrates the algorithm’s practical utility beyond the abstract environments of the original GOEI paper.
- **Clear experimental design**: The separation of environment inference and strategy optimization allows direct evaluation of the learned model’s quality independent of exploration-exploitation trade-offs. The training and testing against a fixed NE opponent provides a clean benchmark.
- **Informative feature-level analysis**: Figure 3’s mutual information decomposition across the five observational features (SD, CT, AH, OH, RT) offers concrete, interpretable evidence about what information is preserved (e.g., CT and RT in early rounds, SD in later rounds) and what is discarded (AH, OH). This lends support to the claim that GOEI extracts complex composite representations.

## Weaknesses

### Fatal
None.

### Major
- **No statistical test for “equivalence” to Nash equilibrium**: The best GOEI run achieves a median reward rate of -0.010. The paper states this is “indistinguishable from the optimal one (≃0),” but provides no hypothesis test, confidence interval, or error bar relative to the exact NE reward rate (0). Given quartiles of [-0.012, -0.009], the difference may be statistically significant. Without a proper test, the claim of near-optimality is unsubstantiated.
- **Limited baseline comparison**: Only Q-learning is compared. The paper would be much stronger by including other state abstraction methods (e.g., bisimulation metrics, MDP homomorphisms, or even a hand-crafted feature reduction) and alternative model-based approaches (e.g., a small Dreamer-style latent model). Without these, it is hard to assess whether GOEI’s advantage is due to the specific reduction method or merely to having any learned abstraction at all.
- **Training/evaluation gap**: GOEI is trained on games between *fixed* Rand and NE strategies, then evaluated against NE. This bypasses the interactive, online setting where the agent’s own policy changes the data distribution. The paper acknowledges this as a limitation, but the problem is central to the claim of practical usefulness—many model-based methods degrade significantly when model learning and policy optimization interact. The contribution is thus weakened without a demonstration in the online scenario.

### Minor
- **Incremental contribution**: The GOEI algorithm is unchanged from Takahashi et al. (2024). The novelty is entirely in the application to a more realistic domain. While the results are strong, the paper is primarily a validation study rather than a methodological advance. The ICLR community may expect more technical novelty.
- **No code or reproducible details**: The NE strategy computation (used to define the “optimal” baseline) is not described in sufficient detail, nor is the training data generation procedure (how the 200 games per epoch from Rand vs. NE are drawn). Without code or full specifications, the experiments are hard to reproduce.
- **Mutual information analysis is univariate**: Figure 3 treats each feature independently, but the paper’s own conclusion is that “required information is maintained in complex combinations.” The analysis does not attempt to measure higher-order interactions or the combinatorial structure of the learned states, so the claim remains qualitative.

### Trivial
None.

## Nice-to-Haves

- Include a statistical test (e.g., bootstrap confidence interval on the reward rate difference from zero) to rigorously support the “near-optimal” claim.
- Release code and training logs to facilitate reproduction.
- Add a comparison with a deep model-based RL algorithm (e.g., a small Dreamer or a tabular world model with learned latent states) to put GOEI’s performance in the context of modern methods.
- Extend the experiment with at least a single online-learning scenario (e.g., GOEI learns by playing against itself or a slowly adapting opponent) to address the interactive limitation.

## Novel Insights

None beyond the paper’s own contributions. The observation that GOEI preserves information about the current table card and remaining table cards while discarding nearly all information about specific hand compositions is interesting, but it is a direct consequence of the game’s structure and the algorithm’s objective (reward prediction). The real insight—that 97% of observed features can be dropped without harming optimal decision-making—is already clearly stated in the paper as its main result.

## Suggestions

- Provide a statistical test (e.g., bootstrapped 95% CI on the reward rate) for the claim that GOEI is indistinguishable from NE.
- Add a baseline that uses the known Nash equilibrium as an abstract model (e.g., a decision tree built from NE action probabilities) to separate the effect of abstraction from the effect of learning.
- Release code and document the exact procedure for computing the Nash equilibrium (the number of states reported as NE’s effective states in Table 1 suggests a specific state aggregation scheme; this should be explained).

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>