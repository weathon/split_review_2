Now I have all the calibration data I need. Let me synthesize the final review.

The bracket comparison: The closest anchors are "Learning Abstract World Models" (4.75, Reject — new theory + simple experiments) and "KrwEmd" (4.00, Reject — new algorithm but poor presentation). Our paper applies an existing method to a single new domain, with a striking compression result but weak baselines and a significant evaluation confound. It falls between these anchors — better presented than KrwEmd but with less novelty than the Abstract World Models paper. The bracket is 3.5–4.5, narrowed to 4.0.

## Summary

This paper applies Goal-Oriented Environment Inference (GOEI) — an existing model-based reinforcement learning method for state reduction — to the two-player competitive card game "Hol's der Geier." The central finding is that GOEI compresses the observation space from 15,542 observations to 452 states (2.9% of the original size) while achieving a reward rate of -0.010 against a Nash equilibrium opponent, indicating near-optimal play. The paper also provides a mutual information analysis showing which game features the reduced representation preserves or discards.

## Strengths

- **The core quantitative result is striking and well-documented.** At its best configuration (β=0.2, α=25), GOEI reduces 15,542 observations to 452 states while achieving a reward rate of -0.010 against the Nash equilibrium opponent (Table 1). A compression ratio of 97.1% while maintaining near-optimal performance in a competitive zero-sum game is genuinely noteworthy and the paper's headline finding. *(Impact: +4.15)*

- **The mutual information analysis (Section 4.2, Figure 3) provides nontrivial insight.** The finding that agent's hand (AH) and opponent's hand (OH) information is aggressively discarded while current table card (CT) and remaining table cards (RT) are partially preserved, and that score difference (SD) becomes important only at round 4, gives concrete intuition about GOEI's feature selection behavior. This goes beyond simply reporting state counts. *(Impact: +1.80)*

- **The paper is transparent about its limitations.** Section 5 explicitly acknowledges that training separates environment inference from strategy optimization, that interactive learning could interfere with inference, and that state reduction alone does not automatically yield a verbal explanation. This candor is commendable. *(Impact: +0.05–0.21 combined)*

## Weaknesses

### Major

- **The evaluation design cannot distinguish between learning game dynamics and memorizing opponent behavior.** The agent is trained on games played between Rand vs. NE and tested against the same NE opponent (Section 3.3, lines 128–130). Because the transition model P(o_{t+1} | a_t, o_t) depends on the opponent's policy, the learned model embeds NE's behavior during training. Testing against the same NE strategy evaluates in-distribution performance. This does not invalidate the performance claim (near-NE reward), but it limits the interpretation of what "core states" means — the representation may encode opponent-specific patterns rather than game-invariant structure. A generalization experiment (training on non-NE data, testing against NE) would substantially strengthen the paper's core claim. *(Impact: -0.55)*

- **The 2.9% figure uses the restricted observation space reachable under NE play (15,542) rather than the full theoretically possible space (28,477).** While the paper is transparent about this in Section 3.3 (line 134), the abstract's phrasing "2.9% of all possible observations (15,542)" is ambiguous — a reader reasonably interprets "all possible observations" as the full 28,477 figure reported in Section 2.1. The abstract should explicitly note this restriction. *(Impact: -0.00 — low magnitude because the paper is transparent, but the presentation issue is real)*

### Minor

