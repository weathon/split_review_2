## Summary

This paper proposes Quantized Zeroth-order Optimization (QZO), a method for fine-tuning quantized LLMs using zeroth-order optimization. The key insight is to perturb the continuous quantization scale Δ (rather than the discrete quantized weights θ̄) for gradient estimation via SPSA, and to apply directional derivative clipping (DDC) for training stability. QZO is orthogonal to both scalar-based (GPTQ, 4-bit) and codebook-based (AQLM, 2-bit) post-training quantization. The method reduces peak memory from 26.8GB (SGD fine-tuning) or 14.8GB (MeZO) to 4.8GB for OPT-6.7B on SST-2, and enables fine-tuning Llama-2-13B (2-bit) within a single 24GB GPU.

## Strengths

- **Novel and principled technical idea (Section 3.2.1).** Perturbing the continuous quantization scale Δ rather than the discrete quantized weights θ̄ for zeroth-order gradient estimation is genuinely clever. It cleanly sidesteps the fundamental tension between discrete weights and continuous gradients without requiring de-quantization/re-quantization at each step. The decomposition θ = Δ ⊙ θ̄ with perturbation on Δ is well-motivated.

- **Real and substantial memory savings (Figure 1, Table 1).** QZO (4-bit) reduces peak memory from 26.8GB (SGD) and 14.8GB (MeZO) to 4.8GB for OPT-6.7B on SST-2. For Llama-2-13B at 2-bit, it uses only 5.78GB. These numbers are believable and practically meaningful — enabling fine-tuning a 13B model on a single 24GB consumer GPU.

- **Orthogonality to existing PTQ methods.** QZO works with both scalar-based (GPTQ, 4-bit) and codebook-based (AQLM, 2-bit) post-training quantization without requiring modifications to either. This generality is demonstrated across two quantization paradigms and four model architectures.

- **Directional derivative clipping (DDC) stabilizes training (Figure 2, Figure 3).** The ablation showing training collapses at step 22 without DDC while DDC maintains stability across 1000 steps is convincing experimental evidence. The sensitivity analysis over C shows a reasonable operating range (C ≥ 75).

## Weaknesses

### Fatal

None.

### Major

- **The variance reduction argument in Eq. 7–8 is mathematically invalid.** The derivation attempts to show that Var[clipped] ≤ Var[unclipped] by substituting (∇L)² for E[||unclipped||]² in the last line of Eq. 8. However, by Jensen's inequality, E[||unclipped||] ≥ ||E[unclipped]|| = ||∇L||, so E[||unclipped||]² ≥ (∇L)². The paper replaces the larger quantity with a smaller one, making the direction of the inequality ambiguous. The claim that "Var[clipped] ≤ Var[unclipped] holds almost surely" does not follow from the equations as written. Since the paper presents DDC's theoretical justification as a core contribution, this is a significant error. (The practical benefit of DDC is still convincingly demonstrated in Figure 2; the flaw is in the theoretical framing.)

- **The FLOPs numbers in Table 2 contain an inconsistency that suggests an arithmetic error.** OPT-6.7B QZO total FLOPs = 8.19×10¹³, while Llama-2-7B QZO = 2.26×10¹⁶ — a **276× difference** despite nearly identical trainable parameter counts (5.03×10⁷ vs. 5.06×10⁷), the same training steps (20k), and the same two-forward-pass structure. The paper's claim that QZO uses "about 1% of the FLOPs of MeZO" is also inconsistent across models: 0.008% for OPT-6.7B (8.19×10¹³ / 9.91×10¹⁷), 2% for Llama-2-7B, and 7% for Llama-3.1-8B. These discrepancies require correction and affect the computation-efficiency claims.

- **Missing experimental comparison against the closest prior works.** Section 2 (Related Work) explicitly discusses Feng et al. (2024), Zhou et al. (2025), and Bar & Giryes (2025), stating they "share the spirit of combining ZO with quantization" and claiming QZO is "inherently more efficient and flexible." Yet none of these methods appear as baselines in any experiment. For a new-method paper, claiming advantages over the most directly related prior work without comparing against it is a critical gap that prevents the claimed advantages from being substantiated.

