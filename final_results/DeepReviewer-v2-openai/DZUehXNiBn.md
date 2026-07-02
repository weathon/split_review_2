## Summary
# Final Review Report

## Summary

This paper proposes VISTA (Voting-based Integration of Subgraph Topologies for Acyclicity), a modular framework for causal structure learning in high-dimensional settings. VISTA decomposes the global DAG learning problem into local subgraphs centered on each variable's Markov Blanket, applies any off-the-shelf base learner to each subgraph, then aggregates the local predictions via a weighted voting scheme that penalizes low-support edges using an exponential confidence weight (1−e^{−λm}). A Greedy Feedback Arc Set heuristic enforces acyclicity. The framework is model-agnostic (no assumptions on base learner internal design), supports full parallelization, and requires only O(n²) aggregation cost.

The paper provides finite-sample error bounds (Theorem 3.2), a practical λ selection range (Theorem 3.4), and an asymptotic consistency result (Theorem 3.5). Experiments on synthetic ER/SF graphs (n=30–300) and the Sachs protein network benchmark across six base learners (NOTEARS, GOLEM, DAG-GNN, GraN-DAG, SCORE, CAM) show that VISTA-WV consistently improves F1 score and reduces SHD relative to standalone baselines, while VISTA-NV (unweighted voting) provides high recall at the cost of unusably dense graphs. Runtime is substantially reduced due to subgraph-level decomposition and parallelism.

The paper addresses a well-motivated problem (scalable causal discovery) with a clean, modular design. However, several claims overstate empirical results, the theoretical guarantees rely on strong independence assumptions, and key dependencies (MB accuracy, known margins δ_p, δ_q) limit practical applicability. With major revisions to scope claims and add missing ablations, the framework has potential.

(External literature verification unavailable in this run; novelty and comparison conclusions are deferred for manual verification.)

## Strengths
**1. Clean, modular framework design.** VISTA's three-stage pipeline (divide via Markov Blankets → conquer via any base learner → merge via weighted voting + FAS) is conceptually simple and well-motivated. The separation between MB identification, local learning, and aggregation makes the framework model-agnostic and practically appealing for practitioners who want to plug in domain-specific learners. The design explicitly supports parallel execution in the divide stage, which is a clear practical advantage.

**2. Theoretical grounding for the aggregation step.** The paper provides finite-sample concentration bounds (Theorem 3.2), a feasible λ selection interval (Theorem 3.4), and an asymptotic consistency guarantee (Theorem 3.5). While these results rely on an independence assumption that is not satisfied in practice, they provide a principled starting point for understanding the aggregation's behavior and a qualitative guide for parameter selection.

**3. Comprehensive empirical evaluation.** The experiments cover a broad range of graph types (ER, SF, Sachs), graph sizes (n=30–300), and six diverse base learners spanning differentiable (NOTEARS, DAG-GNN, GraN-DAG) and combinatorial (CAM, SCORE) methods. The inclusion of normalized data experiments (Table 2) and runtime benchmarks (Table 3) adds robustness. The λ sensitivity analysis (Figure 4) helps readers understand the precision-recall trade-off.

**4. Consistent accuracy improvements for moderate base learners.** For base learners with reasonable standalone performance (e.g., NOTEARS, GOLEM, DAG-GNN at n=100), VISTA-WV consistently improves F1 by 10–40% and reduces FDR by 50–80% relative to baselines. This demonstrates that the weighted voting aggregation provides genuine value for mid-range estimators.

**5. Substantial runtime reductions.** The divide-and-conquer design yields 2–10× speedups across all tested base learners and graph sizes (Table 3). For challenging cases like SCORE at n=300 (where the baseline did not complete), VISTA reduces runtime from infeasible to 225 seconds. This scalability contribution is practically significant.

## Weaknesses
The weaknesses are organized from most to least impactful, following the ranked error board.

### W1. Conclusion claims "without sacrificing recall" — directly falsified by own data  [Issue, Major]

