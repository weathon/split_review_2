Now let me write the final review.

## Summary

This paper proposes QZO (Quantized Zeroth-order Optimization), a method that fine-tunes quantized LLMs by perturbing the continuous quantization scale Δ rather than the discrete quantized weights, enabling zeroth-order optimization on quantized models. It introduces Q-SPSA (a quantized variant of SPSA) and Directional Derivative Clipping (DDC) for training stability. Experiments on OPT-6.7B, Llama-2-7B, Llama-3.1-8B, and Llama-2-13B across 5 NLP benchmarks show QZO achieves ~18× memory reduction vs. AdamW fine-tuning and ~3× vs. MeZO, performing on par with MeZO despite operating at 4-bit precision.

## Strengths

- **Genuinely clever core idea.** Perturbing the continuous quantization scale Δ rather than the discrete quantized weights θ̄ to enable ZO gradient estimation (Section 3.2.1, Eq. 5) is a simple, well-motivated, and non-obvious workaround to the discreteness problem. This is the paper's main technical novelty.

- **Impressive measured memory reduction.** Figure 1 and Table 1 show QZO (4-bit) uses 4.8–6.3 GB compared to 87.6–113.7 GB for AdamW fine-tuning (~18×) and 14.8–20.5 GB for MeZO (~3×). These numbers are clearly documented and meaningful regardless of performance gaps.

- **Compatibility with multiple quantization paradigms.** The method is demonstrated with both GPTQ (scalar-based, 4-bit) and AQLM (codebook-based, 2-bit), and the mechanism in Eq. 5 is agnostic to the quantization scheme, meaning it can ride on top of future quantization improvements.

- **The DDC ablation is informative.** Figure 2 convincingly demonstrates that without directional derivative clipping, training collapses to NaN within ~20 steps. Figure 3 shows stable performance across C ∈ [75, 150]. This is a clean ablation validating the necessity of the proposed component.

## Weaknesses

### Fatal
None.

### Major

- **Theorem 1 (unbiasedness of the clipped gradient estimate) is incorrect for any finite clipping threshold C.** The paper claims (Theorem 1, line 112) that the clipped estimate d'·z is unbiased for ∇_Δ L. This is false. The directional derivative d ≈ zᵀ∇L shares the random variable z with the perturbation direction, so d' = clip(d, −C, C) and z are correlated. For the 1D case, E[z·clip(zg,−C,C)] = g·(2Φ(C/g)−1), which equals g only when C → ∞ (i.e., clipping never triggers). The variance-reduction derivation in Eq. 8 depends on the unbiasedness claim to substitute E[‖∇̂‖]² = (∇L)², so the claimed variance reduction is also not theoretically justified. The empirical ablation (Figure 2) still supports DDC's practical necessity, but the paper's theoretical framework for DDC is unsound as presented. **The paper would be stronger if it dropped the formal unbiasedness claim and presented DDC as a practical heuristic validated by the ablation.**

- **No statistical significance or variance reporting for any result.** ZO methods are acknowledged to be high-variance (line 104). Yet every number in Tables 1 and 3 is a single point with no standard deviations, confidence intervals, or information about number of seeds/runs. Many comparisons are close (e.g., MeZO vs. QZO on OPT-6.7B SQuAD: 79.6 vs. 78.5; BoolQ: 66.8 vs. 66.4), making the claimed "on par" conclusion unverifiable. Given that ZO methods are inherently noisy, this is a critical evidential gap.

### Minor

- **The narrative around "enabling fine-tuning of quantized models" is imprecise.** Line 50 states "quantized LLMs are not suitable for fine-tuning," but QLoRA (Dettmers et al., 2023, cited in references) has enabled 4-bit quantized LLM fine-tuning since 2023 via frozen quantized weights + low-rank adapters. The paper's actual novelty — combining ZO with quantization to avoid adapters and backpropagation — is genuine and well-motivated, but the framing overclaims. A brief discussion situating QZO relative to QLoRA would clarify the contribution.

- **The upper-bound baseline uses SGD, not AdamW** (footnote 2). Memory claims (18×) are benchmarked against AdamW, while the actual task performances are compared against SGD — a weaker optimizer that is itself memory-efficient (26.8 GB for OPT-6.7B vs. 87.6 GB for AdamW). The gap against AdamW-optimized fine-tuning is unknown. This doesn't invalidate the results but weakens the significance of the "upper-bound" comparison.

- **The claim of "computation-efficient" (line 207) is overstated relative to fine-tuning.** For Llama-3.1-8B, QZO FLOPs (7.9×10¹⁶) exceed SGD fine-tuning FLOPs (2.48×10¹⁶). QZO is reliably computation-efficient only relative to MeZO; the FLOPs discrepancy across architectures (orders of magnitude better on OPT-6.7B vs. comparable/worse on Llama models) is unexplained.

### Trivial
None.

## Nice-to-Haves

- Report wall-clock time in addition to FLOPs, which would be a more practical measure of efficiency.
- Extend the clipping threshold sensitivity study (Figure 3) to additional datasets and models.
- Report AdamW fine-tuning results for at least a subset of tasks to calibrate the true performance gap.

