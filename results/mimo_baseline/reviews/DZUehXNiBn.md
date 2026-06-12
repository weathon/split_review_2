## Summary

This paper introduces VISTA, a modular divide-and-conquer framework for causal structure learning that decomposes global DAG learning into local Markov Blanket subgraphs, applies arbitrary base learners to each, and aggregates the results via a weighted voting mechanism with exponential decay penalization and FAS-based acyclicity enforcement. The authors provide finite-sample error bounds and asymptotic consistency guarantees for the aggregation scheme, and demonstrate consistent accuracy and efficiency improvements across six diverse base learners on synthetic and real data.

## Strengths

- **Genuinely model-agnostic and modular design.** VISTA is demonstrated with six very different base learners (NOTEARS, GOLEM, DAG-GNN, GraN-DAG, SCORE, CAM) spanning continuous optimization, GNN-based, and combinatorial approaches. The consistent improvement across all of them—despite their widely varying inductive biases—strongly supports the claim that the gains originate from the aggregation framework itself rather than any particular estimator.

- **Substantial theoretical contribution.** The paper provides both finite-sample error bounds (Theorem 3.2, Corollary 3.3) and asymptotic consistency (Theorem 3.5) with explicit dependence on the graph size, required subgraph count, and voting parameters. The practical λ-range characterization (Theorem 3.4) connects theory to hyperparameter selection. This level of theoretical grounding is uncommon in modular causal discovery frameworks.

- **Significant computational efficiency gains.** Table 3 shows runtime reductions of 2–6× across all base learners and graph sizes, with particularly dramatic improvements at scale (e.g., SCORE at n=300: unsolvable standalone → 225s with VISTA). The O(n²) aggregation cost and natural parallelizability make this practically valuable.

- **Thorough experimental evaluation.** Experiments span ER and scale-free graphs, linear and nonlinear SEMs, four graph sizes, normalized and unnormalized data, and a real biological benchmark. The λ-sensitivity analysis (Figure 4) confirms the precision–recall trade-off predicted by theory.

## Weaknesses

### Fatal
None.

### Major

- **Theoretical independence assumption is a significant idealization.** Theorem 3.2 assumes votes across subgraphs are independent, which the authors acknowledge is violated in practice since subgraphs share variables and are learned from the same dataset. The paper states this is a "qualitative guide" and suggests extending to weakly dependent votes as future work, but no corrected or modified bound is provided. This gap weakens the theoretical guarantees' practical relevance, particularly since the degree of vote correlation is likely to vary with graph density and MB overlap structure.

- **Naive Voting performance reveals a fragility in the pipeline.** NV results (Table 1) show extremely high TPR (>0.95) but FDR >0.85 and SHD values that are 5–10× worse than standalone baselines (e.g., NOTEARS NV: SHD=3171 vs. 209). This means the raw coverage guarantee of MB subgraphs comes at the cost of massive over-discovery, making the framework's practical utility entirely dependent on the WV filtering step. The paper does not deeply analyze why NV produces such poor results—likely due to confounding edges introduced by conditioning on subsets—but this gap is concerning since it suggests the MB decomposition introduces substantial spurious structure that the voting mechanism must overcome rather than merely refine.

- **Limited real-world evaluation.** The only real dataset is the Sachs protein-signaling network with 11 nodes and 853 samples—a benchmark that is small enough to be handled by any method without decomposition. The improvements on Sachs are modest (e.g., GOLEM SHD: 16→16, DAG-GNN SHD: 15→14) and some TPR values actually decrease. A larger-scale real-world evaluation would substantially strengthen the practical relevance claims.

### Minor

- **TPR can decrease with VISTA-WV compared to standalone.** In several settings, the weighted voting reduces true positive rate even while improving F1 (e.g., NOTEARS on ERS: TPR 0.74→0.68; GOLEM on ERS: TPR 0.35→0.50 but on SFS: 0.29→0.40). While F1 improvement is the primary metric, the paper could better characterize when and why VISTA sacrifices recall, and whether this is addressable via hyperparameter tuning versus a structural limitation.

- **The practical guidance for choosing λ and t could be stronger.** The paper uses fixed values (λ=0.5, t=0.7) across all experiments, which is commendable for avoiding cherry-picking, but the theoretical range from Theorem 3.4 depends on m, p, and ε—quantities that are unknown in practice. A brief practical recipe (e.g., estimate p from vote frequencies, choose λ from the feasible interval) would make the method more deployable.

- **The ordering of GreedyFAS and threshold filtering is discussed qualitatively but not validated empirically.** The paper argues that GreedyFAS should precede filtering, but provides no ablation comparing the two orderings.

### Trivial
None beyond parser artifacts.

## Nice-to-Haves

- An analysis of how vote correlation structure depends on graph properties (density, MB size distribution) and how this affects the gap between theoretical and empirical performance.
- Ablation study on the ordering of GreedyFAS vs. threshold filtering.
- Experiments on larger real-world datasets (e.g., biological or financial networks with hundreds of variables) where the scalability advantages would be most impactful.

## Novel Insights

The key novel insight is that even with imperfect, correlated votes from overlapping MB subgraphs, the exponential-decay weighted voting mechanism provides a principled way to suppress spurious edges (introduced by local conditioning on subsets) while preserving weakly but consistently supported true edges. The theoretical characterization showing that the required number of subgraphs per edge scales only as O(log n) for consistency provides a clean efficiency guarantee for this approach, and the practical λ-range result (Theorem 3.4) connects the theoretical framework to actionable hyperparameter selection. The empirical finding that MB identification accuracy is much more stable across graph sizes than base learner accuracy (Figure 1) provides a practical motivation for the decomposition strategy.

## Suggestions

- Provide an ablation comparing GreedyFAS-first vs. filter-first ordering to validate the claimed benefit.
- Add a practical hyperparameter selection guide: given observed vote counts and estimated error rates, how should practitioners choose λ and t?
- Include at least one larger real-world experiment (n > 100) where the scalability advantage is the primary motivation.
- Discuss the relationship between MB identification errors and final graph quality more quantitatively—how does MB precision/recall propagate to the aggregated graph?

## Score and Decision

The paper presents a well-motivated modular framework with novel theoretical analysis and extensive experiments across diverse settings. The model-agnostic design, theoretical guarantees (within their acknowledged assumptions), and consistent empirical improvements are genuine strengths. The major weaknesses—the independence assumption gap, the NV fragility revealing confounding issues, and limited real-world evaluation—weigh against acceptance but do not invalidate the contribution. This is a solid empirical methods paper that would benefit the community, though it falls short of being a strong accept.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>