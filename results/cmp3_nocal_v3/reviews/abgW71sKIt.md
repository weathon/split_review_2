## Summary

This paper investigates why output-matching objectives fail in 1-bit post-training quantization (PTQ) of LLMs, identifying three issues: layer-wise alignment does not guarantee block-level loss reduction; quantization errors accumulate across layers, causing the Activation-conditioned Error objective to diverge from the true full-precision target; and naive output matching disrupts token similarity matrices. The paper proposes a correction (Output Error objective using full-precision inputs), an attention-preserving gating mechanism (AMP), and selectively applies output alignment only to the last FC layer of each block. Experiments on OPT (1.3B–30B) and LLaMA (7B–13B) show consistent improvements over ARB-RC and ARB-X on most benchmarks.

## Strengths

1. **The three-part diagnosis of output-matching failure (Sections 3.1–3.3) is genuinely informative.** The paper cleanly demonstrates (a) that layer-wise output matching does not guarantee block-level loss reduction (Figure 1), (b) that the Activation-conditioned Error objective diverges from the true full-precision target as errors accumulate (Figure 2, top), and (c) that naive output matching distorts token similarity matrices (Figure 2, bottom). These observations are well-motivated and supported by quantitative evidence — particularly the error-accumulation insight (Section 3.2), which directly motivates the paper's core reformulation.

2. **The AMP ablation result is dramatic.** Table 3 shows that removing AMP from the full method on LLaMA-2-7B increases perplexity from 19.25 to 29.12 on C4 and from 15.42 to 26.24 on WikiText-2 — a roughly 10 PPL degradation. The much smaller effect on OPT-6.7B (16.22→16.35, 14.56→14.74) also supports the paper's hypothesized architecture-specific explanation (RMSNorm vs. LayerNorm). This is unusually clear ablation evidence for a design component.

3. **Consistent improvements over strong baselines on most settings.** Across OPT models (1.3B–30B) and most LLaMA benchmarks, the method outperforms ARB-RC and ARB-X on C4, WikiText-2, and average QA accuracy. The improvements are often meaningful (e.g., OPT-1.3B C4: ARB-RC 27.70 → Ours 24.69; LLaMA-2-7B C4: ARB-RC 20.4 → Ours 19.25).

## Weaknesses

### Fatal
None.

### Major

- **Unexplained catastrophic failure on LLaMA-2-7B / PTB (PPL 3166 vs. ARB-RC 763) contradicts the central claim of consistent improvement.** Table 2 reports PPL 3166 on PTB for LLaMA-2-7B — roughly 4–5× worse than ARB-RC (763), ARB-X (681), and PB-LLM (657). The paper acknowledges the exception (line 176: "with the exception of Llama-2-7B model evaluated on PTB dataset") but then dismisses it (line 233: "the large perplexity indicates that the metric cannot provide a meaningful evaluation"). This is evasive: perplexity is a standard, meaningful metric applied uniformly. If it is uninformative for one method, it is equally uninformative for all. The conclusion then reasserts that the method "consistently outperforms" (line 269), directly contradicting this data point. A method intended for practical deployment cannot silently degrade 4× on a standard benchmark without explanation. The paper must diagnose *why* this specific combination fails and either fix it or clearly characterize the limitation.

### Minor

- **The selective-layer design choice (applying output alignment only to the last FC layer of each block) is stated without ablation evidence.** Section 4.2 (line 161) claims this layer "has the most direct impact on the block loss" but provides no comparison with alternatives: (a) output alignment on all layers, (b) on attention layers only, (c) on the first FC layer only, (d) weight alignment only (the ARB-RC baseline). Without this ablation, the contribution of the "selective" design choice — listed as contribution (a) in Section 4 — is unmeasurable, and the reader cannot tell whether improvements come from the Output Error objective, the AMP mechanism, or simply from the specific layer selection strategy.

