## Summary

This paper studies the Kernel Density Estimation (KDE) problem and proposes a data structure that achieves improved query time by using asymmetric Locality Sensitive Hashing (LSH) to trade off space and query time. The main result is a KDE data structure with query time approximately \(1/\mu^{0.05}\) at the cost of space approximately \(1/\mu^{4.15}\), significantly improving the previous best query time of \(1/\mu^{0.173}\) from Charikar et al. (2020). The paper also provides the first known query time vs. space tradeoffs for KDE, and for the linear space regime (\(1/\mu\) space) achieves a query time of \(1/\mu^{0.1865}\), improving the non-adaptive bound from prior work.

## Strengths

- **Novel application of asymmetric LSH to KDE**: The paper identifies that the KDE reduction framework of Charikar et al. (2020) can benefit from asymmetric LSH constructions (Andoni et al., 2017), which allow different exponents for space and query time. This is a clever and non-trivial insight that leads to genuine improvements.

- **First time-space tradeoffs for KDE**: The paper provides the first known tradeoff curve for KDE data structures, allowing practitioners to choose between lower query time and higher space or vice versa. This is a conceptually important contribution to the theory of KDE.

- **Significant numerical improvement**: The query time exponent of 0.05 is a substantial improvement over the previous best of 0.173 (data-dependent) and 0.25 (data-independent). Even in the linear space regime, the exponent 0.1865 is close to the data-dependent bound of 0.173 with a much simpler analysis.

- **Clear technical exposition**: The paper does a good job explaining the high-level intuition for why asymmetric LSH helps, including the key observation that the maximum query time in the reduction occurs at a different distance scale than the one that yields the space bound.

## Weaknesses

### Major

- **The space requirement for the best query time is extremely high**: The data structure achieving \(1/\mu^{0.05}\) query time requires \(1/\mu^{4.15}\) space. For typical values where \(\mu = n^{-\Theta(1)}\), this means space is \(n^{4.15}\), which is likely impractical for most applications. The paper acknowledges this but does not adequately discuss whether such a high space cost is ever justified.

- **The improvement in the linear space regime is marginal**: The query exponent of 0.1865 is only marginally better than the data-independent bound of 0.25 from Charikar et al. (2020), and is actually worse than their data-dependent bound of 0.173. The paper claims "simpler analysis" as an advantage, but the analysis in this paper is still quite involved and relies on numerical optimization.

- **Numerical optimization without analytical guarantees**: The paper relies heavily on numerical evaluation to determine the optimal exponents (0.05, 0.1865, etc.) but does not provide analytical proofs that these are the true optima. The optimization problem in Equation (10) involves a min-max over continuous parameters, and the paper only states that these values are obtained "using numerical methods." This weakens the theoretical contribution.

- **The "constant query time is impossible" claim is not fully justified**: Section 1.2 argues that constant query time KDE is not possible with known ANN results, but the argument is heuristic and based on the specific reduction framework. A formal lower bound or impossibility result is not provided, making this claim speculative.

### Minor

- **The paper focuses exclusively on the Gaussian kernel**: While the Gaussian kernel is important, the paper does not discuss how the results might extend to other kernels (Laplace, exponential, polynomial) that are also commonly used.

- **The dependence on \(\epsilon\) is not optimized**: The paper inherits the \(1/\epsilon^2\) dependence from the Charikar et al. (2020) framework, but recent work (Phillips & Tai, 2020; Charikar et al., 2024) achieves \(1/\epsilon\) dependence. The paper does not discuss whether its techniques could be combined with these improved \(\epsilon\) dependencies.

- **The "simpler analysis" claim is overstated**: While the paper claims its analysis is "much simpler" than the data-dependent scheme of Charikar et al. (2020), the actual analysis in Sections 4-5 and the appendix is still quite technical and involves solving complex optimization problems.

### Trivial

- The paper uses the notation \(\exp_a(b) = a^b\) which is non-standard and slightly confusing.

## Nice-to-Haves

- A discussion of practical implications: For what realistic values of \(n\) and \(\mu\) would the \(1/\mu^{4.15}\) space be acceptable? A concrete example would help ground the theoretical results.
- An analysis of whether the tradeoff curve can be extended to achieve query time exponents between 0.05 and 0.1865 with intermediate space costs, rather than just the two extreme points highlighted in Theorem 17.

## Novel Insights

The key novel insight is that the KDE reduction framework of Charikar et al. (2020) can be reinterpreted as solving a family of \((c, r)\)-ANN problems with different dataset sizes (due to subsampling at different rates), and that asymmetric LSH allows one to allocate different resources (space vs. query time) to each subproblem. The observation that the bottleneck in the reduction occurs at a different distance scale for query time than for space is what enables the improvement. This insight could potentially be applied to other problems that use similar multi-scale reduction frameworks.

## Suggestions

- Provide analytical (not just numerical) bounds on the optimal exponents, or at least prove that the numerical optimization converges to the true optimum.
- Discuss the practical regime where the high-space/low-query-time tradeoff is useful, or acknowledge that the main practical contribution is the linear-space result.
- Clarify whether the "constant query time is impossible" claim is a conjecture or a provable statement, and if the latter, provide a proof sketch.

## Score and Decision

The paper makes a genuine theoretical contribution by introducing the first time-space tradeoffs for KDE and achieving a significantly improved query time exponent. However, the extremely high space cost for the best query time and the reliance on numerical optimization without analytical guarantees temper the contribution. The linear-space result is a modest improvement over prior work. Overall, the paper is a solid theoretical contribution that advances the state of the art, but the practical impact is limited by the space requirements.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>