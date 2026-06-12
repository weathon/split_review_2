## Summary

This paper proposes the first offline change point localization and inference method for dynamic multilayer random dot product graphs (D-MRDPGs). The authors develop a two-stage algorithm that combines seeded binary segmentation with low-rank tensor estimation (TH-PCA), establish consistency for both the number and locations of change points, derive limiting distributions of refined estimators under both vanishing and non-vanishing jump regimes, and provide a data-driven confidence interval procedure. Extensive experiments demonstrate superior performance over existing alternatives.

## Strengths

- **Genuine novelty in theory and methodology.** The paper provides the first limiting distribution results for change point estimators in network data (Theorem 2), deriving explicit two-sided Brownian motion limiting distributions under both vanishing and non-vanishing jump regimes. This is a significant theoretical contribution that goes well beyond localization consistency.

- **Principled two-stage design with strong guarantees.** The algorithm cleanly separates coarse detection (seeded binary segmentation with CUSUM statistics) from refinement (TH-PCA-based scan statistics). Theorem 1 establishes sharp localization rates of order $\kappa_k^{-2}\log(T)$, which is a substantial improvement over the $\kappa^{-2}(d^2 m_{\max} + nd + Lm_{\max})\log(\Delta/\alpha)$ rate of the online method in Wang et al. (2025).

- **Practical confidence interval construction.** The data-driven CI procedure in Section 3.1 is a complete pipeline (estimate jump size → estimate variances → simulate limiting distribution → construct CI), with demonstrated strong coverage in simulations. This fills a real gap, as competitors (gSeg, kerSeg) do not support inference.

- **Thorough experimental evaluation.** The four simulation scenarios systematically test both Model 1-consistent and Model 1-violating settings. The method demonstrates robustness even under model violations (Scenarios 2–3), achieving near-perfect change point count estimation and localization. The real-data application to agricultural trade networks yields interpretable change points aligned with well-documented geopolitical events (German reunification 1991, WTO agreements 1999/2005/2013).

## Weaknesses

### Fatal
None.

### Major

- **Restrictive minimal spacing assumption.** The assumption $\Delta = \Theta(T)$ bounds the number of change points $K$ to be $O(1)$, which is quite restrictive. While the authors acknowledge this can be relaxed using narrowest-over-threshold approaches, the current theoretical results do not cover the practically important case of $K$ growing with $T$. This limits the scope of the theoretical contribution, particularly for applications where change points may be more frequent.

- **Limited competitor comparison for multilayer settings.** The competitors (gSeg, kerSeg) are single-layer methods adapted to multilayer data. While the authors note that no prior offline method exists for multilayer networks, a more systematic comparison with adaptations of the online method of Wang et al. (2025) to the offline setting (e.g., running it on sliding windows) would strengthen the empirical case. The brief mention in Appendix G.1 is not sufficient given that this is the most natural multilayer competitor.

### Minor

- **Threshold tuning sensitivity.** The threshold $\tau = c_{\tau,1} n\sqrt{L}\log^{3/2}(T)$ requires selecting $c_{\tau,1}$, which is set to 0.1 based on Theorem 1's range. While sensitivity analysis is provided, the theoretical range $(c_{\tau,1}, c_{\tau,2})$ may be wide, and more practical guidance on selection (e.g., via cross-validation or data-splitting) would improve usability.

- **Rank selection in TH-PCA.** The choice of input ranks $r_1 = r_2 = 15$, $r_3 = L$ is described as motivated by robustness, but lacks formal justification or sensitivity analysis showing how rank misspecification affects results. The assumption that the intrinsic dimension $d$ is known (Assumption 1(i)) is also a practical limitation not fully addressed.

- **Confidence interval coverage dip in Scenario 3.** The coverage drops to 76.67% for $n=100$ in Scenario 3, which violates Model 1. While the authors explain this is due to model violations and small changes, a more systematic discussion of when the inference procedure breaks down would be valuable.

### Trivial
None.

## Nice-to-Haves

- A formal comparison of computational costs across methods in the experiments section would help practitioners choose between methods.
- A discussion of how to select the number of layers $L$ or handle the case where some layers are uninformative would broaden applicability.

## Novel Insights

The derivation of limiting distributions for change point estimators in network data is genuinely novel. The key insight is that the refined estimator $\hat{\eta}_k$ converges at rate $\kappa_k^{-2}$ (without the log factor from the localization step), and its limiting distribution involves an argmin of a two-sided Brownian motion with asymmetric variance parameters $\sigma_{k,k}$ and $\sigma_{k,k+1}$. These variances depend on the projection of the noise onto the normalized jump direction $\Psi_k$, capturing how the signal direction interacts with the stochastic structure of each segment. This result naturally extends classical CUSUM theory to the tensor-valued, latent-structure network setting.

## Suggestions

- Consider adding a practical rank selection procedure (e.g., based on the elbow method for singular values of the CUSUM tensors) to reduce dependence on knowing $d$.
- Include a more detailed comparison with Wang et al. (2025) adapted to offline settings, even if only in the appendix.
- Discuss the trade-off between the threshold constant $c_{\tau,1}$ and the number of false positives more explicitly, ideally with a calibration procedure.

## Score and Decision

This paper makes a strong contribution by establishing the first offline change point detection framework for dynamic multilayer networks, with novel theoretical results including limiting distributions and confidence intervals. The methodological design is sound, the theoretical analysis is rigorous, and the experiments are comprehensive. The major weaknesses (restrictive spacing assumption, limited competitor comparison) are acknowledged and partially addressed. The paper fills a clear gap in the literature and provides tools that are both theoretically grounded and practically useful.

MY FINAL SCORE: 7.0
MY FINAL DECISION: Accept