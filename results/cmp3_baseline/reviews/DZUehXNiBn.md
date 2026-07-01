## Summary

This paper introduces VISTA, a modular framework for causal structure learning that decomposes the global DAG learning problem into local subgraphs based on Markov Blankets, aggregates them via a weighted voting mechanism with exponential decay, and enforces acyclicity using a Feedback Arc Set heuristic. The framework is model-agnostic, supports parallelization, and is accompanied by finite-sample error bounds and asymptotic consistency guarantees. Experiments on synthetic and real data show that VISTA consistently improves accuracy and runtime over a range of base learners.

## Strengths

- **Model-agnostic modular design**: VISTA operates purely on edge-level outputs of local subgraphs, making it compatible with any base learner and any Markov Blanket identification method without requiring modifications to the internal structure of the learners.
- **Lightweight and efficient aggregation**: The weighted voting scheme is a one-pass edge-level operation with O(|V|²) complexity, avoiding expensive global searches or solver-based optimization. This leads to substantial runtime reductions across all tested base learners (Table 3).
- **Theoretical guarantees**: The paper provides finite-sample error bounds (Theorem 3.2, Corollary 3.3) and asymptotic consistency (Theorem 3.5) under mild conditions, establishing a principled foundation for the voting-based aggregation.
- **Consistent empirical improvements**: Across multiple graph families (ER, SF), graph sizes (30–300 nodes), and six diverse base learners, VISTA with weighted voting improves F1 score and reduces SHD compared to standalone baselines, while also cutting runtime significantly.

## Weaknesses

### Fatal
None.

### Major

1. **Unrealistic independence assumption in theoretical analysis**: Theorem 3.2 and the error bounds assume that votes from different local subgraphs are independent. In practice, subgraphs are learned from overlapping data and share variables, inducing correlations. The paper acknowledges this but provides no analysis or empirical validation of how dependence affects the guarantees. This weakens the theoretical contribution.

2. **Markov Blanket identification method is not specified**: The paper does not state which MB solver is used in the experiments, nor does it compare different MB identification methods. Since MB accuracy is critical to the coverage guarantee (Proposition 3.1) and overall performance, this omission harms reproducibility and makes it difficult to assess the framework's sensitivity to MB errors.

3. **Hyperparameter selection is not principled**: The weighted voting has two hyperparameters (λ and t). The paper fixes λ=0.5 and t=0.7 for all experiments, but the sensitivity analysis (Figure 4) shows that performance varies substantially with λ. No guidance is given for selecting these parameters in practice, and the theoretical range in Theorem 3.4 depends on unknown quantities (m, ε).

4. **Comparison with DCILP is relegated to the appendix**: DCILP is the most relevant prior work on modular causal discovery with formal merging. The main tables do not include DCILP, and the appendix comparison is brief. This weakens the empirical positioning of VISTA against the closest competitor.

5. **Real-data performance is modest**: On the Sachs network, VISTA improves SHD and SID but TPR remains low (0.12–0.29). The paper does not discuss this limitation or analyze why recall is poor on this benchmark.

### Minor

- The paper claims "fully parallelizable" but does not report parallel speedup or wall-clock time with varying numbers of cores.
- The runtime comparison (Table 3) does not clarify whether MB identification time is included in the VISTA runtime. If MB time is excluded, the comparison is unfair.
- The derivation of Corollary 3.3 from Theorem 3.2 is not clearly explained; the bound appears to involve an approximation that is not justified.
- The paper tests only differentiable/score-based base learners (NOTEARS, GOLEM, DAG-GNN, GraN-DAG, SCORE). Including a constraint-based learner (e.g., PC) would strengthen the claim of model-agnosticity.

### Trivial
None.

## Nice-to-Haves

- Include DCILP in the main experimental tables for direct comparison.
- Provide a practical guideline or heuristic for selecting λ and t based on graph sparsity or expected vote counts.
- Analyze the impact of MB identification errors on VISTA's final accuracy, e.g., by varying MB solver quality.
- Test with a constraint-based base learner to further demonstrate model-agnosticity.

## Novel Insights

The paper's key insight is that a simple, calibrated weighted voting scheme—using exponential decay to penalize low-support edges—can effectively aggregate noisy local subgraphs into a globally consistent DAG, with theoretical guarantees that the error rate is controlled. This contrasts with prior work that relies on solver-based optimization (DCILP) or uncalibrated heuristics. The modular separation of MB identification, local learning, and edge-level aggregation is a clean design that enables plug-and-play integration with any causal discovery method.

## Suggestions

- Clarify the MB identification algorithm used in experiments and include a sensitivity analysis with different MB solvers.
- Provide an empirical study of the independence assumption, e.g., by comparing theoretical bounds with observed error rates on synthetic data.
- Move the DCILP comparison to the main paper or at least summarize the key results in the main text.
- Discuss the practical selection of λ and t, perhaps with a cross-validation strategy or a default rule based on graph size.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>