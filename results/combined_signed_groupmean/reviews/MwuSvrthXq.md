Now I have sufficient calibration data. Let me produce the final consolidated review.

---

## Summary

This paper proposes WeCAN, an end-to-end RL framework for heterogeneous DAG scheduling with task-pool compatibility. Two core contributions are (1) a weighted cross-attention (WeCA) layer that places compatibility coefficients outside softmax normalization, enabling the network to preserve distinguishability between tasks with identical features but different compatibility profiles; and (2) integrating skip actions (advancing time to the next completion event) into single-pass network inference, supported by a theoretical analysis (Theorem 1) showing this design can represent optimal solutions where list scheduling cannot. Experiments on TPC-H and Computation Graphs benchmarks show 7.7–9.5% improvements over the best neural baseline and 13.4–18.1% over heuristics, with informative ablations and zero-shot generalization experiments.

## Strengths

1. **Well-motivated architectural contribution: weighted cross-attention (WeCA).** The design choice to place compatibility coefficients *outside* the softmax normalization (Eq. 2) is supported by a concrete counterexample: two tasks with identical attribute vectors but different compatibility profiles. Inside-softmax placement would collapse them to the same embedding; outside placement preserves distinguishability. This is a clean, specific technical decision that follows from the problem structure rather than generic architecture hacking.

2. **Skip-action integration into single-pass inference is non-trivial and theoretically grounded.** The paper's key algorithmic contribution — enabling skip actions (advancing time to the next completion event) within a single-pass network — addresses a genuine limitation of list-scheduling-based neural schedulers. The skip score formula is a simple but effective design that prevents endless idling while maintaining single-pass efficiency. Theorem 1's claim that this design allows representing optimal solutions is a meaningful theoretical result.

3. **Strong empirical results with clean ablations.** On TPC-H, WeCAN-S(256) achieves 18.1% improvement over the best heuristic and 7.7% over the best neural baseline (One-Shot). On Computation Graphs, the improvements are 13.4% and 9.5% respectively. The ablation study (Table 3) systematically isolates the contributions of WeCA placement, LDDGNN, and skip actions, with consistent degradation when any component is removed or replaced.

4. **Generalization experiments (Figure 2) address a real practical concern.** The paper tests whether a policy trained on one environment configuration transfers to configurations with more pools, more pool types, more tasks, or more task types. WeCAN-S(256) consistently outperforms One-Shot-S(256) in these zero-shot generalization settings, with gaps as large as 15.9 percentage points (20.4% vs 9.2% for "more pool").

## Weaknesses

### Major

1. **Incomplete neural baseline comparison weakens the "outperforming state-of-the-art" claim.** The paper cites Lin et al. (2024), Wang et al. (2025), Li et al. (2024), and Sun et al. (2024) in the introduction as related work on neural DAG scheduling and heterogeneous scheduling, yet compares against only PPO-BiHyb (2021) and One-Shot (2023) in experiments. If these methods address different problem variants, the paper should say so explicitly. If they can be compared, the experimental evaluation is incomplete. The abstract's claim of "outperforming state-of-the-art methods" (line 9) is not fully supported by the chosen baselines.

### Minor

2. **Unsupported claim about clustering of poor solutions.** Section 4.2 asserts that skip actions "cluster most poor solutions in the high-*u_a*, high-*u_c* region" and that "excessive skips typically arise from large values of *u_a* and *u_c*" (line 210). This is an important claim for the variance-reduction argument, but the paper provides no analytical proof or empirical evidence (e.g., a scatter plot of *u_a* vs *u_c* for sampled trajectories colored by makespan) to support it. Without evidence, this claim reads as speculation.

3. **"Heavy task" not quantitatively defined.** The paper modifies TPC-H datasets by replacing 1% of tasks with "heavy tasks" (line 310) but does not specify the resource demand multiplier or duration multiplier used. Without this quantitative definition, the heavy-task experiment cannot be reproduced or meaningfully interpreted. (The paper does reference Appendix C for varying heavy-task proportions, which was stripped by the parser; this point concerns only the missing quantitative definition in the main text.)

4. **Figure 3 has confusing labeling.** The data table shows two entries labeled "WeCAN-S(256)" with different values (8.3% and -2.3%) and different bar colors (blue and green), while the caption lists both as "WeCAN-S(256)". One of these is presumably the variant without skip actions, but this is not clearly distinguished, making the figure difficult to interpret without guessing.

