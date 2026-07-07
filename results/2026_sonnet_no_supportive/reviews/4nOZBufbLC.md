## Final Review

## Summary
Count Bridges (CB) introduces a stochastic bridge process on integer lattices via Poisson birth-death dynamics, providing an exact, tractable analogue of diffusion-style models for count data with closed-form conditionals (Binomial/Hypergeometric draws, Bessel slack posterior). The framework is extended to deconvolution via an EM algorithm treating unit-level counts as latent. Applications are demonstrated on nucleotide-resolution single-cell RNA-seq modeling and spatial transcriptomic deconvolution.

---

## Strengths

- **Principled integer-valued bridge (Prop. 3.1):** The construction is mathematically clean — Poisson birth-death processes are identified as the correct integer analogue of the Gaussian bridge. Closed-form Binomial/Hypergeometric bridge conditionals (Eq. 9) and the Bessel slack posterior satisfy both bridge consistency (Eq. 1) and projective posterior (Eq. 2), the precise properties required for theoretically sound multi-step sampling and training. The CUDA kernel for the Bessel sampler makes this computationally viable at scale.

- **Schrödinger bridge connection (Sec. 3.1):** The derivation that CB solves entropy-regularized discrete OT with L1 cost as κ→0 — exactly mirroring the Gaussian case where σ→0 recovers quadratic OT — is substantive. The bridge parameter κ is identified as an entropy-regularization strength, placing the framework in a coherent theoretical lineage rather than just by analogy.

- **Scalability (Fig. 3):** On the low-rank Gaussian mixture transport task, CB stays near zero W1 error across dimensions 4–512, while both CFM and DFM errors grow with dimension. This is a non-trivial empirical finding that supports the claim that integer-native geometry is being genuinely exploited.

- **EM deconvolution framework (Sec. 4, Prop. 4.1):** The aggregate scoring rule lifted from the unit-level energy score gives a sound M-step; Prop. 4.1 motivates the projection operator as a first-order KL projection to the constraint set rather than ad hoc rescaling. The paper also identifies deconvolution identifiability conditions (discussed in appendix), showing the authors understand the framework's failure modes.

---

## Weaknesses

### Fatal
None.

### Major

- **Information asymmetry in biological comparisons (Tables 1 and 4):** In Table 1, CB is trained directly on single-cell PBMC data (10⁶ cells across 10³ donors) while fine-tuned Enformer was designed for and fine-tuned on bulk data. This comparison conflates task specification with model quality: Enformer was never designed for single-cell prediction, so the MSE gap measures task-fit as much as the bridge formulation's contribution. An ablation replacing the bridge loss with a standard MSE/NLL loss on the same architecture and training data would isolate the contribution of the bridge objective; this ablation is absent.

  In Table 4, CB is trained on MERFISH data (even though only on artificial aggregates), while STDeconvolve is entirely unsupervised with zero training data. This tests the paradigm (trained model vs. unsupervised factorization) rather than the deconvolution algorithm. The paper acknowledges reference-based comparisons in Appendix F, which is the right place to look, but Table 4 presents this asymmetric comparison as the headline result.

- **No ablation isolating bridge objective from architecture (Sec. 6.2):** The CB model for the biological applications uses Enformer embeddings, cell-type embeddings, and residual multi-head attention blocks. Section 6.2 does not separate how much of the gain in Table 1 stems from the richer architecture versus the bridge objective and distributional energy-score loss. A single ablation row (same architecture, standard loss) would resolve this ambiguity.

### Minor

- **EM E-step approximation gap (Alg. 3):** The E-step does not sample from Q_θ(·|a₀, x_t, t, z) exactly — it uses projection-guided diffusion as a surrogate. The paper acknowledges this in its own limitations section ("the projection step is a first-order surrogate and lacks serious theoretical support"), but provides no empirical convergence analysis. Showing loss trajectory and E-step sample quality across EM iterations would substantially strengthen credibility of the EM framing.

- **Integrality issue in Prop. 4.1:** The simple scaling projection Π(x₀)_g = a₀ x_{g0}/(Σ_{g'} x_{g'0}) generically produces non-integers. The paper mentions using a learned projection module Π_ψ in Section 6 (for the biological applications), but does not clarify how integrality is handled when the simple scaling is used in practice.

- **Low absolute Spearman correlations not contextualized (Table 2):** CB achieves 0.267, MuSiC 0.186, CIBERSORTx 0.079. All values are low in absolute terms. Without reference to published deconvolution benchmarks, readers cannot assess whether CB's improvement over CIBERSORTx and MuSiC reflects a genuinely strong result or merely best-among-weak-baselines.

### Trivial

- The cross-entropy vs. energy score comparison is a core design choice differentiated from prior discrete diffusion/flow methods, but it is relegated entirely to Appendix D.1. A brief quantitative summary in Section 3.2 would help readers appreciate the motivation.

