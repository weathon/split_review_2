## Summary
This paper proposes VISTA, a modular framework for large-scale causal structure learning that decomposes the global DAG into Markov Blanket subgraphs, applies any off-the-shelf base learner independently on each subgraph, and then merges the local predictions via a weighted voting mechanism with exponential decay. The merged graph is post-processed with a Feedback Arc Set heuristic to enforce acyclicity. The framework is model-agnostic, supports full parallelization, and is backed by finite-sample error bounds and an asymptotic consistency guarantee.

## Strengths
- **Clear model-agnostic design**: VISTA operates purely on edge-level outputs from local subgraphs, imposing no assumptions on the inductive biases of base learners, the data distribution, or identifiability conditions. This makes it broadly applicable as a plug-in module.
- **Theoretical grounding**: The paper provides finite-sample error bounds (Theorem 3.2) and an asymptotic consistency result (Theorem 3.5) for the weighted voting aggregation, which explicitly links the required number of subgraph votes to confidence and margin parameters.
- **Consistent empirical improvements**: Across diverse graph families (ER, SF), graph sizes (30–300 nodes), and six different base learners (both differentiable and combinatorial), VISTA-WV improves F1 scores and reduces FDR relative to standalone baselines, often by large margins (e.g., FDR reduction of 50–80% in Table 1).
- **Scalability**: The divide-and-conquer design with parallel subgraph processing yields substantial runtime reductions (Table 3), especially for expensive learners like GraN-DAG and NOTEARS at 300 nodes.

## Weaknesses
### Fatal
None.

### Major
1. **Asymptotic consistency relies on an unrealistic scaling assumption**: Theorem 3.5 assumes that the number of local subgraphs per candidate edge, \(m\), grows as \(C \log n\). In sparse graphs, the Markov blanket of any node is typically bounded by a constant, and an edge appears only in subgraphs centered at its endpoints and possibly a few spouses. Thus \(m\) does **not** grow with \(n\), making the asymptotic claim vacuous for most practical settings. This undermines the theoretical guarantee advertised in the abstract.

2. **Independence assumption in the theory is violated in practice**: Theorem 3.2 models votes as independent binomial draws, but subgraphs learned from overlapping data produce correlated votes. The authors acknowledge this but still use the independence assumption to justify the analysis. The practical impact on the validity of the error bounds is unclear, and no alternative (e.g., weakly-dependent concentration) is provided.

3. **The Markov Blanket solver is not specified**: The framework’s performance depends critically on accurate MB identification, yet the paper does not state which MB estimator was used in the experiments. This omission harms reproducibility and leaves the sensitivity to MB errors unexplored. The claim that MB accuracy stays high across graph sizes (Figure 1) needs a concrete MB method to be verifiable.

4. **Overclaim about “remedying” performance drops**: The paper repeatedly states that VISTA “remedies the typical performance drop of base learners.” While VISTA-WV consistently improves F1, the absolute gains are often modest (e.g., NOTEARS ER: 0.76→0.79) or leave the learner still at low F1 (GraN-DAG: 0.06→0.17). The improvement is real but not a universal remedy; some base learners remain poor even with VISTA.

### Minor
- Only one hyperparameter sweep (\(\lambda\)) is shown; the threshold \(t\) is fixed at 0.7 across all experiments. The sensitivity to \(t\) and the joint effect of \((\lambda, t)\) are not explored, despite their central role in the precision–recall trade-off.
- The comparison with the closest related divide-conquer method (DCILP) is relegated to an appendix that was not provided for review. This makes it impossible to judge whether VISTA offers advantages over a strong modular competitor.

### Trivial
None.

## Nice-to-Haves
- A practical guideline for choosing the MB estimator (e.g., exact vs. approximate) and its computational cost would strengthen the “plug-and-play” claim.
- An empirical evaluation of the impact of MB errors on final graph quality would help calibrate user expectations.
- Extending the theory to handle correlated votes (e.g., using union bounds or Rademacher complexity) would make the guarantees more trustworthy.

## Novel Insights
Beyond its own contributions, the paper illustrates that a simple, calibrated voting rule with exponential decay can transform the behavior of many causal discovery algorithms, turning high-recall but noisy local predictions into clean global structures. This suggests that the bottleneck in large-scale causal discovery is not only the algorithm but also the lack of a principled fusion mechanism—a point that the causal structure learning community can build on.

## Suggestions
- Clarify the practical scaling of \(m\): report the average number of subgraphs containing a given edge for the tested graph sizes, and discuss whether the logarithmic-growth assumption is ever realistic.
- Include results with a state-of-the-art divide-conquer method (e.g., DCILP) in the main paper, or at least describe the key differences in the main text rather than only in the appendix.
- Add an ablation study that varies the MB estimator (e.g., IAMB, PCMB, or a simple heuristic) to show the framework’s sensitivity.
- Release code with a clear specification of all hyperparameters used (including MB solver, \(\lambda\), \(t\)) and the exact version of each base learner.

## Score and Decision
**Score**: 6 / 10  
**Decision**: Borderline Accept

The paper tackles an important problem (scalable causal discovery) with a clean, modular design and provides both theoretical and empirical support. However, the asymptotic consistency claim is built on an unrealistic scaling assumption, and key experimental details (MB estimator, comparison with DCILP) are missing or deferred. These issues prevent a higher score but do not invalidate the core contribution—a practical, model-agnostic integration framework that consistently improves accuracy across diverse base learners.

MY FINAL SCORE: <score>6</score>  
MY FINAL DECISION: <decision>Accept</decision>