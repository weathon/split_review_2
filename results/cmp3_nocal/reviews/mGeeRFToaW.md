Now here is my final consolidated review.

---

## Summary

This paper proposes Quantized Zeroth-order Optimization (QZO), a method that enables zeroth-order fine-tuning on quantized LLMs by perturbing the continuous quantization scale Δ rather than the discrete quantized weights θ̄. This avoids de-quantization/re-quantization cycles and is compatible with both scalar-based (GPTQ, 4-bit) and codebook-based (AQLM, 2-bit) quantization. Combined with a Directional Derivative Clipping (DDC) stabilizer, QZO achieves ~18× memory reduction versus AdamW fine-tuning and ~3× versus MeZO, with competitive performance on 5 NLP benchmarks.

## Strengths

1. **Clean and well-motivated technical idea.** The core insight — perturbing the quantization scale Δ instead of the discrete weights θ̄ to enable ZO — is elegant and avoids the complexity of sign-based alternatives (Feng et al., Zhou et al., Bar & Giryes). The paper articulates clearly why direct SPSA on quantized weights fails (lines 34, 82).

2. **Impressive and honestly profiled memory reduction.** Figure 1 shows QZO using 4.8–6.3 GB for 7B-class models versus 87.6–113.7 GB for AdamW (~18×) and 14.8–20.4 GB for MeZO (~3×). The memory accounting is transparent (batch size=1, per-device), and the reduction follows directly from 4-bit weight compression combined with the elimination of gradients and optimizer states.

3. **Broad quantization compatibility demonstrated.** QZO is validated with GPTQ (scalar-based, 4-bit) and AQLM (codebook-based, 2-bit) — two structurally different PTQ methods — across three model families (OPT, Llama-2, Llama-3). The 2-bit results on Llama-2-13B (Table 3) are particularly striking, showing QZO can extract meaningful gains even under extreme quantization.

4. **DDC ablation provides clear evidence of its necessity.** Figure 2 directly shows that training collapses (NaN) within 22 steps without DDC, while DDC stabilizes training. Figure 3 provides a sensitivity analysis for the clipping threshold C. This is concrete empirical support for a core component of the method.

## Weaknesses

### Fatal
None.

### Major

1. **No variance or uncertainty reported for any experimental result.** Every number in Tables 1 and 3 is a single-point estimate with no standard deviations, confidence intervals, or mention of multiple seeds. This is a severe omission for a paper built on zeroth-order optimization, where gradient estimates are inherently noisy (Eq. 1 uses a single random perturbation). The paper's own Figure 2 shows directional derivatives varying from roughly −200 to +300 even *with* DDC. Some cross-method differences are large (QZO 85.5 vs MeZO 80.7 on SQuAD, Llama-2-7B), but others are tiny (QZO 66.4 vs MeZO 66.8 on BoolQ, OPT-6.7B), yet all are treated as meaningful. ZO fine-tuning on 1,000-example training sets is intrinsically high-variance; single-run results are not sufficient to distinguish systematic advantage from random seed noise. This undermines the central empirical claims.

2. **No experimental comparison against the directly competing quantized-ZO methods cited in the related work.** Section 2 specifically discusses Feng et al. (2024), Zhou et al. (2025), and Bar & Giryes (2025) as prior work combining ZO with quantization. The paper asserts QZO is "inherently more efficient and flexible" (line 52) but provides zero experimental comparison against any of these methods. The claimed advantages are entirely unsupported by evidence.

3. **FLOPs numbers in Table 2 contain unexplained inconsistencies.** QZO's FLOPs for OPT-6.7B = 8.19×10¹³ vs Llama-2-7B = 2.26×10¹⁶ — a ~276× difference despite both being ~7B models with nearly identical numbers of trainable scales (~50M). For Llama-3.1-8B, QZO FLOPs (7.9×10¹⁶) exceed fine-tuning FLOPs (2.48×10¹⁶) by 3.2×, whereas for OPT-6.7B, QZO uses only 0.4% of fine-tuning FLOPs. The paper provides no explanation for these shifts and does not describe how FLOPs are computed. The claim that QZO uses "about 1% of the FLOPs of MeZO" also varies: 0.008% (OPT-6.7B), 2% (Llama-2-7B), and 7% (Llama-3.1-8B).

### Minor

1. **The "upper-bound" fine-tuning baseline uses SGD rather than AdamW.** Footnote 2 states this is due to budget constraints. While understandable, SGD is known to underperform AdamW for LLM fine-tuning, making this a weaker reference point. The memory profiling chart (Figure 1) includes AdamW (87.6 GB for OPT-6.7B), establishing that the authors know the *actual* upper bound but do not use it for the performance comparison. Additionally, QZO *outperforms* SGD fine-tuning on several metrics (e.g., QZO 85.5 vs SGD 83.7 on SQuAD, Llama-2-7B) — an anomalous result that the paper does not remark on.

