## Summary

This paper studies 1-bit post-training quantization (PTQ) for LLMs. It first diagnoses **why** naive output alignment fails in this setting, identifying three problems: (i) layer-wise output matching does not guarantee block-level loss reduction, (ii) quantization errors accumulate across layers, and (iii) indiscriminate output matching can disrupt token interactions (attention). Based on this analysis, the paper proposes three targeted modifications: (a) restricting output alignment to the last fully-connected layer per block (selective-layer design), (b) switching from Activation-conditioned Error to Output Error to account for accumulated errors, and (c) an Attention Matrix Preservation (AMP) masking mechanism. Experiments on OPT (1.3B–30B), LLaMA-2 (7B/13B), and LLaMA-3 (8B) show consistent perplexity improvements over ARB-RC, ARB-X, BiLLM, and PB-LLM.

## Strengths

1. **Well-motivated preliminary analysis (Section 3).** The diagnostic work is the paper's strongest contribution. The demonstration that ARB-X can reduce layer-level loss while increasing block-level loss (Figure 1) and that Activation-conditioned Error stays low while Output Error grows with depth (Figure 2) cleanly isolates why naive output matching fails. This analysis is concrete, non-obvious, and stands as a genuine contribution independent of the method's novelty.

2. **The AMP ablation is decisive for LLaMA.** Table 3 shows removing AMP collapses LLaMA-2-7B from 19.25 to 29.12 PPL on C4 (a ~10-point degradation). The paper offers a testable hypothesis (RMSNorm vs. LayerNorm sensitivity) for why AMP matters more for LLaMA than for OPT.

3. **Consistent perplexity improvements over strong 1-bit baselines across model families and sizes.** On C4, WikiText2, and PTB, the proposed method outperforms ARB-RC, ARB-X, BiLLM, and PB-LLM on every OPT model size (1.3B–30B) and on most LLaMA evaluations. The gains are directionally consistent across 8 model sizes and 3 datasets, which is non-trivial for 1-bit quantization.

## Weaknesses

### Fatal

None.

### Major

1. **The LLaMA-2-7B / PTB failure case is dismissed without analysis.** On PTB (Table 2), the proposed method yields PPL 3166, compared to ARB-RC (763.19), ARB-X (681.24), and PB-LLM (657.24). The paper states: "However, the large perplexity indicates that the metric cannot provide a meaningful evaluation." This is not an adequate explanation. If the metric is uninformative for all methods, the gap between ARB-RC (763) and the proposed method (3166) would not exist. The same metric produces reasonable rankings for LLaMA-2-13B (Ours: 196.64 vs. ARB-RC: 197.70) and LLaMA-3-8B (Ours: 45.66 vs. ARB-RC: 47.88), so the metric is clearly not universally broken. The paper owes the reader an analysis of what causes this specific degradation — whether it reveals a systematic vulnerability of the selective-layer design or the AMP mechanism on certain architecture/distribution combinations.

2. **No statistical significance or variance reporting for any result.** This is especially problematic for the zero-shot QA results, where the improvements over ARB-RC are frequently <1 percentage point (e.g., OPT-13B: 55.06 vs. 55.01, a 0.05% difference; OPT-30B: 57.70 vs. 57.11, a 0.59% difference). Zero-shot QA accuracy on these benchmarks can vary by 1–2% depending on prompt formatting, decoding parameters, or calibration data seed, so these differences cannot be interpreted as reliable evidence of improvement without variance estimates. Even for the perplexity results, which show larger gaps, standard reporting practice (mean ± std over multiple calibration seeds) would substantially strengthen credibility.

### Minor

3. **The selective-layer design is stated as fact without experimental justification.** The paper restricts output alignment to "only the last fully connected layer of each block" (Section 4.2) but provides no ablation comparing this choice against alternatives (e.g., all layers, only the first layer, only attention layers, or a sweep-determined layer). This design choice is central to the method's thesis that indiscriminate output alignment is harmful, yet the reader cannot assess whether the specific choice matters or whether any single-layer-per-block configuration would work similarly.

4. **The AMP derivation (Equations 9–11) has notational and logical gaps.** (a) The objective starts as ‖A ⊙ B‖ (Frobenius norm of element-wise product) but the next line equates it to Tr[AB]; the Frobenius norm of an element-wise product is *not* equal to the trace of the matrix product — the paper appears to intend an inner product ⟨A, B⟩ = Tr(AᵀB), but the notation conflates norm and inner product. (b) The `sign()` function in Equation (10) returns values in {-1, 0, 1} by standard convention, but the update rule in Equation (11) treats it as a {0, 1} selector mask; the paper never specifies the intended behavior or what happens when sign returns -1 (which would produce an implausible update). These are fixable but should be clarified.

5. **The relationship to ARB-RC's closed-form solutions could be clearer.** The paper states "We following a similar strategy in ARB-RC (Li et al., 2024) to parameterize the quantized model weight" (line 100), but Equations (4)–(8) present closed-form updates for α_c, B, and α_r without explicitly marking which derivation steps are novel (due to the modified objective with S = X̂ᵀX rather than Ŝ = X̂ᵀX̂) and which are directly inherited. A dedicated paragraph stating "Our closed-form solutions for α_c, B, and α_r follow the same strategy as ARB-RC but with a modified objective" would eliminate ambiguity.

