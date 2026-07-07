Now let me produce the final consolidated review.

## Summary

This paper proposes Quantized Zeroth-order Optimization (QZO), a method that enables fine-tuning of quantized LLMs by perturbing the continuous quantization scale parameters rather than the discrete quantized weights during zeroth-order gradient estimation. The key insight—decomposing weights as Δ⊙θ̄ and only updating Δ—circumvents the precision mismatch that would otherwise force repeated de-quantization/re-quantization. QZO works with both scalar-based (GPTQ, 4-bit) and codebook-based (AQLM, 2-bit) quantization, eliminates gradients and optimizer states, and reduces memory by ~18× vs. AdamW fine-tuning (e.g., 5 GB vs. 92 GB for Llama-2-7B). A directional derivative clipping (DDC) mechanism stabilizes training.

## Strengths

- **A genuinely clever core idea.** The insight to perturb the quantization scale Δ rather than the discrete weights θ̄, keeping quantized integers fixed, directly addresses the precision-mismatch challenge for ZO on quantized models. This is clearly articulated in Definition 3.3 and feels natural in retrospect — a hallmark of a good idea.

- **Dramatic and well-measured memory savings.** Memory profiling in Figure 1 shows QZO (4-bit) uses 4.8–6.2 GB for 7B–8B models vs. 14.8–20.4 GB for MeZO (16-bit) and 26–114 GB for full fine-tuning. The 18× factor vs. AdamW is properly benchmarked with a stated protocol (batch size 1, first 100 steps, following MeZO convention).

- **Generality across quantization methods.** QZO works with both scalar-based (GPTQ, 4-bit) and codebook-based (AQLM, 2-bit) post-training quantization, with the AQLM adaptation (fine-tuning channel-wise scales jointly with un-quantized weights) showing attention to implementation details.

- **DDC ablation is informative and honestly presented.** Figure 2 convincingly demonstrates training collapse within 22 steps without DDC, and Figure 3 provides a clear sensitivity analysis showing a performance plateau (C ≥ 75) that gives practitioners actionable guidance.

- **Parameter efficiency.** Fine-tuning only the quantization scales (~5×10⁷ parameters vs. ~7×10⁹ total) is a substantial reduction, clearly documented in Table 2.

## Weaknesses

### Major
None.

### Minor

1. **Performance "upper bound" uses SGD, not AdamW — mismatch between motivation and evaluation.** The paper motivates eliminating AdamW's optimizer states (28 GB for a 7B model) as a central advantage, but all fine-tuning performance comparisons in Table 1 use SGD (acknowledged in Footnote 2). The headline 18× memory reduction (Figure 1) is fairly measured against AdamW, but the *performance* gap the method must bridge is against SGD — a weaker baseline that lacks AdamW's adaptive learning rates and convergence benefits. Calling SGD fine-tuning the "upper bound" inflates the apparent strength of the results. The paper should either add an AdamW reference run or relabel the baseline.

2. **No error bars or variance reporting.** ZO methods are known to have high gradient variance. The paper reports single runs for all experiments. Given that QZO trails MeZO by 21.5 points on CB (69.6 vs. 91.1) and leads by 4.8 points on SQuAD (85.5 vs. 80.7), it is impossible to assess whether these differences are meaningful without variance estimates.

3. **FLOPs numbers are inconsistently defined.** Table 2 reports QZO FLOPs ranging from 265× *less* than fine-tuning (OPT-6.7B: 8.19×10¹³ vs. 2.17×10¹⁶) to 3× *more* (Llama-3.1-8B: 7.9×10¹⁶ vs. 2.48×10¹⁶). The claim that QZO uses "1% of the FLOPs of MeZO" holds roughly for Llama-2-7B (~2%) but not for OPT-6.7B (~0.008%) or Llama-3.1-8B (~7%). The paper does not specify what operations are counted (forward passes? updates only? both?), making these numbers uninterpretable.

4. **DDC variance proof derivation is sloppy.** In Eq. 8, the paper replaces E[‖∇̂‖]² with (∇L)² (the squared gradient norm). This step implicitly assumes E[‖∇̂‖] = ‖E[∇̂]‖, which does not follow from unbiasedness — by Jensen's inequality, E[‖∇̂‖] ≥ ‖E[∇̂]‖ = ‖∇L‖, so E[‖∇̂‖]² ≥ (∇L)² and the inequality direction is not guaranteed as written. The conclusion that DDC reduces variance can be justified more cleanly (d'² ≤ d² plus unbiasedness gives standard variance reduction), so this is a presentation issue rather than an error that threatens the paper, but the proof as written is incorrect.

5. **No experimental comparison with prior quantized ZO methods.** The Related Work discusses prior works on ZO for quantized models (Feng et al., 2024; Zhou et al., 2025; Bar & Giryes, 2025) and claims QZO is "inherently more efficient and flexible," but provides no quantitative comparison. Some empirical context would help validate this claim.

### Trivial

- **Batch size mismatch not discussed.** QZO uses batch size 16 while the fine-tuning baseline uses batch size 8. Larger batches can reduce gradient variance in ZO, potentially favoring QZO.