---

## Nice-to-Haves
- A convergence plot (per-iteration M-step loss and E-step sample quality) to validate the EM procedure in practice.
- For the spatial transcriptomics application, an ablation training CB with only aggregate supervision (no nuclear-stain image side information z) would directly test what the EM deconvolution framework contributes.

---

## Removed Points
*These points were filtered; treat with caution.*

- **Table 3 visual absence:** Parser artifact. Table 3 appears as a text heading in the parsed text (line 325) because PDF parsing stripped it; the data exist in the original submission.
- **Table 5 naive baseline (spot mean):** The paper explicitly characterizes this as a sanity check with a biological motivation ("cells within a spot coordinate their functions"). This is not overclaiming; the headline comparison is Table 4 (vs. STDeconvolve). Removed as over-criticism of an acknowledged limitation.
- **Missing related works:** Cannot verify without external sources; removed per hard rule.
- **Reproducibility / hyperparameter details:** Removed per hard rule.
- **Formatting/parser artifacts:** Removed per hard rule.

---

## Novel Insights
The clean theoretical parallel between the integer and Gaussian cases — κ playing the role of σ, L1 discrete OT playing the role of L2 quadratic OT — is a genuine mathematical insight with implications beyond this paper. It suggests that principled design of forward processes for non-Euclidean data should start from the entropy-regularized OT structure native to the space, rather than forcing an analogy to the Gaussian case. The Bessel slack posterior as the key computational object for integer bridges is non-obvious and may find use in other integer-valued sequential modeling tasks.

---

## Suggestions
1. Add a single ablation row to Table 1: same CB architecture but with MSE or NLL loss instead of the bridge/energy-score objective. This directly demonstrates the bridge formulation's contribution.
2. Provide a brief EM convergence figure (per-iteration count profile quality or M-step loss) in the main body or as a small supplement.
3. Clarify in Section 4 or Sec. 6 how the simple scaling projection Π (Prop. 4.1) handles non-integer outputs when it is used in practice.
4. Add one line contextualizing the Table 2 Spearman values against published benchmarks in the deconvolution literature.
5. Bring a one- or two-number summary of the CE vs. energy score comparison (App. D.1) into the main Section 3.2 text.

---

## Score and Decision

**Calibration anchors:**

| Path | Avg Human Score | Round | Comparison |
|------|----------------|-------|------------|
| 3MnMGLctKb (CFGen) | 6.75 | R1 | Flow-based single-cell count generation — less theoretically grounded than CB, no integer-native bridge, no deconvolution extension |
| IcbC9F9xJ7 (scDiff) | 6.50 | R1/R2 | General single-cell diffusion framework — more general but less technically innovative |
| FtjLUHyZAO (STEM) | 6.67 | R1 | Diffusion for spatial transcriptomics — similar application domain, less principled integer framework |
| Ombm8S40zN (DDPP) | 6.25 | R1 | Steering masked discrete diffusion — comparable methodological depth, more narrow contribution |
| RuP17cJtZo (Generator Matching) | 8.00 | R1/R2 | Modality-agnostic generative framework for arbitrary Markov processes — broader and more theoretical, no specific domain application |
| g7ohDlTITL (RFM) | 8.00 | R1 | Riemannian flow matching — similarly principled framework for non-Euclidean data, landmark paper |
| EO8xpnW7aX (SymmetricDiffusers) | 8.00 | R1/R2 | Discrete diffusion on permutations — similar technical depth, narrower scope |
| G328D1xt4W (Fine-tune discrete diffusion) | 6.00 | R2 | Reward fine-tuning for discrete diffusion in biology — less fundamental contribution |
| gBLEHzKOfF (Generative entropic neural OT) | 6.00 | R2 | Neural OT across spaces — comparable combination of theory and empirics |
| CWoIj2XJuT (Unbalanced DSB) | 4.50 | R1 | Related Schrödinger bridge variant — weaker empirical results, rejected |
| PyERBFX0wJ (Reflected SB) | 4.33 | R1 | Reflected diffusion/SB — principled but narrower and rejected |

**Round 1 bracket:** 6.5 – 8.0

**Round 2 narrowing:** CB's theoretical contribution (integer bridge with Bessel posterior, Schrödinger bridge connection, EM deconvolution) exceeds that of CFGen (6.75) or scDiff (6.5), which lack the principled integer-native construction. However, CB does not reach the landmark-framework level of Generator Matching or RFM (both 8.0) due to the two Major issues: missing ablation and comparison fairness. The 7.0 range (borderline accept to accept) is appropriate for a paper with solid, novel theory and substantial applications that has addressable but genuine empirical gaps.

**Final score: 7.0**

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>