**Evidence:** Page 9 - Conclusion states: "Empirically, across diverse graph families and base learners, VISTA improves accuracy and runtime efficiency, typically increasing precision without sacrificing recall." The Sachs data (Table 4, Page 8) shows TPR drops for 3 of 4 baselines: GraN-DAG (0.53→0.29), GOLEM (0.26→0.18), SCORE (0.18→0.12). In synthetic data (Table 1, Page 7), VISTA-WV reduces TPR relative to baseline for several entries (e.g., NOTEARS ER5: 0.74→0.68).

**Root cause:** The weighted voting and FAS post-processing are inherently conservative — they prune both false and true positive edges. The conclusion's wording was not updated to reflect this systematic trade-off observed in the data.

**Action:** Replace the over-claim with precise language. The corrected sentence should read: "Empirically, across diverse graph families and base learners, VISTA improves precision and reduces SHD, while maintaining moderate recall with some trade-off in high-precision regimes."

---

### W2. Theoretical guarantees assume independent subgraph votes, which is violated in practice  [Issue, Major]

**Evidence:** Theorem 3.2 (Page 4-5) models A ∼ Binomial(m, p) assuming each subgraph votes independently. The paper acknowledges this limitation (Page 5: "subgraphs learned from the same dataset can induce correlations among votes, so the bound should be interpreted as a qualitative guide"), but Theorem 3.5 (asymptotic consistency) and Corollary 3.3 (sample complexity bound) both inherit this assumption without correction.

**Root cause:** Overlapping Markov Blankets cause the same data points to appear in multiple subgraphs (e.g., MB(V_i) and MB(V_j) share spouses), creating positive correlation among votes. Positive correlation reduces effective sample size below m, so Eq. (3) underestimates the required samples.

**Action:** Add a correlation-aware bound: if votes have pairwise correlation ρ, then effective samples m_eff ≤ m/(1+ρ(m−1)). Replace m with m_eff in Eq. (3). Provide an empirical estimate of ρ from bootstrap resampling of subgraphs.

---

### W3. Limitations omit the most critical dependency: MB identification accuracy  [Suggestion, Major]

**Evidence:** Page 9 - Limitations mentions latent confounding and FAS pruning but does not list MB accuracy as a limitation. Proposition 3.1's coverage guarantee (Page 2) states "every edge of G is present in G'" — but this holds only when Markov Blankets are correctly identified. Figure 1 (Page 2) shows MB F1~0.9, but this is under ideal synthetic conditions where the true graph is known.

**Root cause:** The paper emphasizes model-agnostic flexibility but under-emphasizes that the entire framework's correctness hinges on an unsupervised MB estimation step. In real data (e.g., with latent confounders or non-faithfulness), MB accuracy degrades, and errors in the divide step are irrecoverable.

**Action:** Add MB dependency as the first limitation. Revise the Introduction's model-agnostic claim to clarify: "VISTA is model-agnostic with respect to base learners, but its coverage guarantee depends on the accuracy of Markov Blanket identification."

---

### W4. Weighted Voting score ignores the total subgraph count N  [Suggestion, Major]

**Evidence:** Eq. (2) defines s(X→Y) = (1−e^{−λm})·(A/m) where m = A+B is the total occurrences of either direction, not the total subgraph count N. An edge appearing in 2 out of 3 subgraphs (m=3) is treated identically to one appearing in 2 out of 50 subgraphs (m≈2 if only 2 subgraphs contain it). The denominator does not penalize cases where the edge is absent from most subgraphs, which could indicate it is spurious.

**Root cause:** The score uses only observed directional votes (A,B) and discards the "not observed" signal. For sparse graphs where MB overlaps are small, this can retain false edges that happen to appear in a few subgraphs.

**Action:** Consider a normalized score s(X→Y) = (1−e^{−λA})·(A/m)·(m/N)^α where α controls coverage penalty, or add an explicit discussion of coverage assumptions.

---

### W5. Theorem 3.5 margins (δ_p, δ_q) are unknowable, making the consistency result non-operational  [Suggestion, Minor]

**Evidence:** Theorem 3.5 requires δ_p = p−t > 0 and δ_q = t−q > 0. In practice, the true-edge inclusion probability p and false-edge inclusion probability q are unknown. The paper states "In practice, both p and q can be empirically estimated" (Page 6) but does not specify how, nor does it provide confidence intervals for the estimates.

**Root cause:** The theory uses oracle parameters that cannot be verified from observed data. Without a practical diagnostic, the asymptotic consistency claim cannot be checked by users.

