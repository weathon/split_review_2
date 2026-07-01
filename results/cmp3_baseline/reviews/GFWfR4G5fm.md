## Summary

This paper identifies three fundamental limitations of static pre-training in Supervised Causal Learning (SCL)—fragility under distribution shifts, failure in compositional generalization, and poor transfer from synthetic benchmarks to real-world data. To address these, the authors propose a Test-Time Training for SCL (TTT-SCL) framework that dynamically generates training data aligned to each test instance. They introduce the Alignment of Distribution (AD) metric with sparsity constraints and instantiate TACTIC, a method that performs stochastic graph refinement to construct customized training sets. Experiments on synthetic, pseudo-real, and real-world datasets show significant improvements over existing SCL and traditional causal discovery methods.

## Strengths

- **Clear identification of a fundamental problem.** The paper systematically demonstrates three critical weaknesses of static SCL through controlled experiments, establishing that the community's current paradigm of maximizing diversity in pre-training is insufficient for real-world applicability. The compositional generalization failure is particularly insightful and goes beyond prior analyses.
- **Novel and well-motivated framework.** TTT-SCL is a principled paradigm shift from seeking universal diversity to generating instance-specific concentration. The AD metric combined with sparsity provides a theoretically grounded way to quantify causal alignment between training graphs and test data, and the joint optimization objective is clean and interpretable.
- **Strong empirical results.** TACTIC achieves state-of-the-art AUROC on multiple test domains (Linear\_U, Chebyshev\_G, Sachs, SynTReN) and remains competitive on RFF\_G where the static baseline was explicitly trained. The two-stage improvement analysis (seed → highest-score graph → final SCL output) convincingly demonstrates the value of both the search and the supervised learning phase.
- **Rigorous ablations.** The ablation removing sparsity (TACTIC (Notears-s)) shows consistent degradation, validating that AD alone leads to degenerate dense graphs and that causal minimality is essential. The comparison of TACTIC (random) vs. TACTIC (Notears) also confirms the practical benefit of informed initialization.

## Weaknesses

### Major

- **Ambiguity in the AD metric implementation.** The paper defines AD via likelihood (Eq. 3) but does not specify how the conditional distributions \(p(X_i | f_i^k)\) are computed or how the mechanisms \(f_i^k\) are regressed from \(D_{test}\). The default noise distribution is set to standard Gaussian, which imposes a strong parametric assumption. If the true test noise deviates significantly from Gaussian, the likelihood calculation may misalign. The authors claim applicability to any identification assumption but the default choice conflicts with that generality.

- **Lack of details on the stochastic graph refinement procedure.** The paper describes edge additions, deletions, and reversals with a Metropolis-style acceptance ratio, but crucial implementation details are missing: the proposal distribution, how the DAG constraint is enforced during modification, number of iterations, and how the final set of \(K=200\) training graphs is selected. Without these, reproducibility is hindered and it is unclear whether the search is efficient or may get stuck in local optima.

- **Limited comparison to alternative test-time adaptation strategies.** The paper introduces test-time training as a key novelty for SCL, but does not compare against simpler baselines such as fine-tuning the pre-trained SCL model on pseudo-data generated from the seed graph, or using a score-based method (e.g., greedy search with the same score) directly as the final predictor. The distinct advantage of the supervised learning phase over the highest-scoring graph is clearly shown, but a comparison to a score-based method that performs a more exhaustive search with the same objective would strengthen the claim.

### Minor

- **Computational cost is insufficiently discussed.** Test-time training for each instance is inherently expensive; the paper defers complexity analysis to an appendix (F) but the main text gives no runtime estimates. Practitioners would need to know whether TACTIC is feasible for high-dimensional settings (e.g., >100 variables) where the SCL backbone itself may scale poorly.

- **Standard deviations missing for Sachs and SynTReN.** In Table 2, these entries lack standard deviation values. For reproducibility and to assess variability, these should be reported (e.g., via multiple runs with different seeds or bootstrap).

### Trivial

- The figure captions contain redundant repetitions and the diagram description is overly verbose. Minor formatting issues from PDF extraction are not a flaw.

## Nice-to-Haves

- Provide a concrete example of how AD is computed (e.g., for a small graph) to illustrate the mechanics of SIM and likelihood evaluation.
- Include an analysis of the sensitivity to the hyperparameter \(\lambda\) that balances AD and sparsity.
- Report runtime for a typical test instance (number of variables, observations, search iterations) to give practitioners a sense of computational overhead.

## Novel Insights

The key insight beyond the paper's own contributions is that causal similarity between training and test instances can be captured implicitly through distributional alignment without needing to know the true graph. This reframes the SCL generalization problem as a search-then-learn process at test time, analogous to how test-time training works in vision but with a causal structure prior (sparsity). The demonstration that score-based methods (which stop at the highest-scoring graph) can be significantly improved by using that graph to generate training data for a supervised model reveals a fundamental limitation of classical score-based causal discovery that is rarely discussed.

## Suggestions

- Clarify the exact algorithm for the stochastic graph refinement: specify the proposal distribution, the acceptance rule (which appears to be the ratio of scores, not a probability proportional to score), how cycles are avoided, and how the \(K=200\) graphs are sampled from the chain.
- Provide details on how the likelihood in Eq. (3) is computed: is it a Gaussian likelihood with mean estimated via regression and fixed variance? If so, state the regression method (e.g., random forests, neural nets, or linear regression) and whether it assumes additive noise.
- Report runtimes for the main experiments and discuss scalability to larger graphs (e.g., 50–100 nodes).

## Score and Decision

The paper makes a strong, well-motivated contribution. The identified limitations are important and convincingly demonstrated. The TTT-SCL framework is novel and the empirical results are compelling across diverse settings. The weaknesses are manageable and can be addressed with clarifications. The paper is likely to influence future work in supervised causal learning.

MY FINAL SCORE: 8<score>8</score>
MY FINAL DECISION: Accept<decision>Accept</decision>