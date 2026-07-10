Here is the final consolidated review:

---

## Summary

This paper applies Goal-Oriented Environment Inference (GOEI), a variational-Bayesian state-reduction method, to the competitive card game "Hol's der Geier." It reports that GOEI compresses 15,542 possible observations down to 452 representative states (2.9%) while achieving near-Nash-equilibrium performance when trained on games between a random strategy and the Nash equilibrium (NE) strategy and tested against NE. The paper provides mutual information analysis of which features are retained in the compressed states, and is transparent about its limitations.

## Strengths

- **Dramatic and explicitly quantified state compression.** GOEI compresses 15,542 possible observations down to 452 representative states (2.9% of raw observations, and ~35.7% of the NE strategy's own 1,266 states) while retaining information sufficient for near-NE-level play. The compression is documented per round with medians and quartiles over 21 seeds (Table 1, Figure 2B).

- **Principled evaluation via known Nash equilibrium.** Hol's der Geier has a computable Nash equilibrium, providing a ground-truth optimal reward rate (~0). This gives the paper an absolute reference point rather than relying only on relative comparisons to heuristic baselines.

- **Mutual information analysis (Figure 3) provides insight into what the reduced states encode.** The stacked-bar analysis of mutual information per feature (SD, CT, AH, OH, RT) reveals, e.g., that score difference becomes relevant only at round 4, while agent/opponent hand cards are almost entirely discarded. This goes beyond a simple "our method works" claim.

- **Honest limitations section.** The paper clearly acknowledges (Section 5) the gap between its separated-training protocol and interactive online learning, and explicitly notes that state reduction does not automatically yield verbal explainability.

## Weaknesses

### Fatal
None.

### Major

- **Training protocol provides privileged access to the NE strategy.** The agent is trained on data from games between Rand and NE, meaning it observes the NE strategy's actions during training and learns transition dynamics of a world in which the opponent plays NE. The headline claim ("achieves a nearly optimal strategy equivalent to the Nash equilibrium") suggests more autonomy than the experiment actually tests. The paper acknowledges this in the Discussion but the framing in the Abstract and Introduction could mislead readers about what was demonstrated. The experiment shows that GOEI can learn accurate transition dynamics from data that includes the optimal opponent; it does not show that GOEI would converge to NE from scratch without observing NE during training.

### Minor

- **No comparison against other state-abstraction methods.** The paper compares GOEI against Q-learning (no abstraction) and simple heuristic strategies, but not against any other explicit state-abstraction method (e.g., bisimulation metrics, information-bottleneck approaches, aggregation methods from Li et al. 2006). Without such comparisons, it is unclear whether GOEI's compression is uniquely effective or whether any reasonable abstraction method would perform similarly on this game.

- **The Q-learning comparison is in a regime that disadvantages Q-learning.** Q-learning is applied on a fixed offline dataset with a greedy test policy — essentially batch RL without off-policy corrections. GOEI, being model-based and designed for batch transition modeling, is naturally suited to this regime. A model-based baseline without state reduction would better isolate the effect of state reduction.

- **The 2.9% compression figure could be better contextualized.** The abstract touts "only 2.9% (452 states) of all possible observations (15,542)." While arithmetically correct, a more informative comparison is against the NE's own state count of 1,266 (a 64% reduction, not 97.1%). The paper does provide this comparison in Table 1 and Figure 2B, but not in the abstract or discussion.

- **Reward rate averaged across all 3,000 epochs (not just converged).** Averaging across epochs 1–3,000 includes early poor performance, depressing the reported numbers relative to the agent's eventual steady state (visible in Figure 2A). This also makes comparisons to fixed strategies (Rand, π₀) apples-to-oranges, since those are static.

- **The NE state count derivation is vague.** The paper says NE states are defined by "a set of equal expected rewards earned with players' actions" (lines 142–147) but offers no clear explanation of how the 1,266 figure is computed.

### Trivial

- **The Abstract/Introduction sets explainability expectations not fully delivered.** The Introduction frames the paper around XAI and explainability, but the paper never assigns semantic labels to reduced states. The Discussion acknowledges this limitation, but the framing over-promises.

## Nice-to-Haves

- Retrain GOEI on data without NE in the training set (e.g., Rand vs. Rand) and test against NE, to verify that the method does not require observing the optimal opponent to learn useful structure.
- Report reward rates averaged over the final N converged epochs rather than across all 3,000 epochs.
- Include at least one alternative state-abstraction baseline to contextualize GOEI's compression efficiency.

## Removed Points

These points were raised in the input review but are not included as weaknesses in the main review (with justifications):

- *The 28,477 vs 15,542 observation count distinction is "buried":* The paper clearly explains both numbers in context (line 38 vs line 134). The critic's reading is not supported by the paper.
- *Markov assumption about opponent is a restriction:* The critic called this assumption "reasonable." It is not a genuine weakness.
- *Mutual information analysis concern about feature conjunctions:* The paper itself acknowledges that "the required information is maintained in complex combinations of all the features." The concern is already addressed.
- *Memory burden claim is qualitative:* The implied baseline is the full 15,542-observation space, which makes the comparison clear enough.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Retrain GOEI on data without NE (e.g., Rand vs. Rand or Rand vs. heuristic) and test against NE. This single experiment would most directly address the largest weakness.
2. Report converged performance (e.g., average over last 500 epochs) alongside the full-average metric.
3. Include at least one alternative state-abstraction baseline to contextualize whether GOEI's specific mechanism yields unique benefits.

## Score and Decision

### Calibration Anchors

| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| Compositional World Models | EHmjRIA4l2 | 3.00 | R1 | Yes | Lacks fair baselines and experiments don't demonstrate need for abstraction — paper under review is clearly stronger |
| Stochastic Safe Action Model Learning | 5AbtYdHlr3 | 3.00 | R1 | Yes | No experiments — paper under review stronger |
| Reflect-then-Plan | 6jr94SCjH6 | 4.60 | R2 | Yes | Similar missing-baseline and comparison issues; comparable quality |
| Learning Abstract World Models | czpx02orl7 | 4.75 | R1 | Yes | Similar missing-baseline and comparison issues; paper under review has cleaner NE evaluation |
| Offline Equilibrium Finding | Re5iu0hBTs | 4.25 | R2 | Yes | Similar offline game-theoretic setting; paper under review has cleaner evaluation |
| State Combinatorial Generalization | PH7ja3T0vN | 4.50 | R1 | No | Different focus |
| Optimal Action Abstraction | 7J0NsFXnFd | 5.25 | R2 | Yes | Stronger empirical results on complex benchmark (poker beats SOTA) — paper under review is below this |
| Improving Sample Efficiency Zero-Sum Games | x36mCqVHnk | 5.50 | R2 | No | Stronger theory paper, different focus |
| Bayesian Offline-to-Online RL | opZTBFnX2G | 5.75 | R2 | No | Different focus |
| Toward Optimal Policy Population Growth | J2TZgj3Tac | 6.00 | R2 | No | Stronger theory paper |
| Learning Imperfect Info Extensive-form Games | iOAcVOHvEN | 6.00 | R2 | No | Stronger theory paper |

### Calibration Reasoning

**Round 1 bracket (4.0–6.0):** The paper sits clearly above the 3.00-score anchors (Compositional World Models, Stochastic Safe Action Model Learning) which lack fair baselines or have no experiments. It is comparable to the 4.60–4.75 anchors (Reflect-then-Plan, Learning Abstract World Models) which share similar missing-baseline concerns, but this paper benefits from a ground-truth NE evaluation providing an absolute reference point. It sits below the 5.25 anchor (Optimal Action Abstraction) which demonstrates SOTA performance on a complex benchmark.

**Round 2 narrowing:** Comparing itemized favorability ratings against the most comparable anchors: this paper's strongest items (compression at 8.79, NE evaluation at 9.30, MI analysis at 8.93) are genuinely strong, comparable to the top items of the 4.60–4.75 anchors. Its weakest items (missing abstraction baselines at -2.20, training protocol at 2.03) are more severe drags, keeping it below clear acceptance. The paper is most similar to the Reflect-then-Plan anchor (4.60) in profile: a solid core contribution alongside notable missing-baseline gaps that prevent the paper from reaching the 6+ level.

**Final placement:** 5.0 — between borderline reject and borderline accept. The paper has real, well-documented contributions (compression, NE evaluation, MI analysis) but significant limitations (training protocol, missing baselines, comparison fairness) that prevent acceptance at the 6+ level.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>