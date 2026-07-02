## Summary
This paper presents a theoretical and algorithmic study of Separable Neural Networks (SepNNs), which represent multivariate functions as linear combinations of univariate factor networks. The work makes three main contributions: (1) proving universal approximation theorems for CP, TT, and Tucker SepNNs via Stone-Weierstrass combined with MLP approximation; (2) deriving NTK regimes for SepNNs, showing convergence to a deterministic kernel under infinite width+infinite rank and to a random kernel under infinite width+fixed rank; and (3) proposing Separable Preconditioned Gradient Descent (SepPGD), which exploits the separable structure to achieve O(nD) complexity for n^D grid samples, dramatically reducing the cost of NTK-based preconditioning. Empirical evaluations on kernel ridge regression, image/surface INR representation, and PINNs demonstrate convergence acceleration.

**Main strengths:** The paper fills a clear theoretical gap for an emerging architecture, provides the first multivariate universal approximation theorem for SepNNs, and develops a computationally efficient preconditioner that exploits the separable structure. The NTK analysis revealing deterministic vs random regimes based on rank scaling is novel and well-motivated by practical rank choices. The complexity reduction from O(n^D) to O(nD) is substantial for grid-based applications.

**Core weaknesses:** (1) The "provable" spectrum adjustment claim for SepPGD contains logical gaps—the key assumption that the Kronecker-sum NTK approximation K̃ ≈ K is unverified, and full D>2 extension is deferred. (2) The experimental evaluation lacks an Adam/SGD baseline for SepNNs, conflating optimizer type with preconditioner effect, and does not demonstrate the O(nD) scaling advantage for D>3. (3) Notation inconsistencies and missing details in the Stone-Weierstrass proof sketch reduce reproducibility. Novelty comparison against prior work is deferred due to external retrieval unavailability in this run.

**Score:** 6/10 — solid theoretical contributions with nontrivial algorithmic innovation, but claims of "provable" spectral bias alleviation are stronger than the evidence supports, and empirical rigor needs improvement.

## Strengths
**S1. Timely theoretical foundation for an emerging architecture.** SepNNs have demonstrated practical value in INRs, PINNs, and scientific computing, yet their theoretical understanding was limited. This paper provides the first universal approximation theorem covering all three major tensor decomposition forms (CP, TT, Tucker) for multivariate D>2, going significantly beyond prior bivariate-only analyses (Cho et al., 2023). The proof technique combining Stone-Weierstrass with MLP approximation is elegant and broadly applicable.

**S2. Novel NTK regime analysis with practical implications.** The paper derives two distinct NTK convergence regimes based on rank scaling—deterministic under infinite rank vs. random under fixed rank—which correctly captures the practical situation where R is chosen small for generalization. This is a nontrivial extension of standard NTK theory to separable architectures and provides useful guidance for practitioners choosing rank vs. width.

**S3. Computationally efficient preconditioning.** The SepPGD method achieves O(nD) complexity for preconditioner application on an n^D grid, versus O(n^D) for the standard NTK-based PGD (Geifman et al., 2024). The key insight—using the equivalence between Kronecker-product operations and vectorized matrix products to decompose a large preconditioner into small factor-wise preconditioners—is technically sound and yields substantial practical savings.

**S4. Broad empirical validation.** The paper evaluates SepPGD across four distinct tasks (kernel ridge regression, image INR, surface INR, and PINNs), demonstrating consistent convergence acceleration in wall-clock time. The visual results (Fig. 3) show notably improved detail capture with SepPGD, e.g., PSNR increasing from 26.48 (SepNN) to 33.30 (SepPGD) on image representation.

**S5. Open-source code and reproducibility consideration.** The code is provided via GitHub, which supports reproducibility efforts.

## Weaknesses
### W1. Overclaimed "provable" spectral bias alleviation (Major)

The paper's most prominent claim—that SepPGD "provably adjusts the eigenvalue distribution of NTK matrix, effectively alleviating spectral bias" (Abstract, Contribution bullet 3)—is stronger than the evidence provided in Section 4. The theoretical justification contains several gaps:

