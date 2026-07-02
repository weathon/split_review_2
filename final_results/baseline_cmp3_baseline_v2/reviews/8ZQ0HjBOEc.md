## Summary

This paper studies the behavior of the Neural Tangent Kernel (NTK) for infinitely wide, fully-connected ReLU networks as depth grows to infinity. Theoretical results show that the normalized kernel converges to the all-ones matrix (Theorem 2), while the closed-form solution from NTK regression is claimed to converge to a well-defined limit via rough differential equations (Theorem 3). The paper also provides empirical illustrations of convergence rates and lists properties for generalizing the results to other kernels.

## Strengths

- The research question—how the NTK predictor behaves when the kernel becomes degenerate with increasing depth—is well-motivated and potentially important for understanding overparameterized networks.
- The use of rough differential equations as a technical tool to handle convergence when the kernel becomes singular is creative and conceptually interesting.
- The paper provides a concise list of kernel properties (Section 6) that could guide analysis of other architectures, an attempt at generalization beyond the specific ReLU setting.

## Weaknesses

### Fatal
- **Theorem 3, the paper's central claimed contribution, is not convincingly proven.** The proof sketch in the main text is insufficient to establish the result. Key objects (e.g., the paths `v_{ij}^{(L)}`, the rough path lift with `p=1`) are introduced without clear construction or justification. The connection between the interpolated linear system `A_n(t)u(t)=b_n(t)` and the claimed rough differential equation is not explained. The argument that the Itô-Lyons map yields a limiting solution `u_∞(t)` satisfying `u'(t)=0` conflates convergence of driving signals with convergence of the solution, and the boundedness claim is not derived from the preceding inequalities. For a theoretical paper, a rigorous proof is required, and the sketch provided is far from meeting that standard.

### Major
- **The notation `\tilde{\Theta}_\infty^{(L)}` used throughout Theorem 3 and its proof is never defined.** Definition 4 defines `\bar{\Theta}_\infty^{(L)}`; whether `\tilde{\Theta}` refers to the same object, a different normalization, or something else is unclear. This makes the theorem statement and proof unverifiable.
- **The theorem does not characterize the claimed limit.** Theorem 3 asserts existence of a limiting expression for `\tilde{\Theta}_\infty^{(L)}(x^\top X)(\tilde{\Theta}_\infty^{(L)}(XX^\top))^{-1}` but provides no formula, description, or useful property of this limit beyond a generic boundedness bound. Without knowing what the limit is, the practical significance for understanding neural network behavior is unclear.
- **The empirical evaluation is very weak.** Only synthetic data with `n_0=128` is shown in the main text; the MNIST results are relegated to an appendix that was stripped. The experiments only visualize kernel value convergence, not the convergence of actual predictions or any comparison with finite-width neural network training. The paper claims "convergence for the limiting kernel is experimentally fast" but the figures show values still changing noticeably across `L`.

### Minor
- The proof of Lemma 1 (convergence of `ρ^{(L)}` to 1) is not included in the main text and the claimed proof in the appendix is inaccessible due to stripping. While this lemma is likely correct from known properties of the ReLU arc-sine kernel, the paper should include the reasoning or a clear reference.
- The paper acknowledges that the NTK kernel properties studied (convergence to all-ones, degeneracy) are already known from prior work (e.g., Xiao et al. 2020, Bietti & Bach 2021), but does not clearly delineate which results are novel vs. recapitulated.

### Trivial
- The proof of Theorem 3 contains a typographical inconsistency: `\leftrightarrow_{i,j}` and `\leftarrow_{i,j}` appear to be used interchangeably for matrix column replacement.
- Proposition 1 uses a "proof sketch" label but the sketch is too abbreviated to be informative.

## Nice-to-Haves

- Directly characterizing the limiting predictor (e.g., showing it is equivalent to a simple function of the data, or that it interpolates the training points in a specific way) would greatly increase the paper's impact.
- An experiment comparing the NTK predictor at finite `L` with actual gradient-descent-trained finite-width networks would ground the theoretical results in practice.
- Clarifying why rough differential equations are necessary rather than a more direct analysis (e.g., careful study of the limiting inverse of a near-singular kernel) would help readers evaluate the technical contribution.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Provide a complete, self-contained proof of Theorem 3 in the main paper, including a clear definition of `\tilde{\Theta}`, a step-by-step explanation of how the RDE is constructed, and verification of the convergence conditions. Alternatively, use a more direct analytic approach to establish convergence of the predictor without rough path machinery.
2. Characterize the limiting predictor explicitly, or at least provide non-trivial properties (e.g., whether it corresponds to a constant function, or interpolates `y^*` at training points).
3. Include experiments that plot the actual predictor `f_∞(x)` at increasing `L` for a concrete dataset, and compare with the predictions from finite-width networks.

## Score and Decision

**Score: 3**

**Decision: Reject**

**Reasoning:** The paper addresses a relevant question about depth in the NTK regime, but the main theoretical contribution (Theorem 3) is not adequately proven in the presented text, with undefined notation, insufficient justification of the rough-path construction, and an incomplete proof sketch. The empirical evaluation is too minimal to compensate. The kernel convergence results (Theorems 1-2) are largely already known from prior work. The paper's potential value is undermined by these execution issues, and it does not meet the standard of rigor expected for ICLR.

MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>