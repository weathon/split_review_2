## Summary

This paper advances the theoretical foundations of separable neural networks (SepNNs) — architectures that factorize multivariate functions into linear combinations of univariate factor networks. Three contributions are made: (1) a universal approximation theorem proving SepNNs (CP, TT, Tucker) can approximate any continuous multivariate function with arbitrary precision; (2) NTK analysis establishing deterministic (infinite rank) and random (fixed rank) kernel regimes with spectral bias characterization; (3) SepPGD, a preconditioned gradient descent method that exploits the separable structure to reduce per-iteration complexity from O(n^D) to O(nD) on n^D grid samples. Experiments on kernel ridge regression, image/surface INRs, and PINNs demonstrate significant speedups.

## Strengths

**S1. Universal approximation theorem (Theorem 1) is a genuine theoretical advance.** The proof constructs the separable function class A, verifies the Stone-Weierstrass conditions, then approximates elements of A with SepNNs via vector-valued MLP universal approximation. This subsumes the bivariate case (Cho et al., 2023) and covers CP, TT, and Tucker architectures for D ≥ 2, offering a simpler and more general proof.

**S2. NTK decomposition and asymptotic regimes are original and well-reasoned.** Lemma 1 correctly expresses the SepNN NTK as a sum over factor-network NTK matrices scaled by outer products of other factors' outputs. Theorem 2 and Corollary 1 cleanly distinguish the deterministic kernel (infinite width + infinite rank) from the random kernel (infinite width + fixed rank) regimes.

**S3. SepPGD achieves a real and significant complexity reduction.** Decomposing the n^D × n^D preconditioner into D factor preconditioners (size n × n or R × n) is clever. The O(nD) per-iteration scaling is the paper's most practically impactful contribution. Lemma 2's equivalence proof for D=2 cleanly connects SepPGD to classical PGD with a Kronecker-sum preconditioner, and the vectorized matrix-product efficiency argument is sound.

**S4. Empirical results are strong and visually compelling.** PSNR improvement from ~26 to ~33 in image representation (Fig. 3), IoU improvement in surface representation, and consistent convergence speedups across KRR, INRs, and PINNs (Figs. 2, 4) convincingly demonstrate practical value. Convergence is measured against wall-clock time, which correctly reflects the complexity claims.

## Weaknesses

### Fatal
None.

### Major

**M1. The "provably" claim for SepPGD's spectrum adjustment is significantly stronger than what the paper actually proves.** The abstract (line 9) states SepPGD "provably adjusts its NTK spectrum" and the contributions (line 50) say it "provably adjusts the eigenvalue distribution of NTK matrix." However, Section 4's argument (line 201) is heavily hedged: "This can possibly be verified," "Suppose that ... which can be verified using ... Lemma 3," "It is believed that the result ... can be readily extended," and "This is left for future research." Several concrete gaps remain:

- The paper argues that \tilde{S} has better spectrum than \tilde{K}, but moving from \tilde{S}'s spectrum to K\tilde{S}'s spectrum is nontrivial — K and \tilde{S} may not commute, and K\tilde{S} is not symmetric, making standard spectral analysis more complex.
- The claimed closeness of \tilde{K} (the Kronecker-sum approximation) to the true NTK K is asserted without bounds or convergence rates; this is the critical link in the chain.
- The D>2 generalization and the convergence/solution-consistency analysis are explicitly deferred.

The method itself (SepPGD) remains interesting and empirically effective, and Lemma 2's equivalence is a genuine insight. But the "provably" language in the abstract and introduction misrepresents the strength of the theoretical support. This is the paper's most significant flaw and requires correction — the claims should be aligned with what is actually established.

### Minor

**m1. The pseudo-NTK matrix construction is underspecified in the main text.** Line 156 states: "calculating a pseudo NTK matrix K_{Θ_d} ∈ ℝ^{n×n} for each f_{Θ_d} on the corresponding input data \hat{x}_d ∈ ℝ^n using sum-of-logits (Mohamadi et al., 2023)." The factor network f_{Θ_d} maps ℝ → ℝ^R (R outputs), so its true NTK would be nR × nR. How this is reduced to n × n via "sum-of-logits" is not described in the main text. Since this construction is central to the algorithm's reproducibility, at least a brief summary is needed.

**m2. The spectral bias alleviation claim is not directly verified.** The paper attributes SepPGD's faster convergence to adjusting the NTK eigenvalue distribution, but never measures the eigenvalue distribution of the preconditioned effective kernel K\tilde{S}. Fig. 1(d) only shows the spectrum of the un-preconditioned SepNN. Faster convergence could also result from better conditioning of individual factor networks or larger effective step sizes. Direct spectral measurements of the preconditioned system would substantiate the claimed mechanism.

**m3. Notation inconsistency in Corollary 1 (line 130).** The statement writes f_Θ(x_1, ..., x_D) with bold x_d, but each factor network receives a scalar input; x_d (unbolded) would be correct.

**m4. The universal approximation proof sketch does not explicitly verify all Stone-Weierstrass conditions.** The text (line 82) states A must "contain the identity function" but does not show how the CP form realizes constant functions or projections. A brief justification would improve clarity.

### Trivial
None.

## Nice-to-Haves

- An ablation with S_d = I (no eigenvalue modulation) would isolate whether SepPGD's benefits come from the separable update structure itself or from the eigenvalue conditioning specifically.
- Reporting means and standard deviations over multiple seeds for PSNR, IoU, and MSE would strengthen the empirical claims.
- Stating the general form of Lemma 2 for D > 2 (even as a conjecture) would be more informative than "It is believed ... can be readily extended."
- Noting that activations like tanh or sin satisfy both the non-polynomial condition (Theorem 1) and differentiability (NTK analysis) would resolve the implicit tension.

## Removed Points

- **Criticism that full NTK-based PGD comparison is missing** — REMOVED (factually incorrect). The paper explicitly compares SepPGD with "the classical NTK-based PGD, the modified spectrum kernel (MSK)" (line 221), and figures include MLP(MSK) and SepNN(MSK) baselines. The comparison is present.
- **Criticism that the complexity table is imprecise about the O(n^{D-1}) cost** — REMOVED (already addressed). Footnote 3 explicitly acknowledges this cost and justifies why it is not the primary computational bottleneck.
- **Criticism about Lemma 3 not being defined in the main text** — REMOVED (subsumed by M1; appendix is stripped by the parser).
- **Generic strengths** (e.g., "addresses an important problem") — REMOVED. Only concrete, evidence-backed strengths are retained.

## Novel Insights

None beyond the paper's own contributions. The key finding from the review process is that the paper's "provably" framing for SepPGD is substantially more optimistic than the argumentation in Section 4 supports — a calibration issue rather than a novel observation about the work itself.

## Suggestions

1. **Tone down the "provably" language throughout.** Replace "provably adjusts the eigenvalue distribution" with a claim such as "equivalently implements a Kronecker-structured preconditioner derived from the SepNN's NTK, empirically alleviating spectral bias." Lemma 2's equivalence is a genuine insight that stands on its own and does not need the "provably" framing.
2. **Summarize the pseudo-NTK / sum-of-logits construction in 2–3 sentences** in the main text so the algorithm is reproducible without consulting the appendix.
3. **Add at least one direct measurement** of the preconditioned effective kernel's eigenvalue distribution or condition number to substantiate the spectral-bias alleviation narrative.
4. **Fix the notation in Corollary 1** (line 130).

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>