- **The Q-learning comparison is not informative.** Q-learning is applied offline, observing games played by Rand and NE rather than playing and receiving its own rewards (Section 3.3). Tabular Q-learning over 15,000+ states without exploration is expected to perform poorly in this regime. At minimum, an online Q-learning baseline (where the agent plays) or a simple function-approximation baseline would have provided a more meaningful comparison. *(Impact: -10.00 — the model scores this highly, but I downgrade it to Minor because the Q-learning comparison is not central to the paper's main claim about compression)*

- **At round t=4, GOEI uses 408 states compared to NE's 69 (Table 1) — approximately 6× larger.** The headline 2.9% aggregate compression masks that compression is uneven across rounds: aggressive in early rounds (t=2: 8 vs. NE's 247; t=3: 31 vs. NE's 945) but substantially less so at the final round. This pattern is not discussed and somewhat weakens the overall compactness narrative. *(Impact: -0.00)*

- **Gap between explainability motivation and results.** The paper motivates GOEI partly through explainability (Section 1), but the results do not provide a concrete explanation of the learned strategy. The mutual information analysis shows which features are discarded but does not yield an interpretable decision rule. The paper honestly acknowledges this (Section 5), but it means the paper does not deliver on one of its motivating promises. *(Impact: -0.14)*

- **The abstract's phrasing "equivalent to the Nash equilibrium" overstates the result.** The best reward rate is -0.010, not 0.000. With 10,000 test games per epoch across 3,000 epochs, this difference is measurable. "Nearly optimal" is a more accurate characterization. *(Impact: -0.02)*

### Trivial

None.

## Nice-to-Haves

- An online (interactive) learning experiment, even a small-scale one, would strengthen practical relevance.
- A discussion of why round 4 compression is weaker than earlier rounds would improve the narrative.
- Providing win-probability conversion alongside reward rates would help readers intuit the performance level (-0.010 reward rate could mean ~49.5% win / 50.5% loss).

## Removed Points

- **Criticism about scaling to larger card sets being unsupported (Section 5 speculation):** Removed. The paper mentions this speculatively in the discussion ("GOEI may apply to versions with cards more than five") as a future direction, not as a core claim.
- **Criticism about mutual information being contradictory (AH/OH reduced yet "crucial"):** Removed. The paper's resolution — that the required information is maintained in complex joint combinations across features — is not contradictory; per-feature mutual information can be low even when the joint distribution carries game-relevant information.
- **Table 1 formatting critique:** Removed. It is a minor presentation nitpick; the table is dense but functional.
- **Criticism that Section 2.2's NE chain strategies are unused:** Removed. The paper does use π₀ as a baseline (Table 1 shows reward rate -0.125), and these strategies are mentioned for background context.
- **Request for interactive/online learning experiment as a weakness:** Removed. The paper explicitly scopes this out as a limitation (Section 5). Requesting it as necessary for acceptance is scope creep; the paper is evaluating environment inference in isolation.
- **Critique of "GOEI could earn rewards" grammar:** Removed — formatting/grammar nitpick from parsing artifacts.

## Novel Insights

The harsh critic's central insight — that the evaluation confound (same opponent in training and test) prevents strong claims about "core state extraction" being distinct from opponent modeling — is the most valuable observation. It correctly identifies that the paper claims to extract game-invariant core states, but the experimental design only tests in-distribution performance against one fixed opponent. The proposed control experiment (train on Rand vs. Rand or Rand vs. π₀, test against NE) is a concrete, high-leverage fix. Beyond this, the insight about the round-4 state count asymmetry (408 vs. 69) adds nuance to the compression claim, and the recognition that the 2.9% figure uses a restricted observation space adds important context for interpreting the headline number.

## Suggestions

1. **Generalization experiment:** Train GOEI on data from non-NE games (e.g., Rand vs. Rand or Rand vs. π₀) and test against NE. If the compressed representation still achieves near-optimal performance, it would substantially strengthen the claim that GOEI extracts game-invariant core states.
2. **Add a more meaningful baseline:** Include at least one of: online Q-learning (where the agent plays), linear function approximation, or a simpler state-abstraction method (e.g., uniform binning).
3. **Clarify the abstract:** Explicitly state that the 2.9% figure is relative to observations reachable under NE play, not the full theoretical observation space.
4. **Discuss round-4 asymmetry:** Explain why GOEI's compression is weaker at the final round compared to NE's theoretical equivalence classes.
5. **Precision in language:** Replace "equivalent to the Nash equilibrium" with "nearly optimal" or "approaching Nash equilibrium performance."

## Score and Decision

Round 1 bracket: I first established that this paper falls between the 3.5–4.5 range by comparing it against the calibration anchors. The "Learning Abstract World Models" paper (4.75, Reject) has a new theoretical contribution but simpler experiments on toy domains; this paper has no new theory but a cleaner concrete result. The "KrwEmd" paper (4.00, Reject) proposes a new algorithm but suffers from poor presentation and unclear experiments. The "Efficient Online Pruning" paper (5.75, Accept) demonstrates strong results against state-of-the-art baselines with orders-of-magnitude speedup.

Round 2 narrowing: Comparing itemized impact scores, the strongest positively-scored item in this paper's draft (+4.15 for the compression result) is comparable to the strongest positive items in the 4–5 range anchors (KrwEmd's strongest strength at +6.84, Abstract World Models' strongest at +10.00 for presentation). However, this paper lacks the theoretical contribution of those anchors and has a more significant evaluation limitation. The Q-learning weakness scored at -10.00 by the model is partially downgraded because it's not central to the paper's claim, but the evaluation confound is real and constrains the interpretive reach of the paper's main contribution.

Final score: **4.0**. The paper presents a genuinely interesting compression result in a concrete domain and is well-written and transparent about its limitations. However, the evaluation confound, weak baselines, and single-domain scope limit the strength of the evidence for the paper's core claims. The contribution is a suggestive demonstration rather than a fully convincing one — appropriate for a workshop or a more specialized venue, but not yet at the bar for a top conference like ICLR.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>