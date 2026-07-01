## Summary

This paper investigates why naive output-matching objectives underperform for 1-bit post-training quantization of LLMs, and proposes a method combining: (i) a selective application of output matching (only on the last FC layer of each block), (ii) using the full-precision input **X** rather than the quantized input **X̂** as the target (formulating the "Output Error" ‖XW − X̂Ŵ‖ instead of the "Activation-conditioned Error"), and (iii) an Attention Matrix Preservation (AMP) mechanism that hard-masks closed-form updates to preserve token similarity structure. Experiments across OPT (1.3B–30B) and LLaMA (2-7B, 2-13B, 3-8B) models show consistent perplexity improvements over existing 1-bit PTQ methods.

## Strengths

1. **Diagnostic analysis in Section 3 is genuinely informative and stands as a contribution itself.** Figure 1 clearly shows that layer-wise output matching (ARB-X) does not guarantee block-level loss reduction compared to weight matching (ARB) — some layers produce higher block loss despite lower layer-level loss. Figure 2 demonstrates the gap between the activation-conditioned objective and the true output error growing with depth, and the bottom panel shows token similarity matrices drifting from the full-precision baseline. These experiments concretely identify the three challenges the method addresses.

2. **The core reformulation — matching ‖XW − X̂Ŵ‖ instead of ‖X̂W − X̂Ŵ‖ — is correctly motivated and its benefit is empirically confirmed.** The paper identifies that conditioning on X̂ causes the optimization target to drift as errors accumulate, and replacing X̂ with X in the target fixes this. The ablation in Table 4 shows this substitution yields a 0.7 PPL improvement on C4 for LLaMA-2-7B and 0.69 for OPT-6.7B, confirming the insight directly.

3. **Consistent improvements across a broad range of model scales and architectures.** The method beats ARB-RC, ARB-X, BiLLM, and PB-LLM on nearly every perplexity and QA benchmark for OPT 1.3B–30B, LLaMA-2-7B/13B, and LLaMA-3-8B (Tables 1–2). The gains are modest for large models but systematic.

## Weaknesses

### Fatal

None.

### Major

1. **The catastrophic PPL failure on LLaMA-2-7B / PTB (PPL 3166 vs. 681–763 for baselines) is dismissed rather than investigated.** The paper acknowledges this once (line 175, line 233) and then says "the large perplexity indicates that the metric cannot provide a meaningful evaluation." This is not an adequate response — a PPL of 3166 means the quantized model is producing near-garbage on that dataset, and the metric is providing a *meaningful signal of failure*. The other LLaMA models produce reasonable PTB numbers (LLaMA-2-13B: 196.64 vs. ARB-RC 197.70; LLaMA-3-8B: 45.66 vs. ARB-RC 47.88), so this is not a systematic PTB problem but something specific to LLaMA-2-7B × PTB. Possible causes (numerical instability in the pseudoinverse for this specific configuration, a pathological interaction with AMP, or an implementation bug) are not explored. A paper claiming consistent improvement cannot leave its single worst failure unanalyzed.

2. **The selective-layer design choice ("last fully connected layer of each block") is asserted without evidence or ablation.** Line 161 states that output matching is applied "only to the last fully connected layer of each block, since it has the most direct impact on the block loss" — no citation or experiment supports this claim. The diagnostic analysis in Section 3.1 showed that some layers benefit from output matching and others do not, but it did not identify the last FC layer as the systematically best candidate. An ablation comparing output matching applied to each layer type within a block (attention output, first MLP FC, second MLP FC) is missing and would be straightforward to run. This design choice is central to the method's architecture.

3. **The AMP mechanism's hard-masking update rule and the RMSNorm hypothesis are not adequately analyzed.** The AMP update (Eq. 11) applies a hard gate: a parameter is updated to its closed-form optimum only if the sign of its AMP gradient is positive, otherwise it stays at its current value. This could cause optimization to get stuck at suboptimal points; its convergence properties are not discussed. Separately, AMP is crucial for LLaMA (Table 3: PPL improves from 29.12→19.25 on C4) but nearly irrelevant for OPT (16.35→16.22). The paper attributes this to the RMSNorm vs. LayerNorm architectural difference in a single paragraph (line 263) without any controlled experiment (e.g., swapping the normalization or measuring the token-similarity drift for OPT vs. LLaMA under the same conditions). The most novel component of the method has the weakest justification.

### Minor

4. **The framing overstates the novelty relative to the weight-matching baseline.** The paper frames its contribution as fixing output matching, but the strongest baseline across all experiments is ARB-RC, a *weight-matching* method. The proposed method uses ARB-RC internally for all non-last-FC layers, and the incremental gain over ARB-RC is modest (e.g., Table 1: OPT-13B C4: 14.71 vs. 15.07; OPT-30B C4: 13.15 vs. 13.34; Table 2: LLaMA-2-13B WikiText2: 11.5 vs. 12.47). The improvements are genuine but small, and the method's main practical advantage is as a refinement of ARB-RC rather than a fundamentally new approach to output matching.

5. **No variance or statistical significance is reported.** All results in Tables 1–4 are single numbers. Since perplexity can vary with calibration data sampling and random seeds, confidence intervals or multi-run statistics would strengthen confidence, especially for the small improvements over ARB-RC on large models.

6. **The paper does not discuss failure modes or limitations beyond the one-sentence acknowledgment of the PTB anomaly.** A limitations paragraph discussing where and why the method might underperform would improve the paper's scientific completeness.

### Trivial

None.

## Nice-to-Haves

- An ablation comparing which layer within a block output matching is applied to (attention output, first MLP FC, second MLP FC).
- A controlled experiment verifying the RMSNorm hypothesis for AMP's architecture-dependence (e.g., measuring token-similarity drift in OPT vs. LLaMA, or swapping normalization types if feasible).
- Reporting AMP's effect on QA accuracy and on the PTB dataset, not just PPL on C4 and WikiText2.
- Investigating the LLaMA-2-7B/PTB failure to determine whether it stems from numerical instability in the pseudoinverse, an AMP interaction, or another cause.

## Removed Points

The following points from the input review are excluded under the filtering rules:

- **Equation (2) typo concern and other formatting/notation issues** — These are parser artifacts, not author errors.
- **Missing appendix analysis (overhead, proofs)** — The parser strips appendices; they exist in the original submission.
- **Figure 1 caption tension ("generally shows lower loss across most layers")** — The paper's claim is "does not necessarily" improve, which is a weak claim fully compatible with "generally lower on most layers, with exceptions."
- **Computational overhead comparison** — Referenced to Appendix D, which is stripped.

## Novel Insights

The harsh critic makes an insightful structural observation about the paper's framing vs. its actual mechanism: the method's practical strength comes from augmenting a weight-matching baseline (ARB-RC) with selective output matching on one layer per block, not from demonstrating that output matching is generally superior. This reframing clarifies why the gains over ARB-RC are modest and why the most novel component (AMP) is the least justified. The critic also correctly identifies that the PTB/LLaMA-2-7B failure — the single largest deviation in the results — is treated as a measurement artifact when it is in fact a genuine system failure that demands explanation.

## Suggestions

1. Investigate the LLaMA-2-7B / PTB failure case — determine whether it stems from numerical instability in torch.linalg.lstsq, an AMP interaction, or another cause — and report the finding.
2. Add an ablation comparing output matching applied to each layer type within a transformer block, to support or replace the "last FC layer" design choice.
3. Provide confidence intervals or multi-run statistics (at least for the main comparisons), especially where improvements over ARB-RC are small.
4. Present a limitations paragraph that discusses conditions under which the method may not help or may fail.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>