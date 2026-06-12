## Summary

This paper analyzes the behavior of the Neural Tangent Kernel (NTK) for infinitely wide, fully-connected ReLU networks as depth increases. The authors prove that the normalized limiting kernel converges to the matrix of ones, while the corresponding closed-form solution for the network output converges to a well-defined, non-trivial limit. They employ rough differential equations to establish this result without requiring invertibility assumptions on the limiting kernel, and empirically evaluate the convergence rates.

## Strengths

- **Novel theoretical contribution**: The paper addresses an important gap in the NTK literature by analyzing the joint limit of increasing depth and width (with depth growing slower than width), providing rigorous convergence results for the kernel and the predictor. The use of rough differential equations to handle the singular limiting kernel is a technically sophisticated approach.

- **Clear problem framing**: The paper clearly identifies the tension between the kernel converging to a constant matrix (which would suggest degenerate behavior) and the predictor converging to a meaningful limit, and resolves this apparent contradiction through Theorem 3.

- **Generalizable framework**: The authors distill the key properties required for their results (Section 6), providing a template for analyzing other kernel sequences beyond the ReLU NTK.

## Weaknesses

### Fatal
None.

### Major

1. **Theorem 3 is not convincingly proven**: The proof sketch is extremely sparse and contains significant gaps. The construction of the rough path lift, the verification that the driving signals converge to zero in the appropriate topology, and the application of Lyons' Universal Limit Theorem are not adequately justified. The proof relies on Cramer's rule and determinant manipulations, but the connection to rough differential equations is not clearly established. The statement that "the solution u^{(L+1)}(t) converges to the solution u_∞(t) that solves the system u'_∞(t) = 0_n" is asserted without showing the necessary convergence of the vector fields or the rough paths. A rigorous proof would require significantly more detail.

2. **The rough differential equations framework appears unnecessary or misapplied**: The paper introduces heavy machinery from rough path theory, but the actual differential equation being solved (Equation 5) seems to be an ordinary differential equation derived from differentiating a linear system. The claim that the driving signals converge to zero in 1-variation and that this implies convergence of the solution via the Universal Limit Theorem is not properly justified. The connection between the determinant-based expressions and the rough path framework is unclear.

3. **Empirical evaluation is insufficient**: The experiments only show convergence curves for synthetic data and MNIST with a single random seed/configuration. There is no systematic study of how convergence rates depend on input dimension, dataset size, or the distribution of data. The claim that "convergence for the limiting kernel is experimentally fast" is not supported by quantitative metrics or comparisons. Figure 2 (mentioned in the text) is in the appendix and not provided in the main paper.

4. **Missing comparison with existing results**: The paper claims to improve upon Xiao et al. (2020) by not requiring invertibility assumptions, but does not provide a direct comparison of the limiting predictors. It would be valuable to show whether the limiting solution from Theorem 3 matches or differs from the predictions of Xiao et al. (2020) in regimes where both apply.

### Minor

1. **Proposition 1 is stated without proof**: The proof sketch is too brief to verify the claimed formulas. The statement that "μ = 0 implies x^T x' ≥ 0 with probability 1/2" is unclear and appears to contain a typo.

2. **The notation is sometimes confusing**: The use of superscript (L) to denote both the layer index and the total depth is overloaded, and the distinction between Θ_∞^{(L)} and Θ_∞^{(l)} is not always clear. The notation for the "normalized" kernel changes between Definition 4 and Theorem 3 (using both \bar{Θ} and \tilde{Θ}).

3. **The function ψ_d in Definition 6 appears ad hoc**: The specific form of ψ_d is not motivated, and its role in the proof of Theorem 3 is not explained. The parameter d is set to the determinant D, but the dependence on d in the properties (especially property 4) is not connected to the convergence as L → ∞.

### Trivial
None.

## Nice-to-Haves

- A more detailed proof of Theorem 3 in the main text or a clear roadmap of how the rough path theory is applied.
- Quantitative convergence rates (e.g., explicit bounds on how fast the predictor converges as a function of L).
- Experiments on additional datasets and with varying input dimensions to validate the generality of the convergence behavior.

## Novel Insights

The paper's key insight is that even though the normalized NTK converges to the all-ones matrix (which is singular for n > 1), the quantity κ_x^T κ^{-1} that appears in the predictor converges to a well-defined limit. This resolves an apparent paradox in the literature and shows that depth does not necessarily destroy the predictive power of the NTK. The use of rough differential equations to interpolate between different depths and prove convergence is a novel technical approach in this context.

## Suggestions

1. Provide a complete, rigorous proof of Theorem 3, either in the main text or in a clearly marked appendix. The current sketch is insufficient for a top venue.

2. Clarify the connection between the determinant-based expressions and the rough differential equation framework. Show explicitly how the driving signals v_{ij}^{(L)} are defined and why they converge to zero in the 1-variation metric.

3. Add more comprehensive experiments, including: (a) quantitative convergence rates (e.g., relative error vs. depth), (b) experiments with varying input dimension and dataset size, (c) comparison with the predictions of Xiao et al. (2020) where applicable.

4. Improve the exposition of the proof of Theorem 3 by providing a high-level roadmap before diving into the technical details.

## Score and Decision

The paper addresses an important question in the NTK literature and proposes a novel approach using rough differential equations. However, the central theoretical result (Theorem 3) is not convincingly proven, and the empirical evaluation is too limited to fully support the claims. The paper has potential but requires substantial revision to meet the standards of ICLR.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>