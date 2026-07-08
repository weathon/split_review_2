## Summary

This paper studies separable neural networks (SepNNs) and makes three contributions: (1) universal approximation theorems for CP, TT, and Tucker SepNNs via Stone-Weierstrass, (2) analysis of SepNN neural tangent kernel (NTK) identifying two asymptotic regimes — deterministic kernel (infinite width + infinite rank) vs random kernel (fixed rank), and (3) a separable preconditioned gradient descent (SepPGD) method with O(nD) complexity for n^D training samples, along with empirical validation on KRR, image/surface INRs, and PINNs.

## Strengths

- **The NTK two-regime analysis (Theorem 2 and Corollary 1) is a genuinely insightful and nontrivial extension of standard NTK theory to separable architectures.** The paper correctly identifies that the SepNN's limiting kernel depends on whether the decomposition rank R scales to infinity (deterministic kernel) or stays fixed (random kernel). This has practical consequences: practitioners using small rank cannot rely on a fixed NTK. The empirical validation in Figure 1 supports this cleanly, showing that with fixed rank the NTK variance does not vanish as width grows, while both width and rank must increase for convergence to a deterministic kernel.

- **The complexity reduction of SepPGD is significant and well-motivated.** Moving from O(n^D) (full NTK preconditioning) or O(n^D/p) (mini-batch) to O(nD) for preconditioner application is dramatic for any D≥2. Table 1 and Remark 4 provide a clear, honest complexity breakdown, including the O(n^{D-1}) term acknowledged in Footnote 3.

- **The equivalence result (Lemma 2) for D=2 provides a formal bridge between SepPGD and full NTK-based PGD.** Showing that SepPGD with the Kronecker-sum preconditioner S̃ = S₁⊗I + I⊗S₂ is equivalent to the full NTK-based PGD demonstrates that SepPGD is a computationally efficient factorization of a principled preconditioner, not an ad-hoc heuristic.

## Weaknesses

### Fatal

None.

### Major

- **The abstract and introduction claim SepPGD "provably adjusts the eigenvalue distribution of NTK matrix," but the theoretical support in the main text is substantially weaker than this suggests.** The proof chain is: Lemma 2 (equivalence to full PGD, proven only for D=2) → spectral argument for S̃ vs K̃ (sound) → K̃≈K (stated as "Suppose that...") → KS̃ has better spectrum than K. The D>2 extension is explicitly speculative: "It is believed that the result...can be readily extended" (line 201). Convergence guarantees are left for future research. While the D=2 case is valid, the advertised strength "provably" across all settings overstates what is actually demonstrated. This is a significant claim-reality mismatch that should be corrected by either (a) toning down the abstract/intro language to match the conditional support, or (b) proving the full D>2 generalization and the K̃≈K approximation in the main text.

### Minor

- **The 3D PINN experiment (Figure 4) compares SepPINN(SepPGD) only against SepPINN and standard PINN without including a full MSK (NTK preconditioner) baseline.** Since the complexity advantage of SepPGD is most dramatic for D≥3, either including a small-scale MSK comparison (where O(n³) may still be feasible) or explicitly stating its computational infeasibility would strengthen the empirical case.

- **No ablation studies are provided for key hyperparameters** that the paper's own analysis identifies as important: the rank R (which the NTK analysis shows determines whether the kernel is deterministic or random), the preconditioner update frequency (stated as every ten iterations without sensitivity analysis), and the eigenvalue modulation function g(λ).

- **Quantitative results in Figures 3 and 4 are reported as single point estimates** (PSNR 33.30, IoU 0.992, MSE 0.037) without error bars or confidence intervals, even though the training process is stochastic (Figure 1 uses ten runs for NTK validation).

- **Definition 1 (Equations 7–8) uses dense tensor notation** (unfold, mode-specific products, outer-product concatenations) without pseudocode or a worked low-dimensional example, making verification and direct reproducibility harder than necessary for the paper's main algorithmic contribution. The connection to the cleaner D=2 interpretation in Lemma 2 would benefit from a worked D=3 example.

### Trivial

- Figure 1 caption does not specify the metric (e.g., Frobenius norm, spectral norm) plotted for "difference between NTK matrices."

## Nice-to-Haves