6. **The AMP benefit for OPT is marginal and not discussed as an architecture-dependent finding.** Table 3 shows AMP improves OPT-6.7B by only 0.13 PPL on C4 (16.35 → 16.22). The paper acknowledges this indirectly but frames the result uniformly as "model performance degrades for both OPT and LLaMA models without AMP," which understates the near-negligible effect on OPT. Acknowledging that AMP is primarily beneficial for LLaMA and providing the RMSNorm hypothesis as the primary (rather than a speculative) explanation would be more accurate.

7. **PB-LLM's higher bit-width (1.7 vs. 1.11/1.06 bits) is not acknowledged.** PB-LLM uses substantially more bits than all other methods in every comparison. Since the paper's method outperforms PB-LLM despite using fewer bits, this asymmetry favors the baseline and is actually a *favorable* result for the paper, but it should be explicitly noted for fairness in presentation.

8. **No efficiency or latency benchmarks in the main text.** The abstract claims "minimal overhead," but no quantitative efficiency data (optimization time, memory footprint during calibration, inference latency, throughput) appears in the main paper. The overhead analysis is deferred to Appendix D (which is standard for the camera-ready but should be summarized in the main text or the claim should be qualified).

### Trivial

None that are not parser artifacts or already covered above.

## Nice-to-Haves

- An ablation comparing different per-block layer choices for output alignment (first layer, last layer, attention layers, all layers) would validate the selective-layer design decision.
- A cleaner ablation isolating the Output Error objective from the selective-layer design: within a single-layer-per-block setting, compare ARB-X's Activation-conditioned Error vs. Output Error while holding everything else fixed.
- A direct visualization of token similarity matrices (as in Appendix Figure 3) for ARB-X vs. the proposed method with and without AMP, demonstrating that AMP specifically recovers the similarity structure.

## Removed Points

The following points from the input review are removed (with justification):

- **"Equation (2) is identically zero"** — This is a parser/formatting artifact (the PDF extraction dropped a hat diacritic). The original submission does not have this issue. Removed per Hard Rule on formatting artifacts.
- **"Novelty is incremental / contribution feels significantly smaller than framing"** — While the relationship with ARB-RC could be clearer (kept as Minor #5), the reviewer's broader claim that the contributions are "not individually large in scope" is a subjective judgment that conflates the method's simplicity with a lack of novelty. The paper's core contribution is the *diagnosis-to-fix* chain, which is well-articulated and supported. A simple fix for a correctly diagnosed problem is a feature, not a weakness. Removed as a strawman characterization.
- **"The preliminary analysis should compare block-level loss under both the proposed method and ARB-X"** — The preliminary analysis is specifically designed to diagnose *why* existing methods fail, not to benchmark the proposed method. The proposed method's advantages are evaluated in the experimental section. This is a scope-expansion request. Removed.
- **"No inference speed or memory benchmark weakens practical value"** — The overhead analysis is in Appendix D (stripped by the parser). The paper's core contribution is algorithmic; efficiency benchmarks are appropriate for the appendix. Removed as a nice-to-have that exceeds the paper's stated scope.
- **"Missing related works"** — Per Hard Rule, we cannot verify missing related works as we lack external sources.
- **"The comparison is fair... PB-LLM bit-width difference"** — Actually kept as Minor #7 since it's a valid observation about presentation fairness, just downgraded from the critic's framing.
- **"The AMP ablation confounds the effect with the selective-layer design"** — The ablation in Table 4 compares Act. Error vs. Out. Error within the full pipeline; a cleaner isolation would be nice but the current design is still informative. Moved to Nice-to-Haves.

## Novel Insights

The most novel observation from the review process is the asymmetry in how the three proposed fixes interact with different architectures: AMP provides a ~10 PPL gain for LLaMA but only ~0.13 for OPT, while the Output Error objective provides comparable benefits for both. This suggests that LLaMA's RMSNorm (which normalizes per-token to unit norm before scaling) makes it disproportionately vulnerable to quantization-induced disruption of token-level similarity structure — a finding that could inform architecture-specific quantization design beyond this paper. The review also surfaces that the selective-layer design choice (last FC layer per block) is the least-justified component; if the paper could show that this choice matters and why, it would substantially tighten the causal chain from diagnosis to fix.

## Suggestions

1. Add an analysis section explaining the LLaMA-2-7B PTB failure — is it a distribution shift issue, insufficient calibration data for that specific dataset, or a systematic vulnerability? This is the single most important addition.
2. Report mean ± std over at least 3 calibration seeds for the main results, or at minimum acknowledge the absence of variance reporting as a limitation.
3. Add a brief ablation or justification for why the last FC layer per block is the correct layer for output alignment.
4. Clarify the AMP derivation: specify the norm/inner-product convention, and state whether `sign()` is treated as {0, 1} or {-1, 0, 1} and how negative values are handled.
5. Include a short "Relation to ARB-RC" paragraph that explicitly states which derivations are inherited and which are novel due to the modified objective.

## Score and Decision

The paper makes a genuine contribution through its diagnostic analysis (Section 3), and the proposed method yields consistent perplexity improvements. The weaknesses are real but addressable: the PTB failure needs analysis (not dismissal), and variance reporting is needed for the QA results. The paper is above the acceptance threshold but requires these clarifications.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>