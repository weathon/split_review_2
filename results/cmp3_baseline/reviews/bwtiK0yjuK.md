## Summary
This paper studies offline change point localization and inference in dynamic multilayer random dot product graphs (D-MRDPGs). The authors propose a two-stage algorithm that combines seeded binary segmentation with low-rank tensor estimation (TH-PCA), establish consistency for the number and locations of change points, and derive the first limiting distributions for change point estimators in network data. A data-driven confidence interval construction procedure is also provided, and extensive numerical experiments demonstrate strong performance against existing methods.

## Strengths
- **Novel problem and first theoretical results for offline change point detection in dynamic multilayer networks.** The paper addresses an important gap in the literature and provides the first consistency guarantees and limiting distributions for this setting.
- **Rigorous theoretical analysis.** The authors derive high-probability localization error bounds (Theorem 1) and limiting distributions under both vanishing and non-vanishing jump regimes (Theorem 2 and Appendix A), with careful handling of the tensor low-rank structure.
- **Comprehensive experimental evaluation.** The method is tested on four simulation scenarios (including violations of Model 1) and a real-world agricultural trade network, with comparisons to multiple baselines (gSeg, kerSeg) and different input representations. Confidence interval coverage is also assessed.
- **Practical inference procedure.** The construction of data-driven confidence intervals (Section 3.1) is a valuable addition that goes beyond point estimation and is not offered by competing methods.

## Weaknesses
### Fatal
None.

### Major
- **Strong assumptions limit practical applicability.** The model assumes temporal independence of adjacency tensors, which is unrealistic for many real dynamic networks (e.g., transportation networks with temporal autocorrelation). The assumption that minimal spacing Δ = Θ(T) precludes frequent or closely spaced change points. While the authors mention possible extensions, these are not developed.
- **Requirement of four independent tensor sequences.** Algorithm 1 assumes mutual independence of {A(t)}, {A'(t)}, {B(t)}, {B'(t)}. In practice, the authors use odd-even splitting, but the theoretical analysis relies on independence. This may be difficult to satisfy in real data and could affect the validity of the guarantees.
- **Sensitivity to tuning parameters.** The threshold τ and input ranks for TH-PCA (r₁, r₂, r₃) require careful selection. The paper provides some guidance (e.g., τ = 0.1 n √L log^{3/2}(T)), but the sensitivity analysis in Appendix G.1 is limited and the choice of ranks (r₁=r₂=15, r₃=L) is somewhat ad hoc. The method may be brittle in practice without extensive tuning.

### Minor
- **Real data experiment has small T (T=35) and extremely narrow confidence intervals.** The confidence intervals reported in Table 4 (e.g., (5.97, 6.03) for time point 6) are unrealistically narrow given the small sample size and likely overstate precision. This raises questions about the practical reliability of the inference procedure.
- **The paper does not discuss computational cost in sufficient detail.** While a brief complexity statement is given, there is no empirical runtime comparison with baselines, and the cost of TH-PCA (which involves iterative SVD) may be prohibitive for large n, L, or T.

### Trivial
None.

## Nice-to-Haves
- Extend the framework to allow temporal dependence (e.g., Markovian structure) and provide corresponding theoretical guarantees.
- Relax the Δ = Θ(T) assumption using alternative selection strategies (e.g., narrowest-over-threshold) and analyze the resulting localization rates.
- Develop a bootstrap-based inference procedure for the non-vanishing jump regime, as suggested in the conclusion.
- Provide practical guidance on tuning parameter selection (threshold, ranks) with a data-driven or cross-validation approach.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
- Clarify how the independence assumption for the four sequences can be approximately satisfied in practice beyond odd-even splitting, and discuss potential violations.
- Include a sensitivity analysis for the threshold constant c_{τ,1} and input ranks across a wider range, and report the impact on detection accuracy and false positives.
- Add a discussion of the computational cost of TH-PCA relative to the baselines, and provide empirical runtime comparisons for different problem sizes.
- For the real data example, consider using a larger dataset or subsampling to obtain more reliable confidence intervals, and discuss why the intervals are so narrow.

## Score and Decision
**Score:** 8  
**Decision:** Accept

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>