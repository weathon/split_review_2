Now I have verified all claims. Let me write the final consolidated review.

## Summary

This paper makes three contributions to separable neural networks (SepNNs): (1) a universal approximation theorem proving SepNNs with CP, TT, and Tucker structures can approximate any continuous multivariate function; (2) NTK regime analysis showing the SepNN's NTK converges to a deterministic kernel under infinite width+infinite rank and to a random kernel under infinite width+fixed rank, with spectral bias characterization; and (3) SepPGD, a preconditioned gradient descent method reducing per-iteration complexity from O(n^D) to O(nD) for n^D grid samples. The method is validated empirically on KRR, image/surface INRs, and PINNs.

## Strengths

1. **NTK regime characterization with deterministic vs. random kernel distinction (Theorem 2, Corollary 1).** This is the paper's strongest theoretical contribution. The clean delineation of two asymptotic regimes — deterministic NTK under infinite width + infinite rank (Theorem 2), and random NTK under infinite width + fixed rank (Corollary 1) — is genuinely novel. The fixed-rank random regime is practically relevant since SepNN rank is typically chosen small (line 128). The empirical verification using ten random seeds (Fig 1) appropriately supports this theory.

2. **SepPGD's O(nD) complexity advantage (Table 1, Remark 4).** Table 1 and Remark 4 document an exponential-to-linear reduction: O(nD) per-iteration preconditioner application vs. O(n^D) for prior NTK-based PGD (Geifman et al., 2024), with construction cost reduced from O(n^{3D}+n^{2D}P) to O(D(n^3+n²P)). This is a genuine and practically significant improvement for grid-based training common in INRs and PINNs.

3. **Universal approximation theorem for multivariate SepNNs (Theorem 1).** Theorem 1 extends prior results (Cho et al., 2023, bivariate CP only) to arbitrary D≥2 and to CP, TT, and Tucker structures, using a clean proof strategy combining Stone-Weierstrass and universal approximation.

4. **Explicit NTK formula for CP SepNN (Lemma 1).** Equation (4) provides a principled decomposition of the SepNN's NTK as a sum over factor MLP NTK matrices weighted by products of other factor outputs, which is the foundation for both the NTK convergence analysis and the SepPGD design.

5. **Lemma 2 establishes equivalence to classical NTK-based PGD for D=2.** The paper proves that SepPGD in the bivariate case is exactly equivalent to the full preconditioned gradient with a Kronecker-structured preconditioner, providing a formal connection to the prior PGD literature.

## Weaknesses

### Major

1. **Overclaimed "provable" spectral bias alleviation for SepPGD.** The abstract and introduction state that SepPGD "provably adjusts the eigenvalue distribution of NTK matrix" (lines 9, 50). However, the core reasoning in Section 4 (line 201) relies on the supposition that "\(\tilde{\mathbf{K}}\) is close to the true NTK matrix \(\mathbf{K}\) which can be verified using the NTK matrix formulation in Lemma 3." The paper also states that convergence and solution consistency of SepPGD "is left for future research" (line 201). The proof chain therefore has a conditional structure (depending on closeness of \(\tilde{\mathbf{K}}\) to \(\mathbf{K}\)) and leaves the algorithm's convergence unanalyzed, making the unqualified "provably" in the abstract and contributions list stronger than what is actually demonstrated. The complexity advantage and empirical results are not in question, but the rhetorical framing oversells the theoretical guarantee.

2. **SepPGD theory established only for D=2 while experiments include D≥3.** Lemma 2 and the spectral bias alleviation argument are explicitly stated for the bivariate case. The paper says "It is believed that the result in Lemma 2 (and the analysis following) can be readily extended to multivariate cases D > 2" (line 201), but does not provide this extension. Experiments on 3D surface representation (D=3) and 3D diffusion equations (D=4 with the time dimension) therefore lack direct theoretical grounding for the SepPGD claim. The SepPGD algorithm definition (Definition 1) and complexity analysis are general, but the equivalence to classical PGD (and thus the spectral argument) is not.

