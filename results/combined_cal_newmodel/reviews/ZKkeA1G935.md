Now I have a clear picture. Let me finalize the review.

## Summary

This paper studies whether LLMs can alleviate catastrophic forgetting in Graph Continual Learning (GCL). It makes three contributions: (1) exposing a task-ID leakage flaw in the local-testing evaluation setup used by prior GCL work; (2) introducing LLM4GCL, a benchmark evaluating 9 methods across 7 text-attributed graph datasets under NCIL and FSNCIL settings; and (3) proposing SimGCL, a method combining ego-graph-prompted instruction tuning with LoRA in the first session, followed by frozen prototype classification.

## Strengths

- **[Strong]** Exposing the task-ID leakage flaw in local testing (Section 3.1, Table 1): The paper cleanly demonstrates that under the local-testing setup used by prior GCL work, even mean pooling achieves 100% task-ID prediction accuracy and 0% forgetting on all seven datasets — matching TPP, the previous SOTA. This collapses class-incremental learning into task-incremental learning, rendering the evaluation uninformative. The demonstration is unambiguous and important for the GCL community.

- **[Strong]** Comprehensive benchmark scope: LLM4GCL evaluates 9 methods across three families (GNN-based, LLM-based, GLM-based) on 7 TAG datasets under two settings (NCIL, FSNCIL), providing a useful resource for situating future GCL work with LLMs.

- **[Strong]** SimGCL achieves substantially higher absolute accuracy than prior GNN baselines on most datasets (Tables 2, 3). For instance, on Cora NCIL, SimGCL achieves 84.6% average accuracy versus GCN's 57.0% and SimpleCIL's 70.8%. The method is clearly described.

## Weaknesses

### Major

- **SimGCL's LLM backbone for main results (Tables 2, 3, 4) is not specified.** The paper states that SimpleCIL uses RoBERTa (line 78), and Figure 3 tests SimGCL with various BERT and RoBERTa sizes, but nowhere do the main result tables state which backbone SimGCL actually uses. Given that Figure 3 shows RoBERTa-large (355M) performing substantially better than BERT variants, the backbone choice could determine the conclusions. This is a basic reproducibility failure that undermines the paper's primary empirical claims.

- **SimGCL underperforms the simpler SimpleCIL baseline on the largest, most realistic datasets.** On Arxiv-23 NCIL (Table 2): SimGCL scores 38.7/13.6 vs SimpleCIL's 52.4/38.8. On Arxiv-23 FSNCIL (Table 3): 31.8/10.3 vs 49.8/40.0. On Arxiv FSNCIL: 36.3/6.8 vs 46.4/36.6. On Arxiv NCIL, SimpleCIL's A_N (36.5) exceeds SimGCL's (33.8). These are the largest datasets with the most sessions — arguably the most realistic scenarios. The paper's explanations (sparse graph structure, overfitting — lines 193-194) are post-hoc and untested. This is a significant limitation that should temper the headline claims.

### Minor

- **No ablation study isolating SimGCL's components.** SimGCL has three design elements: (a) ego-graph-derived prompt, (b) instruction tuning with LoRA in session 1, and (c) frozen prototypes thereafter. Without ablations, we cannot attribute the performance gains to any specific claimed novelty (graph prompt, instruction tuning) versus the known effectiveness of the frozen-prototype paradigm (already demonstrated by SimpleCIL and recognized in the PTM-CL literature).

- **No variance or statistical significance reported.** All tables report single numbers without standard deviations, confidence intervals, or number of runs. For FSNCIL where sample counts are small, this is a real concern — many reported differences could fall within natural variation.

- **The headline "20% improvement" claim (abstract) compares against GNN-from-scratch baselines.** SimGCL leverages a large pretrained LLM while GNN methods (GCN, EWC, LwF) train from scratch on small labeled sets. The informative comparison (SimGCL vs. SimpleCIL, same LLM regime) shows smaller gaps that are occasionally negative. The paper does include SimpleCIL as a baseline, partially mitigating this, but the headline number is misleading.

- **Observation 4 in Section 4 asserts that "dense graph structures may enhance GLM effectiveness" but this is contradicted by the Arxiv dataset** (dense but low performance). The paper acknowledges this contradiction without resolving it (lines 169-170).

### Trivial

- The observation numbering in Section 4 skips 5 (goes ❶, ❷, ❸, ❹, ❻, ❼, ❽), likely a draft artifact.

## Nice-to-Haves

- An ablation study with at least two conditions: (a) SimGCL minus the graph-structured prompt (text-only prompt) and (b) SimGCL without instruction tuning, to isolate the novel components.
- Reporting variance across multiple runs, especially for FSNCIL.
- A direct computational cost comparison (wall-clock time or FLOPs) between SimGCL and baselines.
- A more thorough investigation of why SimGCL underperforms SimpleCIL on Arxiv-23 and Arxiv, rather than brief post-hoc attribution.

