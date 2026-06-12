Now I have enough calibration data. Let me finalize my review.

**Round 1 bracket:** Based on the retrieved anchors, QZO sits in the range of **4.5–6.0**. The most relevant comparisons:
- LeZO (4.0, Reject), SubZero (4.25, Reject), MeZO-A³dam (4.75, Reject): ZO improvements with less novelty than QZO
- Sparse MeZO (5.5, Reject): Good empirical gains but less novel mechanism
- SensZOQ (5.8, Accept): ZO + quantization, most directly comparable
- HiZOO (5.67, Accept): ZO with theoretical contribution

QZO's core mechanism (perturbing quantization scales) is more novel than the rejected papers, but the incorrect theoretical claim and missing baselines weigh it down. I bracket at **4.5–5.5**.

**Round 2 narrowing:** After comparing with SensZOQ (5.8, Accept) and Sparse MeZO (5.5, Reject), QZO's cleaner mechanism and broader experimental validation push it above the 4.0-4.5 range, but the theoretical error and missing baselines keep it below the ~5.67 accept threshold. Final score: **5.0**.

Now let me compile the final review:

---

## Summary
This paper proposes QZO (Quantized Zeroth-order Optimization), which enables zeroth-order fine-tuning of quantized neural networks by perturbing continuous quantization scales instead of discrete weights, combined with directional derivative clipping (DDC) for training stability. The method eliminates gradients and optimizer states while compressing weights, achieving ~18× memory reduction compared to 16-bit AdamW and ~3× reduction compared to 16-bit MeZO.

## Strengths
- **Novel core mechanism (Q-SPSA)**: Perturbing continuous quantization scales Δ while keeping discrete weights θ̄ fixed (Definition 3.3, Eq. 5) is a clean, principled solution to the precision gap between discrete weights and continuous gradients. Unlike prior ZO+quantization methods (Feng et al., 2024; Zhou et al., 2025; Bar & Giryes, 2025) that quantize perturbation noises and require re-quantization at each step (line 52), QZO avoids de-quantization/re-quantization entirely.
- **Rigorous and comprehensive memory profiling**: Table 1/Figure 1 provide concrete VRAM measurements across three model families (OPT-6.7B: 87.6→4.8 GB, Llama-2-7B: 92.2→5.0 GB, Llama-3.1-8B: 113.7→6.3 GB), confirming consistent ~18× reduction vs. 16-bit AdamW and ~3× vs. MeZO.
- **Orthogonality to diverse quantization paradigms**: Successfully evaluated with both scalar-based GPTQ (4-bit, Table 1) and codebook-based AQLM (2-bit, Table 3), with the 2-bit Llama-2-13B results showing significant gains over zero-shot-Q (SST-2: 80.5 vs. 57.6).
- **Computational efficiency**: Table 2 shows QZO uses ~1% of MeZO's trainable parameters (e.g., 5.03×10⁷ vs. 6.65×10⁹ for OPT-6.7B) and ~1% of its FLOPs, a direct and significant advantage of tuning only quantization scales.
- **Strong DDC ablation**: Figure 2 convincingly demonstrates training collapses at step 22 without DDC; Figure 3 shows robust practical performance across C ∈ [75, 125] with interpretable failure modes at extremes.
- **Practical accessibility**: Fine-tunes Llama-2-13B on a single 24GB RTX 4090 (Table 3), demonstrating real-world usability.

## Weaknesses

### Fatal
None

### Major
- **Theorem 1 (unbiasedness of clipped gradient) appears mathematically incorrect**: Theorem 1 (line 112) claims the clipped gradient estimate d'·z is an unbiased estimate of ∇_Δ L. This is implausible: clipping d = z^T∇_Δ L to d' = clip(d, C) is a nonlinear operation, and for g = (g₁, 0, ..., 0) with z₁ ~ N(0,1), E[clip(g₁z₁, C)·z₁] = g₁·(2Φ(C/|g₁|) - 1) < g₁ for any finite C, showing bias toward zero. This is consistent with the well-known bias-variance tradeoff of gradient clipping in optimization. The variance reduction derivation (Eq. 8, lines 118-122) depends on Theorem 1 to conclude Var[clipped] ≤ Var[unclipped] at line 122. Note: the practical conclusion is still valid via a simpler argument (d'² ≤ d² pointwise implies E[||∇'||²] ≤ E[||∇||²]), but the stated theoretical contribution is compromised.

- **Missing QLoRA baseline**: QLoRA (Dettmers et al., 2023) is the dominant method for fine-tuning quantized LLMs and is cited (line 311) but never compared experimentally. QLoRA targets the same memory-constrained fine-tuning problem (4-bit weights + LoRA adapters + backprop). While QZO's approach is fundamentally different (eliminating gradients entirely), practitioners need this comparison to assess QZO's practical value. This is the single most impactful missing experiment.

### Minor
- **Overstated "on par with MeZO" claim**: The paper states QZO "performs on par with MeZO" (line 249) but results are model- and task-dependent with notable gaps. OPT-6.7B: MeZO wins 4/5 tasks (SST-2 gap: 5.4 points). Llama-3.1-8B: MeZO wins 3/5 with a 21.5-point gap on CB (91.1 vs. 69.6, line 204-205). QZO does win on Llama-2-7B (4/5 tasks). A more accurate characterization: QZO achieves broadly competitive results with ~3× less memory and ~1% FLOPs, with task-specific performance gaps in either direction.

