## Summary

This paper identifies three fundamental limitations of static pre-training in Supervised Causal Learning (SCL)—fragility to distribution shifts, failure in compositional generalization, and poor transfer from synthetic to real-world data—and proposes TTT-SCL, a framework that dynamically generates training data aligned with each test instance. The authors instantiate this as TACTIC, which uses a novel Alignment of Distribution (AD) metric combined with sparsity constraints to perform stochastic graph refinement, generating high-quality, test-specific training data. Experiments on synthetic, pseudo-real, and real-world benchmarks show substantial improvements over existing SCL and traditional causal discovery methods.

## Strengths

- **Well-motivated problem identification with rigorous evidence.** The three issues (Section 3) are supported by systematic experiments using factorial combinations of mechanisms, graph types, and noise distributions. The compositional generalization failure (Issue 2) is particularly novel and important: models trained on all individual components still fail on unseen combinations, revealing that static pre-training is fundamentally insufficient. This insight has broad implications for the SCL community.

- **Genuine paradigm contribution.** TTT-SCL is a creative and well-motivated framework that shifts from diversity-seeking pre-training to concentration-oriented test-time adaptation. The idea that distributional alignment (via AD) can implicitly capture graph correctness is elegant and provides a principled bridge between score-based causal discovery and supervised learning.

- **Strong empirical results on challenging benchmarks.** TACTIC achieves 78.9 vs. 62.3 AUROC (AVICI) on the real-world Sachs dataset and 80.1 vs. 65.4 on the pseudo-real SynTREn dataset—impressive margins. The stage-wise analysis (Table 4) cleanly demonstrates two-stage improvement: search refinement (seed → highest-score graph) and learning refinement (highest-score graph → SCL output), validating the value of the full pipeline.

- **Thorough ablation and diagnostic experiments.** The sparsity ablation (Table 3) convincingly shows that AD alone leads to degenerate dense graphs, and removing sparsity causes consistent performance drops. The stage-wise comparison (Table 4) provides clear evidence that the SCL training stage adds substantial value beyond just finding a good graph.

## Weaknesses

### Fatal
None.

### Major

- **Severe scalability gap relative to claimed real-world applicability.** The central motivation is real-world causal discovery, yet all experiments use ≤20 variables (10 for synthetic, 11 for Sachs, 20 for SynTREn). SCL methods like AVICI are designed for 100+ variables. TACTIC requires iterative graph refinement plus full SCL retraining per test instance, and the graph search space grows super-exponentially with node count. Without evidence that TACTIC scales beyond toy-scale problems, the real-world applicability claims are substantially weakened.

- **Extremely limited real-world evaluation.** The paper's headline claim concerns real-world performance, but there is only one true real-world dataset (Sachs, 853 samples, 11 proteins, a decades-old benchmark). SynTREn is synthetic gene-expression data. For a paper that fundamentally questions the real-world utility of existing SCL, evaluating on a single, small, well-studied real-world dataset is insufficient to support the broad claims.

- **Unanalyzed hyperparameter sensitivity.** The sparsity coefficient λ, the number of generated graphs K=200, and the stochastic refinement acceptance criterion are all critical design choices. No sensitivity analysis is provided for any of these. In particular, λ directly controls the trade-off between AD and sparsity—a poor choice could yield degenerate solutions or overly sparse graphs. Practitioners need guidance on how to set these, especially for new domains.

### Minor

- **Fixed Gaussian noise assumption in generation.** TACTIC defaults to N(0,1) noise for all generated training data regardless of the true noise distribution. This is inconsistent with the paper's own finding that noise distribution shifts cause significant performance degradation (Issue 1, Fig. 2). The tension between this design choice and the paper's own analysis deserves acknowledgment and discussion.

- **Unfair computational cost comparison.** TACTIC performs iterative search plus SCL retraining for each test instance, while baselines like PC, NOTEARS, and pre-trained AVICI require zero or negligible test-time computation. A wall-clock runtime comparison would help practitioners evaluate the cost-benefit trade-off, especially since one motivation is practical applicability.

- **The AD metric's reliance on correct mechanism fitting.** The SIM procedure regresses mechanisms f_i^k from D_test given a candidate graph, then evaluates likelihood. If the true mechanisms are complex and poorly estimated by the regression model, AD could give misleading signals. Discussion of this failure mode would strengthen the paper.

### Trivial
None.

## Nice-to-Haves
- Experiments on graphs with 30-50+ variables to demonstrate scalability
- Multiple diverse real-world benchmarks across different scientific domains
- Sensitivity plots for λ and K
- Wall-clock runtime comparison table
- Analysis of when the AD metric provides misleading rankings

## Novel Insights

The compositional generalization failure (Issue 2) represents a genuinely novel and important observation for the SCL community. Prior work attributed generalization gaps to unseen individual components (e.g., novel mechanisms) and suggested broader diversity in pre-training as the remedy. This paper demonstrates that the problem is more fundamental: even when all components are individually present in training, models fail on novel *combinations*, suggesting memorization of specific configurations rather than learning modular causal representations. This insight has significant implications: it implies that exhaustive static pre-training is combinatorially infeasible and that test-time adaptation is not merely beneficial but *necessary* for bridging the synthetic-to-real gap in causal discovery.

## Suggestions

1. **Add scalability experiments.** Even if TACTIC is slower, demonstrating that it *works* on 30-50 variable graphs would substantially strengthen the real-world applicability narrative. If it doesn't scale, that should be honestly discussed as a limitation.

2. **Expand real-world evaluation.** Include at least 3-5 real-world datasets from different domains (e.g., biological, economic, climate) with established ground-truth causal graphs to substantiate the claims about real-world utility.

3. **Provide hyperparameter sensitivity analysis.** Show how AUROC varies with λ, K, and initialization method across datasets. This is critical for reproducibility and practical adoption.

4. **Acknowledge and discuss the noise mismatch.** Since the paper's own experiments show noise shifts are damaging, explain why fixing Gaussian noise in generation is acceptable or provide an option to adapt it.

## Score and Decision

The paper presents a well-motivated framework with genuine novelty, supported by strong experimental results on the tested benchmarks. The compositional generalization insight alone is valuable. However, the evaluation is limited to small-scale problems with essentially one real-world dataset, which significantly undermines the paper's central claims about real-world applicability. Hyperparameter sensitivity and scalability are unaddressed. These are not fatal flaws but represent substantial gaps that prevent full confidence in the generality of the contribution.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>