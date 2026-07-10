## Summary

This paper proposes WeCAN, an end-to-end reinforcement learning framework for heterogeneous DAG scheduling with task-pool compatibility coefficients. It introduces three main components: (1) a weighted cross-attention (WeCA) mechanism that places compatibility coefficients outside the softmax normalization, enabling pool-count-agnostic encoding; (2) a longest-directed-distance GNN (LDDGNN) for encoding task dependencies; and (3) a skip-action mechanism that allows the scheduler to advance time to the next completion event, designed specifically for the single-pass (non-autoregressive) setting. The paper also provides a theoretical analysis of the optimality gap inherent in list-scheduling-based methods. The framework generates schedules through single-pass network inference, achieving runtime comparable to heuristics while significantly outperforming prior neural and heuristic methods across TPC-H and Computation Graphs benchmarks.

## Strengths

- **The weighted cross-attention (WeCA) mechanism with compatibility coefficients placed outside softmax normalization (Eq. 2, Section 3.1) is a genuine architectural contribution.** The ablation (Table 3: WeCA vs. WeCA-inside, 14.0% vs. 10.5% improvement) empirically confirms this design choice matters, addressing a real limitation in prior work where compatibility information is averaged or one‑hot encoded into fixed‑dimensional representations. This design maintains adaptability across varying numbers of pools and task types.

- **The skip-action design for the single-pass non-autoregressive setting is technically nontrivial (Section 3.2).** The parametric decay formula \(u_a(1 - k/2n)^{u_b} + u_c\) prevents the endless-idling problem that would arise from a fixed skip score. Theorem 1 provides formal guarantees on feasibility (within \(2n\) steps) and expressivity (optimal solutions are representable), and the heavy-task ablation (Figure 3) validates its practical benefit.

- **The theoretical analysis of the list-scheduling optimality gap (Section 4) provides a clean mathematical characterization**, framing the gap in terms of the generation map \(S_{\text{list}}\) not being surjective (\(TS_{\text{list}}\) is neither identity nor onto). Theorem 1(iv) shows the skip-augmented system can represent optimal solutions by greedy selection — a meaningful expressivity guarantee that justifies the architectural choices.

- **Empirical results are strong and consistent across all datasets and problem sizes (Tables 1‑2).** On TPC-H-100, WeCAN-S(256) achieves makespan 61,373 vs. One-Shot-S(256) at 66,173 (~7.3% improvement) and the best heuristic HEFT at 70,137 (~12.5%). Standard deviations are remarkably small (e.g., ±10 on TPC-H-30), suggesting reliable training. Runtime is competitive with heuristics (WeCAN-greedy at 0.15 s on TPC-H-30 vs. HEFT at 0.18 s).

- **Generalization to varying environments is demonstrated (Figure 2)**, with WeCAN significantly outperforming One-Shot under distribution shift (e.g., 20.4% vs. 9.2% improvement for "more pool"). This validates that the WeCA design preserves adaptability across heterogeneous configurations — precisely where the architecture's pool-count-agnostic design should help most.

## Weaknesses

### Fatal

None.

### Major

- **The paper conflates theoretical expressivity with practical learnability when claiming the skip action "closes" or "fixes" the optimality gap (lines 65, 145, 314).** Theorem 1(iv) shows the skip-augmented policy class *can* represent optimal solutions — this is an expressivity result. But the paper's rhetoric implies the training will *find* those solutions. The skip action turns a *structural* gap (optimal solution unreachable under list scheduling) into an *optimization* gap (optimal solution is representable but may not be found by REINFORCE, depending on gradient noise, reward landscape, and the parametric skip-score design). The paper should acknowledge this distinction. This is a framing issue rather than a flaw in the empirical results — the strong performance on tested benchmarks supports the method — but the claim goes beyond what the theory alone guarantees.

### Minor

- **The non-autoregressive decoder's limitations are under-discussed.** Because action probabilities depend only on the initial state (Section 3.2), the policy cannot adapt its preferences based on which tasks have already been scheduled — relative scores of remaining actions are frozen at inference time. The paper presents this design choice only as an advantage ("preserving single-pass efficiency") without discussing situations where contingent decision-making (e.g., "if task A is assigned to pool 1, then task B should go to pool 2") could be important. The comparison with autoregressive decoders is deferred to Appendix B.

- **Heuristic baselines (SFT, MOPNR, CP, HEFT, Tetris) in Tables 1‑2 are reported without standard deviations or instance-level variance.** While heuristics are deterministic per instance, it is unclear whether results are averaged across test instances. Reporting this would help assess whether improvements over heuristics are statistically significant relative to instance-level variability.

- **PRO-BALM appears in Figure 3 but is never explained in the main paper text.** The column labeling is also ambiguous: two columns labeled "WeCAN-S(256)" show different values (8.3% and −2.3%), where one apparently corresponds to a non-skipping variant. This makes the heavy-task ablation difficult to interpret from the main text alone.

### Trivial

None.

## Nice-to-Haves

- A scaling curve (makespan vs. number of samples) for WeCAN-S(n) would show whether S(256) is near saturation or whether further gains are possible.
- A brief discussion of alternative skip-score designs (e.g., learned step-dependent scores via a small network) would contextualize the parametric choice.

## Removed Points

These points are flagged to be removed; treat them with caution:
- Criticisms about LDDGNN being "described too briefly" in the main text (details are in Appendix G, which was stripped by the parser; this is a presentation nitpick, not a substantive weakness).
- Request for missing training details (training time, compute resources, convergence criteria) — removed per guideline on reproducibility nitpicks.
- The observation about "clustering property" (line 210) lacking formal proof — this is a valid observation but is better classified as a minor imprecision, not a critical weakness, since the core contribution does not depend on it.
- Section-by-section notes that were purely descriptive or positive without identifying an actionable weakness.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Revise the language around "closing the gap"** to distinguish structural representability from optimization. For example: "Theorem 1 shows the skip-augmented framework has sufficient expressivity to represent optimal solutions, overcoming a structural limitation of list scheduling. Whether the learned policy finds these solutions depends on optimization dynamics; our empirical results suggest REINFORCE reliably does so on the tested distributions."
2. **Clarify the PRO-BALM entry** and fix the duplicate "WeCAN-S(256)" column labels in Figure 3.
3. **Add a brief discussion** of when the non-autoregressive design could be a limitation and why this does or does not arise on the paper's benchmarks.
4. **Report instance-level variance** for heuristic baselines to enable better statistical comparison.

---

## Score and Decision

This is a strong paper with a genuine architectural contribution (WeCA), a technically nontrivial skip-action mechanism for the single-pass setting, a clean theoretical framing, and consistently strong empirical results across multiple datasets and generalization scenarios. The main weakness is a rhetorical overclaim about "closing the optimality gap" that conflates representability with learnability — this is fixable with revised language and does not undermine the empirical findings. The non-autoregressive design limitation is acknowledged but under-discussed. Overall, the paper makes a meaningful and well-validated contribution to neural DAG scheduling for heterogeneous environments.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>