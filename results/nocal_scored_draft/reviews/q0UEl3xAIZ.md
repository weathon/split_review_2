Now I have the favorability signals. Let me construct the final review.

---

## Summary

This paper validates Goal-Oriented Environment Inference (GOEI), a Bayesian state-abstraction method, in the competitive card game "Hol's der Geier." GOEI compresses 15,542 observations into 452 states (2.9%) while achieving a near-optimal reward rate of −0.010 against the Nash equilibrium opponent — a striking empirical result. The paper cleanly separates environment inference from strategy optimization and provides mutual information analysis showing which game features are preserved versus discarded.

## Strengths

- **The headline quantitative result is genuinely impressive.** GOEI reduces 15,542 observations to 452 states (2.9%) while achieving a reward rate of −0.010 against the Nash equilibrium opponent (essentially zero, i.e., not being exploited). The compression is substantial in both raw state counts and effective state entropy (Table 1, Figure 2).

- **The experimental design cleanly separates environment inference from strategy optimization (Sec. 3.3).** By training on fixed-strategy games (Rand vs. NE) and testing performance against NE separately, the paper isolates the question of whether GOEI's learned transition model captures the structure needed for optimal play, independent of exploration-exploitation dynamics.

- **The mutual information analysis (Sec. 4.2, Figure 3) provides useful face validity.** Score difference information is preserved mainly at the final round (t=4) and discarded earlier, while current table card and remaining table cards are relatively more preserved at t=2 and t=3. This aligns with domain intuition and provides qualitative validation that GOEI retains information in a game-theoretically sensible way.

## Weaknesses

### Major

- **Training and evaluation both use the same fixed opponent (NE), so the learned "core" states are specific to the dynamics induced by that opponent's policy — not established as general to the game.** The agent trains on games between Rand and NE and is tested only against NE (Sec. 3.3). The abstract and introduction frame the contribution as discovering essential game information ("core"), but the protocol only demonstrates that GOEI can learn a best response to a *known, fixed* opponent while compressing observations. Generalization to other opponents (e.g., Rand, π₀, or an adaptive opponent) is untested. While the paper acknowledges this in Sec. 5, the mismatch between the broad framing and the opponent-specific evaluation is the paper's most significant limitation. This restricts the scope of the contribution well below what the abstract suggests.

### Minor

- **The abstract states the learned strategy is "equivalent to the Nash equilibrium," but what is demonstrated is reward rate ~0 against a fixed NE opponent.** This means the agent achieves near-optimal *performance* when facing NE (i.e., it is not exploited), not that the learned strategy *is* a Nash equilibrium. The paper's own operational criterion (Sec. 2.2: "compete equally well against the NE opponent") is clearer, but the abstract's phrasing could mislead readers into thinking a stronger property has been shown.

- **The baseline comparison is too narrow to attribute the improvement to GOEI's specific mechanism.** The only RL baseline is tabular Q-learning with four learning rates (Table 1). No comparison against other state abstraction methods (e.g., bisimulation metrics, MDP homomorphisms, simple feature selection) or against any deep RL method is provided. Without such comparisons, it is unclear whether GOEI's advantage comes from its specific Bayesian state-reduction mechanism or simply from performing *some* form of abstraction in a setting where the raw observation space is too large for tabular methods.

- **The paper's stated motivation (explainability) is not supported by the delivered analysis.** The introduction frames GOEI as addressing the lack of explainability in DNN-based agents. However, the paper does not provide interpretable states or verbal explanations of what the 452 learned states represent. The paper candidly acknowledges this (Sec. 5: "we could not give a verbal explanation of the reduced state representation more concretely than Figure 3"). The compression result is valuable independently, but the XAI framing is not substantiated.

### Trivial

None.

## Nice-to-Haves

- Test whether the learned states transfer to opponents other than NE (e.g., Rand, π₀, an adaptive opponent). This is the single highest-impact experiment to address the scope limitation.
- Provide even a coarse qualitative mapping from some learned states to observation features (e.g., do round-4 states correspond to score-difference intervals?).
- Report statistical significance and runtime/memory comparisons between GOEI and Q-learning.

## Removed Points

The following points from the input review were removed per filtering policy:
- **Table 1 presentation critique**: a formatting/style nitpick.
- **Underspecified for reproducibility** (GOEI description): the paper references Takahashi et al. (2024) for algorithmic details, which is appropriate for a validation paper applying an existing method.
- **28,477 number unexplained**: a minor presentation point that does not affect the paper's claims.
- **Request for statistical tests, runtime/memory, training data quantity analysis**: these are nice-to-haves; the paper's 21-seed median/quartile reporting is adequate for the setting.
- **Observation that |S₄*| exceeds NE states**: the paper explicitly reports this, so it is not a weakness.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

The most impactful improvement would be to test whether GOEI's learned states transfer to opponents other than NE. If the same compressed representation performs well against π₀, Rand, or an adaptive opponent without retraining, that would directly support the claim that GOEI extracts game-relevant structure rather than opponent-specific idiosyncrasies. Additionally, providing even a coarse semantic characterization of what the learned states represent would substantially strengthen the paper, regardless of whether the XAI framing is retained.

## Score and Decision

This paper presents a clean, well-executed validation of GOEI in a non-trivial game, with impressive compression ratios. The strengths are concrete and well-documented. However, the opponent-specific training protocol fundamentally limits the generality of the claims, the baseline comparison is insufficient to isolate the source of GOEI's advantage, and the stated motivation (explainability) is not delivered. For a venue like ICLR, which expects either novel methodology or broad empirical discoveries, the contribution — validating an existing method from a 2024 paper in a single game with a constrained protocol — falls below the acceptance threshold, though it would be a solid fit for a more specialized venue.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>