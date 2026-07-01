Now I have all the information needed to produce the final consolidated review.

## Summary

QZO proposes fine-tuning quantized LLMs by applying zeroth-order optimization (ZO) to the continuous quantization scales Δ while keeping discrete weights θ̄ fixed, avoiding the de-quantization/re-quantization cycles that directly applying ZO to quantized weights would require. Combined with directional derivative clipping (DDC) for stability, QZO achieves ~18× memory reduction vs. 16-bit AdamW fine-tuning and enables fine-tuning Llama-2-13B on a single 24GB GPU. The method is orthogonal to both scalar-based (GPTQ) and codebook-based (AQLM) PTQ methods.

## Strengths

- **Genuinely novel algorithmic idea.** Perturbing the continuous quantization scale Δ rather than the discrete quantized weights for ZO gradient estimation (Section 3.2.1) is a clean, non-trivial solution that sidesteps the discreteness problem without expensive de-quantization/re-quantization cycles.

- **Impressive practical memory reduction.** Figure 1/Table 1 show QZO reduces peak memory from ~15GB (MeZO, 16-bit) to ~5GB (QZO, 4-bit) on 7B models, an ~18× reduction vs. 16-bit AdamW fine-tuning. QZO enables fine-tuning Llama-2-13B within a single 24GB GPU (Table 3: 5.78GB peak).

- **Orthogonality to quantization methods.** QZO works with scalar-based GPTQ (4-bit) and codebook-based AQLM (2-bit) without modification, making it applicable to existing quantized model families.

- **2-bit results are non-trivial.** Table 3 shows QZO improves 2-bit Llama-2-13B from 57.6→80.5 on SST-2 and 55.4→59.4 on SQuAD, demonstrating that meaningful gains are possible under extreme quantization.

## Weaknesses

### Fatal
None.

### Major

1. **Missing comparison to QLoRA, the standard method for fine-tuning quantized LLMs.** QLoRA (Dettmers et al., 2023) is cited in the paper's reference list but never appears in the related work or experiments. It is the most widely used approach for adapting quantized models. The current baselines (zero-shot, MeZO on un-quantized models, full fine-tuning with SGD) do not answer the practitioner's natural question: how does QZO compare to the established standard for quantized-model adaptation? Even though QLoRA uses backpropagation (a different regime), establishing this comparison is essential for assessing practical significance. This is a real gap in the experimental design.

2. **Theorem 1's unbiasedness claim is suspect and the theoretical framing is overclaimed.** Theorem 1 states that the clipped SPSA estimate is an unbiased estimator of the full gradient ∇_Δ L(Δ⊙θ̄). This is questionable on two grounds: (a) the SPSA estimator (Eq. 5) itself is a biased approximation of the gradient for finite ε — it approximates zz^T∇L, which only becomes exact in expectation in the limit ε→0; (b) hard-threshold clipping of the directional derivative d to d' (Eq. 6) introduces additional bias — E[d'·z] ≠ E[d·z] in general when d' is a nonlinear function of d. The variance argument (Eq. 8) depends on this unbiasedness claim to cancel the ||E[·]||² terms. Fortunately, the empirical evidence for DDC (Figure 2 — training collapses without it) is strong and separable. The authors could drop the unbiasedness claim and frame DDC purely as an empirically validated stabilization technique with a guaranteed second-moment bound (Eq. 7, which follows directly from d'² ≤ d² and needs no unbiasedness assumption).

### Minor

3. **FLOPs methodology is unexplained, weakening computation-efficiency claims.** Table 2 reports total FLOPs but gives no explanation of how these are computed. The numbers raise questions: e.g., MeZO's total FLOPs (1.13×10¹⁸) is ~46× that of fine-tuning (2.47×10¹⁶) on Llama-2-7B, despite MeZO only performing forward passes (which are cheaper per step than backprop). Whether this reflects different training budgets, counting conventions, or something else is unclear. Since the paper claims "computation-efficiency," the FLOPs methodology should be stated.

4. **No statistical significance reporting.** All numbers in Tables 1 and 3 are single-run point estimates. For small datasets (CB has 500 validation examples; RTE is small), variance across seeds is non-negligible. Differences of 1–2 points (e.g., QZO 66.4 vs. MeZO 66.8 on BoolQ with OPT-6.7B) are likely within noise. Reporting means and standard deviations over at least 3 seeds would substantially strengthen the evidence.

5. **Fine-tuning upper bound uses SGD, not AdamW.** Acknowledged by the authors (footnote 2: "Due to limited budget on computational resources, fine-tuning experiments are conducted with SGD optimizer"), but this weakens the upper bound since standard LLM fine-tuning uses AdamW. The gap between QZO and "fine-tuning" in Table 1 may therefore overstate QZO's competitiveness.

### Trivial

6. **Limited discussion of scale-only adaptation's implications.** The paper is transparent that only Δ (~0.75% of parameters) is updated (Table 2), but does not discuss how this constrains expressivity. A brief discussion of what kinds of tasks are likely to benefit or suffer from scale-only vs. weight-level adaptation would strengthen the paper.

## Nice-to-Haves

- Report results over at least 3 seeds with means and standard deviations.
- Provide the FLOPs counting methodology.
- Discuss the expressivity trade-offs of scale-only adaptation.
- If resources allow, use AdamW for the full fine-tuning upper bound.

## Removed Points

- "The comparison to MeZO is not meaningful because QZO updates only 0.75% of parameters" — The paper is transparent about this in Table 2 and line 251. The asymmetry is acknowledged; the results are valid within the stated scope.
- "MeZO FLOPs should be roughly 2× inference FLOPs, not ~46× fine-tuning FLOPs" — Conflates per-step and total FLOPs. The broader concern about missing FLOPs methodology is retained in Weakness #3.
- "Missing QLoRA from related work" — Merged into Major Weakness #1.
- Various formatting nitpicks, speculation about unreleased artifacts, and style suggestions — removed per hard rules.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add QLoRA as a baseline** under matched conditions (same quantization method, models, datasets). If QZO is competitive or better, the practical significance is immediately clear. If worse, honestly frame the contribution as targeting settings where backpropagation is unavailable.
2. **Reconsider Theorem 1:** either provide a correct proof with explicit assumptions stated in the main text, or drop the unbiasedness claim and frame DDC as an empirically validated stabilization technique with a guaranteed second-moment bound (Eq. 7), which is sufficient and avoids overclaiming.
3. **Clarify FLOPs methodology** in Table 2 so the computation-efficiency claims can be properly evaluated.
4. **Add error bars** (mean and std over seeds) for at least a representative subset of settings.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>