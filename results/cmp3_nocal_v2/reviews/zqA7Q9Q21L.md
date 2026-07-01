## Summary

This paper presents R2PS, a framework for worst-case robust real-time pursuit strategies in graph-based pursuit-evasion games (PEGs) under partial observability. The contributions are threefold: (1) a theoretical extension of dynamic programming (DP) for Markov PEGs to asynchronous-move settings (Theorem 2, Corollary 1), proving that the DP distance table yields strictly optimal strategies when the evader moves after observing the pursuers; (2) a belief preservation mechanism (Equations 4–7) with O(|V|) per-timestep complexity that handles partial observability while reducing to the perfect-information DP policy when observations are unlimited (Lemma 2); and (3) integration of this belief mechanism into the EPG cross-graph RL framework to train a GNN-based pursuer policy for zero-shot generalization to unseen graphs. Empirical results show that the trained policy outperforms PSRO (trained directly on test graphs) across multiple real-world locations and achieves dramatic speedups (~0.008s GPU inference vs 6–139s DP recomputation on large graphs).

## Strengths

1. **Well-motivated and clearly scoped problem.** The paper identifies a genuine gap — real-time pursuit strategies under partial observability with evader prediction capability — that existing methods (EPG, Grasper, MT-PSRO) do not address. The motivation (Section 1) is specific and grounded in the infeasibility of recomputing DP solutions under dynamically changing graph structures.

2. **Sound theoretical extension of DP to asynchronous moves.** Lemma 1 (the minimax identity for the distance table) and Theorem 2 (strict optimality of the induced policies under asynchronous moves) are clearly stated. This is a non-trivial extension: the original DP algorithm (Lu et al., 2025a) was designed for synchronous moves, and the paper correctly identifies that the distance table D preserves the minimax structure needed for the asynchronous setting. The theoretical analysis is the strongest part of the paper.

3. **Practical and grounded belief preservation mechanism.** Equations (4)–(7) define a belief update that avoids the exponential complexity of full POMDP approaches while maintaining reasonable performance. Lemma 2 verifies the reduction to perfect-information DP when observations are unlimited. The mechanism is simple enough to be practically deployable. The ablation study (Table 4) usefully demonstrates that belief update frequency and opponent-model accuracy both affect performance, confirming the mechanism's relevance.

4. **Convincing empirical advantage over PSRO.** The zero-shot R2PS policy consistently outperforms PSRO (trained directly on each test graph) across all four evader types in Table 2. Against the strongest evader (DP_async), PSRO often achieves 0% success while R2PS achieves non-trivial rates (e.g., 0.95 on Times Square, 0.82 on Big Ben). This is a meaningful result.

5. **Demonstrated real-time capability.** Inference times of ~0.008s on GPU vs 6–139s for DP recomputation on large graphs (Table 3) make the real-time claim credible. The O(n²m) complexity analysis (Section 4.2) provides a formal footing.

## Weaknesses

### Major

1. **The "worst-case robust" claim is stronger than the evidence supports.** The RL policy is trained exclusively against DP_async (Equation 3), which selects evader actions assuming optimal future play by both sides. Against a *suboptimal* RL pursuer, this evader is not guaranteed to be worst-case. The BR_async results in Table 2 confirm this: a directly trained best-responding evader reduces R2PS success rates substantially on several graphs (e.g., Times Square drops from 0.95 to 0.27, Hollywood from 0.38 to 0.10, Downtown from 0.99 to 0.92). The paper acknowledges BR_async but continues to use "worst-case robust" language broadly (abstract: "first approach to worst-case robust real-time pursuit strategies"; contributions list; conclusion). The framing should be qualified: the policy is robust against the class of DP-optimal evaders, with additional evidence that it performs reasonably against trained best-responders, but it has not been shown to be worst-case robust in the formal game-theoretic sense.

2. **No variance or statistical significance reported for any RL experiment.** Tables 2–4 report only point estimates of success rates. While the DP results (Table 1) are averaged over 500 tests, the RL results lack standard deviations, confidence intervals, or the number of independent seeds. The reader cannot assess whether gaps (e.g., Ours=0.99 vs PSRO=0.93 on Sagrada Familia against Stay) are statistically reliable, or how much results vary across different random initializations. For a top-venue submission, this is a significant methodological gap that should be addressed by reporting results over multiple seeds with error bars.

### Minor

