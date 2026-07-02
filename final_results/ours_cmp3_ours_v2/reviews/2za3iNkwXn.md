## Summary

This paper empirically studies how compression methods (quantization, distillation, pruning) affect the reasoning capabilities of DeepSeek-R1 and its distilled variants. It benchmarks compressed models on four reasoning datasets and uses mechanistic interpretability (difference of means + attribution patching) to identify which linear modules are most affected by compression. The core findings — that the final-layer MLP up-projection is a critical component, that current quantization methods over-compress gate projections and final-layer modules, and that protecting ~2% of weights yields a 6.57% accuracy improvement — are specific, actionable, and causally validated through intervention experiments.

## Strengths

- **Breadth across three compression paradigms.** The paper evaluates quantization (dynamic, AWQ, GPTQ, GPTAQ, ANY4/3), distillation (SFT-based), and pruning (SparseGPT, AlphaPruning) within a single framework, enabling comparative conclusions not reachable by single-paradigm studies.

- **Fine-grained module-level interpretability.** The adaptation of difference of means and attribution patching produces importance scores at the individual linear-module level (q, k, v, o, gate, up, down per layer). This granularity is what surfaces the final-layer `up_proj` finding and the gate-projection bottleneck — results that would be invisible at layer-level analysis.

- **Causal validation via weight-level intervention.** The paper does not stop at correlational analysis. It validates its interpretability findings by (a) selectively quantizing the identified `32_up` component to 3-bit, causing a 16.3% accuracy drop (Table 3), and (b) protecting only final-layer MLP modules (~2% of weights) during 3-bit AWQ, yielding a 6.57% average accuracy improvement over the unmodified baseline (Table 4). These experiments directly confirm that the identified components are causally important.

- **Actionable diagnosis.** The finding that current quantization methods over-compress gate projections and final-layer modules is specific enough to guide future compression research — a concrete bottleneck rather than a generic observation that compression hurts performance.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **The "23.17% gain" figure over SOTA quantization is not reconstructible from the main paper's tables.** The abstract and Section 5.2 claim "gains of up to 23.17% over the state-of-the-art quantization." From Tables 1 and 4: protected AWQ achieves 52.57 average accuracy; the best 3-bit baseline (GPTQ at 47.8) yields a ~10% relative improvement. No combination of per-benchmark numbers in the main tables produces 23.17%. This figure may be computed in the appendix, but a headline quantitative claim should be derivable from the main text. The authors should either clarify its computation or state explicitly which baseline and metric it refers to.

2. **No variance or uncertainty reporting.** The paper runs three passes for most models (line 94) and reports averages, but never reports standard deviations or confidence intervals. Several comparisons in Table 1 differ by only 1–2 points (e.g., 4-bit AWQ at 66.6 vs. 4-bit ANY4 at 66.1 for Llama-8B). Without variance estimates, the reader cannot assess whether these differences are meaningful or within noise. Importance scores are also reported as point values with no stability estimates. Adding standard deviations would substantially strengthen the quantitative rigor.

3. **Imprecision in "weight importance" vs. "activation importance" framing.** The attribution patching score I^c_{mℓ} (Section 2.2) uses a gradient with respect to the module's *activation*, not its *weights*. The paper frames the results as identifying "important weights" and "causal relationships between weights and various reasoning capabilities" (abstract, Section 2.2). This conceptual slip is partially redeemed by the intervention experiments (Tables 3, 4), which directly test weight-level importance, but the methodological description should be more precise about what is actually measured.

4. **Cross-family comparison conflates model scale with compression method.** The text states "2.51-bit R1 has the best overall performance than other compression strategies" (Section 3.1). The 2.51-bit model is a compressed 671B R1, while "other compression strategies" (distillation, pruning) operate on models 10–100× smaller (7B–70B). The table is segmented by model family and over-parameterization is acknowledged, but the text still draws comparisons that conflate model scale with the merits of the compression approach.