### Minor

3. **No error bars or multiple-run statistics for main experimental results (Figs 2–4).** Only the NTK verification (Fig 1) uses ten random seeds. Figures 2, 3, and 4 report single convergence curves and single PSNR/IoU/MSE values without variance. Given the random initialization and the random NTK regime under fixed rank, the reader cannot assess whether reported improvements are statistically significant or vary across seeds.

4. **MSK baseline omitted from visual comparison (Fig 3).** The text lists MLP (MSK) and SepNN (MSK) as baselines (line 221), and Fig 2 shows all five methods in convergence curves. However, Fig 3's visual results show only Original, MLP, SepNN, and SepNN(SepPGD) — SepNN(MSK) is absent. Since MSK is the closest prior preconditioning method, this omission makes it harder to attribute visual gains specifically to SepPGD vs. preconditioning in general.

### Trivial

5. **Stone-Weierstrass condition stated as "contains the identity function" (line 82).** Standard formulations of the Stone-Weierstrass theorem require the algebra to contain the constant functions (or the constant 1 function), not the identity function f(x)=x. This is likely an imprecision in the proof sketch; the full proof in the appendix presumably uses the correct condition.

## Nice-to-Haves

- An ablation on rank R showing how SepPGD's effectiveness varies with rank would connect the fixed-rank NTK theory (Corollary 1) with practical preconditioner behavior.
- A small-scale experiment (e.g., n=8, D=2) comparing SepPGD against the full O(n^D) NTK-based PGD (tractable at that size) would directly validate the Kronecker-product approximation chain.
- A wall-clock breakdown of preconditioner construction vs. application costs would strengthen the efficiency claim.

## Removed Points

These points were raised by reviewers but removed as invalid, speculative, or not anchored in the paper:

- **"PSNR improvement magnitude is unexplained/misleading"** — The paper clearly states results are "under the same iteration number" (Fig 3 caption). The critic's speculation about different learning rates or convergence regimes is not anchored in specific evidence from the paper.
- **"O(nD) complexity framing is misleading"** — Remark 4 transparently documents both application and construction costs. Disclosing the full cost while using the per-iteration figure in the abstract is standard practice.
- **"Experimental section is too brief"** — Details are deferred to Appendix A.12, which is standard; the parser strips appendices.
- **"Failure modes not discussed"** — Not required for the paper's scope; a nice-to-have, not a weakness.
- **"Scaling factor 1/√R inconsistency between NTK and approximation theory"** — The paper explicitly notes (line 118) this scaling "does not affect the universal approximation Theorem 1."
- **"Missing related works"** — Cannot verify without external sources; per instructions, do not flag missing references.
- **Various formatting and appendix-deferred proof complaints** — These are parser artifacts and normal practice.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Tone down the "provably" language.** Replace "provably adjusts" in the abstract and introduction with "theoretically motivated" or "empirically demonstrated to adjust," unless the closeness of \(\tilde{\mathbf{K}}\) to \(\mathbf{K}\) is proven in the main paper (not just claimed via Lemma 3 in the appendix) and the deferred convergence analysis is completed.

2. **Add error bars.** Report mean ± std for final PSNR/IoU/MSE values from multiple random seeds in the main paper, or at minimum state that single runs are shown and note the limitation.

3. **Add SepNN(MSK) to Fig 3** or explain why it is omitted; this would help disentangle general preconditioning gains from SepPGD-specific gains.

4. **Address the D=2 to D≥3 gap.** Either provide a proof sketch for why Lemma 2 extends to D>2, or explicitly frame the D≥3 experiments as empirical investigations beyond the established theory.

5. **Correct the Stone-Weierstrass condition** in the proof sketch (line 82) from "contains the identity function" to "contains the constant functions" if that is what the appendix proof uses.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>