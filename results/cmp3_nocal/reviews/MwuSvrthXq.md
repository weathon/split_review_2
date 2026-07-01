Here is the final consolidated review:

---

## Summary

This paper proposes WeCAN, an end-to-end RL framework for heterogeneous DAG scheduling with task-resource compatibility. Its main contributions are: (1) a weighted cross-attention (WeCA) layer that integrates compatibility coefficients as attention biases, handling variable-size pool sets without fixed-dimensional embeddings; (2) a theoretical analysis of list scheduling's optimality gap, with sufficient conditions for a generation map to retain optimal solutions; (3) a skip-action mechanism for the single-pass setting that closes this gap; and (4) strong empirical results on TPC-H and Computation Graphs datasets.

## Strengths

1. **The WeCA layer is well-motivated and architecturally sound.** The paper identifies a concrete limitation in prior neural DAG schedulers — they encode compatibility coefficients via fixed-size embeddings or averaging (lines 40–48). The WeCA layer integrates compatibility as a multiplicative bias outside softmax, and the "outside vs. inside" ablation (Table 3) empirically validates this design choice.

2. **The optimality-gap analysis of list scheduling is a genuine theoretical contribution.** Section 4 formalizes why list scheduling's generation map \(S_{list}\) cannot always yield optimal schedules because \(TS_{list}\) is neither the identity nor surjective. Theorem 2 and Assumption 1 provide sufficient conditions for a generation map to retain optimal solutions, directly motivating the skip-action design.

3. **Strong and consistent empirical results.** On TPC-H (Table 1), WeCAN-S(256) improves makespan over the best heuristic by ~18% and over the best neural baseline by ~5–7%. On Computation Graphs (Table 2), improvements are ~13% over heuristics and ~9% over One-Shot. Gains hold across all problem sizes and graph types with low variance.

4. **Generalization experiments support the adaptability claim.** Figure 2 shows WeCAN trained on one environment and tested on varying pool counts, pool types, task counts, and task types maintains ~14–20% improvement over heuristics, while One-Shot drops to ~6–10%.

## Weaknesses

### Fatal

None.

### Major

1. **The main experimental tables (Tables 1 and 2) do not isolate the skip-action contribution.** The skip action is one of four claimed contributions (Section 1, points 3–4) and is the subject of the theoretical analysis in Section 4. Yet Tables 1 and 2 contain no "WeCAN without skip" row. The reader cannot determine how much of the reported improvement comes from the WeCA+LDDGNN architecture versus the skip mechanism. The skip ablation only appears in the heavy-tasks setting (Figure 3), not in the standard setting. Given that the paper positions the skip action as a core contribution that closes the optimality gap, the primary results should include this breakdown.

2. **Figure 3 has a duplicated and misleading label that undermines the skip-action ablation.** The figure description and table both list "WeCAN-S(256)" twice as column headers — once with 8.3% improvement and once with -2.3% improvement (lines 297–302). The fourth column is clearly the non-skipping variant but is labeled identically to the full method. This makes the central comparison (skip vs. no-skip) in the paper's key ablation figure uninterpretable without guesswork.

### Minor

3. **PRO-BALM appears in Figure 3 without any introduction in the main text.** Section 5.1 (Baselines) lists CP, SFT, MOPNR, Tetris, HEFT, PPO-BiHyb, and One-Shot. PRO-BALM is not among them, yet it appears as a bar in Figure 3. The reader cannot assess whether this is a competitive baseline or what its design is.

4. **The non-autoregressive decoder is a significant design choice with minimal discussion in the main text.** Section 3.2 states that action probabilities depend only on the initial state \(s_1\) for "improving scalability," and defers comparison to an autoregressive variant to Appendix B. The policy commits to all action scores upfront and cannot re-score based on evolving state. The main text should at least summarize the trade-off.

5. **The theoretical claims are stated more ambitiously than the evidence supports.** The prose in Section 4 (line 210) says "Theorem 1 demonstrates that our design in the single-pass setting ensures that \(TS\) is a surjection." However, Theorem 1 part (iv) states that *there exist scores* enabling an optimal solution — an existence claim about representational capacity, not a guarantee about the trained policy. This conflation should be corrected.

6. **The three pool-selection rules used to augment heuristic baselines (Section 5.1, line 218) are not specified.** The reader cannot assess whether these rules could inflate or deflate baseline performance.

### Trivial

None.

## Nice-to-Haves

- Adding a "WeCAN without skip" row to Tables 1 and 2 would directly quantify the contribution split and is the single most impactful improvement.
- A brief summary of the autoregressive vs. non-autoregressive comparison from the appendix would help readers assess the cost of the non-autoregressive design choice.
- Including even a small-scale optimal solver comparison (e.g., MILP via Gurobi/CPLEX on tiny instances) would calibrate how far from optimal the learned methods are.

## Removed Points

These points from the input review were removed after verification against the paper:

- **"No One-Shot greedy times reported"** — the paper claims comparable running time to One-Shot-greedy but does not report its time explicitly. This is a minor documentation gap, not a core weakness.
- **"No optimal solver comparison"** — nice-to-have, not a standard expectation for an RL scheduling paper at this stage.
- **"Training variance/sample efficiency not discussed"** — deferred to appendix; not a main-text gap.
- **"Evaluation on more than 3 pools"** — already addressed by Figure 2's generalization to varying pool counts and types.
- **"Introduction claim is vague"** — a stylistic nitpick without substantive impact.
- **"Discrete-time assumption should be acknowledged"** — standard for list scheduling; scope creep.
- **"Exponent form not explained"** — minor design detail, not a weakness.
- **"Bar colors not labeled"** — formatting nitpick; the accompanying table provides the numerical values.
- **"No MLP baseline in ablation"** — the ablation compares against meaningful architectural variants; a plain MLP baseline is not standard for this architecture class.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Fix Figure 3's labeling:** Rename the duplicated "WeCAN-S(256)" column to "WeCAN-no-skip" or "WeCAN-without-skip" and ensure distinct colors with a clear legend.
2. **Add a skip-action ablation to the primary tables:** Add "WeCAN without skip" to Tables 1 and 2, or explicitly state that the skip action's benefit is concentrated in heavy-task cases while the architecture drives improvements in standard settings.
3. **Introduce PRO-BALM in Section 5.1** or remove it from Figure 3 if it is not a standard baseline.
4. **Temper the theoretical claim:** Clarify that Theorem 1 is an existence result about representational capacity, not a learning guarantee.
5. **Summarize the autoregressive comparison** in the main text rather than deferring entirely to the appendix.

MY FINAL SCORE: <score>8.0</score>
MY FINAL DECISION: <decision>Accept</decision>