5. **MuSiQue confounds knowledge retrieval with reasoning in the knowledge-retention claim.** The finding that "pruning and distillation compress knowledge retention more than reasoning capabilities" (Takeaway 3.3) is based primarily on MuSiQue, which measures multihop reasoning under a closed-book setting — conflating knowledge retrieval with reasoning. The paper references additional experiments in Appendix L, but the main-text claim is presented more strongly than the main-body evidence cleanly supports.

### Trivial

- The discrepancy with Shao & Wu (2025), who found `o_proj` most important, is noted but left unexplored. A brief discussion of possible causes (different models, methods, or behaviors) would strengthen Section 4.1.

## Nice-to-Haves

- Reporting standard deviations for the three-run averages in Table 1 would require minimal effort and would substantially strengthen confidence in the comparisons.
- A direct comparison of the adapted attribution-patching method against simpler baselines (e.g., gradient norms, activation patching) would help establish that the method adds value over simpler approaches.
- The "collapse point" analysis (Section 3.2) could be quantified more systematically, e.g., by computing the sparsity/bit-width at which each benchmark drops below 50% of the uncompressed model's accuracy.

## Removed Points

These points from the input review were considered and removed:
- **Generalizability to non-R1 models (Critic Issue 3):** REMOVED per hard rule. The paper explicitly states "as elaborated in Appendix J" (line 98). The appendix was stripped by the parser; this is a parser limitation, not an author omission.
- **Alternative explanation for Section 5.1 heatmap findings:** REMOVED as speculative. The critic suggested that modules might be inherently more sensitive regardless of method, but offered no evidence for this.
- **120-instance annotation concern:** REMOVED as the paper defers robustness evaluation to Appendix G (stripped by parser). Unverifiable given the stripped appendix.
- **Missing alternative interpretability method comparison:** MOVED to Nice-to-Haves, as it is a suggestion for strengthening, not a weakness.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Clarify the computation of the "23.17%" figure in Section 5.2, stating which specific baseline and metric combination produces it, so readers can verify it from the main text.
2. Add standard deviations or confidence intervals for the three-run averages in Table 1.
3. Distinguish more carefully between "activation importance" and "weight importance" in Sections 2.2–2.3, or include a derivation showing why activation importance implies weight importance under the given approximation.
4. Frame the cross-family comparison in Section 3.1 more cautiously, acknowledging that the 2.51-bit R1 result demonstrates a scale-compression trade-off rather than superiority of quantization over distillation/pruning per se.

## Score and Decision

**Calibration Procedure**

*Round 1 (Bracketing):* I searched six score bands with topic-relevant queries. The closest topical matches fell in the 5.5–7.5 band: papers on activation patching, mechanistic interpretability, and steering vectors applied to language models. Key anchors:

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `Hf17y6u9BC.md` — "Towards Best Practices of Activation Patching" | 6.67 | R1 | Systematic empirical methodology study; stronger methodological contribution, similar analysis rigor |
| `sqsGBW8zQx.md` — "Context-Augmented LMs Through Mechanistic Circuits" | 5.75 | R1 | Causal mediation analysis for QA; rejected for unclear contribution and weak experiments relative to claims — the current paper has clearer contributions and stronger validation |
| `AwyxtyMwaG.md` — "Function Vectors in Large Language Models" | 6.00 | R1 | Causal mediation analysis for ICL; solid and well-received |
| `wozhdnRCtw.md` — "Improving Instruction-Following through Activation Steering" | 7.00 | R1 | Clean, well-executed method paper with solid experiments |
| `wg1PCg3CUP.md` — "Scaling Laws for Precision" | 8.00 | R1 | Thorough, rigorous scaling-law paper with extensive experimental validation — higher standard than the current paper |

- Round 1 bracket: 5.5–7.0 (narrowed from the initial broad search based on topical similarity to the 5.5–7.5 band).

The paper under review has clearer contributions and stronger causal validation than the 5.75 anchor, but has more reporting issues (unverifiable headline figure, no variance estimates) than the 6.67–7.0 anchors. Its contributions are genuine and validated, but the reporting weaknesses prevent it from reaching the top of the band.

Final calibrated score: **6.0**

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>