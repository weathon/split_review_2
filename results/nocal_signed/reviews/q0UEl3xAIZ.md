Here is the consolidated final review.

---

## Summary

This paper validates Goal-Oriented Environment Inference (GOEI), a model-based Bayesian nonparametric method for state compression, on the competitive card game "Hol's der Geier." Training GOEI offline on 300,000 fixed-policy games (Rand vs. NE) and testing against the Nash equilibrium opponent, the paper reports that GOEI compresses 15,542 possible observations down to 452 states (2.9%) while achieving a reward rate close to zero (the NE value). The paper also provides an information-theoretic analysis of which features survive compression.

## Strengths

- **The 97% state reduction (15,542 → 452 states) is striking and well-demonstrated.** The paper reports concrete numbers across multiple configurations (Table 1), with the best configuration (β=0.2, α=25) compressing to 2.9% while maintaining a reward rate close to the Nash equilibrium value. The state count is even lower than the NE strategy's own representation at rounds 2 and 3 (Figure 2B), which is noteworthy.

- **The game choice (Hol's der Geier) is well-motivated.** It is a non-trivial competitive game with a known Nash equilibrium structure, a large observation space (15,542 states), and well-understood simple strategies (π₀–π₄). This allows the paper to ground performance claims against both an optimal baseline (NE) and human-interpretable heuristics, which is more informative than a typical "beats baseline X" RL evaluation.

- **The information-theoretic feature analysis (Figure 3) is a genuine diagnostic attempt.** The finding that CT and RT information is relatively more preserved in early rounds while SD becomes important only at round 4 is coherent with game logic and provides partial sanity-check evidence that the compression is not arbitrary.

## Weaknesses

### Fatal
None.

### Major

- **Offline-only evaluation vs. online framing.** The paper motivates GOEI in terms of online learning and adaptation ("GOEI has the potential to efficiently learn online," line 17) but evaluates it exclusively in an offline setting where the agent trains on fixed-strategy games (Rand vs. NE) and never experiences distribution shift from its own improving policy. The evaluation setup is explicitly designed to isolate environment inference from strategy optimization (Section 3.3), which is a valid scientific choice — but the abstract and introduction state the results without this qualification ("it achieves a nearly optimal strategy," Abstract). The paper honestly acknowledges this gap in the discussion (lines 236–238), but the motivating narrative substantially oversells what is actually shown. A reader cannot conclude from this paper whether GOEI works in interactive settings where the agent's own improving strategy changes the data distribution.

- **Weak baseline comparison.** The only model-free RL baseline is tabular Q-learning, which the paper itself notes cannot handle the state space size (line 182). This comparison shows that an intentionally underpowered method does poorly, but it does not establish that GOEI's specific approach to state reduction is advantageous over alternatives. More informative baselines — Q-learning with linear function approximation, a small neural network, or simpler state aggregation methods — are absent. Without these, the reader cannot distinguish whether the advantage is specific to GOEI's Bayesian nonparametric compression or would accrue to any method that reduces the state space.

### Minor

- **The "indistinguishable" claim lacks statistical support.** The best GOEI configuration achieves a median reward rate of −0.010 (IQR: −0.012, −0.009) averaged across epochs 1–3,000 (Table 1). The paper says the performance at epoch 3,000 is "≃ 0" and "indistinguishable" (line 228) but provides no statistical test (e.g., a confidence interval or significance test against zero). The entire interquartile range lies strictly below zero, suggesting a systematic small negative bias. Whether −0.010 is practically "close enough" to zero is a reasonable judgment call, but the claim of indistinguishability needs precise characterization rather than hand-waving.

- **The mutual information analysis has an unresolved tension.** Figure 3 shows that most information about each individual feature (AH, OH, SD, CT, RT) is lost through compression. The paper then asserts that the required information is "maintained in complex combinations of all the features" (line 200), but provides no direct evidence for combinatorial encoding. If the compressed states cannot be mapped back to interpretable features and their meaning cannot be concretely described, then state reduction alone has not delivered the explainability the paper motivates. This is acknowledged as a limitation in the discussion (line 238), but it undercuts the paper's framing as an interpretability advance.

- **The GOEI method description (Section 3.2) is brief.** The key mechanism — reversing the causal inference direction via Bayes theory — is stated in one sentence without explanation of why this resolves the described model conflict. The variational inference procedure is referenced but not explained. For readers unfamiliar with Takahashi et al. (2024), it is difficult to assess whether the implementation is correct or whether the method is appropriately applied.

### Trivial

- **No computational cost analysis.** The paper mentions using an RTX 4080 SUPER with 12GB but reports no runtime, memory usage, or scaling behavior — an odd omission for a method whose advertised advantage includes reducing memory burden.

## Nice-to-Haves

- Test GOEI in a partially interactive setting: train offline on Rand-vs-NE data, then let the inferred policy continue learning online against the NE opponent to examine whether the inference survives distribution shift.
- Analyze what the learned states represent concretely for a small number of example observations (which observations map to the same state and why), which would strengthen the interpretability claim.
- Calibrate the performance claim precisely: report the reward rate at epoch 3,000 separately (not only averaged across all epochs), and provide a confidence interval or statistical test comparing it to zero.
- Ablate the contribution of the Dirichlet process prior vs. a simpler fixed-capacity state aggregation method.

## Removed Points
These points were flagged by the input review but are removed or demoted for the following reasons:

- **"Introduction over-promises"** — This merges with the offline/online gap weakness already listed above; it is not a separate issue.
- **"Q-learning comparison is about asymptotic performance, not speed"** — The paper claims GOEI "rapidly learns" and the learning curves appear to support this (GOEI reaches its plateau before Q-learning). The characterization mildly misreads the paper.
- **"High variance in learning curves not discussed"** — The paper reports medians and quartiles across 21 seeds, which is appropriate. The claim that curves "look noisy" is subjective, not a concrete technical weakness.
- **"Warm-start experiment not included"** — This is a nice-to-have extension, not a flaw in the current paper. The paper acknowledges this as future work.
- **"GOEI description too methodologically thin for ICLR"** — The paper's contribution is the application and validation in a new domain, not the algorithm itself. The level of detail is reasonable for a methods-applied paper that references the original work.

## Novel Insights
None beyond the paper's own contributions. The input review's primary novel observation is that the gap between the online-learning framing and the offline-only evaluation is larger than the paper acknowledges — which is already reflected in the Major weaknesses above.

## Suggestions

1. Add at least one stronger baseline — e.g., Q-learning with linear function approximation or a small neural network — to clarify whether the advantage is specific to GOEI's compression or generic to state reduction.
2. Provide a statistical test (confidence interval or bootstrap test) for whether the GOEI reward rate at the final epoch differs from zero.
3. Most importantly, test GOEI in a partially interactive setting (offline pretrain → online continued learning) to directly address the acknowledged limitation.

---

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>