- The key assumption that the Kronecker-sum approximation $\tilde{\mathbf{K}} \approx \mathbf{K}$ (where $\tilde{\mathbf{K}}$ is the sum of factor-wise Kronecker products and $\mathbf{K}$ is the true SepNN NTK) is stated as "Suppose that $\tilde{\mathbf{K}}$ is close to the true NTK matrix" without any quantification or error bound. Lemma 3 is referenced but its content is not verifiable from the main text.
- The analysis only covers $D=2$ (Lemma 2); extension to $D>2$ is stated as "believed to be readily extended" but not proven.
- The "provably" claim is undermined by hedging language: "could provably and efficiently adjust the spectrum" (line 107).

**Recommendation:** Replace "provably" with "empirically demonstrated to" in the abstract and introduction. Clearly separate established results ($D=2$ equivalence, complexity analysis) from conjectures ($\tilde{\mathbf{K}} \approx \mathbf{K}$ approximation, $D>2$ extension, convergence guarantees) in Section 4.

### W2. Missing Adam/SGD baseline in experiments (Major)

The empirical comparisons (Section 5, Figs. 2-4) compare SepPGD against MLP, MLP(MSK), SepNN, and SepNN(MSK). However, SepPGD is a preconditioned gradient method — it modifies the gradient update direction—while the SepNN baseline uses standard gradient descent. This conflates two differences: the preconditioner itself and the effective optimizer trajectory. A baseline of SepNN trained with Adam (or another adaptive optimizer) under comparable wall-clock time is essential to isolate the preconditioner's specific contribution.

**Recommendation:** Add a "SepNN + Adam" baseline to all experiments. Report both iteration-count and wall-clock convergence for all methods. Also report the computational overhead of constructing the preconditioner matrices $\{\mathbf{S}_d\}$ (NTK computation + eigendecomposition time) separately from the training time.

### W3. Scalability not demonstrated (Major)

The paper's central complexity claim is $O(nD)$ vs $O(n^D)$ for standard methods. However:

- All experiments use small $D$ (2 for images, 3 for PINNs). A scaling experiment showing wall-clock time as $D$ increases from 2 to 5 (or higher) for fixed $n$ is needed to validate the asymptotic advantage.
- The $O(n^{D-1})$ term in the preconditioner construction (footnote 3) is dismissed as "orders of magnitude less expensive" without empirical verification. For $D \ge 4$, this term can dominate.
- The SeqPGD advantage over mini-batch PGD (Shi et al., 2025) with $p$ large is not empirically compared.

**Recommendation:** Add a scaling plot with $D=2,3,4,5$ showing wall-clock time per epoch for SepPGD vs. standard SepNN vs. full NTK-PGD.

### W4. Stone-Weierstrass proof sketch incomplete (Minor)

The universal approximation proof sketch (Section 2) invokes Stone-Weierstrass but does not explicitly verify all three conditions for the separable function class $\mathcal{A}$:
1. **Contains constant functions:** stated
2. **Separates points:** not explicitly constructed — the paper says "we carefully examine that $\mathcal{A}$ meets these requirements" without showing how coordinate projections are represented in CP form for $D>2$
3. **Closed under algebraic operations:** multiplication closure leads to rank increase ($R_1 R_2$), which requires rank unboundedness; this should be explicitly noted

Additionally, a typo in the definition of $\mathcal{A}$ uses $x_N$ instead of $x_D$ (line 43).

**Recommendation:** Provide explicit constructions for point-separation and closure conditions in the main text or appendix. Correct the $x_N$ typo.

### W5. NTK computation scaling not acknowledged (Minor)

