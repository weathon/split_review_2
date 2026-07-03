Now I have a clear picture of the paper. Let me draft the review.Based on my calibration, let me now write the final review.

---

## Summary
This paper makes three theoretical contributions to separable neural networks (SepNNs): (1) a universal approximation theorem for multivariate CP, TT, and Tucker SepNNs via Stone-Weierstrass density + standard vector-valued MLP UAT; (2) a dual NTK regime analysis showing the NTK converges to a deterministic kernel under infinite width and rank, but remains random at finite rank; and (3) an efficient separable preconditioned gradient descent (SepPGD) with O(nD) complexity for n^D training samples on grid data, shown to be equivalent to classical Kronecker-structured NTK-PGD for D=2. Experiments on KRR, image/surface INRs, and PINNs validate the empirical effectiveness of SepPGD.

---

## Strengths

- **Genuine multivariate universal approximation theorem (Theorem 1).** Prior work (Cho et al., 2023) proved UAT only for bivariate CP SepNNs via orthogonal basis constructions. Theorem 1 covers CP, TT, and Tucker for arbitrary D≥2, using a cleaner argument: Stone-Weierstrass establishes that the separable function class 𝒜 is dense in C(𝒳), and then MLP UAT (extended to vector-valued functions) approximates each separable component. This is a concrete, verifiable improvement over prior art.

- **Dual NTK regime characterization with direct empirical support (Theorem 2, Corollary 1, Figure 1).** The identification that infinite width alone is insufficient for a deterministic NTK — rank must also grow — is practically informative. Figure 1(a) confirms that under fixed R=50, the NTK does not converge even as width increases; Figure 1(b) shows convergence when both grow jointly. This validates both regimes cleanly.

- **Kronecker-structured equivalence and O(nD) complexity gain (Lemma 2, Table 1, Remark 4).** Lemma 2 proves that the SepPGD gradient for D=2 is exactly equivalent to classical NTK-PGD with a Kronecker preconditioner S̃ = S₁⊗I + I⊗S₂. This algebraic identity reveals why the gradient can be factored and computed in O(n) rather than O(n²) space. The resulting O(nD) complexity for O(n^D) samples is a substantial practical gain compared to prior methods (O(n^D) or O(n^D/p)).

---

## Weaknesses

### Fatal
None.

### Major

- **"Provably adjusts its NTK spectrum" is an overclaim.** The abstract and introduction both assert that SepPGD "provably adjusts its NTK spectrum." However, Section 4 (after Lemma 2) explicitly hedges: "This can *possibly* be verified, because the eigenvalue of a Kronecker product matrix…", "It is believed that the result in Lemma 2 can be readily extended to multivariate cases D>2," and "convergence and solution consistency…is left for future research." What is actually proved is the D=2 equivalence with Kronecker preconditioner (Lemma 2) plus a plausibility sketch for spectral improvement. The gap between the abstract's claim and the body's deliverables is material and requires either correction of the abstract/introduction or provision of the missing proof.

- **The D>2 extension for SepPGD is unproven, yet the main experiments operate there.** Lemma 2 is stated and proved for D=2 only. Surface representation (D=3) and all PINN experiments (D=3) in Section 5 use Definition 1 (Eqs. 7–8), which is presented for general D by assertion — "It is believed that the result in Lemma 2 can be readily extended to multivariate cases D>2." No Lemma analogous to Lemma 2 is provided for D>2, and the spectral improvement argument (§4, paragraph following Lemma 2) is sketched only for D=2. The paper's most substantial empirical contributions thus operate in an unanalyzed regime.

### Minor

- **Theory-practice misalignment acknowledged but unresolved.** Corollary 1 and Remark 3 establish that under fixed rank R (the regime practitioners actually use), the NTK is random and Eq. (5)'s deterministic convergence characterization does not uniformly apply. SepPGD's spectral-adjustment motivation is derived entirely from the deterministic NTK and Eq. (5). Remark 3 acknowledges: "the training dynamic can not be characterized uniformly using a fixed NTK matrix as in (5) due to the randomness," but offers only future directions. The experimental evidence at small rank (Appendix Table 3) provides empirical support, but the theoretical framing overstates what the NTK analysis licenses for this practical setting.

- **Table 1 omits the O(P³) construction cost for Hessian-based methods.** Table 1 lists Hessian-based methods at O(P) for applying the preconditioner, which is technically correct for application only. Constructing H⁻¹ costs O(P³), making Hessian methods entirely impractical at scale. Remark 4 carefully notes SepPGD's own construction cost O(D(n³+n²P)), but no analogous remark applies to the Hessian row. This mildly misrepresents the landscape.

- **Figure 3 image comparison under equal iteration count does not clarify long-run behavior.** SepNN(SepPGD) achieves PSNR 33.30 vs. SepNN at 26.48 (~7 dB gap) under the same iteration number. Since SepPGD is a convergence accelerator, the gap may partly or wholly close given more iterations for vanilla SepNN. Figure 2(b) shows convergence vs. execution time but does not clearly show whether there is also an asymptotic quality improvement or only a rate improvement.

