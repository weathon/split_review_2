## Summary

This paper studies offline change point localization and inference in dynamic multilayer random dot product graphs (D-MRDPGs). The authors propose a two-stage algorithm combining seeded binary segmentation with low-rank tensor estimation (TH-PCA), establish consistency for estimating the number and locations of change points, derive limiting distributions of refined estimators under vanishing and non-vanishing jump regimes, and develop a data-driven procedure for constructing confidence intervals. Extensive numerical experiments demonstrate superior performance compared to existing alternatives.

## Strengths

- **Novel problem formulation**: This is the first work to address offline change point detection in dynamic multilayer networks, filling a clear gap in the literature. The D-MRDPG model is a natural and principled extension of existing single-layer and online multilayer frameworks.

- **Comprehensive theoretical contributions**: The paper provides both consistency guarantees (Theorem 1) and limiting distributions (Theorem 2) for change point estimators. The derivation of limiting distributions for network change point estimators is a significant theoretical advance that goes well beyond existing high-probability bounds in the network change point literature.

- **Practical inference procedure**: The data-driven confidence interval construction (Section 3.1) is a valuable practical contribution that enables uncertainty quantification, a capability not supported by competing methods. The real data application to agricultural trade networks demonstrates interpretable and historically meaningful change points.

- **Strong empirical performance**: The numerical experiments across four diverse scenarios (including violations of Model 1) show that CPDmrdpg substantially outperforms gSeg and kerSeg on multiple metrics, with near-perfect detection and localization in most settings.

## Weaknesses

### Fatal
None.

### Major
- **Theoretical assumptions are strong and their practical verification is unclear**: Assumption 1 requires that the latent position matrix X has singular values of order √n with bounded condition number, and that the CUSUM-transformed and averaged Q matrices have bounded condition numbers and singular values bounded away from zero. While these are standard in the tensor estimation literature, the paper does not discuss how practitioners can verify these conditions or what happens when they are violated. The low-rank structure of the CUSUM-transformed Q matrices (Assumption 1(ii)) is particularly opaque—it depends on the specific interval (s,e) and the location t, making it difficult to interpret or check.

- **The SNR condition (Assumption 2) is complex and not empirically validated**: The condition involves multiple terms (nL^{1/2}, d^2 m_max, nd, Lm_max) that scale differently. The paper does not provide guidance on how to estimate these quantities in practice or how to check whether the SNR condition holds for a given dataset. The threshold τ in Algorithm 1 is set based on this condition, but the practical choice (c_{τ,1}=0.1) is justified only by a brief mention in Section 4.1 without sensitivity analysis across different data generating processes.

- **Limited comparison with relevant baselines**: The paper compares only with gSeg and kerSeg, which are generic change point detection methods not designed for network data. The authors mention Wang et al. (2025) for online detection and Li et al. (2024) for deep learning approaches, but defer these comparisons to Appendix G.1. Given that the paper claims "substantially outperform existing state-of-the-art algorithms," a more comprehensive comparison with network-specific methods (even if designed for online settings) would strengthen the empirical claims.

### Minor
- **The computational complexity analysis is incomplete**: The paper states O(Tn²L log²(T)) for Stage I and O(Tn²L r log(n)) for Stage II, but does not account for the cost of TH-PCA itself, which involves SVD computations. The overall complexity O(Tn²L r log²(T ∨ n)) is stated without derivation or empirical runtime comparisons.

- **The real data analysis is limited**: Only one real dataset is presented in the main text (the second is in Appendix G.2). The confidence intervals in Table 4 are extremely narrow (e.g., (5.97, 6.03) for year 1991), which seems implausibly precise for a network with T=35 time points. The paper does not discuss whether these intervals are reasonable or whether they reflect overconfidence.

### Trivial
- The CUSUM definition in (1) has a typographical issue: "[t][s]" and "[e][t]" should likely be "(s, t]" and "(t, e]" respectively.

## Nice-to-Haves

- A discussion of how to select the Tucker ranks (r₁, r₂, r₃) in practice, beyond the heuristic of setting them "relatively large" as in Wang et al. (2025).
- Empirical runtime comparisons to complement the theoretical complexity analysis.
- A sensitivity analysis for the threshold constant c_{τ,1} across different scenarios, not just the single value reported.

## Novel Insights

The key insight is that the expected CUSUM-transformed adjacency tensors in D-MRDPGs admit a low-rank Tucker decomposition (with ranks (d, d, m^{s,e})), which enables the use of tensor heteroskedastic PCA for denoising. This connection between change point detection and low-rank tensor estimation is novel and elegantly exploited. The derivation of limiting distributions for change point estimators in network data is a genuinely new theoretical contribution that opens the door to statistical inference (confidence intervals, hypothesis testing) in dynamic network analysis.

## Suggestions

- Provide guidance on how practitioners can verify the low-rank assumptions or assess their plausibility for a given dataset. For example, discuss diagnostic checks or sensitivity analyses.
- Include a comparison with at least one network-specific change point method (even if designed for single-layer networks) to better contextualize the empirical improvements.
- Discuss the practical interpretation of the confidence intervals in the real data example—why are they so narrow, and what does this imply about the uncertainty in the detected change points?

## Score and Decision

The paper addresses a novel and important problem, provides substantial theoretical contributions (including the first limiting distributions for network change point estimators), and demonstrates strong empirical performance. The main weaknesses are the strength of the theoretical assumptions and the limited baseline comparisons, but these do not invalidate the core contributions. The paper is clearly written and makes a significant advance to the field.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>