### Trivial

5. **Greedy results lack standard deviation.** WeCAN-Greedy and all heuristic baselines in Tables 1 and 2 report only single numbers without standard deviation, unlike the sampling variants which do report std devs. This makes it impossible to assess the statistical significance of the greedy results.

6. **Theorem 1(iv) caveat.** Theorem 1(iv) states there *exist* scores enabling an optimal solution by greedy selection — an existence result that does not guarantee REINFORCE training will find these scores. The paper could be clearer about this limitation to prevent readers from inferring stronger guarantees than the theorem provides.

## Nice-to-Haves

- A brief proof sketch or intuition for how the skip score formula *u_a*(1 − *k*/2*n*)^(*u_b*) + *u_c* connects to the surjectivity claimed in Theorem 1.
- Training details in the main paper (learning rate, number of episodes, convergence criteria) rather than only in the appendix.
- Clarification in the PPO-BiHyb comparison that the runtime gap is expected given the different inference paradigms (multi-round beam search vs single-pass).

## Removed Points

The following points from the input review were removed with justification:

- *"Heavy-task evaluation never varies heavy-task proportion"* — The paper states at lines 194 and 210 that varying-proportion results are in Appendix C. Per guidelines, weaknesses about content stripped by the parser are removed. The kept point is about the missing *definition* of "heavy task" in the main text.
- *"PPO-BiHyb comparison conflates quality and compute budget"* — The paper transparently presents both makespan and runtime for all methods; the reader can assess the trade-off. This is not a genuine weakness.
- *"Missing training details undermine reproducibility"* — Training details are deferred to appendices (standard practice in this field). Per guidelines, complaints about hyperparameters deferred to appendices are removed.
- *Several section-by-section observations* that were editorial notes rather than actionable weaknesses.
- *"Strengthening the Paper on Its Own Terms" items* — These were suggestions, not weaknesses, and are folded into Nice-to-Haves above.

## Novel Insights

None beyond the paper's own contributions. The reviews surface genuine strengths (motivated WeCA design, theoretical analysis of the optimality gap, strong empirical validation) and specific areas for improvement, but do not identify structural issues or alternative framings that the paper itself does not already address.

## Suggestions

- Justify the exclusion of recently cited neural scheduling methods (Lin et al. 2024, Wang et al. 2025) from experimental comparison, or include them in the evaluation.
- Quantitatively define "heavy task" (resource demand multiplier, duration multiplier) in the main paper.
- Provide empirical support (e.g., a scatter plot of *u_a* vs *u_c* for sampled trajectories, colored by makespan) for the claim that poor solutions cluster in the high-*u_a*, high-*u_c* region.
- Fix Figure 3 to clearly distinguish the skip-action variant from the non-skip variant.
- Add a brief caveat after Theorem 1(iv) that this is an existence result and training may not find these scores.

---

**Calibration summary.** Anchors retrieved across all rounds:

| File | Avg Score | Round | Itemized? | Comparison |
|---|---|---|---|---|
| Pipeline Parallelism DRL (b9aCXHhdbv) | 4.50 | R1 | Yes | Weaker strengths (+1.29 to +2.39) vs our paper (+9.66 to +10.00); our paper is clearly stronger. |
| Massively Parallel CO (CJEBFNBLhO) | 4.25 | R1 | No | Engineering contribution; lower technical depth than our paper. |
| VRP Cross-Attention (TbTJJNjumY) | 6.25 | R2 | Yes | Similar strength profile (+8.57 to +10.00) and similar decisive weakness (missing baselines -10.00); accepted. |
| Bin Packing Encoder-Decoder (6hvtSLkKeZ) | 6.40 | R2 | Yes | Similar strength profile (+5.11 to +10.00) with multiple -10.00 weaknesses; accepted. |
| Competitive Fair Scheduling (jBYQAtzp5Z) | 6.80 | R1,R3 | Yes | Stronger theoretical contribution, fewer weaknesses; accepted. |

**Round 1 bracket:** 5.5–7.0. **Round 2 narrowing:** Our paper shares the profile of accepted NCO papers at 6.0–6.5: very strong strengths (+9.66 to +10.00 for all four) combined with one or two decisive weaknesses (missing baselines, unsupported claim). It is clearly above the rejected 4.0–5.0 band (where papers have weak strengths), but below the strongest 6.5+ papers (which have fewer or milder decisive weaknesses). **Final score: 6.0.**

---

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>