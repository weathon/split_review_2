Now I have all the information needed to write the final consolidated review.

---

## Summary

VISTA is a modular framework for causal structure learning that decomposes the global DAG learning problem into local Markov Blanket subgraphs, aggregates them via weighted voting with exponential down-weighting, and enforces acyclicity via GreedyFAS. The framework is model-agnostic (operates purely on edge-level outputs), computationally lightweight (O(|V|²) aggregation), and validated across six base learners and multiple graph families. The paper also provides finite-sample concentration bounds and an asymptotic consistency result for the aggregation rule.

## Strengths

- **Clean, well-motivated framework with thoughtful design choices.** The three-stage pipeline (MB decomposition → weighted voting aggregation → FAS acyclicity enforcement) is conceptually simple, modular, and the ordering decision (GreedyFAS before thresholding, §3.1) shows careful implementation-level reasoning. The exponential down-weighting term $(1 - e^{-\lambda m})$ is a natural middle ground between naive voting and NP-hard solver-based reconciliation.

- **Genuinely model-agnostic and broadly validated.** The framework imposes no restrictions on base learner internals — it operates purely on edge-level outputs. This is demonstrated concretely across six very different base learners (NOTEARS, GOLEM, DAG-GNN, GraN-DAG, SCORE, CAM) spanning differentiable optimization, combinatorial search, and various structural assumptions. The consistent improvements across this diverse set support the claim that gains stem from the aggregation rule rather than any particular estimator.

- **Theoretical scaffolding beyond typical divide-and-conquer papers.** Theorem 3.2 provides finite-sample concentration bounds, Theorem 3.4 gives a feasible range for the weighting parameter $\lambda$, and Theorem 3.5 establishes asymptotic consistency. This is more theoretical grounding than most heuristic merging approaches in this line of work.

- **Computational efficiency of the aggregation itself.** Weighted voting is O(|V|²) matrix operations, trivially parallelizable, and retraining-free for hyperparameter sweeps. Table 3 shows substantial runtime reductions — e.g., NOTEARS from 12,515s to 2,136s at n=300, and SCORE (which could not scale to n=300 standalone) running in 225s with VISTA.

## Weaknesses

### Fatal
None.

### Major

- **The asymptotic consistency condition (m ~ log n) is incompatible with the sparse-graph regime the paper tests.** Theorem 3.5 requires the number of subgraphs containing a candidate edge to grow as $m = C \log n$ (i.e., $m \to \infty$ as $n \to \infty$) for the probability of global error to vanish. However, in the sparse graphs used in experiments (average degree $h \in \{3,5\}$), each node's Markov Blanket size is O(1), and any given edge appears in the MB subgraphs of only O(1) nodes (its endpoints and their spouses). Thus $m$ is bounded by a constant independent of $n$, and the condition $m \sim \log n$ cannot be met. The paper states that this result makes the approach "efficient" (line 166), but does not acknowledge that the theoretical regime it assumes does not align with the empirical one. The theory may be internally valid as an idealized statement, but it does not speak to the experimental setting. This should be clearly caveated or reconciled with the actual algorithm.

### Minor

- **The MB solver used in all experiments is not named in the main text.** The paper states that VISTA is "agnostic" to the choice of MB estimator and provides a flexible interface (line 69), but the specific MB identification algorithm deployed to produce all results (including Figure 1 and Tables 1–4) is never identified — only referenced to Appendix F.2 ("where we also implemented the MB solver used in that work," line 174). While the framework is genuinely MB-agnostic, reproducibility requires knowing which solver was used. The paper should name the MB estimator and briefly justify its choice in the main text.

- **Theoretical guarantees are presented under an independence assumption that the paper acknowledges is violated.** Theorem 3.2 assumes votes from different subgraphs are independent Binomial trials. The paper states (line 138) that "subgraphs learned from the same dataset can induce correlations among votes, so the bound should be interpreted as a qualitative guide." This is transparent, but the abstract and contributions list present the theoretical results without this caveat. The theory as stated describes an idealized model, not a guarantee for the actual algorithm.

