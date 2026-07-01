## Summary

This paper formalizes the problem of identifying critical KV cache entries for LLM inference from an output perturbation perspective. The authors derive an upper bound on the attention-output perturbation (Theorem 3.3), showing that both attention weights and value states projected through the output matrix \(W^O\) matter. They propose a two-stage selection algorithm that can be integrated as a plug-and-play enhancement to existing cache eviction methods (SnapKV, AdaKV, HeadKV). Evaluated on 29 datasets across 3 LLMs (7B–32B), the method consistently reduces quality loss, often substantially, with negligible computational overhead (~0.06s TTFT increase at 32K context).

## Strengths

1. **Formal framing of critical cache identification.** The paper is the first to formulate this as minimizing output perturbation (Definition 3.1) and to derive an upper bound that reveals the role of projected value states \(VW^O\). This goes beyond the heuristic attention-weight-only selection in prior work (H2O, SnapKV, AdaKV) and provides a principled justification for why value-side information matters.

2. **Consistent and substantial empirical improvements.** Across 29 datasets, 3 models, 3 base methods, and multiple cache budgets, the "w/ Ours" variant nearly always outperforms the base method. Many improvements are large — e.g., AdaKV's Ruler average on Mistral-7B goes from 34.88 to 69.17 at 40% cache (Table 1). The 97.8% success rate across 90 long-dependency test cases (Section 4.3) is compelling.

3. **Negligible computational overhead.** The only added computation is \(VW^O\) and elementwise operations. The efficiency evaluation (Section 4.6, Figure 3) shows a TTFT increase of ~0.06s for batch-1 at 32K context, with no decoding latency increase. This makes the method practically usable.

4. **Perturbation analysis closes the loop.** The paper directly measures that the algorithm reduces the actual attention-output perturbation (Figures 4–6), providing internal evidence that the theoretical motivation translates into observable reductions. Over 92% of attention heads in Llama-3.1-8B show reduced perturbation.

## Weaknesses

### Fatal
None.

### Major

