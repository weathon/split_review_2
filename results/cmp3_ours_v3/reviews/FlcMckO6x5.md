## Summary

This paper provides theoretical analysis for Separable Neural Networks (SepNNs): (1) a universal approximation theorem via Stone-Weierstrass for CP, TT, and Tucker variants — extending prior bivariate results; (2) an NTK characterization showing deterministic vs. random kernel regimes under infinite vs. fixed rank; and (3) a separable preconditioned gradient descent (SepPGD) method for mitigating spectral bias. Experiments on KRR, image/surface INRs, and PINNs demonstrate improved convergence.

## Strengths

- **Clean and general universal approximation proof (Theorem 1, Section 2).** The proof strategy — showing the CP-rank-class is an algebra via Stone-Weierstrass, then approximating univariate factors with MLPs — is rigorous and general. It correctly extends beyond the bivariate CP case (Cho et al., 2023) to arbitrary D and to TT and Tucker architectures, where the algebraic closure conditions differ across tensor formats. This is the paper's strongest theoretical contribution.

- **Two-regime NTK characterization (Theorem 2 and Corollary 1).** The insight that SepNN's NTK converges to a deterministic kernel only under *both* infinite width and infinite rank, while fixed rank yields a stochastic kernel, correctly identifies where standard NTK machinery applies and where it does not. This distinction has practical consequences since SepNNs are often used with modest rank. Figure 1 provides empirical validation.

- **Computational insight in SepPGD (Lemma 2, Table 1).** The equivalence between SepPGD (with factor-size preconditioners) and classical NTK-based PGD (with one large Kronecker-structured preconditioner) is a genuine insight. Replacing an n^D × n^D preconditioner with D factor preconditioners each n × n, using the Kronecker-product identity to avoid explicit large-matrix operations, is elegant. The potential savings are substantial in principle.

## Weaknesses

### Fatal
None.

### Major

- **The O(nD) complexity claim in the abstract and Table 1 is materially overstated.** The abstract states "enjoys an efficient O(nD) complexity" and the bullet point repeats "O(nD)" without qualification. However, constructing M_d in Definition 1 (equation 8) involves outer products of size n^{D-1}, costing O(R n^{D-1}) for D > 2. The paper acknowledges this only in Footnote 3 ("a matrix product with complexity O(n^{D-1})"), which is easily missed. The Table 1 caption says "in terms of applying the preconditioner," but the abstract gives no such caveat, so readers will take "O(nD)" as the total cost. The full per-iteration cost includes the construction, which for D > 2 is superlinear in n. This does not invalidate the method's advantage — SepPGD is still cheaper than O(n^D) — but the headline claim as written is misleading and would be propagated by citing works.

- **The "provably adjusts the eigenvalue distribution" claim (abstract, bullet 3, line 50) is not supported by the reasoning in Section 4.** The argument at line 201 is a sketch with heavily hedged language: "This can possibly be verified… Therefore, K̃ would have better spectrum… Suppose that K̃ is close to the true NTK matrix K which can be verified using the NTK matrix formulation in Lemma 3. We can ultimately show…" Every step is hedged or deferred. Lemma 3 is not stated in the main text, so the claim that K̃ ≈ K is unverifiable from the paper. Even if K̃ ≈ K, the chain from improved spectrum of K̃ to improved spectrum of the product K\tilde{S} is not established because K (the true NTK) differs from K̃. The reasoning is also limited to D = 2. The paper should either provide a rigorous proof chain or replace "provably" with language that honestly reflects the conjectural nature of the argument.

### Minor

- **The spectral bias alleviation claim is only indirectly tested.** The experiments show faster MSE-vs-time convergence, which is consistent with spectral bias alleviation but also with other mechanisms (e.g., higher effective learning rate, better conditioning unrelated to NTK eigenvalues, or lower per-iteration overhead). Eigenvalue spectrum comparisons of the preconditioned vs. un-preconditioned NTK would directly validate the claim and substantially strengthen the paper.

- **Lemma 3 is not presented in the main text**, yet it is central to the justification that K̃ ≈ K (line 201). Readers cannot evaluate whether the approximation holds without seeing the lemma's statement and assumptions. This is easily fixed by moving it to the main body.

- **The D > 2 case for SepPGD is addressed only with a hedge.** Lemma 2 and the spectral reasoning are explicitly for D = 2. The paper says "It is believed that the result… can be readily extended" (line 201), but the Kronecker-product structure used in Lemma 2 does not generalize straightforwardly, and the preconditioner construction in (8) changes for D > 2. The paper should either provide the general proof or state this as a clear limitation rather than asserting extendability without evidence.