- **The claim of "minimal overhead" (abstract) is unsubstantiated in the main text.** The paper defers all overhead analysis to Appendix D with a one-line reference (line 265). While the appendix is stripped in this version, the main text should at minimum summarize wall-clock time and peak memory for a representative case (e.g., LLaMA-2-7B calibration) to let readers assess whether the modest PPL improvements justify additional computational cost.

### Trivial
- Minor wording inconsistency around Equation (9): the objective is written as "max L_AMP" but the surrounding text says "the objective to minimize the attention degradation problem" — the intent is clear (maximizing L_AMP minimizes degradation), but the phrasing is slightly confusing.

## Nice-to-Haves

- **Confidence intervals or variance estimates.** Several improvements over ARB-RC are small (e.g., OPT-13B C4: 15.07→14.71; OPT-30B C4: 13.34→13.15). Without variance estimates, it is impossible to tell whether these differences are meaningful or calibration-set noise. While single-run evaluation is common in this field, reporting variability would strengthen the paper.
- **Ablation of the selective-layer design choice** (as described above) to support contribution (a).
- **Clarification of the AMP gating mechanism** — specifically why the *sign* of the gradient of L_AMP with respect to a parameter determines whether the closed-form update is applied (Equation 11), and how near-zero gradients are handled.
- **Discussion of the numerical behavior of the least-squares solution for αᵣ** (Equation 8, replaced with `torch.linalg.lstsq` in practice) — does the solution always exist, and are there cases where it produces extreme values that destabilize the quantized model?

## Removed Points

These points were flagged during review but are removed or relocated for the reasons below. Treat them with caution if referenced.

1. **"The paper bolds the 3166 value as if it were best."** — Factually incorrect. In Table 2, PTB row for LLaMA-2-7B, PB-LLM's 657.24 is bolded as the best value; 3166 (Ours) is not bolded. Only the method name "Ours" appears in bold, which is standard table formatting.
2. **"Equation (2) has both terms as X̂Ŵ instead of X̂W and X̂Ŵ."** — The reviewer notes this is a parser artifact and the intent is clear from context; it was not presented as a criticism.
3. **"PB-LLM uses 1.7 bits vs. 1.11/1.06 bits for others."** — The reviewer acknowledges this actually disadvantages PB-LLM (higher bits, worse performance), so it is not a weakness against the paper.
4. **"No variance or statistical significance is reported."** — Moved to Nice-to-Haves, as single-run evaluation on standard benchmarks is the prevailing norm for LLM quantization papers.
5. **"Section 3.1's protocol is somewhat artificial (quantizing one layer at a time)."** — The paper presents this as a diagnostic analysis, which is standard practice for isolating effects; it is not intended to measure the full pipeline.
6. **"No evaluation on 70B-scale models."** — The paper tests up to OPT-30B, which is reasonable for 1-bit PTQ. Requesting 70B evaluation is scope creep.
7. **"No comparison to more recent sub-2-bit methods."** — The paper compares to contemporaneous methods (BiLLM, ARB-LLM, PB-LLM). Speculating about newer methods is outside the paper's scope.

## Novel Insights

None beyond the paper's own contributions. The reviewer analysis surfaces the severity of the PTB failure case and the lack of ablation for the selective-layer choice, but these are gaps in the paper's evidence, not novel insights derived from the review.

## Suggestions

1. **Diagnose and explain the LLaMA-2-7B/PTB failure.** This is the single most important issue. Whether the cause is numerical instability in the least-squares solver for certain activation statistics, a calibration-set sensitivity, or a fundamental limitation, the paper must either fix it or explicitly characterize when the method can and cannot be trusted. Remove the "metric cannot provide a meaningful evaluation" dismissal.
2. **Add an ablation comparing different layer selection strategies** — all layers, attention layers only, last FC only, first FC only, and weight-alignment-only — to empirically justify the selective-layer design choice.
3. **Include a brief overhead summary in the main text** (wall-clock time, peak memory for LLaMA-2-7B calibration) to support the "minimal overhead" claim.
4. **Revise the conclusion to reflect the PTB exception** rather than claiming "consistently outperforms" without qualification.

## Score and Decision

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>