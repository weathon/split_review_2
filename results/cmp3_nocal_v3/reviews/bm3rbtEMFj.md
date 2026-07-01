Now I'll produce the consolidated review.

## Summary

ELMUR augments each transformer layer with a persistent external memory track — each layer maintains its own memory embeddings, interacts with tokens via bidirectional cross-attention (mem2tok read / tok2mem write), and manages memory slots through an LRU-based update rule that fills empty slots first and then blends new content into the least recently used slot via convex combination. The architecture is evaluated on a synthetic T-Maze benchmark, the MIKASA-Robo robotic manipulation suite (visual observations, sparse rewards), and the diverse POPGym benchmark. On T-Maze, ELMUR achieves 100% success at corridor lengths up to 1M steps with only L=10 context and S=3 training segments. On MIKASA-Robo and POPGym it outperforms baselines consistently, though with variable margins.

## Strengths

1. **Clean architectural design with clear motivation.** The per-layer external memory with dedicated read/write cross-attention and LRU-based slot management (Section 3, Algorithm 1) is well-motivated. The separation of token and memory tracks, together with segment-level recurrence, provides a principled way to extend retention beyond the attention window without quadratic cost. The pseudocode and diagrams (Figures 1–2) make the mechanism easy to follow.

2. **Striking T-Maze results as a proof-of-concept.** The 100% success rate across corridors up to one million steps (Figure 3), with only L=10 context and S=3 training segments, is genuinely impressive. The generalization heatmap (Figure 4) showing 100% success across all 77 train/test length pairs further confirms that the memory mechanism can retain a single cue across extremely long horizons in a noise-free, controlled setting. This convincingly demonstrates that the LRU-based memory *can* work as intended under ideal conditions.

3. **Informative ablation study.** The ablations on RememberColor3-v0 (Figure 6, Table 3) cleanly isolate the contributions of memory size M, blending factor λ, initialization scale σ, and segmentation strategy. The finding that M ≥ N (memory slots ≥ required segments) is necessary for near-perfect performance, and that under-provisioned memory is highly sensitive to hyperparameters, is a concrete, actionable insight. The component ablations (shared memory, no LRU, no relative bias) also provide clear evidence for each design choice.

## Weaknesses

### Fatal
None.

### Major