- **The "pseudo NTK matrix" K_{Θ_d} (line 156) is not defined.** The paper says it is calculated "using sum-of-logits (Mohamadi et al., 2023)" without explaining what "pseudo NTK" means or how it differs from the true factor NTK defined in Lemma 1. This creates ambiguity for readers trying to understand the preconditioner construction.

- **Small-scale experimental validation.** The experiments are conducted on one image (bird), one surface, three PDEs, and synthetic KRR data. No standard large-scale benchmark (e.g., ImageNet-scale INR, standard PDE benchmark suite) is used. While the paper's contributions are primarily theoretical, the empirical support for the practical impact of SepPGD would be strengthened by broader evaluation.

### Trivial

- **Stone-Weierstrass condition wording (line 82).** The paper states the function class must "contain the identity function." The theorem actually requires constant functions (or the function 1). The intended reasoning still works (the constant 1 function is representable in the class), but the exposition is imprecisely worded.

## Nice-to-Haves

- Provide Lemma 3 explicitly in the main paper with a concrete bound on ‖K − K̃‖ in terms of factor NTKs. This would turn the "suppose K̃ is close to K" step into a verifiable claim.
- Include eigenvalue spectrum plots of the preconditioned effective NTK versus the vanilla SepNN NTK, to directly demonstrate condition number reduction.
- Clarify the complexity accounting by splitting it into (a) preconditioner construction cost [O(R n^{D-1})], (b) per-iteration gradient cost [O(nD)], and (c) preconditioner update frequency (e.g., every 10 iterations as noted).
- State explicitly that the NTK and SepPGD analyses are for the CP SepNN only, and that extension to TT/Tucker is a direction for future work rather than asserting ready extendability.

## Removed Points

- **"Missing related works"** — Not verifiable; the paper cites relevant prior work including Cho et al. (2023), Liang et al. (2022), Yu et al. (2024), and Geifman et al. (2024).
- **Reproducibility nitpicks about undisclosed hyperparameters** — The appendix is stripped by the parser; these details exist in the original submission.
- **Formatting/style complaints** — Parser artifacts, not author errors.
- **Speculation about claims from a stripped appendix** — Removed per hard rules.
- **"The Stone-Weierstrass condition is wrong"** — The reviewer correctly notes that "identity function" is imprecise (should be "constant functions"), but the reasoning still works. Moved to Trivial.

## Novel Insights

None beyond the paper's own contributions. The reviews primarily refine the assessment of claims rather than surface novel observations about the paper.

## Suggestions

1. **Qualify the O(nD) claim** in the abstract to include the construction-cost caveat, e.g., "O(nD) per iteration after a one-time preconditioner construction costing O(R n^{D-1})."
2. **Replace "provably adjusts"** with language matching the reasoning in Section 4, e.g., "empirically shown to adjust" or "whose design is motivated by adjusting."
3. **Move Lemma 3 into the main text** and, if possible, provide a bound on ‖K − K̃‖.
4. **Add eigenvalue spectrum plots** of the preconditioned vs. un-preconditioned NTK to directly demonstrate spectral bias alleviation.
5. **Clearly state the D > 2 limitation** as future work rather than claiming ready extension.
6. **Define "pseudo NTK"** and explain how it differs from the standard factor NTK.

**Calibration anchors** (all retrieved across rounds):
- ydlDRUuGm9.md, avg 6.25 (Accept): KAN expressiveness+spectral bias. Same architecture-theory+spectral-bias genre; comparable theory scope and experimental scale. The paper under review is slightly stronger theoretically but has more significant claim-inflation problems.
- dpDw5U04SU.md, avg 7.00 (Accept): Minimum width for UAP. Cleaner theory-only paper. The paper under review is weaker by comparison due to oversold method claims.
- VEJzjAvaIy.md, avg 5.75 (Accept): NTK divergence. Similar theoretical rigor, narrower scope.
- YN4uWzcbtt.md, avg 4.25 (Reject): NTK positive definiteness. Purely theoretical; rejected partly for limited impact. The paper under review has broader scope (theory + method + experiments).
- kkVTeMvC9D.md, avg 3.40 (Reject): Training Jacobian analysis. The paper under review is clearly stronger.
- 8wAL9ywQNB.md, avg 6.00 (Accept): Generalization bounds. Comparable score band; the paper under review has stronger theory but weaker optimization claims.
- FK8tl47xpP.md, avg 6.25 (Reject): Greedy L2O with preconditioned GD. Related optimization paper rejected despite solid theory. The paper under review has broader theoretical contributions beyond the optimization method.

**Round 1 bracket**: 5.5–6.5. Narrowed to 6.0 based on comparison to ydlDRUuGm9 (6.25) — the paper under review is slightly stronger on theory but has more significant overclaim issues, placing it just below the KAN paper.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>