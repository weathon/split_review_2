Now I have a comprehensive picture. Let me finalize the review.

## Summary
This paper proposes QZO (Quantized Zeroth-order Optimization), which enables zeroth-order optimization on quantized LLMs by perturbing continuous quantization scales rather than discrete weights. Combined with Directional Derivative Clipping (DDC) for training stability, QZO achieves ~18× memory reduction compared to 16-bit fine-tuning while performing competitively with MeZO across multiple model families and quantization methods.

## Strengths
- **Novel Q-SPSA formulation**: Perturbing continuous quantization scales (Δ) rather than discrete weights is an elegant solution to the discrete-continuous mismatch in combining ZO with quantization. This is cleanly formalized in Definition 3.3 (Eq. 5, line 92) and enables plug-and-play compatibility with existing PTQ methods.
- **18× memory reduction validated with real GPU profiling**: Table 1 and Figure 1 (lines 24-31) report actual peak VRAM measurements — e.g., 4.8 GB vs 87.6 GB for OPT-6.7B — not theoretical estimates, demonstrating a concrete practical milestone.
- **Compatibility with both scalar and codebook quantization**: Demonstrated with GPTQ (4-bit) on 7B models and AQLM (2-bit) on Llama-2-13B (Tables 1 and 3), showing orthogonality to the underlying quantization scheme.
- **Strong computational efficiency**: Table 2 (lines 209-219) shows QZO uses ~1% of MeZO's trainable parameters (~5×10⁷ vs ~6.7×10⁹) and ~1% of FLOPs.
- **Competitive or superior performance to MeZO on several tasks despite lower precision and memory**: On Llama-2-7B (Table 1, lines 196-200), QZO achieves 90.0 vs 83.5 on SST-2, 69.6 vs 67.9 on CB, and 85.5 vs 80.7 on SQuAD, using 5.0 GB vs 14.8 GB.
- **Effective DDC ablation**: Figures 2-3 convincingly demonstrate DDC's necessity (training collapses without it at step 22) and provide practical guidance on clipping threshold selection.
- **Honest limitation discussion**: Section 5 identifies concrete limitations including dependence on quantization quality and weaker diffusion model performance.

## Weaknesses

### Fatal
None.

