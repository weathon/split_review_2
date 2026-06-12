Now I have sufficient calibration data. Let me analyze my bracket and form the final review.

**Bracketing Analysis:**

Round 1 anchors retrieved:
- **Strong reject band (<1.5):** IC-Light (0.50, irrelevant topic), Financial Markets (1.00), KL GFlowNets (1.00), Time-dependent Discourse (1.00) — none are relevant comparisons.
- **Reject band (1.5-3.5):** Understanding GD through Training Jacobian (3.40), Understanding Optimization of Operator Networks (2.33), Faster GD in Deep Linear Networks (2.33), NTK with Derivative Labels (3.00) — our paper has stronger proofs and more complete contributions.
- **Weak reject band (3.5-5.5):** Inductive Gradient Adjustment for Spectral Bias in INR (4.75 — Shi et al. 2025, the very prior work our paper builds on), Preconditioning for PINNs (5.00), Efficient Over-parameterized Matrix Sensing (5.00), On Positive Definiteness of NTK (4.25) — our paper extends the Shi et al. work to SepNNs with stronger foundations.
- **Borderline band (5.5-7.5):** Greedy Learning to Optimize (6.25), Sharper Guarantees for NN Classifiers (7.00, Accept), Approaching DL through Spectral Dynamics (6.25), Debiasing Mini-Batch Quadratics (6.75, Accept)
- **Strong accept band (7.5-8.5):** Neural ODE Activation Functions (8.00, Accept), DRO with Bias/Variance Reduction (8.00), Spectrally Transformed Kernel Regression (8.00), When can transformers reason (7.60)
- **Very strong (>8.5):** None found.

**Initial bracket: 5.5 to 7.0.**

Compared to the Inductive Gradient Adjustment paper (4.75), our paper has much stronger theoretical foundations (complete approximation theorem, complete NTK analysis), a cleaner efficiency argument (O(nD) vs O(n^D)), and broader experimental validation. Our paper should be above 5.0.

Compared to the Greedy L2O paper (6.25), our paper has more theoretical depth (three contributions), better experiments, and a more practically impactful method.

Compared to Sharper Guarantees (7.0, Accept), our paper has a more practical contribution but an incomplete proof for its central claim. The proofs we do have are solid, but the "provably" claim is overstated.

**Final score: 6.5.** The paper makes genuine theoretical and practical contributions. The approximation theorem and NTK analysis are solid. The SepPGD method is well-designed with proven efficiency gains. The main weakness is overclaiming "provably alleviates spectral bias" when the proof is incomplete, and Lemma 2's D=2 limitation relative to D=3 experiments.

---

## Summary
This paper provides theoretical foundations for Separable Neural Networks (SepNNs) through three contributions: (1) a universal approximation theorem covering CP, TT, and Tucker architectures, (2) an NTK regime analysis establishing dual asymptotic regimes (deterministic kernel under infinite width+rank, stochastic kernel under infinite width with fixed rank), and (3) a Separable Preconditioned Gradient Descent (SepPGD) method that decomposes an n^D×n^D preconditioner into D smaller n×n factor preconditioners, achieving O(nD) complexity for n^D training samples.

## Strengths
- **Complete universal approximation theorem for all three major SepNN variants (Theorem 1, Section 2):** Proves approximation completeness simultaneously for CP, TT, and Tucker architectures, extending prior work (Cho et al., 2023) which only covered bivariate CP. The proof strategy—Stone-Weierstrass density combined with universal approximation for vector-valued MLPs—is elegant and general.

- **Novel dual NTK regime characterization (Theorem 2, Corollary 1, Section 3):** Establishes that SepNN's NTK converges to a deterministic kernel under infinite width AND infinite rank, but to a stochastic kernel under infinite width with fixed rank. This reveals that infinite rank is necessary for deterministic NTK behavior—a practically important insight since SepNNs often prefer small rank for generalization (line 128). Figure 1 validates both regimes empirically.

- **Genuine O(nD) complexity reduction via SepPGD (Table 1, Remark 4):** The method decomposes the n^D×n^D preconditioner into D separate n×n factor preconditioners, reducing preconditioner application from O(n^D) to O(nD) and construction from O(n^{3D}+n^{2D}P) to O(D(n³+n²P)). This is a polynomial reduction that scales to practical problem sizes.