1. **BC-MLP achieving ~70% on T-Maze is unexplained and raises questions about the task's properties.** Figure 3 shows that BC-MLP — a feedforward network with no temporal processing — achieves roughly 70% success at 1M-step corridors. If the T-Maze genuinely requires recalling a binary cue from the start of a million-step corridor, a memory-free MLP should obtain only the 50% chance level (consistent with the Random and Persistent baselines also shown in Figure 3). The ~70% result suggests either (a) the observation at the junction leaks information about the cue, (b) the expert demonstrations contain a statistical bias an MLP can exploit, or (c) some other regularity makes the task partially solvable without memory. The paper does not discuss or explain this result. Since the paper's strongest claims about horizon extension (100,000×) rest on T-Maze, the properties of this benchmark need to be clarified. (RATE also achieves ~70% at 1M steps, further narrowing the gap ELMUR's mechanism claims to close.)

2. **Rhetorical calibration: the headline claims outpace the evidence on realistic benchmarks.** The abstract states that ELMUR "extends effective horizons up to 100,000 times beyond the attention window" as a general property of the method, but this is demonstrated only on the synthetic T-Maze. On MIKASA-Robo, the absolute success rates on harder variants are near chance — RememberColor5-v0: 0.19±0.03 (best among baselines, but at or below random); RememberColor9-v0: 0.23±0.02. The paper claims a "70% aggregate improvement" over the previous best baseline, but this aggregate figure cannot be verified from the main paper (deferred to Appendix Table 8, which is not in the review copy). The POPGym aggregate improvement over RATE is 0.9 points (10.4 vs. 9.5), a modest margin. The gap between the "100,000× horizon" rhetoric and the actual gains on realistic tasks needs to be narrowed or the claims need to be qualified more precisely.

3. **Inconsistency in MIKASA-Robo task count.** The Introduction (line 27) states ELMUR "rank[s] first on 21 of **23** tasks," while the caption of Table 1 (line 236) references "all **32** MIKASA-Robo tasks" in the appendix. These numbers are inconsistent and need to be resolved.

### Minor

4. **Theoretical analysis is basic and disconnected from the experiments.** Proposition 1 (exponential forgetting from repeated convex updates) and Proposition 2 (boundedness under convex combinations) follow directly from the definitions and are straightforward. This is not problematic per se, but the effective horizon formula (H(ε) = M·L·ln(ε)/ln(1-λ)) is never instantiated: the paper does not report which λ and M were used in the T-Maze experiment or check whether the predicted retention horizon matches the observed 100% retention at 1M steps. The ablation in Figure 6a tests λ only on RememberColor3-v0 and only under the M<N regime. The theory would carry more weight if it were validated against the experiments.

5. **Hyperparameter values for specific experiments are deferred to the appendix.** The main paper does not report M, λ, σ, L, S, or D_max used for each benchmark (referenced to Appendix Table 7). These are critical for reproducibility and evaluation of claims about effective horizon.

6. **POPGym aggregate scores lack error bars.** Table 2 reports aggregate returns for "All (48)," "Puzzle (33)," and "Reactive (15)" without standard errors or confidence intervals, even though individual task means have them per the evaluation protocol (line 206). This makes it impossible to assess whether ELMUR's 0.9-point aggregate advantage over RATE (10.4 vs. 9.5) is statistically meaningful.

7. **Relative bias clamping is not discussed as a limitation.** The relative bias mechanism clamps offsets to [−D_max+1, D_max−1] (line 118), meaning the model cannot distinguish between events that occurred D_max steps ago and events that occurred 10× D_max steps ago. This could matter for the very-long-horizon claims and should be acknowledged.

### Trivial

8. **MoE-FFN vs. MLP-FFN.** The ablation (Table 3) shows that replacing MoE-FFN with MLP-FFN preserves accuracy (1.00 ± 0.00) while the paper notes it "improves computational efficiency" (line 261). If MLP-FFN is both simpler and more efficient with identical accuracy, the paper should either justify the MoE choice (e.g., for future scalability) or simplify the architecture.

9. **CartPole sanity check.** The finding that all methods achieve 500/500 on CartPole confirms only that the models do not catastrophically fail on a trivial fully-observable task. This provides no information about memory behavior and should be de-emphasized or dropped.

## Nice-to-Haves

- A diagnostic experiment explaining the gap between 100% on T-Maze and ~19–23% on RememberColor5/9 (e.g., is the bottleneck visual encoding, multiple cues, distractors, or continuous actions?) would be more valuable than additional benchmarks.
- Instantiate the effective horizon formula with experimentally used λ, M, L values and compare predicted vs. observed retention.
- The paper could include a summary table of hyperparameters (M, λ, σ, L, S, D_max) per benchmark in the main text rather than deferring fully to the appendix.

## Removed Points

These points from the input review are removed or demoted with justification:

- **Missing baseline comparison** (Block-Recurrent Transformer, Memformer, ETT): Removed per policy — do not mention missing related works.
- **CQL comparison is unfair**: Removed — the paper includes BC-MLP and DP as BC-based baselines; ELMUR outperforms these as well, so the comparison does not depend on CQL. The critic's concern about IL-vs-RL framing is kept (Minor) since the paper uses RL language while training via BC, but this is a presentation issue, not a methodological flaw.
- **"Most modern approaches rely solely on instantaneous information" is overstated**: Removed as a rhetorical nitpick common in introductions.
- **Related work reads as a catalog**: Subjective and not a concrete weakness.
- **BC-MLP on T-Maze "narrows the claimed advantage" to 30 percentage points**: The raw numbers (100% vs 70%) are correct, but the framing implies this is a fatal weakness. It is better framed as a need for explanation (Major weakness #1).
- **Segmentation strategy not specified**: The paper explains segment construction at line 82. Removed.
- **Missing D_max value for experiments**: This is a subset of the broader hyperparameter disclosure issue (Minor #5), already included.

## Novel Insights

The harsh review surfaces one genuinely novel observation beyond the paper's own contributions: the unexplained 70% BC-MLP result on T-Maze. If this anomaly signals that T-Maze does not purely isolate memory, it has implications not just for this paper but for the broader community's use of T-Maze as a diagnostic. The review also correctly notes that the gap between the synthetic demonstration and the realistic benchmark results is larger than the paper's rhetoric acknowledges, which is a useful calibration insight that the authors should address directly rather than by adding more benchmarks. Otherwise, the insights in the review largely mirror what the paper itself reports (e.g., the ablation findings, the per-task results).

## Suggestions

1. **Explain the BC-MLP and RATE ~70% results on T-Maze.** Determine whether the observation at the junction leaks information or the expert data has a statistical bias. If T-Maze is not a pure memory test, reframe the claims about it accordingly.
2. **Calibrate the headline claims.** Qualify the "100,000× horizon" as a T-Maze-specific demonstration. Report the full MIKASA-Robo results in the main paper or a prominent supplement, with error bars for the aggregate metrics.
3. **Resolve the 23 vs. 32 task count inconsistency** in MIKASA-Robo.
4. **Add hyperparameter tables to the main text** (or the supplement available for review). Report λ, M, L, S, D_max per benchmark and, where possible, validate the predicted effective horizon against observed retention.
5. **Add error bars to the POPGym aggregate summary** (Table 2) so readers can assess the significance of the reported advantages.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>