## Removed Points

These points from the harsh critic were removed with justifications:

1. **"Theorem 1 is fatal/structural"** — Downgraded to Major. The empirical evidence for DDC (Figure 2) stands independently; the method does not require the theorem to be correct. The ablation is stronger evidence than the flawed proof.
2. **"The proof is relegated to Appendix A, which was stripped by the parser, so I cannot verify it"** — Removed. This speculates about a stripped appendix. The mathematical error is verifiable from the main text alone.
3. **"QLoRA omission is structural (framing)"** — Downgraded to Minor. While the omission is worth noting, the paper's contribution (ZO + quantization without adapters) remains genuinely novel.
4. **"Wall-clock time comparison"** — Moved to Nice-to-Haves. It's a useful addition but not a core weakness.
5. **"FLOPs inconsistency is Evidential severity"** — Downgraded to Minor. The computation-efficiency claim is slightly overstated but not false (QZO is still far more efficient than MeZO).

## Novel Insights

None beyond the paper's own contributions. The harsh critic's analysis of the Theorem 1 flaw is the most novel observation — revealing that the unbiasedness claim is mathematically incorrect for any finite clipping threshold — which the paper itself does not acknowledge.

## Suggestions

1. **Fix or remove Theorem 1.** Drop the formal unbiasedness claim and reframe DDC as a practical heuristic whose empirical benefits are validated by the ablation (Figure 2). The method is compelling without a flawed theorem.
2. **Add statistical rigor.** Run 3–5 seeds and report means ± standard deviations across all experiments, especially for close comparisons (MeZO vs. QZO).
3. **Discuss QLoRA explicitly.** Clarify that QZO differs by (a) not requiring added adapter parameters and (b) working without backpropagation. A memory/performance comparison table would strengthen the paper.
4. **Explain the FLOPs discrepancy across architectures.** The orders-of-magnitude difference between OPT-6.7B and Llama models in QZO FLOPs warrants explanation.
5. **Report AdamW fine-tuning results** for at least a subset of tasks, or explicitly frame the upper-bound as SGD fine-tuning throughout (not just in a footnote).

## Score and Decision

**Calibration anchors used (retrieved across rounds):**

| Path | Avg Score | Round | Itemized | Comparison |
|---|---|---|---|---|
| SubZero (FK6T0U4Mg1) | 4.25 | R1 | Yes | Similar ZO-for-LLM paper, rejected. QZO has more novel core idea but a flawed theorem. SubZero had stronger theory. |
| EfficientQAT (6Mdvq0bPyG) | 3.00 | R1 | No | Quantization-aware training, less relevant. QZO is stronger. |
| CVXQ (0T8vCKa7yu) | 3.00 | R1 | No | LLM quantization, less relevant. |
| PrefixQuant (vw0NurJ7UX) | 3.00 | R1 | No | Activation quantization, less relevant. |
| MeZO-A³dam (OBIuFjZzmp) | 4.75 | R2 | Yes | Adaptive ZO optimizer, rejected. QZO has more novel idea but worse theoretical flaw. MeZO-A³dam had mostly-correct proofs. |
| Q-GaLore (rBzvEEbrF7) | 5.00 | R2 | Yes | Quantized GaLore, rejected (mixed reviews). QZO has more novel core idea. |
| L4Q (KJzz4UwqTb) | 4.50 | R2 | No | Quantization-aware PEFT. Comparable score range. |
| SensZOQ (myYzr50xBh) | 5.80 | R1 | Yes | ZO + quantization, **accepted**. QZO's Theorem 1 flaw is more damaging than SensZOQ's weaknesses. SensZOQ had sound theory. |
| HiZOO (bEqI61iBue) | 5.67 | R2 | No | Hessian-informed ZO, accepted. Stronger theory than QZO. |
| LQ-LoRA (xw29VvOMmU) | 6.75 | R2 | No | Quantized + low-rank, accepted. Stronger empirical package. |

**Round-1 bracket:** [3.5, 5.5] based on comparison with SubZero (4.25), MeZO-A³dam (4.75), Q-GaLore (5.00), and SensZOQ (5.80).

**Narrowing:** Compared itemized impact scores. QZO's strengths (core idea +9.99, DDC ablation +9.99, multi-quantization +9.37) are comparable to SubZero's best strengths. However, QZO's weaknesses (Theorem 1 flaw -10.00, no stat sig -10.00) are more damaging than SubZero's
(-9.54 novelty, -9.70 scope) because they strike at the paper's claimed theoretical grounding. Relative to MeZO-A³dam (4.75), which had one reviewer identify a proof error (-10.00) but otherwise sound theory, QZO's Theorem 1 is more fundamentally flawed. Relative to SensZOQ (5.80, accepted), QZO has a more novel core idea but SensZOQ's theory was sound (+9.46 impact).

**Final placement:** Score 4.5. The core idea is genuinely novel and the memory savings are compelling, but the flawed Theorem 1 and lack of any statistical significance prevent acceptance in the current form. The paper sits in the borderline-reject range — below the 5.0+ threshold where papers begin to be accepted — but the issues are fixable.

<score>4.5</score>
<decision>Reject</decision>