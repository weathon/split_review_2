Now I have all the calibration data I need. Let me compile the final review.

**Calibration Analysis:**

**Round 1 bracket (wide):** Based on comparison with RATE (4.75) and Foundation Policies with Memory (3.00), ELMUR is clearly stronger on both empirical results and methodological clarity. The nearest comparable paper is Think Before You Act: DT-Mem (5.75). ELMUR's strengths are competitive with or stronger than DT-Mem's, and its worst weaknesses (POPGym protocol favorability=3.16, theory favorability=-2.13) are less severe than DT-Mem's worst weaknesses (novelty favorability=-5.20, unclear advantages favorability=-3.87). ELMUR has a cleaner architectural specification and stronger T-Maze demonstration. **Initial bracket: 5.5–6.5.**

**Round 2 narrowing:** Within 5.5–6.5, ELMUR's strength favorabilities (8.61–11.08) match or exceed DT-Mem's (7.58–10.15). ELMUR's core contributions — per-layer external memory with LRU management, strong T-Maze/MIKASA-Robo results, clean ablations — are genuine. The POPGym protocol omission is the most significant gap but affects only one of three benchmarks. The task count inconsistency (23 vs 32) and overclaimed 100,000× framing are presentation issues, not methodological flaws. **Final score: 6.0** (borderline accept — paper has real contributions but needs to address protocol specification and framing issues before acceptance).

---

## Summary

ELMUR proposes a transformer architecture augmented with per-layer external memory managed by a Least Recently Used (LRU) update/rewrite mechanism. The design adds a parallel memory track to each transformer layer, with bidirectional cross-attention for reading from and writing to memory, and a convex blending update rule. The paper evaluates on three benchmarks: synthetic T-Maze (100% success at 1M steps with L=10 context), MIKASA-Robo visual manipulation (0.89 vs 0.65 on RememberColor3, 0.78 vs 0.42 on TakeItBack), and POPGym (best aggregate score 10.4).

## Strengths

- **Strong results on the synthetic T-Maze benchmark (Section 5.2, Figure 3).** ELMUR achieves 100% success rate on corridors up to one million steps while using a context window of only L=10 tokens, cleanly demonstrating that the LRU-based external memory mechanism can store and retrieve a cue across extremely long delays. The generalization experiment (Figure 4) showing 100% accuracy across all train/validation length pairs adds further confidence.

- **Meaningful improvements on MIKASA-Robo (Table 1).** On RememberColor3-v0, ELMUR achieves 0.89 ± 0.07 vs RATE's 0.65 ± 0.04, and on TakeItBack-v0 it achieves 0.78 ± 0.03 vs 0.42 ± 0.24. These are genuine gains on visual, continuous-action robotic tasks where memory matters.

- **Clean ablation study (Table 3, Figure 6).** The ablations cleanly isolate the contribution of each component. The finding that removing LRU drops performance from 1.00 to 0.43, and that removing both LRU and relative bias drops it to 0.22, confirms that both mechanisms are functional. The ablation of M vs N capacity (Figure 6c-d) reveals a clear threshold behavior that aligns with the theoretical analysis.

- **Sanity check on fully observable MDPs.** The CartPole-v1 result (all models achieve 500 ± 0) is a useful negative control, showing that the added memory mechanisms do not harm performance on tasks where memory is unnecessary.

## Weaknesses

### Major

- **POPGym training protocol is not specified.** ELMUR is trained via Behavior Cloning (supervised learning on demonstrated actions), but POPGym environments provide reward functions, not expert demonstrations. The paper never explains where the action targets for POPGym come from — whether they use a scripted expert, an RL-trained oracle, or some other source. Without this information, the POPGym results in Table 2 cannot be fully interpreted or reproduced. This is a significant gap in a central empirical result. (The paper states "All models are trained from scratch under the same data budgets and preprocessing," implying a shared data source, but the data source itself is not described.)

- **MIKASA-Robo task count inconsistency.** The Abstract and Introduction state ELMUR achieves "the best success rate on 21 out of 23 tasks" and "ranking first on 21 of 23 tasks," but Table 1's caption reads "See results for all 32 MIKASA-Robo tasks" (emphasis added). This discrepancy between 23 and 32 tasks affects the headline empirical claim and must be resolved.

### Minor

