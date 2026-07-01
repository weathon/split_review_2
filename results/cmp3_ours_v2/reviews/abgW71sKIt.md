## Summary

This paper investigates why output-matching (activation-conditioned error) underperforms weight-matching in 1-bit LLM post-training quantization. The authors identify three issues: (1) layer-wise output alignment doesn't guarantee block-level loss reduction, (2) quantization errors accumulate causing objective drift, and (3) token similarity matrices degrade. They propose a selective layer-wise output alignment strategy that applies output-matching only to the last FC layer of each block, uses the full-precision input as target (Output Error instead of Activation-conditioned Error), and introduces an Attention Matrix Preservation (AMP) mechanism. Experiments on OPT (1.3B–30B) and LLaMA-2/3 (7B–13B) show consistent improvements over prior 1-bit PTQ methods.

## Strengths

- **Well-motivated diagnostic analysis (Section 3).** The paper systematically demonstrates three concrete failure modes of naive output alignment for 1-bit LLM quantization: block-level loss not improving despite layer-level improvement (Fig. 1), error accumulation causing objective drift (Fig. 2, top), and degradation of token similarity matrices (Fig. 2, bottom). This analysis is the strongest contribution and correctly motivates the proposed design.

- **Clean ablation studies (Tables 3, 4).** The ablation on Output Error vs. Activation-conditioned Error (Table 4) and the AMP mechanism (Table 3) directly validate each of the two proposed components. The finding that AMP is far more critical for LLaMA (PPL drop from 29.12→19.25 on C4) than for OPT (16.35→16.22) is informative and supports the paper's narrative about architecture-dependent sensitivity.

- **Broad model coverage.** Experiments span OPT (1.3B–30B), LLaMA-2 (7B, 13B), and LLaMA-3 (8B), providing reasonable evidence that the method does not overfit to a single architecture or scale.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Notational gap in AMP derivation (Eq. 9).** The first line of Eq. 9 writes `|| (X̂ŴŴ^TX̂^T) ⊙ (XWW^TX^T) ||` and substitutes in line 2 with `Tr[X̂ŴŴ^TX̂^T XWW^TX^T]`. Under the Frobenius norm (used elsewhere in the paper), the norm of a Hadamard product does not simplify to the trace of the matrix product. The intended objective—maximizing the Frobenius inner product Tr[AB] between two token similarity matrices—is clearly sensible and is unambiguously specified from line 2 onward. However, line 1 is notationally incorrect/inconsistent with the rest of the paper and should be fixed. This does not undermine the method itself.

- **Selective layer strategy is under-justified (Section 4.2).** The paper restricts output alignment to "only the last fully connected layer of each block" with a one-sentence justification ("since it has the most direct impact on the block loss"). Given that the paper's own diagnostic analysis (Section 3.1, Fig. 1) shows that different layers within a block respond differently to output vs. weight alignment, a principled justification or ablation for this specific choice would significantly strengthen the paper. The claim is plausible but unsubstantiated.

- **PTB result caveat could be clearer.** On LLaMA-2-7B evaluated on PTB, the proposed method achieves PPL 3166 vs. PB-LLM's 657.24. The paper notes "the large perplexity indicates that the metric cannot provide a meaningful evaluation." This caveat is reasonable (PTB is a poor fit for LLaMA models), but it appears immediately after this unfavorable result and is not repeated where PTB results favor the proposed method (e.g., LLaMA-3-8B). The caveat should either be stated as a general note wherever PTB results are reported, or applied symmetrically.

### Trivial

- The paper categorizes its method as "Output Alignment (OA)" in Tables 1 and 2. Since output alignment is applied to only one layer per block and weight alignment to all others, this is a hybrid approach. The categorization is defensible but could be clearer.

- The headline "up to 4.85 and 3.42 reductions in perplexity" does not specify which baseline or dataset. (These are improvements over ARB-RC on PTB—the strongest baseline, not the weakest—so the concern is about clarity, not honesty.)

## Nice-to-Haves

- A brief runtime/memory overhead summary in the main paper (currently deferred to appendix).
- Variance or confidence intervals for the main results, given modest margins over ARB-RC.
- Direct testing of the RMSNorm hypothesis for LLaMA's AMP sensitivity (presented as speculation in the text).

## Removed Points

These points are flagged for removal; treat them with caution:

- **"AMP derivation is structurally flawed / fatally undermines the method"** — The intended objective (maximizing Tr[AB], the Frobenius inner product of two token similarity matrices) is unambiguously clear from lines 2–4 of Eq. 9 onward. The issue is a notational error in line 1, not a mathematical error in the method itself. Downgraded from "structural/fatal" to minor notational cleanup.

- **"Headline numbers are selectively reported against the weakest baseline"** — The critic claimed the 4.85/3.42 improvements are "computed relative to ARB-X (PPL 47.60 → 24.69 for OPT-1.3B on C4)." This is factually incorrect: 4.85 = 43.03 − 38.18 (ARB-RC→Ours on OPT-1.3B PTB), and ARB-RC is the strongest baseline, not the weakest. The critic's own arithmetic (47.60−24.69=22.91) does not match 4.85. Removed entirely.

- **"Selective dismissal of PTB results damages confidence in evenhandedness"** — The paper makes a single general statement about PTB being a poor metric for LLaMA models, which applies symmetrically to all methods. The concern about asymmetric presentation is genuine but minor; downgraded and merged into the Minor weakness above.

- **General concerns about missing variance estimates, overhead deferred to appendix, and untested RMSNorm hypothesis** — These are generic or speculative concerns; moved to Nice-to-Haves.

- **"Broader model coverage" as a strength** — Kept but trimmed; it is valid but somewhat generic.

## Novel Insights

None beyond the paper's own contributions. The reviews surface no genuinely novel observation that the paper itself does not already articulate.

## Suggestions

1. **Fix the notation in Eq. 9.** Replace line 1 with the Frobenius inner product (or trace objective) directly, removing the problematic Hadamard-product-to-trace simplification.
2. **Ablate the selective-layer choice.** Use the diagnostic methodology already available (Fig. 1) to show that the last FC layer indeed has the largest gain from switching from weight alignment to output alignment. If confirmed, state it explicitly; if not, revise the selection rule.
3. **Add a blanket note on PTB limitations** wherever PTB results appear, rather than only near the one unfavorable result.
4. **Specify the baseline and dataset** when reporting headline improvement numbers in the abstract and results section.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>