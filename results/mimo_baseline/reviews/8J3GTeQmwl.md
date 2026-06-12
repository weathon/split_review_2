## Summary
This paper proposes a cross-validation method for graphon models based on random imputation of held-out edges followed by an affine distributional correction. The method provides an efficient alternative to edge cross-validation (ECV) approaches that rely on expensive matrix completion, and the authors prove asymptotic consistency of the CV-imputation score. Experiments across synthetic graphon datasets and real-world networks demonstrate superior accuracy and computational efficiency over ECV.

## Strengths
- **Clean and well-motivated methodological contribution.** The core idea—replacing held-out edges with random Bernoulli samples and correcting the distributional shift via the affine transformation in Eq. (6)—is elegant, simple to implement, and avoids the expensive matrix completion step required by ECV (Li et al., 2020a). Lemma 1 provides a crisp justification for why this works.
- **Sound theoretical foundation.** Theorem 1 establishes that V_K(M) is asymptotically parallel to L(M) + Λ up to a controlled error rate, under a computationally verifiable condition on the optimism bias. The uniform convergence result ensures model selection consistency.
- **Comprehensive empirical evaluation.** Experiments span four graphon functions (dense/sparse, low-rank/full-rank) and four estimation methods (NS, SAS, USVT, ICE), with 100 replications. CV-imputation consistently achieves lower MSE than ECV across all configurations (Table 1), with the gap most pronounced for dense networks (Graphon 1).
- **Compelling real-world application.** The COVID-19 drug-disease co-occurrence network case study is well-structured: the authors use temporal holdout validation (training on Jan–Apr 2020, testing on May 2020) and demonstrate that CV-imputation selects a model yielding better link prediction accuracy. The identification of ledipasvir as a potential COVID-19 treatment, subsequently supported by clinical evidence, provides a tangible demonstration of practical value.
- **Scalability advantages.** The complexity analysis clearly shows CV-imputation adds only O(n²) per fold versus O(n³) for matrix completion in ECV, and Table 2 confirms substantial speedups (e.g., ~30× faster on the Yeast network).

## Weaknesses
### Fatal
None.

### Major
- **Sensitivity to the imputation parameter θ.** The random imputation uses Bernoulli(θ) draws, and while the affine correction in Eq. (6) accounts for the distributional shift, the paper's treatment of θ is deferred to the appendix. This is an important practical concern: the imputed entries effectively add noise to the training adjacency matrix, and the estimator must absorb this noise. For very sparse or very dense networks, a poorly chosen θ could degrade estimation quality in early folds before the affine correction takes effect. A brief in-paper sensitivity analysis or guidance on choosing θ (e.g., θ = empirical network density) would strengthen the work considerably.

- **Limited theoretical scope of Condition 1.** The polynomial decay assumption on the optimism bias Q_K(M) is critical to Theorem 1, yet the paper only verifies it for the trivial Erdős–Rényi case. For the graphon estimation methods actually used in experiments (NS, SAS, USVT, ICE), the rate α is unknown. While the computational verification in Figure S.3 (appendix) is appreciated, the gap between what theory guarantees and what experiments demonstrate weakens the theoretical contribution.

### Minor
- **Narrow baseline comparison.** The paper compares exclusively against ECV (Li et al., 2020a). Other cross-validation strategies for network data exist (e.g., node-based CV with appropriate adjustments, the approaches in Jasra et al. or Li et al. 2020b). Including even one additional baseline would strengthen the empirical claims.

- **Method selection accuracy is incomplete for smaller networks.** In Figure 5, at n=50 the method selection accuracy is only ~50-60% for some graphons, comparable to random selection among four methods. While this improves with n, the practical utility for moderate-sized networks could be better discussed.

### Trivial
- Figure 3 caption appears garbled by the parser (claims ECV is faster, contradicting all data in the paper). This is clearly a parsing artifact.

## Nice-to-Haves
- A discussion of how to choose K (number of folds) in practice, beyond the standard trade-off considerations.
- Extension to directed networks, which are common in practice.
- An analysis of how the affine correction interacts with different estimators—for some estimators (e.g., thresholding-based like USVT), the shifted distribution P^{[-k]} = w_k θ11^T + (1-w_k)P may interact non-trivially with the thresholding step.

## Novel Insights
The key novel insight is that network cross-validation can be made both theoretically sound and computationally cheap by combining random edge imputation with a post-hoc affine distributional correction. This avoids the fundamental tension in network CV between preserving graph structure and achieving independence between training and validation sets. The observation that the training distribution is an affine transform of the true distribution (Eq. 5) is the linchpin that makes the simple correction in Eq. 6 valid without requiring matrix completion or low-rank assumptions.

## Suggestions
- Add an in-paper sensitivity analysis for θ across different network densities and sizes, even if briefly.
- Discuss the practical guidance for choosing K and how it interacts with network sparsity.
- Clarify in the main text (not just appendix) how the method handles very sparse networks where most imputed entries are 0 and the effective training signal per fold is reduced.

## Score and Decision
This is a well-executed methodological paper that addresses a genuine problem (CV for graphon estimation), proposes an elegant and practical solution, provides asymptotic theory, and validates extensively. The contribution is clean but somewhat narrow in scope—specific to graphon model selection with independent edges. The theoretical condition could be better motivated, and the sensitivity to θ deserves more in-paper attention. Overall, it represents solid, useful work worthy of acceptance at a top venue, though not a breakthrough.

MY FINAL SCORE: 6.0
MY FINAL DECISION: Accept