- **No competing ZO+quantization baselines compared experimentally**: Feng et al. (2024), Zhou et al. (2025), and Bar & Giryes (2025) are discussed as prior work (line 52) but not compared. The claim that QZO is "inherently more efficient and flexible" lacks empirical support.

- **SGD upper-bound baseline**: Fine-tuning upper bound uses SGD (line 178) rather than AdamW, due to computational budget constraints. Since AdamW typically outperforms SGD for LLM fine-tuning, the performance gap between QZO and the true upper bound may be understated.

### Trivial
None

## Nice-to-Haves
- Confidence intervals or multi-seed reporting would strengthen confidence given ZO methods' known instability.
- Characterization of the clipping-induced bias empirically would complement a corrected theoretical analysis.

## Removed Points
These points are flagged to be removed, treat them with caution:
- The strength finder's claim about "theoretical proof that DDC preserves unbiasedness while reducing variance" is invalidated by the verified mathematical error in Theorem 1 and was removed from strengths.
- A generic reproducibility concern was removed as too vague.

## Novel Insights
The key insight—that perturbing continuous quantization scales (rather than discrete weights or quantized noise) bridges ZO optimization and model quantization without de-quantization/re-quantization—is genuinely novel and well-motivated. This insight yields a practical ~18× memory reduction while maintaining broadly competitive performance, and is orthogonal to both scalar and codebook quantization paradigms.

## Suggestions
- Correct or retract Theorem 1. The practical benefit of DDC (variance reduction for stability) is well-supported by experiments (Figures 2-3) and can stand on its own. Reframe around the bias-variance tradeoff.
- Add QLoRA as a baseline in at least one representative setting.
- Recharacterize the MeZO comparison honestly, emphasizing the 3× memory / ~1% FLOPs advantages while acknowledging task-specific gaps.

## Reporting: Calibration Anchors

All retrieved anchors across both rounds:

| Anchor | Path | Avg Score | Round | Comparison |
|--------|------|-----------|-------|------------|
| Systematic Review of LLMs | 8QTpYC4smR | 1.0 | 1 | Irrelevant survey, not comparable |
| NEMESIS Jailbreaking | 5kMwiMnUip | 1.4 | 1 | Irrelevant jailbreak paper |
| Cross-Lingual Humanoid Robots | gwZ90hFSL2 | 1.0 | 1 | Irrelevant robotics paper |
| KL Divergence GFlowNets | Uj0h13lVrR | 1.0 | 1 | Irrelevant GFlowNet paper |
| EfficientQAT | 6Mdvq0bPyG | 3.0 | 1 | Quantization-aware training, not ZO; rejected |
| PrefixQuant | vw0NurJ7UX | 3.0 | 1 | Inference quantization; rejected |
| LLM Compression CVXQ | 0T8vCKa7yu | 3.0 | 1 | Weight quantization; rejected |
| Cut Cross-Entropy | E4Fk3YuG56 | 8.5 | 1 | Very different topic (loss computation); accepted |
| Efficient Fine-Tuning Quantized LLMs | zcx6rIMbbR | 5.4 | 1 | Quantized LLM fine-tuning (not ZO); rejected |
| LeZO (Layer-wise Sparse ZO) | vqJZb9SX1T | 4.0 | 1 | ZO optimizer improvement, less novel than QZO; rejected |
| SubZero | FK6T0U4Mg1 | 4.25 | 1 | Random subspace ZO, less novel mechanism; rejected |
| ZO-Offloading | euZD4YTXKu | 3.75 | 1 | ZO + offloading for single GPU; rejected |
| SensZOQ (Sparse ZO + Quantization) | myYzr50xBh | 5.8 | 1 | Most directly comparable (ZO + quantization); accepted |
| LOZO (Low-rank ZO) | 9BiVepgmWW | 7.0 | 1 | Low-rank ZO, strong theory/experiments; accepted |
| HiZOO (Hessian-informed ZO) | bEqI61iBue | 5.67 | 1 | ZO with Hessian info; accepted |
| LQ-LoRA | xw29VvOMmU | 6.75 | 1 | Quantized + LoRA, not ZO; accepted |
| Scaling Laws for Precision | wg1PCg3CUP | 8.0 | 1 | Precision scaling laws; accepted, not comparable |
| MoE++ | t7P5BUKcYv | 8.0 | 1 | MoE acceleration; not comparable |
| LLMs for Bayesian Optimization | OOxotBmGol | 8.0 | 1 | Not comparable |
| HiRA (Hadamard Adaptation) | TwJrTz9cRS | 8.0 | 1 | PEFT method; not comparable |
| MeZO-A³dam | OBIuFjZzmp | 4.75 | 2 | Adaptive ZO Adam; less novel than QZO; rejected |
| Sparse MeZO | 4Kw4KAoVnx | 5.5 | 2 | Sparse parameter selection for ZO; less novel; rejected |
| Memory-Efficient BCD for HiZOO | q8H9t10Vsy | 4.0 | 2 | Block coordinate ZO; rejected |

**Round 1 bracket:** 4.5–6.0 (narrowed to 4.5–5.5 after considering theoretical error)
**Round 2:** Confirmed 5.0 as final score. QZO's novel core mechanism places it above the 4.0-4.5 rejected papers (LeZO, SubZero), but the incorrect theoretical claim and missing QLoRA baseline place it below the ~5.67 accept threshold (HiZOO, SensZOQ).

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>