1. **Mismatch between Algorithm 1's pseudocode and the theoretical/textual description.** The paper's claimed formal grounding rests on a two-stage algorithm where stage 1 selects by attention weights (so Assumption 3.4 applies: cumulative attention weight \(\sigma > 0.5\)) and stage 2 selects by a composite score. The text (Section 3.4, line 126–127) and Assumption 3.4 explicitly describe stage 1 as prioritizing entries with high attention weights. Theorem 3.5's derivation depends on this premise.

   However, Algorithm 1's pseudocode (lines 5 and 8) appears to use the **same composite score** \(\mathcal{A} = (A+\varepsilon) \odot \|VW^O\|_1\) for both stages:
   - Line 5: stage 1 selects entries where \(\mathcal{A}_i \in \text{Top}_k(\mathcal{A}, b')\) [ambiguously written as \(A_i \in \text{Top}_k(\mathcal{A}, b')\)]
   - Line 8: stage 2 selects entries where \(\mathcal{A}_i \in \text{Top}_k(\mathcal{A}, b'')\)

   If both stages use the same criterion \(\mathcal{A}\), then: (a) Assumption 3.4 (which requires selection by attention weight \(A\)) does not apply, and (b) the two-stage decomposition is vacuous — selecting top \(b'\) by \(\mathcal{A}\) then top \(b''\) from the remainder is equivalent to selecting top \(b\) by \(\mathcal{A}\) in a single pass. The paper must clarify whether the actual implementation matches the text (stage 1 = attention weights, stage 2 = composite score) or the pseudocode (both stages = composite score), and align the theory and algorithm accordingly. This is a **real inconsistency** that undermines the paper's claimed formal contribution as currently presented. [Evidence: Algorithm 1 lines 5, 8; Section 3.4 lines 126–127; Assumption 3.4; Theorem 3.5]

### Minor

1. **\(\alpha\) inconsistency.** Algorithm 1's input specifies \(\alpha = 0.25\) as default, but all experiments use \(\alpha = 0.5\) (Section 4.1, line 200) and the sensitivity analysis (Table 4) tests \(\{0.0, 0.3, 0.5, 0.7\}\) without including 0.25. This needs to be corrected to avoid confusion. [Evidence: Algorithm 1 line 132; Section 4.1 line 200; Table 4]

2. **"More than half" claim masks considerable per-configuration variation.** The claim (abstract, Figure 1 caption) that the algorithm "reduces the compression loss by more than half on average" is technically true (average relative reduction ~62% on Ruler), but individual improvements vary widely — from ~20% (SnapKV on Mistral Ruler: 58.92%→46.90%) to ~97% (AdaKV on Qwen Ruler: 24.30%→0.69%). Reporting the distribution of reductions alongside the average would give readers a more accurate picture. [Evidence: Figure 1 data]

3. **No error bars or variance estimates.** None of the main tables report confidence intervals, standard deviations, or significance tests. For the smaller improvements (e.g., LongBench gains of 1–2 points in some domains), it is unclear whether these differences are statistically meaningful. [Evidence: Tables 1, 2, 3, 4]

4. **SCBench Retr.KV improvements are marginal.** The gains on the Retr.KV task are 0.4–0.8 points across all three cache budgets (Table 3), which is well within typical noise ranges. The paper should acknowledge this limitation rather than grouping it with the more substantial gains on EN.QA and Math.Find. [Evidence: Table 3, Retr.KV row]

5. **Equation (2) uses \(\sqrt{d}\) instead of \(\sqrt{d_h}\).** The softmax temperature in the per-head attention equation should use the head dimension \(d_h\), not the model dimension \(d\). The keys are \(d_h\)-dimensional, so the dot products have variance proportional to \(d_h\). This is a minor mathematical imprecision. [Evidence: Equation (2), line 84]

### Trivial

- The small epsilon (\(\varepsilon = 10^{-4}\)) added to attention weights in Algorithm 1 line 3 is noted in a footnote but its effect is not analyzed. If \(\varepsilon\) is non-negligible relative to small attention weights, it could change the effective selection criterion, especially at low cache budgets.

## Nice-to-Haves

- **Per-dataset breakdowns** for the "more than half" claim, so readers can see the distribution of relative reductions rather than just the average.
- **Ablation of the epsilon term** to confirm that it does not materially affect the selection.
- **Confidence intervals or significance tests** for the smaller improvements on LongBench.

## Removed Points

These points from the input review are flagged to be removed; treat them with caution:

1. **"Algorithm structure is vacuous" (from Critical Issue #1, partial):** The claim that the two-stage structure is "vacuous" depends on the unverified assumption that both stages use the same criterion. If the pseudocode has a typo and stage 1 actually uses attention weights (matching the text), the two stages are not vacuous. I have kept the core mismatch as Major but removed the characterization of "vacuous" as an overreach given the ambiguity.
2. **Critic's claim about the "structural flaw" being fatal:** Demoted from the critic's "structural/fatal" framing to Major because: (a) the empirical results are independently strong and the fix is straightforward, (b) whether the pseudocode or the text reflects the actual implementation, the core contribution (composite score improves over attention-only selection) remains intact.
3. **Critic's Section-by-Section note about the "clarity of the motivation being clear":** This is a generic strength removed per filtering rules.
4. **Critic's recommendation of "Revise and re-review":** Removed as an editorial judgment; the final review provides its own recommendation.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's main novel observation — the algorithm-theory mismatch in the pseudocode — is a valid point about presentation consistency rather than a novel scholarly insight about the problem domain.

## Suggestions

1. **Resolve the algorithm-theory alignment.** Either: (a) correct Algorithm 1 so stage 1 genuinely selects by attention weights \(A\) (matching the text and Assumption 3.4) and stage 2 selects by the composite score, or (b) if the actual implementation uses the composite score for both stages, reframe the theoretical justification accordingly and drop the two-stage framing. Option (a) preserves the claimed theoretical contribution.

2. **Fix the \(\alpha = 0.25\) typo** in Algorithm 1's input signature to read \(\alpha = 0.5\) (matching the experiments).

3. **Add error bars or variance estimates** for at least the main results (Ruler and LongBench) to establish statistical significance, especially for small-magnitude improvements.

4. **Acknowledge the SCBench Retr.KV results** as within noise range rather than presenting them uniformly as positive evidence.

## Score and Decision

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>