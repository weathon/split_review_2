Now I have all the information needed to produce the final consolidated review.

## Summary

This paper investigates why naive output matching fails for 1-bit post-training quantization of LLMs, identifying three key failure modes (block-level loss mismatch, error accumulation, attention degradation). It proposes a data-aware PTQ method with (a) an output error reformulation that accounts for accumulated quantization errors, (b) selective layer-wise output alignment restricted to the last layer of each block, and (c) an Attention Matrix Preservation (AMP) mechanism to prevent attention degradation. The method is evaluated on OPT (1.3B–30B), LLaMA-2 (7B, 13B), and LLaMA-3 (8B) models.

## Strengths

- **The preliminary analysis (Section 3) is the paper's strongest component.** It cleanly identifies three non-obvious failure modes of naive output matching: layer-wise output alignment does not guarantee block-level loss reduction (Figure 1), the ARB-X objective uses a target that drifts as quantization errors accumulate (Figure 2 top), and output alignment distorts token similarity structure in deeper layers, which is particularly damaging for attention mechanisms (Figure 2 bottom). These diagnostic experiments are well-designed and provide genuine insight that goes beyond prior work — this analysis alone is a standalone contribution.

- **Comprehensive evaluation across model families and scales.** The method is tested on OPT (1.3B–30B), LLaMA-2 (7B, 13B), and LLaMA-3 (8B), across three perplexity datasets and seven zero-shot QA datasets. This breadth is appropriate for a quantization paper and exceeds what many 1-bit PTQ papers cover.

## Weaknesses

### Fatal
None.

### Major

- **The "consistently outperforms" claim in the abstract and conclusion is contradicted by a clear failure case (Table 2, LLaMA-2-7B on PTB).** On this setting, the proposed method achieves PPL=3166 vs ARB-RC=763 and ARB-X=681 — substantially worse than two strong baselines. The paper acknowledges this in Section 5.2 ("with the exception of Llama-2-7B model evaluated on PTB dataset") but dismisses it with "the metric cannot provide a meaningful evaluation." This is unsatisfactory: other methods produce lower (better) perplexity values, showing the metric *is* discriminative. The unqualified "consistently outperforms" language in the abstract and conclusion overstates the results, and the failure mode is never analyzed. This undercuts a headline claim.

- **The selective layer-wise strategy (Section 4.2) is disconnected from the paper's own analysis.** The method restricts output alignment to only the last fully connected layer of each block, justified as having "the most direct impact on the block loss." However, the paper's own analysis (Section 3.1, Figure 1) tests every layer individually but never identifies which layers by position within their block benefit most from output alignment vs weight alignment. No evidence is provided that the last layer is systematically the right choice. An adaptive per-layer selection or even a simple analysis mapping Figure 1's results onto the "last layer of each block" would ground this design choice. As presented, the gap between the motivating analysis and the design decision weakens internal coherence.

- **No ablation of the selective vs non-selective layer decision.** The paper ablates AMP (Table 3) and the output error objective (Table 4), but never compares applying output alignment to all layers vs only the last layer of each block, nor any adaptive alternative. Since the selective approach is a core design component motivated as addressing Issue (i) from Section 3, leaving it unablated makes it impossible to assess how much this design choice contributes to the reported gains.

### Minor

- **The AMP optimization (Section 4.1) is heuristic and not compared to simpler alternatives.** The approach computes binary masks from the sign of the gradient of L_AMP and uses them to blend between old parameter values and closed-form solutions from the *output error* objective (Eq 11). There is no analysis of convergence, optimality, or what combined objective this procedure optimizes. While the ablation (Table 3) validates that AMP helps empirically, the paper does not compare this approach to simpler alternatives such as adding L_AMP as a regularizer to the output error loss and jointly optimizing. The empirical validation is sufficient for acceptability, but the methodological gap should be acknowledged.

- **The RMSNorm hypothesis (Section 5.3) is untested.** The paper attributes LLaMA's higher AMP sensitivity to RMSNorm vs LayerNorm as a post-hoc explanation, but never isolates this factor experimentally (e.g., by comparing to a model variant). Without an isolation experiment, this remains a plausible but unvalidated hypothesis.

### Trivial
None.

## Nice-to-Haves

- Report variance or multiple seeds for perplexity results since C4 calibration data is sampled.
- Include a clearer breakdown of which component (output error vs AMP vs selective layers) contributes what for each model family, since the relative gains vary substantially (e.g., AMP gives ~10 PPL improvement on LLaMA-2-7B but only 0.13 on OPT-6.7B).

## Removed Points

These points are flagged to be removed; treat them with caution:
- **Equation (2) having identical terms**: Parser artifact, not author error. The intended equation is clear from the RHS expansion.
- **AveQA aggregation masking variation**: The paper promises individual dataset results in the appendix, which was stripped by the parser.
- **PB-LLM bitrate comparison**: Already transparently reported in the tables (1.7 bits vs 1.11/1.06 bits).
- **Overhead analysis inaccessible**: The appendix was stripped by the parser; this is not an author omission.
- **"AMP disparity between LLaMA and OPT not discussed"**: Factually incorrect — the paper *does* discuss this at line 263 with the RMSNorm hypothesis.
- **Section 4.2 parameterization**: The paper clearly states it uses ARB-RC for non-output-aligned layers, so this is a clarification rather than a genuine weakness.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Qualify the headline claim.** Replace "consistently outperforms" with a precise statement acknowledging limitations (e.g., LLaMA-2-7B on PTB), and discuss the failure mode rather than dismissing it.
2. **Ground the selective layer choice or replace it.** Either provide evidence from the paper's own analysis (Figure 1) that the last layer of each block is the optimal choice, or add an ablation comparing selective vs full vs adaptive selection.
3. **Compare the AMP optimization to a simpler regularization baseline.** If the binary-mask approach outperforms a tuned regularization weight, that would justify the design; if not, the simpler approach should be preferred.
4. **Investigate the PTB failure.** Determine whether it is a calibration set mismatch, an interaction with AMP, or a model-specific pathology.

## Score and Decision

The paper makes a genuine analytical contribution (Section 3 diagnostics) that advances understanding of why naive output matching fails in 1-bit PTQ. The method shows consistent improvement over baselines on most settings. However, the headline claim is overstated given a clear counterexample (LLaMA-2-7B/PTB), a core design choice (selective layer application) is not grounded in the paper's own evidence and goes unablated, and the AMP optimization approach is heuristic. These weaknesses are significant enough to require major revisions but do not invalidate the paper's analytical contributions.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>