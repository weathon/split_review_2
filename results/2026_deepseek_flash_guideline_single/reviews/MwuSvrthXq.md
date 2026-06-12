Now I have a clear picture of where this paper sits. Let me write the final consolidated review.

## Summary

This paper proposes WeCAN, an end-to-end reinforcement learning framework for heterogeneous DAG scheduling. It introduces a weighted cross-attention (WeCA) layer that places compatibility coefficients outside softmax to better differentiate tasks with identical attributes but different compatibility profiles, and a longest directed distance GNN (LDDGNN) for dependency encoding. The paper also provides a theoretical analysis of the optimality gap in list scheduling and develops a skip-action mechanism that operates within a single-pass framework. Empirical evaluations on TPC-H and Computation Graphs datasets show consistent makespan improvements over heuristic and neural baselines.

## Strengths

- **Principled weighted cross-attention design (Section 3.1, Eq. on line 121).** The placement of compatibility coefficients *outside* the softmax normalization is well-motivated: two tasks with identical attribute vectors but different numbers of compatible pools should receive different embeddings, and the outside-softmax design achieves this. This is a concrete architectural improvement over approaches that average compatibility coefficients or use fixed-size embeddings (Zhou et al. 2022; Zhadan et al. 2023). The ablation study (Table 3) validates this design choice empirically — the outside-softmax variant (14.0% improvement) consistently outperforms the inside-softmax variant (10.5% improvement).

- **Theoretical analysis of the optimality gap and skip action (Section 4, Theorems 1–2).** The paper formalizes when list scheduling fails to be surjective (Section 4.1), provides criteria for generation maps that can represent optimal solutions (Assumption 1, Theorem 2), and demonstrates how skip actions address this gap within a single-pass framework (Theorem 1). This is a genuine theoretical contribution that goes beyond most empirical scheduling papers.

- **Strong and consistent empirical results with thorough ablation.** Tables 1–2 show makespan improvements up to 18.1% over the best heuristic and 9.5% over One-Shot across both datasets, with 30–40% runtime reduction compared to PPO-BiHyb. Table 3 provides a clean ablation across 7 architectural variants, convincingly validating the WeCA placement (outside vs. inside), location (encoder+decoder vs. decoder-only), and GNN choice (LDDGNN > GAT). The generalization experiments (Figure 2) credibly demonstrate robustness to varying pool counts, task types, and problem sizes.

## Weaknesses

### Fatal
None.

### Major

1. **Missing comparison against heterogeneous-specific neural scheduling baselines.** The paper discusses several methods designed specifically for *heterogeneous* DAG scheduling in the introduction (lines 36–48): READYS (Grinsztajn et al., 2021), Zhou et al. (2022), Zhadan et al. (2023), Wang et al. (2025). These are described as having limitations (e.g., averaging compatibility coefficients, fixed-size embeddings), yet **none are used as experimental baselines**. The neural baselines that are included — One-Shot (designed for homogeneous scheduling) and PPO-BiHyb (a bi-level method not specific to heterogeneous settings) — do not represent the most relevant prior work for the paper's claimed setting. The abstract's claim of "outperforming state-of-the-art methods" is overbroad without direct comparisons to methods that also target heterogeneous scheduling with compatibility constraints. While HEFT (a classic heterogeneous heuristic) and Tetris (multi-resource scheduling) are included, the omission of neural heterogeneous schedulers means the reader cannot fully assess whether the WeCA architecture advances the state of the art or simply outperforms methods not designed for this setting.

### Minor

1. **Limited experimental evidence for the skip-action mechanism, despite its prominence as a contribution.** The skip action is presented as contribution (3) in the introduction, receives substantial theoretical treatment in Section 4, and Theorem 1 claims that it enables representation of optimal solutions. However, the empirical support is confined to a single experiment (Figure 3) on one modified dataset with only one proportion (1% heavy tasks). The paper claims "as the rate of heavy task increases, the gap also increases" (line 194) but provides no experiment varying this rate. No experiment toggles the skip action on/off on standard (non-heavy) datasets to measure its general contribution. The non-skipping variant in Figure 3 is not clearly distinguished from the skipping variant (the parser output shows "WeCAN-S(256)" appearing with two different values, indicating likely labeling ambiguity). Given the theoretical weight placed on this mechanism, the empirical support is disproportionately thin.