3. **The PSRO baseline is underspecified.** The paper states PSRO was run for 10 iterations with 10,000 episodes per iteration but does not describe the architecture (neural network type, size), training algorithm, or opponent pool. If PSRO was training against self-play opponents rather than DP-based adversaries, the comparison is not apples-to-apples. The underspecification limits the reader's ability to assess whether PSRO's poor performance reflects a limitation of the paradigm or simply an underpowered implementation.

4. **No comparison against EPG without the belief mechanism.** Since the paper builds directly on EPG, an ablation comparing R2PS (EPG + belief mechanism) against EPG (without belief) under the same partial-observability conditions would isolate the belief mechanism's contribution. The DP_belief vs DP_Pos comparison (Table 1) provides indirect evidence, but a direct RL-level comparison is missing.

5. **The transitivity argument in Section 4.1 is hand-wavy and out of place.** The paragraph claiming that "cross-graph policy will be improved at an exponential level" relies on an unformalized "half space" intuition and has no supporting evidence or formal justification. In an otherwise technically precise paper, this speculative passage weakens the exposition and should either be made rigorous or removed.

6. **The success rate drop on enlarged graphs deserves more candid discussion.** In Table 3, success rates against DP_async drop substantially compared to Table 2 (e.g., Times Square from 0.95 to 0.56, Hollywood from 0.38→0.46 actually increased a bit, but Sagrada Familia 0.20→0.33). The paper says this "maintains desirable overall performance," but drops of this magnitude warrant analysis — are these due to GNN capacity limits, insufficient training graph diversity, or the increased graph size itself?

7. **The "first approach" priority claim is stated too broadly.** The claim that this is "the first approach to worst-case robust real-time pursuit strategies under partial observability" appears three times (abstract, contribution list, conclusion). Given the extensive POMDP and partially-observable game-solving literature, this should be qualified to the specific graph-based PEG setting (e.g., "first approach *in the graph-based PEG RL literature*").

### Trivial

8. **The definition of "optimal strategy" in the asynchronous setting** (Section 2.1) is given in prose ("worst-case termination timesteps are maximized/minimized") rather than via a formal Bellman-style equation, making the theoretical claims in Section 3 slightly harder to verify.

## Nice-to-Haves

- Analyze why the DP_async vs BR_async gap varies dramatically across graphs (e.g., gap of 0.03 on Downtown vs 0.68 on Times Square). Understanding this could strengthen the worst-case robustness characterization and guide future work.
- Provide failure-mode analysis: are R2PS failures concentrated in particular graph regions (high-degree vertices, bottlenecks)?
- Consider whether the GNN architecture limits scalability to very large graphs, given the observed performance drops in Table 3.

## Removed Points

- **Empty code URL in footnote**: Removed as a potential parser artifact (the footnote reads "Code can be found at ." with an empty URL). Per the hard rules, formatting artifacts of this kind are not author errors to criticize.
- **Belief update with uniform ν may be arbitrarily wrong**: Reduced from standalone criticism to a weak inclusion (the paper acknowledges this limitation in Section 5.3, stating "if we manage to obtain such information in reality, we can instantly improve the pursuit performance," and Table 4 demonstrates the benefit of using known opponent information). The criticism remains implicit in the belief mechanism design but does not warrant standalone mention as a weakness.
- **EPG comparison mentioned as missing but paper partially addresses via DP_belief vs DP_Pos**: Moved to Minor (point 4 above) with the caveat that indirect evidence exists.
- **Training/test distribution mismatch concern**: Removed as speculative — the training set includes 150 Google Maps urban locations, which should share distributional similarity with the real-world test graphs. Without evidence of a meaningful mismatch, this is noise.
- **Strength about "empirical comparison against PSRO is informative"**: Retained but implicitly qualified by weakness 3 (PSRO underspecification limits informativeness).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Qualify the worst-case robustness claim.** Replace unqualified "worst-case robust" language with more precise phrasing: "robust against DP-optimal evaders, with empirical evidence of reasonable performance against trained best-responders." This would better match the evidence.

2. **Add statistical rigor.** Report results over at least 5 random seeds with standard deviations or confidence intervals for all RL experiments (Tables 2–4). This is essential for a venue like ICLR.

3. **Specify the PSRO baseline.** Describe the neural architecture, training algorithm, and opponent pool used for PSRO. If PSRO used self-play rather than DP-based opponents, this should be stated explicitly.

4. **Tighten or remove the transitivity argument in Section 4.1.** The current "exponential improvement" claim is unsupported and detracts from the paper's technical rigor.

5. **Discuss the enlarged-graph performance drops more candidly.** Acknowledge the magnitude of the drops and hypothesize causes (GNN capacity, training diversity, graph topology).

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>