- Show MSE vs iteration alongside MSE vs execution time to separate the preconditioner's effect on convergence rate from its per-iteration computational acceleration.
- Test SepPGD against the full MSK preconditioner in a small-scale D=3 setting (e.g., n=8, giving 512 samples where the full 512×512 NTK is manageable) to validate that SepPGD approximates the full preconditioner's behavior in higher dimensions.
- Study the effect of rank R on SepPGD effectiveness, as the NTK analysis identifies rank as the key parameter determining the kernel regime.
- Provide the explicit D>2 generalization of Lemma 2 or a clear statement of why SepPGD for D>2 is equivalent to a specific form of full NTK preconditioning.

## Removed Points

These points from the harsh critic input were excluded. Treat them with caution:

- "Lemma 3 is not stated in the main text" and "The reliance on the appendix (which is removed) for the actual proof details" — removed per instructions: the parser strips appendix content; references to appendix material are not author errors. The relevant issue (conditional proof with "Suppose that" language) is already captured in the Major weakness.
- "The comparison would be more informative if it also showed MSE vs iteration" — moved to Nice-to-Haves. The paper explicitly justifies plotting MSE vs time because the efficiency advantage is per-iteration, which is a valid choice.
- Criticism about fixed noise level (std 0.01) without robustness analysis — removed as scope creep; the paper's KRR experiments include both noiseless and noisy settings for comparison with prior work (Geifman et al., 2024), and studying noise robustness is not a claimed contribution.
- "Unclear whether SepNN baseline uses optimally tuned hyperparameters" — removed as speculative without concrete evidence of undertuning.
- "Whether the improvement comes from the preconditioner or from other factors (e.g., different effective learning rates)" — removed as speculation; the comparison is between SepPINN and SepPINN(SepPGD) under otherwise identical settings.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Tone down the "provably" language** in the abstract and introduction to match the conditional theoretical support. The paper currently says SepPGD "provably adjusts" the NTK spectrum in the abstract, while the main text concludes it "could provably" do so, with conditions and limitations. Fixing this mismatch is the single most impactful revision.
2. **Add ablation studies** on rank R and preconditioner update frequency to understand when SepPGD helps most.
3. **Report error bars** or confidence intervals on all quantitative comparisons in Figures 3 and 4.
4. **Add pseudocode** for Definition 1 and a worked D=3 example to improve reproducibility.
5. **Either prove the D>2 generalization of Lemma 2** in the main text, or clearly scope the theoretical contribution to D=2 while noting the D>2 extension as heuristic supported by experiments.

## Score and Decision

**Round 1 bracket**: 5.5–7.5. Anchors consulted (all rounds):
- /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/h7GAgbLSmC.md (7.00, accepted) — stronger theoretical rigor (fully proven bounds) but only one contribution; itemized.
- /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/tNn6Hskmti.md (6.25, accepted) — theory paper accepted despite limitations in assumptions; itemized.
- /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/FK8tl47xpP.md (6.25, rejected) — preconditioned gradient method rejected partly due to insufficient justification of a central assumption (BGD); itemized.
- /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/5EtSvYUU0v.md (6.00, rejected) — NTK theory paper rejected for lack of rigor; itemized.
- /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/GqI4fTVUXC.md (6.00, rejected) — empirical NTK study rejected for unclear conclusions.
- /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/bWz8aOPwsJ.md (3.75, rejected) — NTK trace paper, weaker.
- /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/fUz6Qefe5z.md (3.00, rejected) — NTK derivative labels paper, weaker.
- /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/YwJkv2YqBq.md (6.75, accepted) — Nesterov acceleration theory paper.
- /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/8vKknbgXxf.md (7.20, accepted) — AD theory paper.

**Bracketing logic**: The paper has three contributions (approximation theory, NTK regimes, SepPGD) with strong weights on all three strengths (9.20–11.19). It is stronger than FK8tl47xpP (6.25, rejected) because its main weakness (overclaimed "provably") is addressable without invalidating the core results, and it has more contributions. It is weaker than h7GAgbLSmC (7.00, accepted) because the SepPGD theoretical support is partial/conditional rather than fully proven. **Final placement**: 6.0 — the paper has genuine value (novel NTK regime analysis, practical algorithm with dramatic complexity reduction), but the claim-reality mismatch on SepPGD's theoretical guarantees and the incomplete experimental evaluation (no ablations, no error bars, missing PINN baseline) prevent a higher score.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>