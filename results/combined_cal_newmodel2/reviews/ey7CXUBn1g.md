Now I have a comprehensive calibration picture. Let me produce the final review.

## Summary

This paper proposes AdaSVD, an SVD-based LLM compression method with two components: (1) **adaComp**, which corrects post-truncation errors by alternately updating the singular matrices using Moore-Penrose pseudoinverse-based least-squares, and (2) **adaCR**, which assigns layer-specific compression ratios based on cosine-similarity importance. Experiments on LLaMA2-7B, OPT-6.7B, Mistral-7B, and Vicuna-7B show consistent perplexity improvements over SVD-LLM, the strongest prior SVD method, across compression ratios of 40%–80%.

## Strengths

- **Consistent improvements over SVD-LLM.** Across compression ratios (40%–80%) and all four tested LLMs, AdaSVD achieves lower perplexity than SVD-LLM. At 60% compression on LLaMA2-7B, the gap is ~40 PPL on WikiText-2 (50.33 vs. 89.90), indicating substantial practical benefit at high compression levels. (favorability=11.54)

- **Clean ablation structure.** Table 3 separates the contributions of adaComp and adaCR clearly. The iteration and mrr ablations provide practical guidance, and the paper honestly reports that 1 iteration is often optimal, acknowledging overfitting with limited calibration data. (favorability=13.21)

- **Compatibility with weight quantization demonstrated.** Table 4 shows AdaSVD+GPTQ consistently outperforms SVD-LLM+GPTQ across all compression ratios, confirming orthogonality to other compression techniques as claimed. (favorability=12.93)

- **Well-motivated problem framing.** The paper correctly identifies two genuine limitations of prior SVD-based LLM compression: the absence of post-truncation residual correction and the use of uniform compression ratios that ignore differential layer importance. (favorability range 6.64–9.99)

## Weaknesses

### Minor

1. **Table 1 data error in the Original reference row.** The Original row in Table 1 shows C4=45.30 and MMLU=7.34. Table 4 shows the same original model with C4=7.34, and standard LLaMA2-7B MMLU is ~45%. The C4 and MMLU values are clearly swapped in Table 1. This error is limited to the reference row — the compressed-model comparisons are internally consistent — but it is a data integrity issue in the main results table that must be corrected. (favorability=5.37)

2. **Framing of adaComp as "alternating update until convergence" overstates what the evidence supports.** Table 3c shows that 1 iteration is best in 5 out of 6 comparisons. Additional iterations consistently hurt or provide only marginal gains. The paper acknowledges overfitting but the method description (Section 3.1, Eq. 16, Figure 2d) presents iterative alternating minimization as the mechanism. What actually works is a single pseudoinverse-based correction step. (favorability=1.00)

3. **Unsupported claim about iterations at high compression ratios.** The paper states that "under higher compression ratios, additional iterations lead to performance improvements" (Section 4.3). However, in Table 3c at 60% compression, 1 iteration outperforms 3 and 15 iterations on both WikiText-2 and C4. This claim is not supported by the data shown in the main paper (the 70% and 80% results are in the supplementary). (favorability=1.52)

4. **VLM evaluation is purely qualitative.** Figure 5 shows only four cherry-picked image captioning examples with no automatic metrics (CIDEr, SPICE, BLEU, METEOR). The paper claims "extensive experiments across multiple LLM/VLM families," but provides no quantitative VLM evidence. This does not meet the evidentiary standard for the VLM contribution claim. (favorability=-2.06)

5. **All experiments on 7B-scale models only.** Testing is limited to LLaMA2-7B, OPT-6.7B, Mistral-7B, and Vicuna-7B. The paper motivates SVD compression for "resource-constrained devices such as smartphones and IoT devices," where compressing larger models (13B+) would have greater practical impact. While Figure 4 includes LLaMA-13B in the importance visualization, no compression results are reported for larger models. (favorability=4.52)

6. **Percentages in Table 1 AdaSVD rows are unexplained.** Values like "14.76 (18%)", "304.62 (158%)" appear in parentheses but are never defined in the text or table caption. They do not clearly correspond to relative improvement over any baseline, making them confusing. (favorability=4.12)

7. **adaCR normalization creates coupling that is not discussed.** Equation (18) normalizes layer importance by the mean across layers, so changing one layer's compression ratio affects the normalization for all others. The paper does not discuss whether this assignment converges to a fixed point or how sensitive results are to this interdependence. (favorability=4.95)

8. **Stack-of-batch bucket size not reported.** The bucket size M is a key hyperparameter (Algorithm 1) but its value and sensitivity are not reported. The paper only states that 32 samples barely fit on an 80GB GPU. (favorability=3.89)

### Trivial

None.

## Nice-to-Haves