- **Lemma 2 grounding SepPGD theoretically (Section 4, line 197):** For D=2, proves exact mathematical equivalence between SepPGD and classical NTK-based PGD via the Kronecker product identity (C^T⊗A)vec(B) = vec(ABC), establishing SepPGD is not a heuristic but a computationally cheaper reformulation.

- **Empirical improvements across diverse domains (Figures 2-4):** ~7 dB PSNR improvement for image representation (26.48→33.30), improved IoU for surface representation (0.983→0.992), and accelerated convergence for PINNs across diffusion, Klein-Gordon, and Helmholtz equations.

## Weaknesses

### Fatal
None.

### Major
- **The central "provably alleviates spectral bias" claim is overstated relative to the supporting argument.** The abstract states SepPGD "provably adjusting its NTK spectrum" and line 50 claims it "provably adjusts the eigenvalue distribution of NTK matrix." However, the actual argument in Section 4 (line 201) reads: "This **can possibly be verified**, because the eigenvalue of a Kronecker product matrix S₁⊗Iₙ is the product of eigenvalues of S₁ and Iₙ. Therefore, Ŝ **would have** better spectrum... **Suppose that** K̃ is close to the true NTK matrix K which can be verified using the NTK matrix formulation in **Lemma 3**)." The phrase "We can ultimately show that KS̃ has better spectrum than K" follows without a formal derivation. "Lemma 3" is referenced for the key link but is not formally stated in the main text. The word "provably" appears 3 times in the abstract and introduction but the supporting argument is a plausibility sketch with multiple unverified links. The paper should either complete the proof or restate the claim (e.g., "effectively adjusts" based on empirical evidence, or "provably equivalent to classical PGD which is known to alleviate spectral bias").

- **Lemma 2 proven only for D=2, while primary experiments use D=3.** The equivalence between SepPGD and classical PGD is stated for "f_Θ(x) = f_{Θ₁}(x₁)⊤f_{Θ₂}(x₂) : ℝ² → ℝ" (line 197). For D>2, the paper states "It is believed that the result in Lemma 2 (and the analysis following) can be readily extended to multivariate cases D > 2" (line 201). The main experiments—image representation (D=2 grid but with higher-dimensional extensions), 3D surface representation, and 3D PDEs—all use D≥3. This creates a gap between what is theoretically justified and what is experimentally demonstrated.

### Minor
- **Gap between the deterministic NTK regime and practical settings:** The spectral bias characterization via equation (5) assumes a fixed NTK matrix K, which requires both W→∞ and R→∞. In practice, R is finite and often small. Remark 3 (line 136) acknowledges: "Under the fixed rank condition, the training dynamic can not be characterized uniformly using a fixed NTK matrix as in (5) due to the randomness." While the paper does not hide this, it means the spectral bias motivation for SepPGD rests on an asymptotic regime different from practical usage.

- **Narrow experimental comparisons for INR tasks:** For image representation, comparisons include only vanilla MLP (26.64 dB), SepNN (26.48 dB), and MSK variants. No comparison with other spectral bias mitigation methods or INR architectures (e.g., Fourier feature networks, SIREN). While the contribution is specifically about SepPGD for SepNNs, at least one comparison would contextualize the PSNR gains.

- **No ablation of key hyperparameters:** The number of preconditioned eigenvalues k, the preconditioner update frequency ("every ten iterations," line 201), and the effect of rank R on SepPGD effectiveness are not explored. Given that k controls the spectral adjustment and R affects the NTK regime, ablations would connect experiments to theory.

### Trivial
None.

## Nice-to-Haves
- A convergence rate analysis for SepPGD (even for D=2) analogous to what Geifman et al. provide for standard PGD.
- Showing SepPGD performance as a function of rank R to connect experiments with the dual-regime theory.
- Error bars or variance across random seeds for main experimental results (Figures 2-4), consistent with the NTK verification experiments (Figure 1) which do show variance.