## Removed Points

These points from the input review are removed with justification:

1. **"SimGCL solves forgetting by not doing continual learning at all" (flagged as Fatal).** Removed because it mischaracterizes the method. Accumulating class prototypes incrementally from a fixed embedding space IS a form of continual learning — the model learns new classes over time without forgetting. This is a recognized PTM-based CL paradigm (SimpleCIL does the same; the paper's Section 5 discusses "frozen-backbone approaches"). The paper is transparent about the mechanism. The criticism reflects an overly narrow definition of continual learning rather than an actual flaw.

2. **"The comparison with GNN-based methods conflates LLM pretraining power with CL capability."** Removed as a standalone weakness because the paper includes SimpleCIL (LLM-based) as a baseline, which addresses the concern. The remaining issue about the "20%" headline is merged into Minor above.

3. **Miscellaneous section-by-section notes** about "previous knowledge leakage" and "label imbalance" being asserted rather than demonstrated, Observation 6 being "argument by exemplar," Table 4 arrow annotations — these are presentation observations or comments about what the paper does not analyze, not specific weaknesses.

4. **Formatting/style nitpicks, missing related works, appendix content complaints.** Parser artifacts or unverifiable without external sources.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Specify the LLM backbone used for SimGCL in every main experiment table and in Section 3.3.** This is the single most important fix for reproducibility.
2. **Add at minimum a two-condition ablation** separating the effect of the graph-structured prompt from the instruction tuning from the frozen-prototype mechanism.
3. **Report variance across multiple runs**, especially for FSNCIL.
4. **Reframe the "20% improvement" claim** to clarify the comparison class (GNN-from-scratch) and explicitly compare against SimpleCIL when claiming continual-learning-specific gains.
5. **Address the SimpleCIL outperformance on Arxiv-23 and Arxiv** with deeper analysis — these are the most realistic settings and the current post-hoc explanation is insufficient.

## Score and Decision

**Calibration Protocol (summary of anchors used across all rounds):**

| Anchor | Avg Human Score | Round | Itemized? | Comparison |
|--------|:-:|:-:|:-:|---|
| CLDyB (RnxwxGXxex) | 5.67 | R1 | Yes | PTM-CL benchmark paper, Accept. Our paper has a similar benchmark contribution PLUS a task-ID critique PLUS a method, but with more significant experimental gaps. |
| Online Continual Graph Learning (4sJJixGIZX) | 5.00 | R1+R2 | Yes | Pure benchmark (no method), Reject. Our paper has more contributions (critique + method) but similar evaluation issues. |
| Graph Pooling Benchmark (Onw93uJCWO) | 4.75 | R1 | Yes | Pure benchmark with straightforward observations, Reject. Our paper has stronger original insights (task-ID critique). |
| Label-free Node Class. w/ LLMs (hESD2NJFg8) | 6.50 | R2 | Yes | LLM+graph method paper, Accept. Stronger execution overall, fewer experimental gaps. |
| Prototype Antithesis (bRqaHn3J5I) | 5.75 | R2 | Yes | Prototype-based FSCIL, Accept. Mixed reviews (3,6,8,6). Similar methodological framing concerns. |
| CIL via Likelihood Ratio (8QfK9Dq4q0) | 6.00 | R1 | Yes | CIL method, Accept. Some concerns about reliance on pretrained models mirror our framing concern. |

**Round-1 bracket:** The paper sits between pure benchmark papers (~5, Reject) and well-executed LLM+graph method papers (~6.5, Accept).

**Narrowing (Round 2):** The task-ID leakage critique is a genuinely novel and well-demonstrated contribution that raises the paper above pure benchmark papers. The CLDyB benchmark paper (5.67, Accept) provides the closest reference point: it had a well-motivated benchmark contribution and was accepted despite clarity issues. Our paper has a stronger critical contribution but the missing backbone specification and the Arxiv/Arxiv-23 underperformance are more impactful weaknesses.

**Final score grounded in favorability comparison:** Our strengths (11.2–11.9) are comparable to CLDyB's (9.8–12.9). Our weaknesses (favorability -0.73 to 1.85) are somewhat more negative than CLDyB's weakest items (which touched -2.13) but our two major weaknesses (backbone unspecified at 1.12, underperformance at 0.35) are substantial. The missing backbone specification is fixable in rebuttal; the Arxiv underperformance is a genuine limitation. Balancing the strong critique contribution against these gaps places this paper slightly below the CLDyB anchor at 5.67, but above the pure-benchmark reject papers at ~5.00.

**Score: 5.5**

**Decision: Accept** — The task-ID leakage critique is a valuable contribution that the community needs to see. The missing backbone specification can be addressed easily. The Arxiv underperformance is a genuine limitation that should be more prominently discussed rather than treated as a minor caveat.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>