### Major
- **Theorem 1 (unbiasedness of clipped gradient estimate) is incorrect.** Theorem 1 (line 112) claims the clipped gradient estimate $\hat{\nabla}' = d' \cdot z$ is unbiased for $\nabla_\Delta \mathcal{L}$. This is false for any finite $C$. In the limit $\epsilon \to 0$, $d \approx z^T g$ where $g = \nabla_\Delta \mathcal{L}$. For $g = e_1$ and $z \sim \mathcal{N}(0,I)$: $\mathbb{E}[\text{clip}(z_1, -C, C) \cdot z_1] = 2\Phi(C) - 1 < 1 = g_1$ for any finite $C$. This is a well-known property of gradient clipping. The variance reduction derivation in Eq. 8 (line 120) depends on this claim — the final step uses unbiasedness to substitute $(\nabla_\Delta \mathcal{L})^2$ for $\mathbb{E}[\|\hat{\nabla}'\|]^2$, which fails when bias is introduced. **However**: Eq. 7 (line 116, reduced second moment) holds independently and is well-supported by the strong experimental evidence in Figures 2-3. The theoretical analysis needs correction — e.g., showing DDC reduces the second moment, or providing a bias-variance tradeoff bound.

- **No empirical comparison with the most directly related methods.** The Related Work (lines 50-52) describes three prior ZO+quantization methods — Feng et al. (2024), Zhou et al. (2025), and Bar & Giryes (2025, ZOQO) — and claims QZO is "inherently more efficient and flexible," but this is asserted purely qualitatively. Without experimental comparison, a reader cannot assess whether QZO's different design actually translates into better accuracy, memory usage, or convergence. These are the paper's true competitors, not just MeZO on unquantized models.

### Minor
- **No error bars or standard deviations.** All results are reported as single numbers despite ZO optimization having inherently high-variance gradient estimates. Even 3 runs with mean ± std would significantly strengthen confidence.
- **Fine-tuning upper bound uses SGD rather than AdamW** (acknowledged in footnote 2). Using AdamW would provide a more informative ceiling representing standard practice.

### Trivial
None.

## Nice-to-Haves
- Comparison with QLoRA would contextualize QZO's practical value, though these operate in fundamentally different paradigms (full-parameter ZO vs. adapter-based backprop).
- Memory breakdown by component (weights/activations/optimizer states/overhead) would clarify where exactly QZO's savings originate.

## Removed Points
These points are flagged to be removed, treat them with caution:
- **Strength Finder's "theoretically grounded variance reduction for DDC"** — This conflicts with the verified weakness that Theorem 1 is incorrect. While the practical effect of DDC is well-supported empirically, the theoretical grounding as presented is flawed.
- **Missing QLoRA comparison** — This was weakened to a nice-to-have since QLoRA operates in a fundamentally different paradigm (adapter-based backprop vs. full-parameter ZO).
- Any parser/formatting issues are not author errors.

## Novel Insights
The key novel insight is that perturbing continuous quantization scales rather than discrete quantized weights is the natural bridge between zeroth-order optimization and model quantization. This insight — that the quantization scale Δ is the "right" continuous parameter to perturb — is conceptually clean, avoids de-quantization/re-quantization cycles that prior work requires, and has significant practical implications. The demonstration that this approach works with both scalar and codebook quantization, and achieves 18× memory reduction while sometimes beating full-precision MeZO, makes a strong case that quantization-aware ZO is a valuable paradigm for memory-constrained LLM adaptation.

## Suggestions
1. Fix Theorem 1 by replacing the unbiasedness claim with the correct characterization that DDC reduces the second moment (which Eq. 7 already supports). Alternatively, provide explicit bias-variance tradeoff bounds.
2. Add empirical comparison with at least ZOQO (Bar & Giryes, 2025) on Llama-2-7B across the five datasets.
3. Report mean ± standard deviation over 3+ random seeds for the main results.

## Calibration Report

**Round 1 brackets and anchors retrieved:**

| Paper | Score | Decision | Round | Relevance |
|-------|-------|----------|-------|-----------|
| Cross-lingual Humanoid Robots | 1.00 | Reject | R1 | Irrelevant |
| Systematic Review of LLMs | 1.00 | Reject | R1 | Irrelevant |
| NEMESIS Jailbreaking | 1.40 | Reject | R1 | Irrelevant |
| KL Divergence GFlowNets | 1.00 | Reject | R1 | Irrelevant |
| EfficientQAT | 3.00 | Reject | R1 | Moderate (QAT vs. ZO) |
| PrefixQuant | 3.00 | Reject | R1 | Moderate (inference quantization) |
| LLM Compression CVXQ | 3.00 | Reject | R1 | Moderate (quantization only) |
| Cut Cross-Entropy | 2.67 | Accept | R1 | Low (different topic) |
| SubZero | 4.25 | Reject | R1 | **High** — ZO for LLMs; similar missing-baselines issue but less novel |
| LeZO | 4.00 | Reject | R1 | **High** — ZO for LLMs; incremental (BCD + MeZO) |
| Block Coordinate Descent ZO | 4.00 | Reject | R1 | High — ZO for LLMs |
| Efficient FT Quantized LLMs | 5.40 | Reject | R1 | **Very High** — Fine-tuning quantized LLMs; less novel method |
| SensZOQ (Static Sparsity) | 5.80 | Accept | R1 | **Very High** — ZO + quantization; limited novelty, unfair memory comparison |
| LOZO (Low-rank ZO) | 7.00 | Accept | R1 | **High** — Low-rank ZO; stronger theory, narrower model coverage |
| LQ-LoRA | 6.75 | Accept | R1 | Moderate (PEFT + quantization, different paradigm) |
| HiZOO | 5.67 | Accept | R1 | **High** — Hessian-informed ZO; first to do so |
| Scaling Laws for Precision | 8.00 | Accept | R1 | Low (different topic) |
| MoE++ | 8.00 | Accept | R1 | Low (different topic) |
| HiRA | 8.00 | Accept | R1 | Low (PEFT method) |

**Round 2 anchors:**

| Paper | Score | Decision | Round | Relevance |
|-------|-------|----------|-------|-----------|
| SensZOQ | 5.80 | Accept | R2 | Same as R1 |
| Sparse MeZO | 5.50 | Reject | R2 | High — ZO + sparsity for LLMs |
| Efficient FT Quantized LLMs | 5.40 | Reject | R2 | Same as R1 |
| HiZOO | 5.67 | Accept | R2 | Same as R1 |
| Bilevel ZOFO | 5.50 | Reject | R2 | High — ZO + PEFT; limited scale |

**Bracket and scoring rationale:**
- Round 1 bracket: 5.5–7.0. The paper is clearly above the 4.0–5.5 range (SubZero, LeZO, Sparse MeZO, Bilevel ZOFO — all rejected, with less novel ideas and/or weaker experiments) and comparable to or slightly above HiZOO (5.67, accept) and SensZOQ (5.80, accept). Below LOZO (7.00, accept) which has stronger theoretical grounding.
- Round 2 confirms: QZO's core idea is more novel than SensZOQ or Sparse MeZO, its experiments cover more models and tasks, and it achieves larger memory reduction. But the theoretical error and missing ZO-quantization baselines prevent it from reaching 7+.
- Final score: **6.0** — a solid paper with a genuinely novel contribution and strong practical results, held back by the incorrect Theorem 1 and missing comparisons with the most directly related methods.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>