## Removed Points
These points are flagged to be removed, treat them with caution.
- The harsh critic raised a concern about the O(n^{D-1}) matrix product complexity in footnote 3. The paper addresses this directly (line 187): the primary computational costs are NTK computation and eigenvalue decomposition, and this product is "orders of magnitude less expensive in practice." Adequately addressed.
- Concern about the preconditioner update frequency being "every ten iterations" without justification — this is a practical implementation choice (line 201) and the paper empirically shows it works.
- Concern about the deterministic NTK being random under fixed rank — this is already acknowledged by the paper in Remark 3 and Figure 1(a), and the paper provides empirical evidence that SepPGD works even with small rank (Appendix Table 3 referenced in Remark 3).

## Novel Insights
The dual-regime NTK characterization (deterministic under infinite width+rank vs. stochastic under infinite width+fixed rank) is genuinely novel for SepNNs. The observation that infinite rank is necessary for deterministic NTK behavior—combined with the practical preference for small rank (line 128)—identifies a fundamental tension between theoretical tractability and practical design that the field should investigate further. The separable decomposition of the NTK preconditioner (decomposing an n^D×n^D matrix into D separate n×n factor matrices) is also a conceptually clean insight that could inspire similar decompositions for other structured architectures.

## Suggestions
- Complete the spectral bias alleviation proof for D=2 or reframe the claim to match what is demonstrated (equivalence to classical PGD + empirical effectiveness).
- Add at least one comparison with a dedicated INR method (Fourier features or SIREN) in the image representation experiments.
- Add ablation plots for the number of preconditioned eigenvalues k and the rank R.
- Report variance across random seeds for main experimental results, consistent with the NTK verification experiments.

## Calibration Report

**Round 1 anchors:**
| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| u1cQYxRI1H | 0.50 | 1 | Irrelevant (illumination harmonization) |
| nSDOkm0SKo | 1.00 | 1 | Irrelevant (financial networks) |
| Uj0h13lVrR | 1.00 | 1 | Weak GFlowNet theory, no depth |
| P49gSPmrvN | 1.00 | 1 | Weak visualization study |
| kkVTeMvC9D | 3.40 | 1 | GD training Jacobian analysis — less complete than our paper |
| xpmDc76RN2 | 2.33 | 1 | Operator network optimization — incomplete proofs, low quality |
| NbbsRnPBoS | 2.33 | 1 | GD in deep linear networks — narrower scope |
| fUz6Qefe5z | 3.00 | 1 | NTK with derivative labels — less substantial |
| TNYLCF7vZA | 4.75 | 1 | **Shi et al. 2025 — our paper extends this with SepNN theory; our paper is more complete** |
| 2C3CWCPxNS | 5.00 | 1 | Preconditioning for PINNs — weaker theory, one reviewer rated soundness 1/4 |
| b6juTJZ1I9 | 5.00 | 1 | APGD for matrix sensing — our paper has clearer motivation and better experiments |
| YN4uWzcbtt | 4.25 | 1 | Positive definiteness of NTK — narrower scope |
| FK8tl47xpP | 6.25 | 1 | Greedy L2O — convergence guarantees but weak experiments; our paper has more depth |
| h7GAgbLSmC | 7.00 | 1 | Sharper Guarantees — complete proofs, tighter bounds; our paper has more practical impact but less complete proofs |
| PJjHILiQHC | 6.25 | 1 | Spectral dynamics — empirical, less theoretical |
| Q0TEVKV2cp | 6.75 | 1 | Debiasing mini-batch quadratics — different domain |
| AoraWUmpLU | 8.00 | 1 | Neural ODE activations — rigorous, complete proofs throughout; our paper has incomplete spectral bias proof |
| TTrzgEZt9s | 8.00 | 1 | DRO — different domain, complete proofs |
| OeQE9zsztS | 8.00 | 1 | STKR — different domain, complete proofs |
| STUGfUz8ob | 7.60 | 1 | Transformer reasoning — different domain |

**Round 1 bracket:** Between 5.5 and 7.0. The paper is clearly more substantial than the ~5.0 rejected papers (stronger theory, better experiments, cleaner method) but has the "provably" overclaiming issue and incomplete proof that the 7.0+ accepted papers don't have.

**Final score reasoning:** The paper sits between the 6.25 Greedy L2O paper (which has convergence guarantees but weaker experiments) and the 7.0 Sharper Guarantees paper (which has complete proofs but less practical impact). Our paper has three distinct contributions of substance, a genuine practical efficiency improvement, but an incomplete proof for its central practical claim. Score: **6.5**.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>