- **Real-data (Sachs) results are modest and the narrative overclaims.** On the only real-world benchmark, SHD reductions are 0–4 points across six base learners. GOLEM+VISTA leaves SHD unchanged at 16; for GraN-DAG+VISTA, SHD drops from 16 to 12 but TPR falls from 0.53 to 0.29 (near-halving of recall). The FDR=0.00 for GraN-DAG+VISTA is achieved by being extremely conservative (TPR=0.29). On an 11-node graph, the divide-and-conquer overhead is unnecessary, and the results should be at least comparable to global methods. These mixed results temper the claim that VISTA "consistently demonstrates the effectiveness" (abstract) across all settings.

- **Large standard deviations and unreported trial counts.** In Table 1, many SHD standard deviations are comparable to or larger than the mean (e.g., NOTEARS: 208.80 ± 190.71; GOLEM+VISTA-WV: 306.70 ± 87.75). The paper reports mean ± std but never states the number of random trials or runs (line 176 says "multiple simulation settings" without a number). This makes it difficult to assess whether the observed improvements are statistically significant.

- **Fixed hyperparameters (λ=0.5, t=0.7) without dataset-specific tuning.** The paper defends this as avoiding "cherry-picking" and uses the theoretical range in Theorem 3.4 as justification. However, Figure 4 shows that optimal λ varies across base learners and graph types. Since λ sweeping is "retraining-free" (the paper's own characterization, line 205), reporting results with a data-informed λ or showing that the fixed choice is near-optimal across settings would strengthen the empirical case.

### Trivial

None.

## Nice-to-Haves

- Including the DCILP runtime and accuracy comparison in the main text (currently in Appendix F.2) would strengthen the positioning against the closest competing paradigm.
- An ablation study removing GreedyFAS would help isolate how much of the improvement comes from weighted voting vs. cycle removal.
- Providing confidence intervals or paired significance tests for the main synthetic results would address the high-variance concern.

## Removed Points

These points are flagged to be removed; treat them with caution:

- *"The runtime comparison is not against the relevant baselines (Table 3 tells us nothing distinctive about VISTA's efficiency)."* — REMOVED. Comparing VISTA+base_learner vs base_learner standalone directly demonstrates the computational benefit of divide-and-conquer, which is a core claim. The DCILP comparison is provided in Appendix F.2. The claim that the table "tells us nothing distinctive" is factually incorrect.

- *"The VISTA-NV results are catastrophically bad… this raises questions about the quality of local subgraph estimates."* — REMOVED. The paper explicitly presents NV as a strawman (§3.1, "NV does not distinguish between strong and weak statistical support") and WV as the fix. The paper is transparent about NV's limitations. The speculation about local subgraph quality is not supported by evidence and the paper does not claim NV as a competitive method.

- *"SCORE at n=300 is '—'… needs explanation"* — REMOVED. The reviewer later acknowledges this as "a real win" for VISTA. The missing entry signals that the baseline could not scale, which is a positive result for VISTA, not a weakness.

- *"The independence assumption means theoretical claims do not actually apply to the real setting"* (framed as a critical/fatal issue) — DEMOTED to Minor. The paper explicitly acknowledges the assumption is idealized (line 138) and frames the bounds as "qualitative guides." While the theory is under an idealized model, the paper is transparent about this limitation. This is standard practice in ML theory papers.

## Novel Insights

None beyond the paper's own contributions. The review surfaces one genuine theoretical tension (m ~ log n vs. sparse-graph bounded m) that the authors should address, but does not produce a fundamentally new insight.

## Suggestions

1. Reconcile the asymptotic consistency condition (m ~ log n) with the fact that m is bounded by O(1) in the sparse graphs you evaluate on. Either (a) clarify that Theorem 3.5 applies to a different regime (e.g., denser graphs or settings with multiple datasets), or (b) provide an alternative analysis for the bounded-m setting.
2. Name the MB solver used in the main text and briefly justify its choice. This is the single most important missing implementation detail.
3. Report the number of random trials and add statistical significance tests (or at minimum confidence intervals) for the main synthetic results.
4. Discuss the Sachs results more critically — acknowledge the TPR drop in the GraN-DAG case and explain why improvements are marginal on this small benchmark.
5. Consider reporting results with dataset-specific λ selection (since sweeping is retraining-free) in addition to the fixed operating point, to demonstrate robustness to tuning.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>