- **Fine-tuning step count not reported.** QZO uses 20k steps, but the number of steps/epochs for the fine-tuning baseline is not specified, making training cost comparisons difficult to interpret.

## Nice-to-Haves

- A single AdamW fine-tuning run on one model/dataset (e.g., Llama-2-7B on SST-2) would resolve the ambiguity about where QZO stands relative to the optimizer that motivated the work.
- Reporting the number of training steps for fine-tuning baselines would make FLOPs and convergence comparisons interpretable.

## Removed Points

These points were flagged during review but removed for the reasons stated:

1. **"Per-element vs per-layer perturbation underspecified"** — REMOVED. The paper explicitly states in Algorithm 1's caption and Section 3.2.1 (line 98) that in practice all quantization scales within a linear layer are perturbed together. The critic misread this.

2. **"No comparison with QLoRA"** — REMOVED. QLoRA uses a fundamentally different paradigm (backprop through LoRA adapters with stored gradients and optimizer states) that retains the components QZO eliminates. The paper's scope is explicitly about ZO methods that eliminate all gradients/optimizer states. Mentioning QLoRA as a missing baseline would be scope creep.

3. **"Memory profiling batch size of 1 not representative"** — REMOVED. The paper clearly states this follows MeZO's convention to measure minimum VRAM requirements. This is standard practice in the field.

4. **"DDC proof is fatally flawed"** — REMOVED (downgraded to Minor). While the specific step in Eq. 8 is sloppy, the conclusion (DDC reduces variance) can be justified via the standard argument: E[‖∇'‖²] ≤ E[‖∇‖²] by clipping, and unbiasedness (Theorem 1) gives E[∇'] = E[∇], so Var[∇'] = E[‖∇'‖²] − ‖E[∇']‖² ≤ E[‖∇‖²] − ‖E[∇]‖² = Var[∇]. The empirical evidence (Figure 2) is strong. The paper should correct the derivation but the core claim stands.

5. **"Per-layer perturbation affects runtime and gradient quality — paper should state which was used"** — REMOVED. The paper does state this (Algorithm 1 caption: "in practice one may perturb the entire quantization scales of a linear layer to save training time").

6. **"FLOPs numbers are physically implausible"** — REMOVED (downgraded to Minor definitional issue). For Llama-2-7B (2.26×10¹⁶ vs. 2.47×10¹⁶) and Llama-3.1-8B (7.9×10¹⁶ vs. 2.48×10¹⁶), the numbers are comparable to fine-tuning, which is physically plausible if only forward passes are counted. The problem is inconsistent definition, not implausibility.

## Novel Insights

None beyond the paper's own contributions. The reviews confirm the paper's stated contributions and identify areas for improvement in evaluation rigor, without offering fundamentally new perspectives on the method.

## Suggestions

1. Correct the DDC variance derivation in Eq. 8 to use the standard variance definition (E[‖∇‖²] − ‖E[∇]‖²), which makes the proof clean and correct.
2. Add error bars (at least 3 seeds) for the main results in Table 1.
3. Clarify the FLOPs accounting methodology — specify whether forward passes are included and why numbers vary so widely across models.
4. Either add an AdamW fine-tuning reference point for one model/dataset, or relabel "upper bound" to "SGD fine-tuning baseline."
5. Report the number of training steps for fine-tuning baselines.

## Score and Decision

**Calibration summary.** All retrieved anchors:

| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| SubZero (ZO-LoRA) | FK6T0U4Mg1 | 4.25 | R1 | Yes | Severe novelty concerns (-7.42: most improvements from GaLore). My paper's core idea is genuinely novel; no equivalent weakness. |
| SensZOQ (Static Sparsity) | myYzr50xBh | 5.80 | R2 | Yes | Novelty concern is crippling (-11.01: mask selection from prior work). My paper is clearly stronger on novelty. |
| LeZO (Layer-wise ZO) | vqJZb9SX1T | 4.00 | R1 | Yes | Has -9.38 (novelty from LISA), -6.07 (math errors). My paper is substantially stronger. |
| Quantized LLM FT (3-stage) | zcx6rIMbbR | 5.40 | R1 | Yes | Has -8.68 (limited novelty), -7.24 (PRGA=NSGA-II). My paper is stronger. |
| Low-rank ZO (LOZO) | 9BiVepgmWW | 7.00 | R1 | Yes | Stronger paper with cleaner evaluation and theory (+6.87 novelty weight). My paper is below this. |

**Round-1 bracket: 5.5–7.0.** The paper sits well above papers with fundamental novelty concerns (~4.0–5.4) but below the most polished work (~7.0+). The heaviest negative weights in my draft (FLOPs: -5.15, missing prior ZO comparison: -3.30, no error bars: -3.14) are about evaluation rigor, not contribution validity — distinguishing it from the lower-scored anchors whose heaviest negatives attack the core contribution itself.

**Final score: 6.0.** The core idea (perturbing quantization scales rather than discrete weights) is genuinely novel and the memory savings are real and well-measured. However, the evaluation has three gaps that prevent the paper from being stronger: the performance "upper bound" uses SGD rather than the AdamW that motivated the work, there are no error bars for a method with inherently noisy gradients, and the FLOPs claims are inconsistently defined. These are fixable issues that do not invalidate the contribution.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>