**Action:** Add bootstrap-based estimation of p̂ and q̂ with 95% confidence intervals. Provide a rule of thumb: if the estimated margins δ̂_p, δ̂_q are positive with high confidence, the conditions of Theorem 3.5 are empirically supported.

---

### W6. VISTA-NV failure mode under-discussed  [Suggestion, Minor]

**Evidence:** Table 1 (Page 7) shows VISTA-NV produces SHD values of 3000+ for several baselines (e.g., NOTEARS ER5: 208→3171), meaning the graph structure is essentially random. The paper mentions this implicitly through FDR numbers but never explicitly states that "VISTA-NV produces unusably dense graphs."

**Action:** Add a sentence in Section 4.1: "The SHD explosion of VISTA-NV (>3000) confirms that naive edge union without confidence weighting produces dense, highly cyclic graphs that are unusable in practice. This motivates the need for weighted voting."

---

### W7. Sachs results show consistent recall decline — presented as unqualified improvement  [Suggestion, Major]

**Evidence:** Table 4 (Page 8) shows TPR declines for 3/4 methods. The text states: "Incorporating VISTA consistently reduces false discoveries and improves structural accuracy, measured by SHD and SID... highlighting that VISTA is a plug-and-play module that can reliably enhance the performance." The word "consistently" is accurate for FDR but misleading for the overall recovery (SHD improvements are marginal: 16→16, 18→15, 15→14, 16→12).

**Action:** Add a balanced assessment: "VISTA reduces false discoveries across all methods on Sachs, though recall declines for most base learners. Net structural accuracy (SHD, SID) shows modest improvement, suggesting the framework is best suited for applications prioritizing precision over recall."

---

### W8. Runtime comparison uses wall-clock time without parallelization efficiency analysis  [Suggestion, Minor]

**Evidence:** Table 3 reports total elapsed time. The divide stage uses parallelism (24 cores), while baseline methods likely use single-process execution. The paper states the speedups are "not due to algorithm-specific acceleration but result directly from our divide-and-conquer design." This conflates two factors: parallelism × decomposition benefit.

**Action:** Report speedup per-core (parallel efficiency) and decomposition benefit separately. Also report peak memory usage, as the O(n²) aggregation may be a bottleneck for n > 10^4.

---

### W9. Introduction narrative structure needs reorganization  [Suggestion, Major]

**Evidence:** The first introductory paragraph (Page 1) mixes broad motivation, an identifiability caveat about VISTA (before the method is explained), and a survey of constraint-based/score-based challenges. The identifiability statement "our VISTA framework inherits whatever identifiability guarantees each base learner provides" appears before the reader knows what VISTA is.

**Action:** Restructure: (P1) motivation + challenges of constraint-based and score-based methods. (P2) divide-and-conquer survey + gap. (P3) VISTA overview. (P4) model-agnostic properties + contributions. Move the identifiability caveat to the Method section.

---

### W10. FAS ordering claim lacks empirical support  [Suggestion, Major]

**Evidence:** Page 4 argues that applying GreedyFAS before filtering (rather than after) "avoids discarding high-confidence edges." This is an intuitive claim but is not backed by any ablation experiment comparing FAS→filter vs. filter→FAS.

**Action:** Add a brief ablation on synthetic data (n=100, ER3) comparing both orderings. Report SHD, F1, and number of edges removed by FAS in each case.

---

### ASCII Diagrams

```text
ASCII Diagram — Paper Structure & Evidence Map

[Problem: Scalable causal structure learning]
    |
    |-- [Claim: MB decomposition preserves all edges] (Prop 3.1)
    |       |-- Evidence: Proof by MB definition (Page 2)
    |       |-- Gap: Assumes correct MB identification
    |
    |-- [Claim: Weighted Voting improves accuracy] (Eq. 2)
    |       |-- Evidence: Table 1 (F1 improvements 0.35→0.60 for GOLEM)
    |       |-- Counter-evidence: Table 4 (TPR drops for 3/4 methods)
    |       |-- Risk: Score ignores total subgraph count N
    |
    |-- [Claim: Finite-sample error bounds] (Theorem 3.2)
    |       |-- Evidence: Concentration inequality derivation
    |       |-- Gap: Assumes independent votes (violated in practice)
    |
    |-- [Claim: Asymptotic consistency] (Theorem 3.5)
    |       |-- Evidence: m = C log n requirement
    |       |-- Gap: δ_p, δ_q margins unknowable
    |
    |-- [Claim: Consistent runtime improvement] (Table 3)
    |       |-- Evidence: 2-10x speedups across baselines
    |       |-- Gap: Parallelization vs decomposition confounded
```

