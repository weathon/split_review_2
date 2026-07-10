Now I have all the verification. Let me write the final consolidated review.

---

## Summary

This paper investigates why naive output matching fails in 1-bit post-training quantization of LLMs (Section 3), and proposes a selective hybrid method that applies output alignment (using a corrected "Output Error" objective) to only the last layer per block while using weight alignment (ARB-RC) for the remaining layers, plus an Attention Matrix Preservation (AMP) mechanism. The diagnostic analysis is the paper's strongest contribution, and the method shows consistent perplexity improvements over prior 1-bit PTQ methods on most benchmarks.

## Strengths

- **Strong diagnostic analysis (Section 3):** The paper identifies three concrete, empirically grounded reasons why naive output matching fails in 1-bit PTQ: (i) layer-wise output matching does not guarantee block-level loss reduction (Figure 1), (ii) the Activation-conditioned Error objective diverges from the true Output Error as quantization propagates (Figure 2), and (iii) output matching can distort token-level similarity structure. This goes well beyond a standard "our method works better" narrative and provides real insight into why prior output-alignment approaches underperform.

- **Clean, well-structured ablations:** Table 3 isolates AMP's dramatic contribution (~10 PPL improvement on LLaMA-2-7B), and Table 4 isolates the Output Error vs. Activation-conditioned Error gain (~0.7 PPL). These clearly attribute improvements to specific components.

- **Consistent empirical improvements across most benchmarks:** The method outperforms all prior 1-bit PTQ methods (PB-LLM, BiLLM, ARB-RC, ARB-X) on nearly all dataset-model combinations spanning OPT (1.3B–30B) and LLaMA-2/3 families, with systematic rather than cherry-picked gains.

## Weaknesses

### Fatal
None.

### Major

- **Unclear/incorrect notation in the AMP objective (Eq. 9):** The paper writes $\| (\hat{X}\hat{W}\hat{W}^\top\hat{X}^\top) \odot (XWW^\top X^\top) \| = \text{Tr}[\hat{X}\hat{W}\hat{W}^\top\hat{X}^\top XWW^\top X^\top]$. Under standard definitions, the Frobenius norm of a Hadamard product is $\sqrt{\sum A_{ij}^2 B_{ij}^2}$, while the trace (Frobenius inner product) is $\sum A_{ij} B_{ij}$. These are not equal. The paper must clarify the intended norm and correct the algebra. This is a correctness issue in a central equation.

- **Catastrophic PTB failure on LLaMA-2-7B dismissed rather than analyzed:** The method scores 3166 PPL on PTB (Table 2), while ARB-RC gets 763 and ARB-X gets 681 (FP baseline is 37.91). The paper states "the large perplexity indicates that the metric cannot provide a meaningful evaluation" — yet applies the same metric without caveats to all other models and datasets. This is the worst result among the method's closest competitors, and it deserves investigation rather than dismissal. The credibility of the evaluation is weakened when a clear failure case is sidestepped.

- **Framing overstates the output-alignment contribution relative to the actual hybrid design:** The method applies output alignment to only the last fully connected layer per block (1 of ~4–6 layers) and uses ARB-RC (weight alignment) for all remaining layers. The abstract, introduction, and contribution list frame this as an "output alignment" approach without clearly disclosing that the majority of parameters are quantized via weight alignment. The justification in Section 4.2 (that the last layer has "the most direct impact on the block loss") is asserted without any supporting experiment or ablation.

### Minor

- **AMP masking mechanism (Eq. 10–11) is a heuristic with limited explanation:** The binary sign-based mask blends between the current parameter value and the Output Error closed-form solution, but the paper does not explain why a sign-based (rather than magnitude-based) criterion is appropriate, how the AMP objective and the Output Error objective interact, or what the mask mechanistically achieves beyond an empirical PPL gain.

- **Choice of the last layer for output alignment is unjustified:** No ablation is provided comparing different choices of which layer receives output alignment (e.g., attention output projection vs. FFN first layer vs. last layer vs. all layers), undercutting the claim that the last layer is optimal.

- **No variance reporting:** All results are point estimates without standard deviations or confidence intervals. For settings where gains over ARB-RC are small (e.g., OPT-30B C4: 13.34→13.15, a ~1.4% relative improvement), variance could affect the ranking.

### Trivial
None.

## Nice-to-Haves

- Provide efficiency benchmarks in the main paper (calibration time, inference throughput) to substantiate the "minimal overhead" claim in the abstract; the paper currently defers entirely to Appendix D.
- Analyze the LLaMA-2-7B PTB failure — even a brief diagnostic (e.g., whether the AMP mask saturated, or a numerical instability in the least-squares solve) would strengthen the paper.
- Add an ablation comparing different layer choices for selective output alignment.
- Report confidence intervals for main results.

## Removed Points

These points from the input review are removed or demoted with justification:

1. **"No efficiency measurement whatsoever"** — REMOVED. The paper explicitly references Appendix D for overhead analysis (line 265). The appendix was stripped by the parser; the criticism cannot be verified.
2. **"Every baseline gets a lower value" on PTB LLaMA-2-7B** — REMOVED as factually incorrect: BiLLM scores 5243, which is higher than the method's 3166.
3. **Speculative criticisms about appendix content** — REMOVED as unverifiable.
4. **Criticism about not including LLaMA-1** — REMOVED per policy on questioning release status of cited models.
5. **Criticism about single-layer vs. all-layer quantization experiment in Section 3.1** — REMOVED as a request for a different experiment, not a flaw in the existing one.
6. **Pure speculation about what "could" be wrong with the method** — REMOVED.

## Novel Insights

None beyond the paper's own contributions. The diagnostic analysis in Section 3 is the paper's most novel insight. 

## Suggestions

1. **Fix Eq. 9:** Replace the ambiguous norm-of-Hadamard-product notation with the Frobenius inner product (trace of A^T B) and verify the subsequent algebra.
2. **Add a diagnostic for the PTB failure:** Even a paragraph explaining the mechanism behind the 3166 PPL would significantly improve the paper's credibility.
3. **Clarify framing:** Revise the abstract and introduction to accurately describe the method as a hybrid (weight alignment for most layers, targeted output alignment on the last layer) rather than a pure output-alignment approach.
4. **Ablate layer selection:** Compare output alignment applied to different layers to justify the claim about the last layer.

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>