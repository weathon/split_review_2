## Summary

This paper theoretically analyzes the behavior of the Neural Tangent Kernel (NTK) for infinitely wide fully-connected ReLU networks as depth increases. It claims that the normalized limiting kernel converges to the matrix of ones (Theorem 2), while the closed-form solution for the learned function \(\kappa_x^\top \kappa^{-1}\) converges to a well-defined, non-trivial limit (Theorem 3). The proof of Theorem 3 employs rough differential equations (RDEs) to handle the limiting singularity. Empirical illustrations on synthetic and MNIST data are provided.

## Strengths

- The paper tackles a genuinely important question: how depth affects the NTK and the resulting predictor in the infinite-width limit.
- The observation that the normalized kernel becomes constant while the predictor still has a meaningful limit is interesting and potentially clarifies the "ordered phase" behavior described in prior work.
- The attempt to use rough path theory to handle singular limiting kernels is novel and, if carried out rigorously, could provide a useful tool for the community.

## Weaknesses

### Fatal

1. **Theorem 3 is not convincingly proved.** The proof sketch of Theorem 3 is far from rigorous. The construction of the driving path \(v_{ij}^{(L)}\) and the rough path lift is not properly defined; the application of Lyons’ Universal Limit theorem is not justified given the incomplete specification of the RDE; the inequalities involving determinants are hand-wavy and do not clearly establish convergence of the solution. The claim that \(v_{ij}^{(L)} \to 0\) in 1-variation and that this implies convergence of the solution to \(u'(t)=0\) via rough path theory is asserted without the necessary technical details. As it stands, the proof does not meet the mathematical standards required for a theoretical contribution at a top venue.

### Major

2. **Extremely weak empirical evidence.** The experiments consist of a single figure (plus a similar figure in the appendix for MNIST) showing convergence curves of kernel entries for one synthetic dataset and MNIST. There are no quantitative metrics, no comparison with actual finite-width neural network training, no analysis of how the limiting solution relates to test performance, and no evaluation of the claimed fast convergence of \(\kappa_x^\top \kappa^{-1}\). The paper claims to “empirically evaluate the order of magnitude in network depth required” but provides no such quantitative estimate.

3. **Writing is unclear and disorganized.** The paper jumps between definitions, propositions, and theorems without a clear narrative. Key steps in the proofs are left to the appendix (which is stripped), but even the main text contains non-sequiturs and incomplete derivations. The notation is excessive and sometimes inconsistently used (e.g., \(\tilde{\Theta}\) appears without proper definition in Theorem 3). The flow makes it difficult to assess what is actually proven versus speculated.

4. **Overclaiming relative to what is shown.** The paper says “Our results apply to arbitrary data with support on the sphere” but offers no proof or experiment showing the results hold beyond uniform data or MNIST. The claim that the results “do not require any assumptions on the spectrum of the Hermite expansion” is true but the proofs instead rely on a new set of assumptions that are equally restrictive (e.g., compact support on the sphere, invertibility of certain determinants along the interpolation path).

5. **Missing connection to practice.** The paper does not explain what the limiting solution actually means for generalization, representation learning, or training dynamics. The theoretical results are presented in isolation without any interpretation or validation on actual finite-width networks.

### Minor

- Proposition 1 and its proof sketch are too sparse; the derivation of \(\Theta_\infty^{(L+1)}\) for perfectly correlated inputs is not fully convincing.
- The list of “essential properties” for generalizing to other kernels (Section 6) is vague and not validated on any other kernel beyond a trivial example \(\eta^{(L)}\).
- The paper repeatedly contrasts with Xiao et al. (2020) but the exact nature of the improvement is not clearly delineated.

### Trivial

- The figure caption appears garbled with LaTeX artifacts.
- Some references are incomplete (e.g., “(see Table 1 in Appendix E)” but the appendix is missing).

## Nice-to-Haves

- A clear comparison (both theoretical and numerical) with the finite-depth, finite-width case to show the practical relevance of the infinite-depth limit.
- Quantitative estimates of the convergence rate of \(\kappa_x^\top \kappa^{-1}\) and how it depends on \(n_0\) and dataset size.
- A self-contained, rigorous proof of Theorem 3 that does not rely on rough path machinery unless that machinery is fully introduced and its application justified step-by-step.

## Novel Insights

None beyond the paper’s own contributions. The idea that the NTK becomes constant with depth while the predictor still converges is already implicit in the “ordered phase” literature (Xiao et al., 2020; Seleznova & Kutyniok, 2022). The use of RDEs is novel but not sufficiently developed to yield new insights.

## Suggestions

1. Either provide a complete, rigorous proof of Theorem 3 (including all necessary definitions from rough path theory and a clear justification of each step) or reframe the contribution without relying on RDEs.
2. Add quantitative experiments: compare the limiting solution with actual trained finite-width networks at various depths; report numerical convergence rates of \(\|\kappa_x^\top \kappa^{-1} - \text{limit}\|\) vs \(L\); include error bars and multiple random data samples.
3. Improve the exposition: clearly separate assumptions, statements, and proofs; ensure every notation is defined before use; provide a roadmap of results.
4. Discuss the implications of the limiting solution for generalization or training dynamics, even if speculatively.

## Score and Decision

The main theoretical result (Theorem 3) is not convincingly established, and the empirical validation is insufficient to support the claims. The paper has interesting ideas but does not meet the rigor and completeness standards required for acceptance at a top venue.

**Score:** The paper has a fatal flaw in its central proof and lacks empirical support. A score of 3 (reject) is appropriate.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>