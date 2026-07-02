## Summary

This paper applies Goal-Oriented Environment Inference (GOEI) — a variational Bayesian method that compresses observations into minimal "core" states sufficient for reward prediction — to the two-player competitive card game Hol's der Geier. The primary empirical finding is that GOEI reduces 15,542 distinct observations (from games between a random player and a Nash equilibrium player) into 452 states (2.9%) while the policy derived from the compressed model achieves near-Nash-equilibrium performance against the NE opponent. A mutual information analysis shows which observation features are preferentially preserved across game rounds.

---

## Strengths

1. **Impressive state compression with near-optimal performance.** GOEI reduces observations to 2.9% of the original count (452 vs. 15,542 states) while the resulting policy achieves a reward rate near zero (indistinguishable from NE vs. NE) against a fixed NE opponent (Table 1, best hyperparameters β=0.2, α=25). This goes well beyond the abstract grid-world validation of Takahashi et al. (2024) and demonstrates that the method scales to a non-trivial competitive game.

2. **Mutual information analysis provides interpretability of what is preserved.** The analysis in Section 4.2 (Figure 3) shows that information about the current table card (CT) and remaining table cards (RT) is preferentially retained in early rounds, while score difference (SD) information emerges only at round 4. This pattern coheres with game-theoretic intuition about when each feature matters and gives concrete insight into what the compressed representation captures — far more than typical state-compression work.

3. **Methodologically careful evaluation design.** Training uses 21 seeds with median/quartile reporting, separates the environment-inference phase from the performance-test phase (Section 3.3, line 128), and tests against a well-defined optimal baseline (NE). The paper is transparent about its training protocol and acknowledges limitations.

---

## Weaknesses

### Fatal

None.

### Major

1. **The training protocol evaluates offline compression on expert data, not online RL as the framing suggests.** The paper motivates GOEI with the challenge of online learning (introduction: "much room for improvement in tasks that require online learning," "potential to efficiently learn online"). However, experiments train GOEI on 300,000 pre-generated games of Rand vs. NE (Section 3.3, lines 128–130), where the opponent's fixed NE strategy is part of the training data. The learned transition model captures dynamics under the assumption that the opponent plays NE. What the paper demonstrates is that GOEI can compress expert-play data offline and derive a near-optimal policy for playing against that same fixed opponent. This is a valid and interesting finding, but the experiments never evaluate the online setting that motivates the work. The paper acknowledges this only in the final paragraph of the Discussion (lines 236–237: "The effectiveness of the GOEI function in interactive learning should be further confirmed") as a minor future direction, when it is a central scope limitation that should be elevated to a front-and-center caveat.

2. **No evaluation of whether compressed states generalize across opponents.** Because training data comes exclusively from Rand vs. NE games, all results are conditioned on the opponent playing NE. The paper does not test whether the compressed model or derived policy works against a different opponent (e.g., the heuristic strategies π_k or a mixed-strategy opponent). Without this experiment, it is unclear whether GOEI finds genuinely useful structure of the game or merely overfits to the specific opponent's strategy. This is the single most informative missing experiment.

### Minor

3. **The Q-learning baseline is not informative.** Tabular Q-learning is trained on the same pre-generated offline data (Rand vs. NE games) rather than through online interaction. The paper concludes that "the poor performance of Q-learning indicates that the number of observations is too large even for the simple Q-learning algorithm" (line 182). This is a known limitation of tabular methods on ~15K states; a neural-network-based function approximator could handle the full state space. The comparison is staged in a way that makes GOEI look better than an apples-to-apples benchmark would, and it does not provide meaningful evidence that state reduction is necessary.

4. **The NE state count comparison is not apples-to-apples.** The paper reports that GOEI has fewer states than NE at rounds 2 and 3 (Table 1, Fig. 2B) and highlights this as noteworthy. However, NE states are computed by grouping observations with equal expected reward under the NE strategy (lines 142–174), while GOEI groups observations by shared transition dynamics. These are different formalisms with no reason to align, and the comparison does not establish that GOEI's representation is more efficient. At round 4, GOEI has 408 states vs. NE's 69, which is not discussed.

