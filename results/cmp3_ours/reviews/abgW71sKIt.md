**Final Calibration:**

Round 1 bracket: [5.5, 7.5]. Narrowing against direct-competitor anchors: STBLLM (6.00, sub-1-bit LLM quantization, accepted despite novelty concerns), PB-LLM (6.75, 1-bit LLM quantization, accepted with limited evaluation concerns), OmniQuant (6.40, LLM quantization, accepted with limited novelty concerns). Our paper sits between these bounds — its diagnostic analysis is more novel than any of these anchors, and its evaluation is more comprehensive, but the unexplained PTB failure case (4× degradation vs ARB-RC on LLaMA-2-7B) is a genuine evidential gap that prevents it from reaching the 6.5–7.5 range. Final score: 6.0 (borderline accept).

---

## Summary

This paper diagnoses three failure modes of naive output alignment in 1-bit post-training quantization (PTQ) for LLMs, and proposes a selective layer-wise method with three components: (1) using Output Error (matching full-precision targets) instead of Activation-conditioned Error, (2) selectively applying output alignment only to the last layer of each block, and (3) Attention Matrix Preservation (AMP), a masking mechanism that preserves token-similarity structure during quantization. Experiments on OPT (1.3B–30B) and LLaMA-2/3 models show consistent perplexity improvements over prior 1-bit PTQ methods across most benchmarks.

## Strengths

- **Section 3's diagnostic analysis is genuinely informative and specific.** The paper identifies three distinct, measurable failure modes of naive output alignment in 1-bit PTQ: (i) layer-wise matching does not guarantee block-level loss reduction (Section 3.1, Figure 1), (ii) quantization errors accumulate across layers causing the optimization target to drift (Section 3.2, Figure 2), and (iii) output alignment can distort token-level similarity structure, degrading attention mechanisms (Section 3.3). This goes beyond the generic "error accumulation" observations common in prior quantization work and provides a principled motivation for the proposed method.

- **AMP (Attention Matrix Preservation) is a novel mechanism with strong empirical support.** The idea of preserving the token-similarity matrix during quantization (Eq. 9–11) is directly motivated by the paper's own diagnostic analysis. The ablation (Table 3) is compelling: removing AMP degrades perplexity from 19.25 to 29.12 on LLaMA-2-7B (~50% relative increase), while the effect on OPT-6.7B is smaller (16.22→16.35), consistent with the paper's architectural explanation (RMSNorm vs LayerNorm sensitivity). This differential behavior cleanly validates the mechanism's purpose.

- **Consistent improvements over prior methods across most benchmarks.** The method outperforms ARB-RC (the strongest baseline) on nearly all metrics in Tables 1 and 2. Gains are particularly notable on smaller OPT models (up to ~4.85 PPL reduction on OPT-1.3B C4 vs ARB-RC). The zero-shot QA results (AveQA in Table 1) also show consistent improvements, and the method uses the same 1.11-bit budget as ARB-RC.

## Weaknesses

### Fatal
None.

### Major
- **Unexplained catastrophic failure on PTB with LLaMA-2-7B.** On LLaMA-2-7B evaluated on PTB (Table 2), the proposed method achieves perplexity 3166 compared to ARB-RC's 763.19 and ARB-X's 681.24 — roughly a 4× degradation over the strongest baseline. The paper's dismissal ("However, the large perplexity indicates that the metric cannot provide a meaningful evaluation") is insufficient. If PTB is unreliable for the proposed method at 3166, the same logic applies to ARB-RC at 763 and ARB-X at 681, yet those numbers are reported without similar caveats. On LLaMA-2-13B PTB the method roughly matches ARB-RC (196.64 vs 197.70), so the issue appears specific to LLaMA-2-7B. The paper must either explain why the method catastrophically degrades on this specific model+dataset combination, or present a principled reason to exclude PTB from evaluation entirely. This directly undercuts the "consistently outperforms" claim and is the most significant weakness.

### Minor
- **Mathematical imprecision in Eq. (9).** The paper writes `max || (X̂ŴŴ^T X̂^T) ⊙ (XWW^T X^T) || = Tr[ X̂ŴŴ^T X̂^T XWW^T X^T ]`. The Frobenius norm of the Hadamard product is ||A ⊙ B||_F = sqrt(Σ(A_ij B_ij)²), which is not equivalent to Tr[AB] = Σ A_ij B_ij (the Frobenius inner product). The paper likely intends the latter (maximizing alignment between two similarity matrices) and the subsequent derivation to Tr[Ŵ^T M Ŵ] is valid, but the notation as written is mathematically incorrect and must be corrected before publication.