2. **The skip score formula is presented without justification or validation against alternatives.** The specific form $u_{\pi_{skip}} = u_a(1 - k/2n)^{u_b} + u_c$ (line 145) is introduced as fixing the optimality gap and preventing over-prioritization of the skip action. No reasoning is given for this particular functional form, and no ablation compares it against alternatives (linear decay, constant score, learned score, etc.). Theorem 1(iv) claims existence of scores enabling optimal solutions, but whether this specific three-parameter parametric form is sufficiently expressive for all problem instances is not argued (the proof is deferred to the inaccessible appendix).

3. **No statistical significance tests or confidence intervals for main results.** Standard deviations are reported for sampling-based variants of WeCAN and One-Shot in Tables 1–2, but greedy results have no variance reported, and the number of random seeds is not stated. Without confidence intervals or statistical tests, it is difficult to assess whether the reported improvements are statistically significant or within the noise floor of the RL training process.

4. **REINFORCE baseline is underspecified.** The baseline $b(X)$ is described as "average rewards" (line 186) without specifying whether this averages across rollouts within a batch, across problem instances, or some other aggregation. No entropy bonus or other variance reduction techniques are mentioned.

5. **Ablation test set is small.** The ablation study (Table 3) is conducted on "10 test problems" per variant (line 308). While standard deviations appear tight, 10 problems is a limited sample for heterogeneous scheduling where instance difficulty varies substantially.

6. **Generalization experiment provides only one data point per condition.** Figure 2 evaluates four fluctuation conditions (more pool, more pool type, more task, more task type) with one data point each and no repeated trials, providing thin evidence for claims about robust generalization.

### Trivial
None.

## Nice-to-Haves

- Compare against at least one heterogeneous-specific neural scheduler (READYS or Zhou et al. 2022) to validate the SOTA claim.
- Test the skip-action ablation on standard (non-heavy) datasets and vary the proportion of heavy tasks to support the claimed monotonic relationship.
- Compare the skip score formula against alternative decay schedules.
- Report confidence intervals or statistical tests for main results.
- Clarify the training configuration: number of random seeds, batch size, learning rate schedule, number of training episodes.
- Report the number of seeds used for main experiments.

## Removed Points

The following points from the input review were removed per the filtering rules (moved here for completeness but excluded from the assessment):

- Criticisms about missing appendix content (proofs in Appendix A, details in Appendix G) — the parser strips appendices from all papers; these exist in the original submission.
- Concern about "WeCAN-S(256)" appearing twice in Figure 3 — this is a parser formatting artifact; the original figure likely has distinct labels.
- "Hyperparameter reporting" (learning rate, hidden dimensions, number of layers) — removed per the rule that undisclosed hyperparameters are nitpicks about reproducibility that should not be counted as weaknesses.
- "Single-seed results" — the paper reports standard deviations (Table 1 footnote: "standard deviation among random seed"), indicating multiple seeds were used, though the exact number is not stated explicitly.
- Formatting/style nitpicks and parser artifacts.
- Speculative criticisms about what may or may not be verifiable from the appendix.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add heterogeneous-specific baselines.** The single highest-impact improvement would be to compare against at least one of READYS, Zhou et al. (2022), or Zhadan et al. (2023) — methods specifically designed for heterogeneous DAG scheduling. Even a comparison on a subset of the datasets would substantially strengthen the empirical claims.

2. **Strengthen the skip-action evaluation.** (a) Run WeCAN with and without the skip action (everything else identical) on standard TPC-H and Computation Graphs datasets, not just on the heavy-task variant. (b) Vary the heavy-task proportion (e.g., 0.5%, 1%, 5%, 10%) to support the claim that "as the rate of heavy task increases, the gap also increases." (c) Clearly label the non-skipping variant in the figure.

