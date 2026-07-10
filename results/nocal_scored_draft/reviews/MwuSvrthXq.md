Now I have all the verification I need. Let me produce the final consolidated review.

## Summary

This paper proposes WeCAN, an end-to-end reinforcement learning framework for heterogeneous DAG scheduling with task-pool compatibility coefficients. The key technical contributions are: (1) a weighted cross-attention (WeCA) mechanism that places compatibility coefficients outside softmax to preserve distinguishability across tasks with different compatibility profiles; (2) a longest-directed-distance GNN for encoding task dependencies; (3) a skip-action mechanism adapted to the single-pass setting, with theoretical analysis showing it enables the generation map to represent optimal solutions. Empirical results on TPC-H and Computation Graphs benchmarks show consistent improvements over existing neural and heuristic schedulers.

## Strengths

- **Well-motivated and principled architectural design (Section 3.1, Eq. 2).** The weighted cross-attention mechanism that places compatibility coefficients *outside* the softmax is justified with a concrete reasoning example (lines 124-126) explaining why the "outside" placement preserves distinguishability across tasks with different compatibility profiles. This is a genuine architectural insight, not an off-the-shelf component.

- **Consistent and substantial empirical improvements (Tables 1, 2).** Across both datasets and all problem sizes, every variant of WeCAN outperforms all baselines. Improvements are not marginal: 7.7% over the best neural baseline on TPC-H and 9.5% on Computation Graphs. These improvements are consistent across all six data configurations.

- **Skip-action mechanism with theoretical grounding (Section 4, Theorem 1).** The paper identifies a real gap in list-scheduling-based methods and provides an existential guarantee (Theorem 1, parts ii–iv) that the skip-augmented generation map can represent optimal solutions. The practical design of the skip score as a parametric function of the step count (Eq. 3) is a clean way to introduce this capability in the single-pass setting without per-step network inference.

- **Strong ablation study (Table 3).** The ablation compares 7 architectural variants including two different GNN backbones (GAT forward, GAT bidirectional), two versions of WeCA (inside vs. outside), and partial ablation of WeCA layers. All ablated variants are worse, and the relative ordering is clean and monotonic.

- **Generalization experiments (Figure 2).** Evaluating on environments with more pools, more pool types, more tasks, and more task types than training demonstrates that the adaptability claim is tested, not just stated. The gap over One-Shot widens in out-of-distribution settings (e.g., 20.4% vs. 9.2% improvement for "more pool"), directly supporting the claim that the weighted cross-attention mechanism preserves adaptability better than fixed-size embedding alternatives.

## Weaknesses

### Fatal

None.

### Major

- **The theoretical claim about closing the optimality gap conflates representation capacity with learned policy performance.** Theorem 1(iv) states that there *exist* scores enabling an optimal solution — this is a guarantee about the *representation capacity* of the generation map, not about the REINFORCE-trained policy. The paper repeatedly uses phrases like "closing the optimality gap" (lines 65, 145, 190, 210, 314) and "this approach fixes the optimality gap" (line 145) that imply the learned system overcomes the gap, but the theoretical result only covers the generation map, not whether training will find those scores. This is a framing issue: the existential guarantee is meaningful, but it should be clearly separated from the empirical question of whether the trained policy realizes it.

- **The non-auto-regressive decoder commits the policy to fixed action scores computed once from the initial state (Section 3.2, lines 137-143):** $p_\theta(\pi_l | s_t, \pi_{<l})$ reduces to $p_\theta(\pi_l | s_1)$, meaning the network runs once and produces scores that never update as tasks are scheduled. The only dynamic element is the skip score (which depends on $k$, the step count). This means the policy cannot re-prioritize tasks based on which tasks have been scheduled, what resources are currently occupied, or how the schedule is unfolding. The paper presents this purely as a speed advantage but under-discusses the trade-off in scheduling flexibility. The comparison against One-Shot, which has the same limitation, is fair, but the framing of the method's capabilities should acknowledge this limitation more directly.

### Minor

- **The skip score decay formulation ($u_{\pi_{skip}} = u_a(1 - k/2n)^{u_b} + u_c$, Eq. 3) is not empirically validated against simpler alternatives.** The paper justifies the design to prevent skip from being "overly prioritized" (line 145), but provides no ablation showing that this specific parametric decay is necessary or that simpler formulations (e.g., a constant learned score with a decaying mask) would not work as well.

- **The table in Figure 3 includes a "PRO-BALM" column that is never introduced or explained in the main text (lines 299-302).** The baseline list in Section 5.1 does not mention PRO-BALM. Additionally, the table appears to have duplicate "WeCAN-S(256)" column headers, suggesting a possible rendering or labeling issue that obscures the experimental setup.

- **The main text does not specify the number of random seeds used for the reported standard deviations** (Tables 1, 2 state "standard deviation among random seed" but omit the count). While training details may be in the appendices, the seed count is a basic experimental design parameter relevant for assessing statistical reliability.

### Trivial

None.

## Nice-to-Haves

- Reporting training time and computational resources required would help practitioners evaluate adoption costs.
- Ablating the heavy-task proportion (e.g., 0.5%, 1%, 2%, 5%) in the main text would more directly substantiate the claim that the skip-action benefit increases with heavy-task proportion (currently referenced to Appendix C).

## Removed Points

These points are flagged to be removed, treat them with caution:
- Heavy-task experiment lacking varying proportions (the paper explicitly references Appendix C for this evidence; parser strips appendices, so this cannot be evaluated as a main-text flaw)
- Missing training details (reproducibility hyperparameter nitpicks are excluded per review guidelines; paper references Appendices D, E, H for experimental details)
- Various Section-by-Section formatting/style notes (compatibility coefficient prose clarification, LDDGNN mask description terse, figure caption verbosity)
- Statistical rigor complaint about greedy mode reporting no variance (standard for deterministic greedy decoding)

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add a short discussion in Section 3.2 acknowledging the fixed-score limitation of the non-auto-regressive decoder and contrast with auto-regressive alternatives (the comparison is referenced to Appendix B but a concise main-text note would help readers).
2. In the presentation of Theorem 1, explicitly separate the existential representation-capacity guarantee from the empirical question of whether training finds those scores, perhaps in a short paragraph after the theorem statement.
3. Include an ablation comparing the proposed skip-score decay formulation against a simpler constant-learned-score variant.
4. Clarify the Figure 3 table: label all columns consistently, and introduce PRO-BALM (or correct the parser-corrupted column header) in the main text baseline description.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>