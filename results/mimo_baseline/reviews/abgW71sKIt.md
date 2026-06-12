## Summary

This paper investigates why naive layer-wise output alignment fails for 1-bit post-training quantization of LLMs, identifying three key issues: (1) layer-wise output matching doesn't guarantee block-level loss reduction, (2) quantization errors accumulate across layers degrading the alignment target, and (3) indiscriminate output matching distorts attention mechanisms. Building on these insights, the authors propose a selective output alignment strategy applied only to the last FC layer per block, a modified objective using full-precision inputs to account for accumulated error, and an Attention Matrix Preservation (AMP) mechanism, achieving consistent improvements over existing 1-bit PTQ methods.

## Strengths

- **Well-motivated and clear diagnostic analysis.** The paper's three key observations about why output alignment fails (Sections 3.1–3.3) are well-supported by empirical evidence. The demonstration that layer-wise output alignment can increase block-level loss (Fig. 1) and that error accumulates across blocks (Fig. 2) provides genuine insight into a previously underexplored problem. These observations constitute a valuable conceptual contribution beyond just the proposed method.

- **Comprehensive and consistent experimental evaluation.** The method is evaluated across two model families (OPT: 1.3B–30B; LLaMA-2 and LLaMA-3: 7B–13B), three perplexity benchmarks, and seven zero-shot QA tasks. The results consistently show improvements over all baselines, with particularly strong gains on smaller models (up to 4.85 PPL reduction on OPT-1.3B). Ablation studies cleanly validate each component (Tables 3–4).

- **Practically simple and computationally reasonable.** The selective output alignment strategy (apply output error only to the last FC layer per block, weight alignment elsewhere) is elegant and avoids the overhead of applying output matching to all layers. The AMP mechanism adds minimal cost while providing large gains, especially for LLaMA architectures.

## Weaknesses

### Fatal
None.

### Major

- **PTB result for LLaMA-2-7B is anomalous.** The method reports 3166 PPL on PTB for LLaMA-2-7B, compared to 763.19 for ARB-RC and 681.24 for ARB-X. This is dramatically worse than all baselines and contradicts the paper's claims. While the authors briefly acknowledge "the large perplexity indicates that the metric cannot provide a meaningful evaluation," this is unsatisfying—the method should not degrade catastrophically on any standard benchmark. This suggests a potential failure mode that warrants investigation and explanation rather than dismissal.

- **Heavy reliance on ARB-RC as a component.** The method uses ARB-RC (a baseline) for all layers except the last FC layer per block, with the output error objective and AMP applied only to that final layer. This makes the contribution more incremental than it may appear—the core quantization machinery is inherited, and the novelty is in the objective reformulation and selective application. The paper would benefit from a clearer characterization of what fraction of the improvement comes from each design choice.

### Minor

- **Improvements on LLaMA-3-8B are marginal.** For WikiText2, the gain over ARB-RC is 27.42 → 27.20 (0.22 PPL), which is within typical noise ranges for quantization experiments. The paper should discuss whether the method generalizes equally well to newer architectures or if there are architecture-specific limitations.

- **The paper mentions computation overhead analysis in Appendix D, but this is stripped.** Without knowing the cost of the iterative optimization (Eq. 5–8 involves matrix pseudoinverses), it's hard to fully assess the practical value, particularly for very large models.

- **Closed-form solutions (Eqs. 5–8) lack sufficient intuition.** While derivations are deferred to the appendix, the paper would benefit from a brief intuitive explanation of why the output error objective changes the optimization landscape compared to the activation-conditioned error—e.g., how the cross-term X^T X̂ versus X̂^T X̂ fundamentally alters the solution structure.

### Trivial

- Table 2 for PTB appears to have an error in the LLaMA-2-7B row for Ours (3166 seems like it may be a formatting issue, possibly 316.6 or similar).

## Nice-to-Haves

- A comparison of wall-clock quantization time across methods would strengthen the practical contribution claim.
- Analysis of how the method performs with different calibration set sizes would be valuable, given the emphasis on minimal calibration data.
- Discussion of how the selective layer strategy generalizes beyond transformer blocks to other architectures.

## Novel Insights

The paper's most novel insight is that the effectiveness of output alignment in 1-bit PTQ is fundamentally limited by the accumulation of quantization errors across layers: the target output used in existing methods (X̂W) progressively diverges from the true full-precision output (XW), making layer-wise alignment increasingly misaligned with the actual quantization goal. Combined with the observation that output alignment can disrupt attention patterns in RMSNorm-based architectures (explaining LLaMA's sensitivity), the paper provides a principled understanding of why data-aware output alignment requires architectural awareness rather than naive universal application.

## Suggestions

- Investigate and explain the catastrophic PTB result for LLaMA-2-7B rather than dismissing it. Even if PTB is noisy, a 5× degradation over ARB-RC signals a real issue.
- Add an ablation that replaces ARB-RC with other weight-alignment methods for the non-output-aligned layers to demonstrate that the improvements are not tied to a specific base method.
- Provide a brief analysis of computational overhead in the main text, even if detailed numbers are in the appendix.

## Score and Decision

The paper presents a well-motivated diagnostic analysis of why output alignment fails for 1-bit LLM quantization, backed by solid empirical evidence. The proposed method is simple and effective, with consistent improvements across models and benchmarks. However, the anomalous PTB result, the heavy reliance on ARB-RC as a component, and the marginal gains on some settings temper enthusiasm. The conceptual contributions (understanding of output alignment limitations) are valuable, but the methodological contribution is somewhat incremental.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: Reject