3. **Validate the skip score parameterization.** Either provide theoretical justification for why the form $(1 - k/2n)^{u_b}$ is sufficient to represent optimal schedules (as required by Theorem 1(iv)) or compare against alternative decay schedules empirically.

4. **Report statistical significance.** Add confidence intervals or paired statistical tests for the main results, and explicitly state the number of random seeds used.

5. **Clarify training details.** Specify the aggregation for the REINFORCE baseline, learning rate schedule, batch size, and number of training episodes.

## Score and Decision

### Calibration anchors

All anchors from retrieval rounds:

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| Uj0h13lVrR.md | 1.00 | R1 | Unrelated topic; much weaker paper |
| bEgDEyy2Yk.md | 1.00 | R1 | Unrelated topic; much weaker paper |
| 5kMwiMnUip.md | 1.40 | R1 | Unrelated topic; much weaker paper |
| bntJK4NyIW.md | 2.00 | R1 | Decentralized training; weaker evaluation than our paper |
| ArJikvI6xo.md | 3.40 | R1 | FL heterogeneity; less relevant, similar score tier |
| **10eQ4Cfh8p.md** | **3.00** | R1 | **RL for FJSP scheduling; most comparable rejected paper — weaker ablation, no std devs, less architectural novelty** |
| b9aCXHhdbv.md | 4.50 | R1 | Pipeline parallelism DRL; less thorough evaluation |
| **8WtBrv2k2b.md** | **5.00** | R1 | **Quantum resource scheduling RL; similar structure but unclear claims** |
| CJEBFNBLhO.md | 4.25 | R1 | Massively parallel CO environments; different contribution type |
| K7l94Z81bH.md | 5.25 | R1 | Dispatch RL; well-executed but different problem |
| Dgc5RWZwTR.md | 4.75 | R2 | Multi-task CO training; weaker empirical support |
| Kc3yoIL5oR.md | 5.25 | R2 | Unified CO model; mixed reviews, rejected |
| DKfcxPxunu.md | 5.75 | R2 | Multi-task routing; mixed reviews, rejected |
| CFLEIeX7iK.md | 5.75 | R2 | Neural solver selection; rejected |
| **yEwakMNIex.md** | **6.25** | R2 | **Unified neural CO; accepted — clean evaluation against relevant baselines** |
| **TbTJJNjumY.md** | **6.25** | R2 | **Large-scale VRP with cross-attention; accepted — good baselines, clear contribution** |
| **AloCXPpq54.md** | **6.00** | R2 | **Sequential stochastic CO with HRL; accepted — novel problem, clean evaluation** |
| GM7cmQfk2F.md | 7.00 | R2 | Multi-objective CO; stronger empirical validation |
| jBYQAtzp5Z.md | 6.80 | R1 | Scheduling with predictions; accepted — rigorous theory |
| Cs6MrbFuMq.md | 6.00 | R1 | Heterogeneous LLM inference; accepted |
| hB2hXtxIPH.md | 7.00 | R1 | Heterogeneous MARL; accepted |

**Round 1 bracket:** 4.5–6.5  
**Round 2 narrowing:** Compared to accepted papers at 6.0–6.25 (AloCXPpq54, yEwakMNIex, TbTJJNjumY), this paper has comparable contributions but is held back by the missing heterogeneous-specific baselines and limited skip-action evidence. Compared to rejected papers at 4.75–5.75, this paper has stronger architectural novelty and more thorough ablation.  
**Final score:** 5.5

The paper presents genuine architectural (WeCA) and theoretical (skip action optimality gap) contributions with solid ablation support. However, the evaluation does not compare against the most relevant prior work for the claimed setting (heterogeneous DAG scheduling with compatibility), and the empirical support for the skip-action mechanism is disproportionately thin relative to its theoretical prominence. The contribution is real but the empirical case is incomplete.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>