### Minor

- **The claim that QZO performs "on par with MeZO" overstates the results in some cases.** While this is a reasonable summary for most tasks, the Llama-3.1-8B CB result shows a 21.5-point gap (QZO 69.6 vs. MeZO 91.1) that is not discussed or explained. More careful characterization of when and why QZO underperforms would strengthen the paper.

- **No ablation comparing DDC against standard gradient clipping approaches.** The paper shows DDC vs. no clipping (Figure 2) but does not compare against standard gradient norm clipping or value clipping on the full gradient estimate. This makes it unclear whether the specific form of DDC matters or whether any reasonable clipping strategy would suffice.

- **No training time or throughput reported.** Memory is one dimension of efficiency; wall-clock time is another. QZO requires two forward passes per step. A comparison of training time against MeZO (also two forward passes) and SGD fine-tuning would help practitioners assess the practical trade-offs.

- **Limited hyperparameter sensitivity analysis.** Only the DDC clipping threshold C is ablated. The learning rate (η = 10⁻⁷) and perturbation scale (ε = 10⁻³) are fixed without exploration of their sensitivity, which is relevant for practitioners applying the method.

### Trivial

- The Limitations section (Section 5) discusses dependence on quantization quality and the diffusion model gap, but does not explicitly discuss that QZO only updates quantization scales (not the underlying quantized weights). While this is clearly stated in the methodology (Section 3.2.1) and evident from the trainable parameter counts, including it in the limitations would improve completeness.

## Nice-to-Haves

- Reporting results with statistical significance/variance across multiple seeds. While single-run reporting is standard practice in this setting, ZO methods have high gradient variance, and run-to-run variability could be meaningful.
- A comparison with QLoRA, the de facto standard for memory-efficient fine-tuning of quantized LLMs, to contextualize QZO's performance/efficiency trade-off against the broader literature.

## Removed Points

- **"18× figure inflates the apparent advantage by using AdamW as reference":** The paper clearly shows both AdamW and SGD comparisons in the same Figure 1, and the 18× figure is accurate for the AdamW reference. The data is transparently presented; this is a presentation choice, not a factual error.
- **"Theoretical unbiasedness (Theorem 1) is suspect due to missing appendix proof":** The proof is in Appendix A, which was stripped by the parser per standard procedure. The core mathematical flaw is in the variance reduction argument (Eq. 7-8), which IS in the main paper body and is retained above.
- **"Seed-based perturbation trick should be stated explicitly":** Algorithm 1 already uses random seeds for perturbation, which is stated in the pseudocode.
- **"No statistical significance" raised as a core weakness:** Downgraded to Nice-to-Have since single-run reporting is standard practice in this specific literature (MeZO and most LLM fine-tuning papers report the same).
- **Missing related works:** Removed per instructions as I cannot independently verify their existence or relevance.
- **Formatting, style, and presentation nitpicks:** These are parser artifacts or non-substantive.

## Novel Insights

The harsh reviewer's most valuable observation is that the variance reduction derivation (Eq. 7-8) commits a specific mathematical error by equating E[||unclipped||]² with (∇L)², which is invalid by Jensen's inequality. This is more specific and actionable than a generic "the theory is weak" critique. The FLOPs inconsistency across models of similar size is another concrete finding that the authors need to address. Both insights go beyond surface-level evaluation and point to specific fixes.

## Suggestions

1. **Fix the variance reduction derivation.** Either provide a correct bound or retract the theoretical variance reduction claim and reframe DDC as an empirically motivated heuristic. The empirical evidence (Figure 2) stands on its own.
2. **Correct the FLOPs calculations in Table 2** and verify the "1% of MeZO FLOPs" claim, as the numbers are currently inconsistent across models.
3. **Include at least one of the closest prior works** (Feng et al., 2024; Zhou et al., 2025; Bar & Giryes, 2025) as an experimental baseline to substantiate the claimed advantages.
4. **Add training time comparisons** so practitioners can assess the memory/speed trade-off.
5. **Discuss the CB performance gap for Llama-3.1-8B** and characterize when QZO underperforms MeZO.

## Score and Decision

<score>4</score>
<decision>Reject</decision>