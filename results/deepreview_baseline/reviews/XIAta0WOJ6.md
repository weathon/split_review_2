## Summary

This paper studies stochastic bilevel optimization under higher-order smoothness assumptions on the lower-level variable. The authors reinterpret the F²SA method as a forward-difference hyper-gradient approximation and propose a generalized family F²SA-p that uses p-th order finite differences. They prove an improved SFO complexity of \(\tilde{\mathcal{O}}(p\epsilon^{-4-2/p})\) for p-th order smooth problems, which approaches the \(\Omega(\epsilon^{-4})\) lower bound as p grows. The paper also provides an \(\Omega(\epsilon^{-4})\) lower bound for stochastic bilevel optimization via a separable construction, showing near-optimality when \(p = \Omega(\log \epsilon^{-1} / \log \log \epsilon^{-1})\).

## Strengths

- **Novel theoretical contribution**: The paper provides a clean and elegant connection between bilevel optimization and finite-difference approximations, generalizing the F²SA framework to higher-order smoothness. The insight that higher-order finite differences can improve the hyper-gradient approximation error from \(\mathcal{O}(\nu)\) to \(\mathcal{O}(\nu^p)\) is both original and well-motivated.

- **Rigorous analysis with improved bounds**: The main theorem (Theorem 3.1) provides a rigorous complexity analysis with explicit dependence on all problem parameters. The improvement from \(\tilde{\mathcal{O}}(\epsilon^{-6})\) to \(\tilde{\mathcal{O}}(p\epsilon^{-4-2/p})\) is significant, and the paper correctly identifies the regime where the method becomes near-optimal.

- **Clean lower bound construction**: The \(\Omega(\epsilon^{-4})\) lower bound in Theorem 4.1 uses a fully separable construction that avoids the smoothness violations present in prior lower bound constructions (Dagré et al., 2024; Kwon et al., 2024a). This is a technically sound contribution that cleanly extends the single-level lower bound to the bilevel setting.

- **Practical insight for p=2**: The observation that F²SA-2 requires the same number of lower-level solves as F²SA (2 solves) while providing better error guarantees under second-order smoothness is practically valuable. The algorithm improvement "almost comes for free" in terms of per-iteration cost.

## Weaknesses

### Fatal
None.

### Major

- **The experimental validation is insufficient to support the theoretical claims.** The experiments only show test loss and accuracy versus iterations on a single dataset (20 Newsgroups) for a single problem (learn-to-regularize logistic regression). The paper does not:
  - Verify that the \(\epsilon\)-stationary point condition is actually achieved (no gradient norm plots).
  - Compare wall-clock time or total SFO calls, which is the actual complexity metric being analyzed.
  - Show convergence curves for different \(\epsilon\) values to demonstrate the scaling behavior predicted by theory.
  - Include error bars or multiple random seeds, making it impossible to assess statistical significance.
  
  The experiments are more of a "proof of concept" than a validation of the claimed complexity improvements.

- **The normalized gradient step is a significant algorithmic modification that is not adequately justified.** The paper states "we believe that all our theoretical guarantees also hold for the standard gradient step via a more involved analysis" (Remark 3.1), but this is not proven. Normalized gradient descent has fundamentally different behavior from standard gradient descent, and the analysis relies on this normalization to control the change in \(y^*_{j\nu}(x_t)\). This is a non-trivial gap between what is analyzed and what would be practically useful.

- **The condition number dependence is extremely poor and not discussed critically.** The complexity \(\tilde{\mathcal{O}}(p\kappa^{9+2/p}\epsilon^{-4-2/p})\) has a \(\kappa^9\) dependence even in the best case. The paper acknowledges this gap (Table 1 shows \(\Omega(\kappa^{5/2}\epsilon^{-4})\) lower bounds from concurrent work), but does not provide any intuition about whether this is fundamental or an artifact of the analysis. For problems with large condition numbers (common in practice), this dependence could dominate the \(\epsilon\) dependence.

- **The assumption of higher-order smoothness only in y (not jointly in x,y) is somewhat artificial.** While the paper correctly notes that this is a weaker assumption than joint smoothness (Huang et al., 2025), it is unclear which practical problems satisfy Assumption 2.5 but not the stronger joint smoothness. The examples given (logistic regression with softmax weights) are smooth in all variables jointly, so the distinction seems unnecessary for the claimed applications.

### Minor

- The paper claims to "improve the upper bound to \(\tilde{\mathcal{O}}(p\epsilon^{-4-2/p})\)" but the actual bound includes \(\kappa^{9+2/p}\) and \(\bar{L}^{2/p}\) factors. The abstract and introduction somewhat oversimplify the result by focusing only on the \(\epsilon\) dependence.

- The comparison to concurrent work (Ji, 2025; Chen & Zhang, 2025) is mentioned but not discussed in sufficient detail. The paper would benefit from a clearer explanation of how these lower bounds relate to the upper bounds presented.

### Trivial
None.

## Nice-to-Haves

- Experiments on additional datasets and problem types (e.g., data hyper-cleaning from Example 2.1) would strengthen the empirical validation.
- A comparison of the practical performance of F²SA-2 versus F²SA on problems that do NOT satisfy second-order smoothness would test the claim that F²SA-2 is "at least as good as F²SA."
- A discussion of how the finite-difference coefficients \(\alpha_j\) are computed in practice and whether numerical stability is a concern for large p.

## Novel Insights

Beyond the paper's own contributions, the key insight is that the penalty-based approach to bilevel optimization (F²SA) can be naturally interpreted as a finite-difference approximation of the hyper-gradient. This perspective opens the door to using classical numerical analysis techniques (higher-order finite differences) to improve convergence rates. The observation that the approximation error in the hyper-gradient can be reduced from \(\mathcal{O}(\nu)\) to \(\mathcal{O}(\nu^p)\) by solving \(p\) (or \(p+1\)) lower-level problems in parallel is both elegant and practically relevant. The paper also provides a tighter analysis of the Lipschitz continuity of \(\frac{\partial^{p+1}}{\partial \nu^p \partial x} \ell_\nu(x)\) (Lemma 3.2), which improves upon prior bounds even for the \(p=2\) case.

## Suggestions

1. **Strengthen the experiments**: Add gradient norm convergence plots, wall-clock time comparisons, and error bars. Show the scaling behavior with \(\epsilon\) by running experiments at multiple target accuracies.

2. **Address the normalized gradient step**: Either prove that the same results hold for standard gradient descent, or provide a more detailed justification for why normalization is necessary and how it affects practical performance.

3. **Discuss the condition number dependence more thoroughly**: Provide intuition about whether the \(\kappa^9\) dependence is tight or can be improved, and discuss the practical implications for problems with large condition numbers.

## Score and Decision

The paper makes a solid theoretical contribution by connecting bilevel optimization to finite-difference approximations and providing improved complexity bounds under higher-order smoothness. The analysis is rigorous, the lower bound construction is clean, and the algorithmic insight is novel. However, the experimental validation is weak, the reliance on normalized gradient steps is a concern, and the extremely poor condition number dependence limits practical relevance. The paper is a clear accept for a theory-focused venue, but the empirical claims are not well-supported.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>