- Report computational cost comparison (runtime) between AdaSVD and SVD-LLM, since the pseudoinverse adds overhead.
- Add at least one automatic captioning metric for the VLM experiment.
- Demonstrate results on a 13B or larger model to strengthen the generalization and practical motivation claims.
- Report variance or multiple seeds for perplexity measurements, especially where gaps between methods are small.
- Provide deeper analysis of why more iterations overfit (e.g., calibration set size, eigenvalue properties of the update).

## Removed Points

- **Parser artifact (Figure 1 table):** Lines 19-25 show all values ~1.1–1.2 from an embedded image; this is a PDF extraction error, not an author error. Removed per hard rule.
- **"Stack-of-batch is standard batch averaging":** The paper presents this as a practical engineering trick under memory constraints, not a primary contribution. The criticism overstates the issue. Removed.
- **Performance gap remains large at 80%:** The claim that AdaSVD "narrows the performance gap" is comparative (vs. SVD-LLM: 372→206 PPL), not absolute. Removed as misreading the comparative framing.
- **No statistical significance:** Single-run evaluation is standard for this setting. Removed as applying standards not typical for the field.
- **Practical deployability at high PPL:** Goes beyond the paper's scope of improving over baselines. Removed.
- **"Alternating update" section-by-section note:** Already addressed by the kept weakness #2 above; redundant.

## Novel Insights

None beyond the paper's own contributions. The reviews do not surface a novel perspective that the paper itself does not articulate.

## Suggestions

1. **Fix Table 1:** Correct the C4 and MMLU values in the Original row to match Table 4.
2. **Reframe adaComp:** Acknowledge that a single correction step is empirically optimal, and present the iterative framing as a generalization that is typically unnecessary with limited calibration data.
3. **Correct the iteration claim:** Revise the statement that "additional iterations lead to performance improvements at higher compression ratios" unless the supplementary results clearly support it.
4. **Define the parenthetical percentages** in Table 1's AdaSVD rows.
5. **Report the bucket size M** used in stack-of-batch and the sensitivity of results to this choice.
6. **Add quantitative VLM metrics** or remove the VLM claim from the contributions.

## Score and Decision

**Calibration anchors (all rounds):**

| Anchor | Path | Avg Score | Round | Itemized | Comparison to AdaSVD |
|--------|------|-----------|-------|----------|----------------------|
| ASVD | HyPofygOCT.md | 6.25 (Reject) | 1 | Yes | More pioneering SVD compression work; AdaSVD is less novel |
| Basis Sharing | gp32jvUquq.md | 6.50 (Accept) | 1 | Yes | More novel concept (cross-layer sharing); AdaSVD is simpler/incremental |
| Low-Rank Correction (Quant) | FA3iYp1y6z.md | 5.00 (Reject) | 2 | Yes | Similar contribution level; fewer presentation issues |
| MoE-SVD | ho7ZUS1z8A.md | 5.00 (Reject) | 1 | Yes | Focused on MoE; comparable contribution magnitude |
| Targeted Low-Rank Refinement | s6Q7aVZWIn.md | 4.50 (Reject) | 3 | Yes | Similar idea (correct compression errors with low-rank); comparable quality |
| AutoTrunc | 3KEwJGYNzH.md | 4.00 (Reject) | 1 | Yes | Weaker methodology and experiments |
| LLM-Codebook | nMbWsXPUVL.md | 4.75 (Reject) | 2 | No | Different approach (codebook); similar score band |

**Round 1 bracket:** The most relevant anchors (ASVD at 6.25, Basis Sharing at 6.50, AutoTrunc at 4.00, MoE-SVD at 5.00) suggest this paper sits between 4.0 and 6.5. The paper is clearly stronger than AutoTrunc (4.00) but weaker than ASVD (6.25) — ASVD was more pioneering and had a cleaner data presentation.

**Round 2 narrowing:** Low-Rank Correction for Quantized LLMs (5.00) and Targeted Low-Rank Refinement (4.50) are the closest analogues in contribution type (post-compression error correction). AdaSVD has a cleaner ablation structure than Targeted Low-Rank Refinement but has a data error in Table 1 that neither comparison paper has. Comparing favorability: AdaSVD's most negative weakness items (VLM evaluation at -2.06, iteration framing at 1.00, unsupported claim at 1.52) are comparable in magnitude to the most negative items in Low-Rank Correction (-4.20 for limited novelty) and Targeted Low-Rank Refinement (-5.08 for insufficient novelty). AdaSVD's strengths have higher favorability (13.21 for ablation) than either anchor's highest strengths. The balance places AdaSVD at the lower end of the 4.5–5.0 range.

**Final calibration:** AdaSVD is a solid incremental contribution to SVD-based LLM compression with clean experiments and consistent results, but the Table 1 data error, the mismatch between the iterative framing and the single-step evidence, and the qualitative-only VLM evaluation prevent it from reaching the acceptance threshold. The paper is comparable to Low-Rank Correction for Quantized LLMs (5.00) and Targeted Low-Rank Refinement (4.50), both of which were rejected.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>