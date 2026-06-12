") is a practical insight, though the paper doesn't deeply explore what this actually means semantically - the model is being asked to produce answers without reasoning, which fundamentally changes the conditional distribution.

**Theoretical Analysis:**
The theoretical results are largely straightforward applications of standard results about convex combinations of estimators:
- Theorem 1 (variance reduction) is trivial: variance of a convex combination with a deterministic component is just α² times the variance of the random component.
- Theorem 2 (MSE optimal combination) is a standard result about optimal linear combinations of estimators.
- Theorems 3 and 4 about SGD convergence are standard results from the biased SGD literature.

The theorems are correct but not particularly deep. The connection between MSE minimization and SGD convergence is well-known in the stochastic optimization literature.

**Empirical Evaluation:**
The experiments show consistent improvements across three model scales (1.5B, 7B, 8B) on both alignment benchmarks and math reasoning benchmarks. The improvements are meaningful (up to 7.8 points on AlpacaEval 2). However, there are some concerns:

1. Only two baselines (DPO and SimPO) are compared. Given the extensive literature on DPO variants, this seems limited.
2. The paper doesn't report the optimal α found for each setting, which would be informative.
3. The reasoning improvements from general conversational data are interesting but not well explained.
4. The models evaluated are all from the DeepSeek-R1 family, so generalizability is unclear.

**Key Concerns:**
1. The theoretical contribution is somewhat incremental - the results follow directly from well-known statistical and optimization theory.
2. The empty-trace approach is somewhat ad-hoc. Conditioning on an empty trace "## Summary
This paper identifies trace-induced gradient variance as a key bottleneck when applying preference optimization (e.g., DPO) to Large Reasoning Models (LRMs), and proposes BVPO, which mixes a high-variance trace-based gradient estimator with a low-variance empty-trace gradient estimator via a convex combination optimized for MSE. The method yields consistent improvements across three model scales on alignment benchmarks (up to 7.8 points on AlpacaEval 2) and, notably, also improves math reasoning performance despite using only conversational training data.

## Strengths
- **Timely and well-motivated problem.** The paper systematically identifies a genuine and practically important challenge—trace-induced gradient variance—that arises when applying existing preference optimization methods to LRMs. This is a gap that, to my knowledge, has not been formally addressed.
- **Consistent empirical improvements.** BVPO outperforms DPO and SimPO across three DeepSeek-R1 distill models (1.5B, 7B, 8B) on both Arena-Hard and AlpacaEval 2, in both Thinking and NoThinking modes. The gains are substantial and consistent across scales (Tables 1 and 2).
- **Interesting secondary finding.** That alignment with general conversational data improves math reasoning by up to 4.0 average points is a non-trivial and practically valuable observation, suggesting alignment and reasoning need not be at odds.
- **Clean and simple method.** BVPO is a drop-in modification requiring only the addition of an empty-trace loss term, making it easy to adopt in practice.

## Weaknesses
### Fatal
None.

### Major
- **Limited baseline comparison.** Only DPO and SimPO are compared, omitting other DPO variants (IPO, KTO, ORPO, R-DPO, TGDPO) and RLHF-based approaches that could serve as stronger baselines. This makes it difficult to assess whether the gains come from the variance reduction specifically or from other factors.
- **Shallow theoretical contribution.** The core theoretical results—Theorem 1 (variance of a convex combination with a deterministic component), Theorem 2 (MSE-optimal linear combination of two estimators), and Theorems 3–4 (SGD convergence with biased estimators)—are largely standard applications of well-known results from statistics and stochastic optimization. The paper does not clearly articulate what is novel beyond applying these to the specific context of LRM alignment.
- **Insufficient analysis of the empty-trace gradient.** The empty-trace estimator conditions on $r = \emptyset$ by appending "