- **100,000× claim lacks scope qualification.** The claim is stated in unqualified terms in the Abstract and Introduction. The T-Maze task requires retaining a single binary cue (turn left or right). Achieving 100% success across one million steps on this task is genuinely impressive, but the framing invites readers to infer that ELMUR can retain complex, high-dimensional observations across similarly extreme horizons — a claim for which no evidence is provided. The paper should explicitly scope the claim to the binary T-Maze setting.

- **MoE-FFN included without demonstrated benefit.** The paper justifies the DeepSeek-MoE FFN for "parameter efficiency and specialization," but Table 3 shows that replacing MoE with a standard MLP yields identical performance (1.00 ± 0.00). The paper then acknowledges that this replacement "preserves accuracy while improving computational efficiency." The MoE component is a distraction from the paper's core memory contribution.

- **Theoretical analysis is straightforward algebra presented as a contribution.** Propositions 1 and 2, and the half-life corollary, are direct algebra applied to the convex update rule — the textbook expression for an exponential moving average. The boundedness proof follows from the triangle inequality applied to convex combinations. The contribution list claims "establishing formal bounds on forgetting, retention horizons, and stability of memory embeddings," which overstates what is basic algebra. This material would be better positioned as exposition of the method's design parameters rather than a formal theoretical contribution.

- **Relative Bias D_max not reported.** The value of D_max (maximum relative distance supported by the bias table) governs the range over which temporal offsets remain distinguishable. Without this value, readers cannot assess whether the bias saturates at realistic temporal offsets on the long-horizon tasks tested.

- **LRU is "oldest written" not "least recently accessed."** Algorithm 2 selects the slot with the smallest anchor value p_j (earliest last-update time). This design does not distinguish between read and write access recency — a slot frequently read but rarely written can be overwritten despite being actively used. The paper does not discuss this design choice.

- **Baselines in Figure 3 not fully described.** Several models appearing in Figure 3 (RMT, TrXL, Persistent, Random) are not described in the baseline list (Section 5.1), which only mentions DT, RATE, DMamba, BC-MLP, BC-LSTM, CQL, and DP.

- **No guidance on λ selection in practice.** The ablation (Figure 6a) shows that intermediate λ ≈ 0.4–0.6 produces instability when M < N, but the paper provides no practical guidance on how to select λ. Since λ controls the stability–plasticity trade-off, this is a gap for practitioners.

### Trivial

None.

## Nice-to-Haves

- Provide λ selection guidance based on task properties
- Report D_max value and analyze saturation behavior
- Include statistical significance tests for baselines with large SEMs (e.g., RATE on TakeItBack: 0.42 ± 0.24)

## Removed Points

These points were raised in the initial input but are removed after verification:

- **Hardware not specified for timing measurements**: The paper explicitly states "All experiments were run on a single NVIDIA A100 (80 GB) per job" (Section 5.1). Factually wrong — removed.
- **IL/RL framing conflation**: The paper explicitly frames its central question as "how can we equip IL policies with efficient long-term memory to solve long-horizon, partially observable tasks." The title "RL Problems" refers to the problem domain, not the method. No conflation — removed.
- **Related Work "bloated"**: Subjective style criticism not grounded in a specific problem — removed.
- **Missing appendix content**: The appendix is stripped by the PDF parser; criticisms about missing appendix details cannot be verified — removed.

## Novel Insights

None beyond the paper's own contributions. The reviews converge on the same set of issues: the POPGym protocol gap, the task-count inconsistency, and the overclaimed 100,000× framing. No novel methodological insight emerged from the cross-referencing of reviews.

## Suggestions

1. Specify the POPGym data collection protocol: how are expert demonstrations generated for each task?
2. Resolve the MIKASA-Robo task count inconsistency (23 vs 32).
3. Qualify the 100,000× claim as specific to the binary T-Maze task — e.g., "on a binary cue-retention task, ELMUR retains information across horizons 100,000× beyond its attention window."
4. Report D_max and provide guidance on λ selection.
5. Either remove MoE from the main architecture or demonstrate its benefit on a task where it matters.
6. Reposition the theoretical analysis as exposition of the method's design properties rather than a formal contribution.
7. Document that the LRU policy tracks write recency only and discuss potential implications.
8. Add descriptions for all baselines that appear in figures (RMT, TrXL, etc.).

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>