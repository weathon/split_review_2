Now I have all the calibration data I need. Let me produce the final review.

**Calibration bracket**: After Round 1, the paper sits between 4.0 and 5.5. After Round 2 narrowing against KrwEmd (4.00, practical abstraction for games) and Offline Equilibrium Finding (4.25), the paper is comparable or slightly above — it has a cleaner evaluation and a more striking result, but less algorithmic novelty than either.

---

## Summary

This paper validates Goal-Oriented Environment Inference (GOEI), a previously published model-based RL method, on the competitive card game Hol's der Geier. GOEI reduces ~15,542 observations to ~452 states (2.9%) while achieving near-Nash-equilibrium performance (reward rate -0.010 vs. optimal 0.000). The paper demonstrates that GOEI's state-compression approach, previously validated only in abstract environments, works in a more realistic competitive game with a known optimal strategy.

## Strengths

1. **Well-chosen testbed with ground-truth optimal play.** Hol's der Geier has a known Nash equilibrium, providing a clear optimal baseline. The game's sequential structure (4 rounds, 5-card hands) creates a genuine state-reduction problem with ~15K–28K observations, making the evaluation meaningful.

2. **Clean experimental design (Section 3.3).** The authors separate environment inference from strategy optimization by training GOEI offline on games between fixed strategies (Rand vs. NE) and testing the derived policy separately. This isolates the quality of environment inference from confounding factors like exploration or strategy adaptation.

3. **Impressive quantitative result.** Reducing 15,542 observations to 452 states (2.9%) while achieving a reward rate of -0.010 against the Nash equilibrium (where 0.000 is optimal) is non-trivial. The fact that the reduced state count at rounds 2 and 3 (8 and 31 states) is *smaller* than the number of equivalence classes used by the NE strategy itself (247 and 945) is striking and worth noting.

4. **Mutual information analysis (Section 4.2).** The analysis showing which features are preserved at which rounds (CT and RT at early rounds, SD at the final round) provides some insight into what the method retains, consistent with game-theoretic intuition about when each feature matters.

## Weaknesses

### Fatal
None.

### Major

1. **Insufficient baselines to contextualize the contribution.** The paper compares GOEI against only tabular Q-learning, simple deterministic strategies (π₀–π₄), and random play. None of these is a competitive baseline for a top-tier venue in 2025/2026. Tabular Q-learning with 15K+ states is a known strawman — data-inefficiency is precisely why function approximation exists. The paper concludes that "the poor performance of Q-learning indicates that the number of observations is too large," but this is a known limitation of tabular methods, not a finding distinctive to GOEI. Missing baselines include DQN/PPO on raw observations, Deep CFR (Brown et al., 2019, which the paper cites), or an alternative model-based method. Without at least one strong baseline, the paper cannot support the claim that GOEI's state reduction is the key driver of performance — a simple DQN with the same data might match GOEI's reward rate trivially, making the contribution much more modest.

2. **Misalignment between motivation and evaluation.** The Introduction motivates GOEI partly by noting that DNN-based agents "are based on offline learning with vast amounts of data" and that "there is much room for improvement in tasks that require online learning to adapt to opponents." However, the evaluation is entirely offline: GOEI is trained on games between two fixed strategies (Rand vs. NE) and tested against the same NE opponent seen during training. The hardest parts of competitive online play — exploration, opponent adaptation, learning from self-generated data — are absent. The authors acknowledge this in the Discussion, but the gap between motivation and evaluation is large enough that the headline claims are broader than the evidence supports. The paper demonstrates that GOEI learns compressed representations from offline data against a known opponent, not that it learns effective strategies in an online interactive setting.

### Minor

1. **"Near-optimal" claim lacks statistical support.** The best GOEI reward rate is -0.010 (quartiles -0.012, -0.009) vs. NE's 0.000. The paper states it is "indistinguishable from the optimal one" without any statistical test. Given 21 seeds, a one-sample t-test or sign test is easily doable.

2. **No runtime or memory usage reported.** The paper mentions 12GB memory limit but never reports actual runtime, peak memory usage, or number of variational iterations per epoch. Given the emphasis on computational efficiency, this is a notable omission.

3. **Evaluation metric pulls down reported performance.** Averaging reward rates across epochs 1–3,000 includes early learning phases when performance is poor, systematically lowering the reported average relative to final converged performance. Reporting final-epoch performance in addition would be more informative (Figure 2A partially mitigates this, but Table 1 uses epoch-averaged rates).

4. **Explainability framing is overstated.** The paper frames GOEI as improving explainability, but the authors acknowledge they "could not give a verbal explanation of the reduced state representation more concretely than Figure 3" (line 238). State reduction does not equal interpretability. The paper would be more accurately framed around computational efficiency (reduced memory/data requirements).

5. **Opponent-modeling assumption is not stress-tested.** The paper assumes the opponent depends only on the current observation o_t (line 56). The sensitivity of GOEI's compressed model to history-dependent opponents is not evaluated.

