## Summary

This paper studies sparse signal support recovery when observations come from two sources: a small number of high-quality (low-noise) measurements and a larger number of low-quality (high-noise) measurements. It provides sufficient conditions for information-theoretic recovery in both an agnostic setting (decoder unaware of per-sample noise variances) and an informed setting (decoder knows the variances), introducing the *Price of Quality*—the number of low-quality samples needed to replace one high-quality sample in these sufficient conditions. The paper also extends the classical LASSO recovery phase transition (Wainwright, 2009) to the heterogeneous-noise agnostic setting, showing that the threshold depends only on total sample size and average noise level, not on individual noise variances.

## Strengths

- **Timely and practical problem.** Combining high-quality and low-quality data (e.g., human vs. LLM labels) is a central challenge in modern machine learning. The paper formalizes this for sparse recovery and provides the first theoretical results in this direction.
- **Clear conceptual contribution.** The *Price of Quality* is an intuitive and well-defined quantity that cleanly captures the trade-off between data sources. The contrast between the agnostic setting (price ≤ 2) and the informed setting (price can be arbitrarily large) is insightful and has practical implications.
- **Rigorous extension of known results.** The LASSO analysis (Theorem 3) carefully generalizes Wainwright (2009) to heterogeneous noise, overcoming the loss of Wishart structure via a QR decomposition and Haar-measure arguments. The proof sketch is clear, and the necessary and sufficient conditions on noise scaling (Proposition 4.1) are provided.
- **Well-structured and clearly written.** The paper is organized logically, the theorems are stated precisely, and the interpretations (e.g., the three SNR regimes) help the reader understand the qualitative behavior of the results.

## Weaknesses

### Fatal
None.

### Major
- **Information-theoretic results are only sufficient, not necessary.** The price of quality is derived from a sufficient condition (Theorems 1 and 2), so it is a property of the analysis, not necessarily the true information-theoretic trade-off. The paper acknowledges this (Remark 3.2) but does not provide matching lower bounds. This limits the strength of the claims about the price of quality.
- **No experimental validation.** The paper is purely theoretical. While theory papers can be accepted without experiments, the lack of any simulations or real-data illustrations makes it harder to assess the tightness of the sufficient conditions or the practical relevance of the price-of-quality concept.
- **Algorithmic recovery only analyzed in the agnostic setting.** The informed setting is left for future work (Remark 4.2). Given that the informed setting yields a qualitatively different price of quality at the information-theoretic level, understanding the algorithmic threshold there would complete the picture.

### Minor
- **Binary signal assumption for information-theoretic results.** The paper assumes $\beta^* \in \{0,1\}^p$ (or non-zero entries at least 1). While this is common in the literature and the paper argues it is representative, it restricts the generality of the results.
- **Gaussian design and noise.** The results rely on Gaussianity of both the design matrix and the noise. The paper mentions possible extension to sub-Gaussian errors but does not provide details. The analysis may not transfer to heavy-tailed or discrete distributions.
- **The agnostic estimator (8) is combinatorial and not tractable.** The information-theoretic threshold in the agnostic setting uses an MLE that is NP-hard in general. The paper does not discuss this computational issue, though it is standard in the literature.

### Trivial
None.

## Nice-to-Haves

- Simulations illustrating the price of quality in both settings and comparing the sufficient conditions to empirical recovery thresholds would greatly strengthen the paper.
- A discussion of how the price of quality could be estimated or used in practice (e.g., to decide whether to collect more high-quality or low-quality data) would increase practical impact.
- An analysis of the informed algorithmic setting (e.g., a weighted LASSO) would complete the picture and is a natural next step.

## Novel Insights

Beyond the paper’s own contributions, the key insight is that the information-theoretic and algorithmic thresholds respond very differently to data heterogeneity. At the information-theoretic level, knowing which samples are high-quality can dramatically increase the value of those samples (price of quality can be arbitrarily large). At the algorithmic level (LASSO in the agnostic setting), the threshold is completely insensitive to heterogeneity—only the total sample size and average noise matter. This suggests that the robustness of the LASSO to heteroscedasticity is a genuine property of the algorithm, not just an artifact of the homogeneous-noise analysis.

## Suggestions

- Provide matching lower bounds (or at least a discussion of the difficulty of obtaining them) for the information-theoretic thresholds to clarify whether the price-of-quality expressions are tight.
- Add a small simulation study (even in the appendix) to demonstrate the predicted phase transitions and the price of quality, e.g., by plotting recovery success as a function of $(n_1, n_2)$ for different noise ratios.
- Discuss the computational complexity of the agnostic MLE and whether the information-theoretic threshold is relevant for tractable algorithms beyond the LASSO.

## Score and Decision

**Score:** 6  
**Decision:** Accept

MY FINAL SCORE: <score>6</score>  
MY FINAL DECISION: <decision>Accept</decision>