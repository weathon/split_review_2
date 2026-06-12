Now I'll write the final consolidated review.

## Summary

This paper proposes WeCAN, an end-to-end RL framework for heterogeneous DAG scheduling with task-pool compatibility. Key innovations are (1) a weighted cross-attention (WeCA) layer that places task-pool compatibility coefficients outside the softmax normalization to preserve distinguishability, (2) a longest directed distance GNN for encoding DAG dependencies, and (3) a parametric skip-action mechanism that closes the optimality gap of list scheduling while preserving single-pass inference speed. The paper provides theoretical analysis of the optimality gap (Theorem 1, 2) and demonstrates strong empirical results on TPC-H and Computation Graphs benchmarks.

## Strengths

1. **Well-motivated weighted cross-attention design (Section 3.1, Eq. 119–121)** — The paper identifies a subtle architectural issue: placing compatibility coefficients *inside* softmax causes tasks with identical features but different compatibility profiles to receive indistinguishable embeddings due to normalization. The outside-softmax placement preserves this information. Ablation (Table 3) directly validates the design: the inside version yields 10.5% improvement vs. 14.0% for the full model on TPC-H-30 — a 3.5 percentage-point gap directly attributable to this architectural choice.

2. **Single-pass skip action with theoretical grounding (Theorem 1, Figure 3)** — Prior skip-action methods (Mao et al., 2016) required multi-round network inference, sacrificing speed. This paper derives a parametric skip score computed from a single forward pass and proves (Theorem 1.iii–iv) that without skip the policy cannot assign positive probability to optimal solutions for some instances, while with skip it can. Heavy-task experiments confirm the benefit: 8.3% improvement with skip vs. 2.6% without on TPC-H-30-heavy.

3. **Formal analysis of list scheduling optimality gap (Section 4, Theorem 2, Assumption 1)** — Rather than merely observing that list scheduling can be suboptimal, the paper formalizes the problem through the lens of the TS map not being identity or surjective. Assumption 1 and Theorem 2 give precise criteria for generation maps capable of producing optimal solutions. This goes beyond prior heuristic analyses.

4. **Strong and consistent empirical results (Tables 1–2, Figure 2)** — WeCAN outperforms all baselines including HEFT, Tetris, PPO-BiHyb, and One-Shot across both real-world TPC-H and synthetic Computation Graphs datasets (up to 18.1% over best heuristic, 7.7% over best neural baseline). Standard deviations are very small relative to improvements, suggesting statistical reliability. Generalization experiments (Figure 2) show WeCAN maintains 6.7–20.4% improvement under environment shifts (pool count, pool types, task count, task types), while One-Shot drops to 0.9% under pool-type shifts — directly validating the adaptability claims.

5. **Computational efficiency (Tables 1–2)** — WeCAN-Greedy runs in 0.15–1.72s on TPC-H datasets, comparable to or faster than heuristics (CP: 0.29–3.35s) and orders of magnitude faster than PPO-BiHyb (20–179s), while achieving strictly better makespan. This combination of quality and speed is a non-trivial achievement.

## Weaknesses

### Fatal
None.

### Major

1. **Missing comparison against directly relevant heterogeneous neural schedulers** — The related work (lines 36–48) cites Zhou et al. (2022), Zhadan et al. (2023), and Wang et al. (2025) as neural methods specifically designed for heterogeneous DAG scheduling — the same core problem addressed by WeCAN. The paper also mentions Grinsztajn et al. (2021), another RL method for heterogeneous dynamic scheduling. Yet the experimental evaluation (Section 5.1) only compares against PPO-BiHyb and One-Shot as neural baselines. Without comparisons against these methods, the claim of "outperforming state-of-the-art methods" (abstract) is supported only against a subset of the most relevant SOTA. This does **not** invalidate the method or its demonstrated gains over included baselines, but it weakens the scope of the empirical positioning. The ablation study and generalization experiments independently validate the core architectural claims; this gap is about the *comparative* claim.

### Minor

1. **Heuristic skip score formula with limited grounding from the theoretical analysis** — Theorem 1 proves expressiveness (there exist scores enabling optimality) but does not justify why the specific parametric form $u_a(1 - k/2n)^{u_b} + u_c$ is well-suited for *learning*. The claim that the design "clusters most poor solutions in the high-$u_a$, high-$u_c$ region" (Section 4.2) is stated without empirical analysis of learned coefficient values or sensitivity analysis. While the heavy-task experiments (Figure 3) validate the mechanism empirically, the link between the formal theory (Assumption 1, Theorem 2, ideal map $S_n$) and the practical implementation could be tighter.

2. **Figure 3 labeling issues** — The heavy-task experiment figure lists "WeCAN-S(256)" twice with different values (8.3% and −2.3%). From context, the second instance is likely WeCAN without skip, but the identical label makes the figure uninterpretable without cross-referencing the text. Additionally, "PRO-BALM" appears in this figure but is not defined in the main text baselines (Section 5.1). These are presentational issues that should be corrected.