- **Selective layer choice ("last layer only") is asserted without evidence.** Section 4.2 restricts output alignment to "only the last fully connected layer of each block" because it "has the most direct impact on the block loss." This heuristic lacks experimental support. Section 3.1 shows that some layers benefit from output alignment over weight alignment and others do not, but provides no analysis of whether the beneficial layers systematically correspond to the last layer, nor does it compare against alternatives (all layers, first layer only, data-driven selection).

- **AMP's hard binarization and conflicting objectives are not discussed.** The AMP masks (Eq. 10) are computed as `sign(gradient)`, yielding values ±1. When the mask is -1, the update (Eq. 11) becomes `α_r = 2α_r - α_r^*`, which does not simply "preserve" the original value. The paper does not discuss whether softer masking (e.g., magnitude-based) would lead to more stable convergence. Additionally, the AMP objective (maximized) and the reconstruction loss (minimized, Eq. 3) could conflict — this trade-off is not addressed.

- **AveQA reported only as an aggregate.** The zero-shot QA evaluation (Table 1) averages accuracy over 7 datasets without per-dataset breakdown in the main text, which could hide variance across tasks.

### Trivial
None.

## Nice-to-Haves
- **Variance reporting.** Most gains over ARB-RC are modest (0.2–1.0 PPL), and calibration data is sampled. Reporting results across multiple calibration seeds or providing confidence intervals would strengthen the empirical claims, though single-run evaluation is standard in PTQ papers.
- **Computational overhead summary.** The paper defers overhead analysis to Appendix D (stripped by parser). A brief quantitative summary in the main text (quantization time, peak memory, inference throughput vs. ARB-RC) would improve practical transparency.
- **Ablation isolating the selective strategy from the Output Error.** Table 4 shows that Output Error helps within the selective framework, but does not isolate whether the selective strategy or the Output Error contributes more.

## Removed Points
These points are flagged to be removed; treat them with caution:
- "Section 3.1 comparison would be more informative if it also showed whether the proposed method's selective approach improves upon both" — removed as a suggestion for additional experiments, not a weakness of the existing work.
- "The paper's framing that existing methods are 'weight-centric' is slightly overstated" — removed as a framing nitpick that does not affect the technical contribution.
- "Eq. (2) has identical terms on both sides of minus sign (parser artifact)" — correctly identified by the critic as a parser artifact, not an author error.
- "Table 4 conflates two variables" — removed because the ablation cleanly isolates the objective change (Output Error vs. Activation-conditioned Error) within the same framework; the conflation claim is unwarranted.
- "Computational overhead not reported in main text" — moved to Nice-to-Haves per rule: the appendix (stripped by parser) exists and contains this analysis; the concern is about presentation placement.
- "The relative ranking (ARB-RC < Ours < BiLLM) contradicts the headline claim" — the ranking is factually correct from Table 2, but the BiLLM comparison is irrelevant because BiLLM performs even worse (5243). The core concern (Ours is worse than ARB-RC) is already captured in the Major weakness above.

## Novel Insights
Beyond the paper's own contributions, the most valuable observation is the severity of the PTB failure case on LLaMA-2-7B. The paper acknowledges the exception but offers no diagnostic analysis, leaving a 4× degradation over ARB-RC effectively dismissed. This is a genuine evidential gap: the paper claims "consistently outperforms" but this single model-dataset pairing presents a stark counterexample that remains unexplained and unanalyzed. The notation issue in Eq. (9) — conflating the Frobenius norm of a Hadamard product with the Frobenius inner product — is also a correct mathematical observation, though the underlying method is likely salvageable with corrected notation.

## Suggestions
1. Fix Eq. (9): replace the norm of the Hadamard product with the Frobenius inner product (Tr[AB]) and explicitly state which norm is being used throughout. The subsequent derivation is valid under the corrected interpretation.
2. Investigate the PTB failure on LLaMA-2-7B: run diagnostics to determine whether the selective strategy, AMP over-correction, or the Output Error objective causes the 4× degradation vs. ARB-RC. Either fix the issue or provide a principled criterion for excluding this result.
3. Justify the "last layer only" heuristic with an ablation comparing alternative selection strategies (all layers, first layer only, data-driven selection based on the Section 3.1 diagnostic).
4. Add per-dataset breakdowns for zero-shot QA results and variance estimates across calibration seeds for at least the main perplexity comparisons.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>