2. **The DDC variance-reduction derivation (Eq. 8) contains a subtle error.** The step from line 3 to line 4 of Eq. 8 equates `E[||∇̂_Δ L||]²` with `(∇_Δ L)²`. This is not generally true: by Jensen's inequality, `E[||X||] ≥ ||E[X]||`, with equality only for constant X. The overall conclusion (clipping reduces variance) is still correct — it can be reached via `||E[∇̂'_Δ L]||² ≤ E[||∇̂'_Δ L||]²` — but the derivation as written is slightly sloppy. This should be corrected for clarity.

3. **No comparison with LoRA or QLoRA.** LoRA (Hu et al., 2022) and especially QLoRA (Dettmers et al., 2023) — which combines 4-bit NF4 quantization with low-rank adapters — are the most widely used methods for memory-efficient LLM fine-tuning. QLoRA is cited in the paper's references but never discussed. Since both QZO and QLoRA aim to reduce memory on weights, gradients, and optimizer states, readers need guidance on how QZO's memory-performance trade-off compares.

4. **No wall-clock training time reported.** Table 2 reports FLOPs but never actual runtime. ZO requires 2 forward passes per step with no backward pass, so wall-clock time depends heavily on implementation (e.g., kernel efficiency, memory bandwidth). Reporting actual training time on the 24GB GPU would be informative for practitioners.

5. **The interaction between quantization range and perturbation structure is not discussed.** When Δ is perturbed, the effective perturbation on the de-quantized weights is `(Δ + εz)⊙θ̄ = Δ⊙θ̄ + ε(z⊙θ̄)` — the perturbation on the *actual* weights is scaled by θ̄, not by identity. For int4 weights taking values like {−7,…,7}, this creates a structured perturbation pattern. The paper does not discuss how this affects gradient estimation quality.

### Trivial

- The claim "maximum reduction in memory consumption" (line 36) is overly absolute; QLoRA achieves substantial reductions through a different mechanism.
- C=100 is the default clipping threshold with ablation only on SST-2 with one model. Some guidance on how to set C in practice (e.g., as a percentile of observed d values) would be helpful.

## Nice-to-Haves

- **Analyze how Δ changes during training.** Since QZO only updates quantization scales, showing whether scales systematically increase/decrease and how this correlates with performance would deepen understanding of *how* QZO works.
- **FLOPs computation methodology.** A brief explanation of how FLOPs are counted (which operations are included) would resolve the apparent inconsistencies.
- **Extend DDC threshold ablation to more tasks.** The current ablation (Figure 3) is on one dataset (SST-2) with one model. Showing robustness across tasks would strengthen the claim.

## Removed Points

These points from the input review are removed with justification:

1. **"DDC theory has internal gaps not resolved in the main text"** — Partially removed and demoted to Minor (point 2 above). The reviewer claimed the derivation "does not obviously yield the claimed inequality" and that the step from Eq. 8 to the variance inequality "relies on the squared norm of the true gradient being bounded by the squared norm of the clipped estimate's expectation — a relation that does not follow from the definitions given." This is incorrect: the relation `||E[X]|| ≤ E[||X||]` follows directly from Jensen's inequality for convex norms, making the overall conclusion sound. However, the derivation has a separate minor error (equating `E[||∇̂_Δ L||]²` with `(∇_Δ L)²`), kept in the Minor section.

2. **"The proof of Theorem 1 is relegated to the appendix"** — Removed per the hard rule about parser-stripped appendix content. The appendix exists in the original submission.

3. **"1,000-example training set is very small"** — Removed. This follows MeZO's standard setup; criticizing it here without also criticizing MeZO is inconsistent.

4. **"Different hardware used for fine-tuning (A100) vs QZO (4090)"** — Removed as a confounding concern. The paper acknowledges this openly; it's a budget constraint, not a design flaw.

5. **"Hyperparameters not justified / no sensitivity analysis for lr and ε"** — Removed. These are standard practices in the ZO literature (MeZO uses the same approach); excessive sensitivity analysis is not a requirement.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Run 3–5 seeds for all core experiments and report mean ± std.** This is the single highest-leverage improvement. Without it, the reader cannot distinguish signal from noise in the ZO results.

2. **Add at least one quantized-ZO baseline (Feng et al., Zhou et al., or Bar & Giryes) to the experimental comparison.** The paper claims superiority over these methods in the related work but provides zero experimental evidence.

3. **Clarify how FLOPs are computed and explain the large discrepancies across models** (particularly why QZO FLOPs for OPT-6.7B are ~276× lower than for Llama-2-7B despite similar model size and architecture).

4. **Include QLoRA as a memory-efficient fine-tuning baseline** to help readers situate QZO's performance in the context of standard practice.

5. **Report wall-clock training time** on the 24GB GPU, not just FLOPs.

6. **Correct the minor error in Eq. 8** (the unjustified equality of `E[||∇̂_Δ L||]²` and `(∇_Δ L)²`) and provide a clean derivation using Jensen's inequality.

## Score and Decision

The paper presents a genuinely novel and well-motivated idea — perturbing quantization scales to enable ZO fine-tuning on quantized models. The memory savings are impressive and the method is validated across diverse quantization schemes and model families.

However, the experimental evaluation has significant gaps: the complete absence of variance/uncertainty reporting is particularly concerning for a ZO method, the lack of any experimental comparison against the quantized-ZO baselines cited in the related work leaves core claims unsupported, and the FLOPs numbers contain unexplained inconsistencies. These are addressable issues, but as presented the evidence does not fully support the paper's conclusions.

Score: 6 — borderline accept. The contribution is real but the validation is incomplete.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>