3. **Skip score dependence only on step count** — The skip score depends only on step index $k$ (beyond the three global coefficients $u_a, u_b, u_c$ derived from average embeddings). This means it cannot adapt to the dynamic state of resource usage mid-schedule. This limitation should be acknowledged.

### Trivial
None.

## Nice-to-Have

1. Analysis of learned skip coefficients ($u_a, u_b, u_c$) after training (e.g., histograms or typical ranges) to empirically verify the claim about clustering of poor solutions.
2. Including at least one of the cited heterogeneous neural methods (Zhou et al., 2022; Zhadan et al., 2023; Wang et al., 2025) as a baseline to strengthen the comparative evaluation.
3. Reporting raw makespan values alongside the improvement percentages in the generalization experiments (Figure 2) to help calibrate the magnitude of the improvements.

## Removed Points

- **Criticism about the outside-softmax illustrative example (Harsh Critic):** The critic constructed a specific numerical scenario where both inside and outside versions produce the same embedding, claiming the paper's argument is flawed. The critic's calculation relies on a contrived choice of compatibility coefficients (values chosen so that they happen to sum to the same total) and does not invalidate the paper's core point about the structural limitation of the inside version (normalization fundamentally washes out scale information). The paper's architectural choice is validated by ablation (Table 3: 14.0% vs. 10.5% improvement). **Removed** as the criticism is not substantiated against the actual paper's claims.

- **Criticism about missing implementation details (baseline computation, learning rate, hardware, LDDGNN dimensionality):** Per the hard rules, missing appendix/proofs details are removed as the appendix was stripped by the parser and these details likely appear there.

- **Criticism about REINFORCE baseline ambiguity ("average rewards"):** Appendix was stripped; this detail likely appears there.

- **Generic concerns about reproducibility (hyperparameters, training details):** These are standard details for the appendix and are not required to appear in the main text.

## Novel Insights

Beyond the paper's own contributions, the most notable insight from the reviews is the observation that the generalization experiments (Figure 2) provide particularly strong evidence for the WeCA design's effectiveness: under "more pool type" shifts where compatibility profiles change qualitatively, WeCAN maintains 6.7% improvement while One-Shot collapses to 0.9%. This 5.8 percentage-point gap specifically validates the claim that WeCA's outside-softmax placement of compatibility coefficients enables genuine adaptability rather than overfitting to a fixed pool configuration. The ablation study's systematic degradation pattern (Table 3) further confirms that each architectural component contributes positively, with the WeCA encoder being particularly crucial (dropping it causes −4.2% on TPC-H-50).

## Suggestions

1. Add at least one directly comparable heterogeneous neural scheduler (e.g., Zhou et al., 2022 or Wang et al., 2025) as a baseline to strengthen the comparative evaluation.
2. Fix the duplicate "WeCAN-S(256)" label in Figure 3 and define PRO-BALM in the main text.
3. Provide analysis of learned skip coefficients ($u_a, u_b, u_c$) to empirically ground the claim about clustering of poor solutions.
4. Acknowledge the limitation that the skip score depends only on step index rather than the full mid-schedule state.

## Score Calibration

**Round 1 (Bracketing) — 6 queries spanning score bands:**
- Band (−1.0, 1.5): anchor papers at 1.0 (GFlowNet KL divergence), 1.0 (financial news impact). Our paper is clearly not in this band.
- Band (1.5, 3.5): FJSP RL paper at 3.0 (no ablation, missing baselines, sloppy writing). Our paper is substantially stronger.
- Band (3.5, 5.5): GNN NCO paper at 5.33 (unfair baseline comparisons, narrow setting); QRF-GNN at 4.25 (limited novelty, no ablation). Our paper is stronger than both.
- Band (5.5, 7.5): SSCO HRL at 6.0 (accepted — solid RL+CO but design justification gaps); PO for CO at 5.75 (rejected — limited scope, missing SOTA); CoRMAB at 6.0 (accepted — novel problem but lacks theory, missing baselines). Our paper has comparable or better empirical rigor and stronger theoretical grounding than these.
- Band (7.5, 8.5): Papers at 8.0 (robotics RL, attention mechanisms, differential transformer) — different domains and higher polish level. Our paper does not reach this band.

**Narrowing (Round 2):** Search within (6.5, 7.5) returned four anchors at 6.6–6.8 (accepted). Neural Spacetimes at 6.8 (accepted) — has theoretical guarantees but lacks real-world task evaluations, similar pattern to our paper. Competitive Fair Scheduling at 6.8 (accepted) — theory paper with predictions framework.

**Final score: 6.5.** The paper has clear novel contributions (WeCA architecture, skip mechanism in single-pass), solid theoretical analysis, and comprehensive experiments with strong results. The main factor preventing a higher score is the missing comparison against directly related heterogeneous neural schedulers cited in the related work. This is a genuine evidential gap, but the paper's core contributions are independently validated by ablation and generalization experiments.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>