## Summary
This paper establishes theoretical foundations for Separable Neural Networks (SepNNs) across three axes: (1) a universal approximation theorem proving SepNNs (CP, TT, Tucker) can approximate any continuous multivariate function on compact sets to arbitrary precision, (2) NTK regime analysis showing SepNN's NTK converges to a deterministic kernel under infinite width/rank and a random kernel under infinite width/fixed rank, and (3) an efficient Separable Preconditioned Gradient Descent (SepPGD) method that alleviates spectral bias with O(nD) complexity for n^D training samples, validated across KRR, INR, and PINN applications.

## Strengths
- **Coherent and complete theoretical arc**: The paper follows a natural progression from representation capacity → training dynamics (NTK) → optimization improvement (SepPGD), providing a comprehensive theoretical foundation for a practically important architecture. Each piece motivates the next.
- **Genuinely efficient algorithm**: The SepPGD achieves O(nD) complexity for n^D training samples, which is a substantial improvement over O(n^D) for standard NTK-based PGD (Geifman et al., 2024) and O(n^D/p) for mini-batch variants (Shi et al., 2025). This is backed by a clean theoretical argument via Kronecker product decomposition (Lemma 2).
- **New NTK characterization**: The distinction between deterministic NTK (infinite width + infinite rank) and random/stochastic NTK (infinite width + fixed rank) is a genuinely interesting finding. Corollary 1 reveals that infinite rank is necessary for deterministic NTK, which has practical implications for understanding when the standard NTK analysis framework applies to SepNNs.
- **Broad experimental validation**: Experiments span KRR, image/surface representation (INRs), and PDE solving (PINNs), demonstrating consistent improvements from SepPGD across domains (Figs. 2–4).
- **Well-written and clearly structured**: The paper is accessible, with clean notation, illustrative remarks, and logical flow between sections.

## Weaknesses
### Fatal
None.

### Major
- **Incomplete proof of spectrum adjustment**: The abstract and introduction claim SepPGD "provably" adjusts the NTK spectrum, but the actual justification in Section 4 is an argument sketch rather than a rigorous theorem. The paper states "it is believed that the result in Lemma 2 (and the analysis following) can be readily extended to multivariate cases D > 2" and that the rigorous convergence analysis "is left for future research." This gap weakens the strongest claimed contribution—the provable spectral bias alleviation. A formal theorem stating conditions under which $\mathbf{K}\tilde{\mathbf{S}}$ has improved spectrum relative to $\mathbf{K}$ would significantly strengthen the paper.
- **Limited experimental rigor**: The image representation experiments appear to show results for only a single image (bird), and the surface representation for a single object (dragon). A broader set of test cases would make the claims more convincing. Additionally, the paper lacks standard deviation/error bars across multiple runs for most experiments, which is important given that SepPGD involves eigenvalue computations that may be sensitive to initialization.

### Minor
- **NTK analysis limited to two-layer MLPs**: Theorem 2 explicitly considers two-layer factor MLPs, with Remark 1 noting multi-layer extensions are "straightforward" using existing NTK formulations. While this is a reasonable scope limitation, providing at least a sketch for the multi-layer case would strengthen the generality claims.
- **Random NTK dynamics unresolved**: Remark 3 acknowledges that under fixed rank, "the training dynamic can not be characterized uniformly using a fixed NTK matrix" and frames this as a "promising future direction." Since fixed rank is the practical regime (Liang et al., 2022; Luo et al., 2024), this leaves a significant gap between theory and practice.
- **The 1/√R scaling factor**: Introducing the 1/√R scaling in the SepNN definition (for NTK convergence) while claiming it doesn't affect Theorem 1 deserves more explicit discussion. How does this scaling interact with the rank R needed for approximation quality?

### Trivial
None beyond parser artifacts.

## Nice-to-Haves
- A formal theorem (or at least a proposition with explicit conditions) proving that the constructed preconditioner $\tilde{\mathbf{S}}$ improves the condition number of $\mathbf{K}\tilde{\mathbf{S}}$ relative to $\mathbf{K}$, closing the gap between Lemma 2's equivalence and the claimed spectral benefit.
- Extension of the NTK verification experiments (Fig. 1) to multi-layer SepNNs to demonstrate robustness beyond the two-layer case analyzed in Theorem 2.

## Novel Insights
The decomposition of SepNN's NTK into a weighted sum of factor NTKs (Lemma 1, Eq. 4) is a structurally revealing result—it shows that the SepNN's kernel inherits a "separable" structure analogous to the network itself, with the cross-factor interactions encoded in the vectors $\mathbf{a}_d(\mathbf{x})$. This insight directly enables the SepPGD construction: because the NTK has separable structure, the preconditioner can also be decomposed into per-factor components. The random NTK result (Corollary 1) further reveals that the fixed-rank regime introduces irreducible stochasticity in the kernel, which is an interesting theoretical distinction from standard over-parameterized networks where the NTK is deterministic.

## Suggestions
- Add a formal theorem or proposition (even under simplifying assumptions) proving that $\mathbf{K}\tilde{\mathbf{S}}$ has improved spectral properties (e.g., condition number bound) compared to $\mathbf{K}$, closing the theoretical gap in Section 4.
- Expand experiments with multiple test images/surfaces and include error bars across random seeds to strengthen empirical claims.
- Provide a brief multi-layer extension of Theorem 2, even at the level of stating the result without full proof, to demonstrate generality beyond two-layer factor MLPs.

## Score and Decision
The paper presents three coherent theoretical contributions of genuine value to the SepNN community. The universal approximation theorem is clean if not surprising, the NTK characterization reveals new structural insights (especially the deterministic vs. random distinction), and the SepPGD method offers a compelling efficiency improvement. However, the strongest claim—provably alleviating spectral bias—lacks rigorous proof, and the experiments, while broad, need more thoroughness (multiple test cases, error bars). This places the paper in borderline accept territory: the theoretical foundation work is important and well-executed enough to merit publication, but the gaps in the spectrum adjustment proof and experimental rigor prevent a stronger recommendation.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: Accept