Lemma 1 requires computing $\mathbf{K}_{\Theta_d}(x_d, x'_d) \in \mathbb{R}^{R \times R}$ — the full NTK matrix between all pairs of output components of each factor MLP. This costs $O(R^2 P_d)$ per input pair, which becomes expensive for large $R$ (e.g., $R=300$ in Fig. 1). The paper does not discuss this computational burden or potential approximations (diagonal NTK, Nyström, etc.).

**Recommendation:** Add a remark in Section 3 about the $O(R^2)$ per-factor NTK cost and discuss approximation strategies for large $R$.

### W6. Experimental details deferred to unavailable appendix (Minor)

The paper repeatedly references "Appendix Section A.12" for experimental settings, "Appendix Section A.5" for proofs, and "Appendix Fig. 10" for additional results. Since the appendix is not included in the submission, these claims cannot be verified. Critical details such as exact network architectures, hyperparameters, rank choices, and dataset splits are missing from the main text.

**Recommendation:** Move at least the key experimental settings (network width, depth, rank $R$, learning rate, number of preconditioner eigenvalues $k$) to the main text or a self-contained supplement.

### W7. Conclusion lacks limitations (Minor)

The concluding section discusses potential impact but does not acknowledge key limitations:
1. The $O(nD)$ advantage is specific to grid-structured inputs
2. The provable spectral guarantee is incomplete for $D>2$
3. Approximation rates (how fast error decreases with $R$ and network width) are not provided

**Recommendation:** Add a "Limitations" paragraph as suggested in the annotation.

## Score
**Final Score: 6/10**

**Rationale:** The paper makes solid theoretical contributions (universal approximation theorem for multivariate SepNNs, NTK regime analysis) and presents a computationally efficient preconditioning method that exploits separable structure. These are genuine contributions to an emerging architecture class. However, the score is constrained by: (1) overclaimed "provable" spectral bias alleviation that is not fully supported by the theoretical analysis; (2) incomplete experimental baselines that make it difficult to isolate the preconditioner's effect; (3) lack of scaling validation for the claimed $O(nD)$ complexity at higher dimensions; and (4) deferred novelty verification due to external retrieval unavailability in this run. The paper would benefit from toning down claims, adding Adam baselines, and including a scaling experiment for $D=2$ to $5$.

**Note on Novelty:** External literature verification was unavailable in this run (Retrieval-Disabled Mode). The universal approximation theorem for $D>2$ SepNNs appears to extend prior bivariate results in a natural way; the NTK regime analysis distinguishing deterministic vs. random kernels based on rank scaling is conceptually novel. A thorough novelty assessment requires manual literature comparison.

```text
ASCII Diagram — Paper Structure & Evidence Map

[Problem: SepNN theoretical foundations lacking]
    → [C1: Universal approximation theorem (Section 2)]
        → Evidence: Stone-Weierstrass + MLP approximation (proof in appendix)
        → Gap: No explicit approximation rates, point-separation not fully constructed
    → [C2: NTK regime analysis (Section 3)]
        → Evidence: Lemma 1 (NTK expression), Theorem 2 (deterministic limit), 
                     Corollary 1 (random limit), Fig. 1 validation
        → Gap: NTK regime only applies asymptotically; practical finite-width regime
    → [C3: SepPGD algorithm (Section 4)]
        → Evidence: Lemma 2 (D=2 equivalence), Table 1 (complexity)
        → Gap: "Provable" spectral adjustment unverified; D>2 extension not proven
    → [Experiments (Section 5)]
        → Evidence: KRR, Image INR, Surface INR, PINNs — consistent acceleration
        → Gap: Missing Adam baseline, no scaling experiment for D>3
```

```text
ASCII Diagram — Revision Strategy Roadmap

[Overclaiming "provably"] 
    → Replace with "empirically demonstrated" 
    → Expected: claims match evidence, stronger reviewer trust

[Missing Adam baseline]
    → Add SepNN+Adam to all experiments 
    → Expected: isolate preconditioner effect, fair comparison

[No scaling experiment]
    → Add D=2,3,4,5 wall-clock scaling plot 
    → Expected: validate O(nD) vs O(n^D) empirically

[Stone-Weierstrass gap]
    → Add explicit point-separation construction 
    → Expected: proof becomes self-contained

[Missing limitations]
    → Add concrete limitation paragraph 
    → Expected: improved scientific honesty, reduced reviewer criticism
```