5. **The abstract's "all possible observations (15,542)" is slightly misleading without context.** The full observation space is 28,477 (line 38); the 15,542 figure is the subset reachable under Rand vs. NE play (line 134). The paper clarifies this in Section 3.3, but the abstract could mislead a casual reader about what is being compressed.

### Trivial

None that survive filtering (the above minor points capture the substantive issues).

---

## Nice-to-Haves

- **Evaluate against other opponents.** The most informative extension is to train GOEI on Rand vs. NE data and then test the derived policy against heuristic opponents π_k, Rand, or a mixed strategy. If the compressed states generalize, this would be strong evidence GOEI finds genuinely useful structure. If the policy fails against different opponents, that honestly clarifies the limitation.
- **Replace or supplement the Q-learning baseline** with a comparison to a simple aggregation baseline (e.g., merging states with identical feature values modulo one feature) or to a deep-RL method (DQN) on the full observation space to demonstrate that state reduction offers a benefit over function approximation.
- **Ablate the effect of expert data.** Train GOEI on Rand vs. Rand games instead of Rand vs. NE to test whether the compression depends on seeing optimal play or is a property of the environment structure itself.
- **Report final-epoch performance separately** rather than averaging across all 3,000 epochs (which includes early learning), to give a cleaner picture of convergence.

---

## Removed Points

These points were flagged in the harsh review but are removed after verification against the paper; they should be treated with caution:

- **"The reduced states are not actually evaluated as 'core' states (Critical Issue 3)"** — The paper assumes (Section 3.1, lines 56–57) that the opponent depends only on the current observation, making the opponent part of a stationary Markovian environment. Under this clearly stated assumption, the core states defined by Eq. (4) are valid for the evaluated setting. The criticism that states are core "relative to a particular opponent" reflects the paper's explicit scope rather than a hidden flaw. The generalization concern is real (see Major weakness #2 above), but the theoretical concept is correctly applied as scoped.

- **"Section 4.2 confusion about AH/OH"** — The critic claims a contradiction between "AH and OH were almost completely reduced" and "these pieces of information are likely to be crucial." The paper immediately resolves this: "the required information is maintained in complex combinations of all the features" (line 200). Individual feature information is lost but preserved in a distributed encoding across features. This is coherent, not a non-sequitur.

- **"Introduction over-promises on explainability"** — The paper mentions explainability as motivation but explicitly acknowledges in the Discussion (line 238) that "we could not give a verbal explanation of the reduced state representation more concretely than Figure 3." This is an honest limitation statement, not an over-promise.

- **Generic framing critiques (e.g., "closer to offline inverse reinforcement learning or behavioral cloning")** — GOEI learns a transition model and derives a policy through the Bellman equation; it does not clone behavior. The characterization is inaccurate.

- **"The NE state count comparison is apples-to-oranges" framed as a Major weakness** — Demoted to Minor (#4) because the comparison is a secondary observation, not a core claim, and the paper does not draw strong conclusions from it.

---

## Novel Insights

The harsh review highlights a genuine and important observation that goes beyond the paper's own framing: the core empirical finding — offline compression of game dynamics from optimal-play data to 2.9% of the observation space while retaining near-NE performance against the same fixed opponent — is interesting in its own right and does not need an online RL framing to be valuable. The review correctly identifies that the paper's most impactful result is the sheer compression ratio and the mutual information analysis, not the (untested) online learning claim. The missing generalization experiment is the key question that would make the difference between a solid empirical report and a genuinely impactful contribution.

---

## Suggestions

1. Reframe the contribution honestly: the paper demonstrates offline state compression from optimal-play data, not online RL. Adjust the title, abstract, and introduction to match.
2. At minimum, test the derived policy against one non-NE opponent (e.g., π_0 or Rand) to probe whether the compressed states generalize.
3. Replace or supplement the Q-learning baseline with a more meaningful comparison (simple aggregation baseline or deep-RL baseline).
4. Elevate the interactive-learning limitation from a buried discussion paragraph to a clearly stated caveat in the abstract or introduction.

---

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>