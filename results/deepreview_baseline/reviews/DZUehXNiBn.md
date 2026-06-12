## Summary

This paper introduces VISTA, a modular framework for causal structure learning that decomposes the global DAG learning problem into local subgraphs based on Markov Blankets, aggregates them via a weighted voting mechanism with exponential decay, and enforces acyclicity using a Feedback Arc Set algorithm. The framework is model-agnostic, supports parallelization, and comes with theoretical guarantees including finite-sample error bounds and asymptotic consistency. Experiments on synthetic and real data show that VISTA consistently improves both accuracy and efficiency across diverse base learners.

## Strengths

- **Model-agnostic and modular design**: VISTA operates purely on edge-level outputs of local subgraphs, making it compatible with any causal discovery method without requiring assumptions about the base learner's inductive biases, parametric form, or identifiability conditions. This is a genuine practical advantage over prior fusion approaches that are algorithm-specific.

- **Strong theoretical foundation**: The paper provides finite-sample error bounds (Theorem 3.2), a practical range for the weighting parameter λ (Theorem 3.4), and asymptotic consistency guarantees (Theorem 3.5) showing that the required number of subgraphs per edge grows only logarithmically with graph size. These results go beyond the heuristic merging rules used in prior divide-and-conquer methods.

- **Consistent empirical improvements across diverse settings**: The experiments cover multiple graph families (ER, SF), graph sizes (30-300 nodes), linear and nonlinear data, and six different base learners. VISTA-WV consistently reduces FDR by 50-80% relative to baselines while maintaining reasonable TPR, and the runtime improvements are substantial (e.g., 2-10x speedup for NOTEARS, DAG-GNN, GraN-DAG at n=300).

- **Lightweight aggregation**: The weighted voting mechanism requires only a one-time O(|V|²) aggregation without any solver or training overhead, making it practical for large-scale applications. The ability to sweep λ without retraining (reusing cached votes) is a nice practical feature.

## Weaknesses

### Major

- **Unclear Markov Blanket identification methodology**: The paper repeatedly states that VISTA is agnostic to the MB identification method, but never specifies what MB solver was actually used in the experiments. This is a critical missing detail—the quality of MB identification directly determines the coverage guarantee (Proposition 3.1) and the overall performance. Without knowing the MB estimator, the results are not reproducible. The paper should specify the MB algorithm, its hyperparameters, and ideally compare different MB estimators.

- **The independence assumption in Theorem 3.2 is unrealistic and unaddressed**: The theorem assumes votes from different local subgraphs are independent, but the paper acknowledges this is violated in practice since subgraphs are learned from the same dataset. The claim that "we expect the same monotone trend to hold" is not supported by any analysis or experiment. Given that this assumption underlies the main theoretical guarantee, the paper should either provide a corrected analysis under dependence or empirically validate that the bound remains useful despite the violation.

- **No comparison to the most relevant baseline (DCILP) in the main experiments**: DCILP (Dong et al., 2024) is discussed as a related ILP-based fusion approach, and the paper mentions a comparison in Appendix F.2, but the main tables (Tables 1-4) do not include DCILP. Given that DCILP is the most directly comparable modular framework, its absence from the primary results makes it difficult to assess VISTA's relative merits. The appendix comparison should be moved to the main paper or at least summarized.

- **The NV results are problematic and raise questions about the framework's behavior**: In Table 1, VISTA-NV achieves TPR > 0.90 but FDR > 0.84 across all base learners, meaning the naive voting produces extremely dense, noisy graphs. This suggests that the MB subgraphs contain many spurious edges, and the weighted voting is doing most of the heavy lifting. The paper should discuss why NV performs so poorly and whether this indicates a fundamental issue with the MB decomposition (e.g., false edges from latent confounding in subgraphs).

### Minor

- **The choice of λ=0.5 and t=0.7 for all experiments is not well justified**: While the paper states these are "fixed" to avoid cherry-picking, the sensitivity analysis (Figure 4) shows that performance varies significantly with λ. The paper should provide guidance on how to select these hyperparameters in practice, or show that VISTA is robust to reasonable variations.

- **The real data experiment (Sachs) shows mixed results**: While FDR improves, TPR sometimes decreases (e.g., SCORE: 0.18→0.12, GraN-DAG: 0.53→0.29). The paper claims VISTA "consistently reduces false discoveries and improves structural accuracy," but the TPR drop for some methods is concerning. A more nuanced discussion of the precision-recall trade-off on real data would be appropriate.

- **The runtime comparison may conflate MB identification with base learner execution**: The paper reports total runtime for VISTA including MB identification, but the MB solver's runtime is not separately reported. If MB identification is expensive, the claimed speedups may be less impressive for methods where the base learner is already fast.

### Trivial

- The pseudocode in Figure 2 uses "MB_v ∪ v" which is slightly confusing notation (v is already in MB_v by definition).

## Nice-to-Haves

- An ablation study comparing different MB identification methods (e.g., IAMB, PCMB, TC) would strengthen the claim of model-agnosticism.
- A discussion of how VISTA handles variables that are not in each other's Markov Blankets (i.e., non-adjacent variables) would clarify the edge-level voting process.
- The paper could benefit from a complexity analysis that separates MB identification cost from base learner cost.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Specify the MB identification algorithm used in all experiments, including hyperparameters and implementation details, to ensure reproducibility.
2. Add DCILP as a baseline in the main experimental tables (or at minimum provide a summary of the appendix comparison in the main text).
3. Provide an empirical analysis of the independence assumption violation—e.g., measure the correlation between votes from overlapping subgraphs and show that the theoretical bounds remain approximately valid.
4. Include a discussion of how to select λ and t in practice, perhaps with a validation set or a heuristic based on graph sparsity.

## Score and Decision

The paper presents a well-motivated, theoretically grounded, and empirically effective framework for modular causal discovery. The model-agnostic design and lightweight aggregation are genuine contributions. However, the missing specification of the MB identification method, the unrealistic independence assumption in the main theorem, and the absence of the most relevant baseline (DCILP) from the main experiments are significant weaknesses that prevent full confidence in the results. The paper is solid but not yet ready for acceptance at a top venue.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>