### Trivial
None.

---

## Nice-to-Haves
- Formally extend Lemma 2 to D>2. The paper itself notes in Appendix Section A.3 that the CP SepNN's NTK matrix over grid inputs can be expressed as a Kronecker product of smaller NTK matrices — this is precisely the structure needed. Even for the two-layer case, a D>2 Lemma would close the gap between abstract claims and delivered proofs, and cover all experimental settings.
- Add a baseline comparing SepNN+MSK (applying Shi et al.'s inductive gradient adjustment directly to SepNN) more systematically across image, surface, and PINN tasks to isolate whether SepPGD's benefit is primarily the preconditioner design or the computational efficiency.
- Study whether SepPGD's empirical effectiveness degrades at very small rank, as Corollary 1 implies may matter theoretically, to connect the random-NTK regime to practical performance.

---

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **"Straightforward extension to multi-layer MLPs for NTK" is non-trivial** (harsh critic §Section 3 notes): The paper cites Arora et al. (2019b) and says the extension is straightforward. Given standard recursive NTK formulations are well-established, this is a reasonable claim and not a soundness issue. Removed.
- **Appendix Lemma 3 not visible in main text**: Per hard rules, the parser strips appendix content. Removed.
- **Appendix Table 3 at small rank not visible**: Same reason. Removed.

---

## Novel Insights
The most intellectually interesting observation in this paper is the dual NTK regime for SepNNs: infinite width alone is insufficient for a deterministic NTK when rank is fixed, because the variance across rank components does not vanish. The algebraic identity in Lemma 2 — that SepPGD is exactly equivalent to NTK-PGD with a Kronecker-sum preconditioner S̃ = S₁⊗I + I⊗S₂ — is elegant and non-obvious: it reveals that the separable structure of SepNNs can be exploited not only for forward-pass efficiency (O(nD) evaluations) but also for optimization-level algorithmic design, without any approximation. Together, these results suggest a broader design principle: separable architectures admit both computational and optimization-level factorizations, making them amenable to theoretically grounded preconditioning in a way that standard MLPs are not.

---

## Suggestions
1. Correct the abstract and introduction to say SepPGD is "motivated by NTK spectrum analysis and shown to be equivalent to a Kronecker-structured preconditioner for D=2, with an analogous structure conjectured for D>2" rather than "provably adjusts its NTK spectrum."
2. Provide Lemma 2's D>2 analog (even for two-layer CP SepNN) to cover the experimental regime.
3. Add long-run convergence curves (or asymptotic MSE comparison) for the image representation experiment to clarify whether SepPGD changes the attained solution quality or only the convergence rate.
4. Note in Table 1 that Hessian-based methods require O(P³) construction, not just O(P) application.

---

## Score and Decision

**Anchor summary:**

| Path | Avg score | Round | Comparison |
|---|---|---|---|
| TNYLCF7vZA (INR spectral bias / NTK PGD) | 4.75 | R1 | Closest topical neighbor — direct predecessor (Shi et al., 2025); current paper extends it with more theory and 3 contributions |
| 2C3CWCPxNS (Preconditioning for PINNs) | 5.00 | R1 | Similar application domain but narrower scope, no UAT or NTK regime theory |
| pOUAVXnOQP (STAF for INR) | 5.25 | R1 | Architectural work on spectral bias, less theory |
| muN3B40keb (Phase transitions / NTK for INRs) | 5.80 | R1 | NTK + INR theory, observational rather than algorithmic |
| dpDw5U04SU (Minimum width UAT for ReLU) | 7.00 | R1/R2 | Pure approximation theory paper — cleaner proofs, no algorithmic gap |
| 5EtSvYUU0v (Connecting NTK and NNGP) | 6.00 | R2 | Unified NTK framework, theoretical, similar breadth but no algorithm |
| VEJzjAvaIy (NTK divergence in classification) | 5.75 | R2 | NTK theory paper, narrower scope, accepted |
| OeQE9zsztS (Spectrally transformed kernel regression) | 8.00 | R1 | Highly rigorous theoretical paper — cleaner, fully proved |
| S04xvGXjEs (Collective variables / NTK spectrum) | 6.00 | R2 | NTK empirical analysis, no algorithm, rejected |

**Round 1 bracket:** 5.5–7.0. The paper has three genuine contributions, each verifiable, and is substantially richer than the 4.75–5.00 anchors (direct topical neighbors). It falls below the 7.0+ anchors (clean pure-theory or fully-proved algorithmic papers) because of the D>2 gap and abstract overclaim.

**Round 2 narrowing:** The closest structural comparisons are 5.75–6.25 papers — NTK theory + algorithm papers with some missing pieces. The paper under review is at least as substantial as those, and its experimental validation is more comprehensive. The D>2 unproven extension is a real gap but not fatal (experiments still work, proof strategy is clear). I settle on **6.0**.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>