### Trivial
None.

## Nice-to-Haves

- Testing a smaller version of the game (e.g., 3 cards) in an online interactive setting where GOEI learns from self-play, to directly examine the adaptive-learning scenario that motivates the work.
- Reporting reduction rates against the full observation space (28,477) rather than only the restricted space (15,542) from the Rand-vs-NE data distribution.
- A per-round breakdown of performance to understand where GOEI's compression works best and where it struggles (especially round 4, which retains 408 states).

## Removed Points

These points were raised by the harsh critic but are removed for the following reasons:

1. **"Q-learning comparison is structurally unfair (batch vs. incremental)"** — GOEI's batch processing is an inherent property of the method (variational Bayesian inference). The comparison shows that batch variational inference with state reduction outperforms incremental tabular learning given the same data — a valid algorithmic comparison, not an unfair setup.

2. **"Mutual information analysis cannot tell us what IS preserved"** — The analysis does show what is preserved: CT and RT at rounds 2-3, SD at round 4 (Section 4.2). The analysis is limited but not uninformative.

3. **"Speculation about scalability is unsupported"** — The paper explicitly frames this as speculation ("may apply," "open to future studies," line 234), not as a claimed result.

4. **"The Markov property assumption is not justified"** — The paper explicitly states this follows from the assumption that the opponent's action depends only on o_t (line 56). This is a clear design choice.

5. **"Table 1 is difficult to parse"** — A presentational preference. The table is dense but decipherable.

## Novel Insights

The harsh critic's observation that the evaluation setup avoids the hardest parts of competitive online play (exploration, opponent adaptation, self-generated data) is a useful insight that goes beyond the authors' own Discussion section. The critic articulates precisely why the offline evaluation, while methodologically clean, limits the generality of the conclusions. Additionally, the observation that the mutual information analysis reveals what is NOT preserved more clearly than what IS preserved (beyond the CT/RT/SD patterns) is a worthwhile caveat.

## Suggestions

1. **Add at least one non-tabular baseline** (DQN, PPO, or Deep CFR on raw observations) — this is the single most impactful improvement. If GOEI matches or exceeds a neural method while using 2.9% of the states, that is a strong result.
2. **Provide a statistical test** comparing the best GOEI reward rate against the NE's 0.000 to support the "indistinguishable" claim.
3. **Report actual runtime and peak memory usage** for GOEI training.
4. **Calibrate the motivating narrative** to match the offline evaluation, or add a small-scale online experiment.
5. **Report final-epoch performance** in addition to epoch-averaged performance.

---

**Calibration anchors used (all rounds):**

| Path | Avg Score | Round | Comparison to this paper |
|------|-----------|-------|-------------------------|
| Uj0h13lVrR.md (GFlowNets) | 1.00 | R1 | Completely different topic; our paper is coherent with real experiments |
| 5kMwiMnUip.md (LLM jailbreaking) | 1.40 | R1 | Different topic; our paper far more substantial |
| 7ienVkNf83.md (Emergent language) | 3.00 | R1 | Proposes new method for abstraction; more novelty than our paper |
| rRRgj3iIHR.md (AlphaDou card game) | 3.00 | R1 | Applied card game AI with incremental improvements; our paper more principled (NE ground truth) |
| XWfjugkXzN.md (Info set sampling) | 1.67 | R1 | Different direction; not comparable |
| nRgGCnw8eZ.md (KrwEmd abstraction) | 4.00 | R2 | Practical abstraction for poker; proposes new algorithm. Our paper has more striking result but less novelty |
| Re5iu0hBTs.md (Offline EF) | 4.25 | R1 | More novel paradigm but questionable formulation; our paper cleaner but less novel |
| 7J0NsFXnFd.md (Optimal action abstr.) | 5.25 | R1 | Novel method, strong poker results; our paper less novel |
| p5SurcLh24.md (Unifying MB/MF RL) | 4.75 | R1 | Novel method+theory; more substantive |
| czpx02orl7.md (Abstract world models) | 4.75 | R1 | Novel method+theory; more substantive |
| MTcgsz1SHr.md (Online pruning) | 5.75 | R2 | Novel method, accepted; stronger than our paper |
| odY3PkI5VB.md (Goal repr. HRL) | 6.33 | R1 | Novel HRL method; stronger |
| hgwGi81ndj.md (Object-centric abstr.) | 6.80 | R1 | Novel method+theory; stronger |
| 9pW2J49flQ.md (DeepLTL) | 8.00 | R1 | Strong method+theory; far stronger |

**Round 1 bracket:** 4.0–5.5  
**Final score determination:** Compared against KrwEmd (4.00, new algorithm with mixed reviews) and Offline EF (4.25, novel paradigm with questionable formulation) — this paper has a cleaner evaluation and more striking empirical results but less novelty. Placed slightly above KrwEmd at 4.5.

---

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>