```text
ASCII Diagram — Revision Strategy Roadmap

[P0 — Must fix before resubmission]
    W1: Correct "without sacrificing recall" → "with moderate recall trade-offs"
    W3: Add MB accuracy as first limitation
    W7: Add balanced assessment of Sachs recall decline

[P1 — Should fix for stronger paper]
    W2: Add correlation-aware effective sample size bound
    W4: Discuss or fix the N-ignoring issue in weighted voting
    W9: Restructure Introduction for clearer narrative
    W10: Add FAS ordering ablation experiment

[P2 — Nice to have for completeness]
    W5: Add bootstrap diagnostic for δ_p, δ_q margins
    W6: Explicitly discuss VISTA-NV failure mode
    W8: Report parallel efficiency and memory usage
```

```text
ASCII Diagram — Related-Work Taxonomy Tree (Layered)

Root: Causal Structure Learning from Observational Data
├── Branch 1: Full-graph learning
│   ├── Leaf 1.1: Constraint-based (PC, FCI) [Spirtes et al.]
│   ├── Leaf 1.2: Score-based (GES, NOTEARS, GOLEM) [Chickering, Zheng, Ng]
│   └── Leaf 1.3: Gradient-based (DAG-GNN, GraN-DAG) [Yu, Lachapelle]
├── Branch 2: Divide-and-conquer / modular
│   ├── Leaf 2.1: Random-partition merging (SADA) [Cai et al.]
│   ├── Leaf 2.2: ILP-based reconciliation (DCILP) [Dong et al.]
│   ├── Leaf 2.3: Heuristic neighborhood fusion [Gao, Gu, Mokhtarian, Tsamardinos]
│   └── Leaf 2.4: Weighted voting aggregation (VISTA) ← this paper
└── Branch 3: Markov Blanket learning
    └── Leaf 3.1: MB discovery algorithms [Tsamardinos et al., various]

Note: External literature verification unavailable in this run;
taxonomy is based on paper's own citations and is provisional.

## Score
**Final Score: 6/10**

**Scoring rationale:**
- **Research value and novelty (primary dimension):** VISTA's core idea — calibrated weighted voting over Markov Blanket subgraphs — is a reasonable engineering contribution that combines existing components (MB identification, any base learner, weighted aggregation, FAS) in a modular pipeline. The primary research value lies in the theoretical analysis of the aggregation step and the comprehensive empirical validation. However, the theoretical guarantees are weakened by the independence assumption, and the empirical claims show systematic recall-precision trade-offs that are under-acknowledged. Deferred novelty verification is needed to assess overlap with existing divide-and-conquer causal discovery methods (DCILP, SADA, and others).
- **Validity and soundness:** The main claims are directionally supported but several are overstated (conclusion recall claim, "consistent improvement" language, under-discussed Sachs trade-offs). The theoretical core is sound under stated assumptions but the independence violation is a significant practical limitation.
- **Reproducibility:** Code is provided. The method is well-specified algorithmically. The fixed λ=0.5, t=0.7 operating point aids reproducibility. Missing details (parallelization implementation, memory usage) reduce full reproducibility.
- **Presentation quality:** The paper is generally well-written but the introduction narrative could be sharper and several over-claims need correction. The modular pipeline is clearly explained.

**Strengths-outweigh-weaknesses assessment:** The modular framework design and comprehensive experiments are genuine strengths. The identified weaknesses (over-claims, independence assumption gap, omitted limitations) are fixable with moderate revisions. The paper has potential for a top-tier venue after a well-executed revision addressing W1–W4 and W9.

**External literature verification:** Unavailable in this run. Novelty and comparison conclusions are deferred for manual verification by the authors or an external reviewer with access to a literature database.