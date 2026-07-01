Now I have all the information needed. Let me produce the final consolidated review.

## Summary

This paper makes three contributions to separable neural networks (SepNNs): (1) a universal approximation theorem for CP, TT, and Tucker SepNNs using Stone-Weierstrass combined with standard universal approximation, extending the prior bivariate-only result; (2) a derivation of the neural tangent kernel (NTK) for SepNNs, showing convergence to a deterministic kernel under infinite width+rank and to a random kernel under fixed rank; and (3) a separable preconditioned gradient descent (SepPGD) method with O(nD) per-iteration complexity for n^D grid samples, motivated by spectral bias alleviation. Experiments on KRR, INRs, and PINNs demonstrate empirical speedups.

## Strengths

**1. Clean, general universal approximation theorem (Theorem 1, Section 2).** The proof combining Stone-Weierstrass with universal approximation extends prior results (which covered only the bivariate case or specific activations) to CP, TT, and Tucker SepNNs with any non-polynomial activation, for any D ≥ 2. The proof sketch is clear and the result fills a genuine gap in the theory of separable architectures.

**2. NTK decomposition and convergence regimes for SepNNs (Lemma 1, Theorem 2, Corollary 1, Section 3).** Deriving the NTK formula for SepNNs and proving convergence to a deterministic kernel under double asymptotics (infinite width + infinite rank) and a random kernel under fixed rank is genuinely novel. The Kronecker-product structure noted for the SepNN's NTK is a useful observation that can enable further efficiency results.

**3. SepPGD complexity analysis and D=2 equivalence (Lemma 2, Table 1).** The O(nD) per-iteration complexity for the preconditioner application, compared to O(n^D) for full NTK-PGD, is the central computational contribution and is convincingly derived. Lemma 2's equivalence between SepPGD and classical PGD for D=2 provides a clean theoretical connection to prior work and justifies the separable decomposition.

## Weaknesses

### Major

**1. Overclaim of "provably" adjusting the NTK spectrum, relative to what the main text actually shows.** The abstract and contributions list state that SepPGD "provably adjusts the eigenvalue distribution of NTK matrix, effectively alleviating spectral bias." However, the actual reasoning in Section 4 (page 8, line 201) is a chain of hedged or conditional statements: "This can possibly be verified" … "would have better spectrum" … "Suppose that K̃ is close to the true NTK matrix K" (which points to a Lemma 3 in the appendix) … "could provably" (an oxymoron) … "It is believed that the result … can be readily extended" … "This is left for future research." The equivalence is proven only for D=2 (Lemma 2), the D>2 extension is explicitly unproven, and the convergence analysis is deferred. The paper has solid theoretical contributions (Theorems 1, 2) independent of this claim, but the "provably" language in the abstract overstates what the main text demonstrates. Either the proof should be completed or presented in the main paper, or the claim should be honestly downgraded to an empirically motivated preconditioner.

### Minor

**2. No error bars or statistical significance on main experimental results.** Fig. 1 (NTK verification) reports variance over ten runs, but the main convergence curves (KRR in Fig. 2, PINN in Fig. 4) show no standard deviations, confidence intervals, or stated number of runs. For a paper making convergence claims, this omission weakens the empirical evidence.

**3. No ablation study on preconditioner design choices.** SepPGD has at least two tunable elements: (a) the eigenvalue modulation function g(λ_i) = λ_k (hard threshold), and (b) the update frequency (every ten iterations). Neither is ablated. Without such analysis, it is unclear which design choices drive the observed gains.

**4. Unqualified O(nD) complexity claim in the abstract.** The abstract states "O(nD) complexity for n^D training samples" without qualification. The main text clarifies this is the per-iteration cost of *applying* the preconditioner, and Footnote 3 acknowledges the O(n^{D-1}) construction cost. The abstract and Table 1 should make this distinction clearer to avoid misleading readers.

## Nice-to-Haves

- An ablation on the eigenvalue modulation function (e.g., soft threshold vs. hard threshold) and preconditioner update frequency would strengthen the empirical claims.
- A brief discussion of limitations (the grid-input assumption, the D>2 gap in the equivalence proof, and the fact that SepPGD reduces to standard complexity for non-grid inputs) would improve the paper's completeness, though the paper does acknowledge the grid assumption in a footnote.
- The Stone-Weierstrass conditions in Section 2 could briefly note that A is an algebra (closed under multiplication), which is true since CP ranks multiply. The paper states these are "carefully examined" in the appendix, which is acceptable.

## Removed Points

These points were raised in the input review but are removed after cross-checking:

- **"Limited baselines for the main claim":** The reviewer argued that SepPGD should be compared against classical PGD on an MLP. The paper *does* include MLP and MLP+MSK baselines in Fig. 2. The within-architecture comparisons (SepNN vs SepNN+SepPGD vs SepNN+MSK) are the most relevant, and these are shown.
- **"Overclaiming of noiseless vs noise case results":** The paper provides adequate qualitative description and the figures speak for themselves. Not a substantive weakness.
- **"Missing quantitative experimental details" (n, R, W, etc.):** These details are standard for the appendix, which the parser strips. Per instructions, appendix-specific criticisms are removed.
- **Stone-Weierstrass justification in Section 2:** The paper states the properties are verified in the appendix. This is standard practice.
- **Notation density / presentation concerns:** These are stylistic preferences, not substantive weaknesses.
- **Missing limitations section:** Not a standard requirement; the paper acknowledges the grid assumption in a footnote.
- **"Missing related works":** Per instructions, I cannot verify the existence of missing references.

## Novel Insights

None beyond the paper's own contributions. The review does surface a specific and verifiable mismatch between the "provably" language in the abstract and the hedged/conditional reasoning in Section 4, which is a useful calibration signal.

## Suggestions

- Revise the abstract and contribution list to replace "provably adjusts" with qualified language (e.g., "empirically adjusts" or "theoretically motivated to adjust") unless a complete proof is added to the main text. The paper is strong enough on its theoretical merits (Theorems 1, 2) without overclaiming on the PGD front.
- Add error bars to the convergence plots (KRR, INR, PINN).
- Include a brief ablation on the eigenvalue modulation function and preconditioner update frequency.

## Score and Decision

<score>6</score>
<decision>Borderline Accept</decision>

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>