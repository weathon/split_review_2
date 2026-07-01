## Summary

This paper identifies a training-inference mismatch in tree-based speculative decoding: draft models are trained on linear sequences but used to generate trees at inference time. It proposes two contributions: (1) TALF, a tree-aware loss function that trains the draft model on trees constructed by the target LLM, and (2) SALF, a dynamic tree construction algorithm with a provably monotonic stopping criterion that trades tree optimality against drafting overhead. Experiments on Llama-2-7B, Llama-3.1-8B, and DeepSeek-R1-Distill-Llama-8B across five benchmarks show consistent speedups over EAGLE-2 and HASS.

## Strengths

- **Well-motivated identification of a real mismatch.** The analysis in §3.1 cleanly demonstrates that existing training methods degrade sharply on lower-ranked tokens, while Figure 2(a) shows tokens ranked ≥5th account for >10% of the draft tree. The quantification makes concrete why tree-aware training matters.

- **Comprehensive ablation design (Table 2).** Testing all 9 combinations of 3 tree-construction methods × 3 loss functions cleanly separates TALF's contribution (improving τ for any fixed tree construction) from SALF's (improving speedup for any fixed loss). TALF improves τ by 7–13% over prior losses at the same tree construction method, and SALF improves speedup by 14–19% over optimal tree search at the same loss.

- **SALF is principled and well-characterized.** Theorem 1 provides a clean monotonicity guarantee for the stopping criterion. Table 4 shows a smooth Pareto frontier between τ and speedup as *th* varies, confirming SALF genuinely balances draft quality against overhead.

- **Consistent empirical results across diverse settings.** Improvements hold across 3 models × 5 tasks × 2 temperatures. The DeepSeek experiment uses equal training time (24 hours each), confirming 22.9–28.4% improvement over HASS under a fair comparison.

## Weaknesses

### Fatal

None.

### Major

- **Training asymmetry for Llama experiments (§4.1, lines 196–197).** For Llama2-7B and Llama3-8B, EAGLE is trained for 10 epochs while HASS and TALF start from the 10-epoch EAGLE checkpoint and receive 3 additional epochs. This gives HASS/TALF more total training, so some portion of the headline improvements (15.6–39.4% over EAGLE-2, 6.5–24.4% over HASS) may be attributable to extra training rather than the methods themselves. The HASS vs. TALF comparison is fair (both get the same extra epochs), and the DeepSeek experiment with equal 24-hour training provides a cleaner controlled comparison that still shows large gains. However, the Llama numbers in Table 1 and the abstract are confounded and should be interpreted with caution.

- **TALF drops the regression loss without ablation (line 114).** TALF differs from HASS in two orthogonal ways: (a) tree-aware classification loss, and (b) no regression loss for feature alignment. The paper states that removing the regression loss "was sufficient" but provides no ablation to disentangle whether TALF's gains come from tree awareness, from removing the regression loss, or from both. A controlled comparison (e.g., "HASS without regression loss" or "TALF with regression loss added back") is needed to establish cause.

### Minor

- **Fixed training tree may partially recreate the mismatch (§3.2, lines 110–111).** The training tree is preprocessed by the target model and fixed in advance to avoid repeated target invocations. During inference, the tree is constructed dynamically using the draft model's own probabilities (via SALF). If the draft model's probability estimates differ from the target's — which is the very gap TALF aims to fix — the inference-time tree structure will differ from the training-time structure. The paper acknowledges this as a computational tradeoff, which is reasonable, but the residual mismatch is not quantified.

- **Rejection sampling guarantee not discussed for non-greedy sampling.** Standard speculative decoding (Leviathan et al., 2023; Chen et al., 2023) provably preserves the target model's output distribution via rejection sampling. The paper mentions this in §5 but does not verify or discuss whether SALF & TALF maintain this property for T=1 sampling.

### Trivial

- **Theorem 1 qualifier "for i ≥ 2" not explained.** The monotonicity guarantee starts only from iteration 2 (S₁ corresponds to the root node's unconditional probability of 1). The reason for this qualifier and its practical implications are not discussed in the main text.

## Nice-to-Haves

- Report variance (standard deviations or confidence intervals) for speedup measurements. While single-run reporting is standard in this subfield, some improvements are modest (e.g., 6.5% over HASS for Llama2-7B at T=0), and variance estimates would help assess reliability.
- Quantify the wall-clock training cost of TALF relative to EAGLE/HASS.
- Provide a heuristic for selecting the SALF threshold *th* for a new model or workload beyond the default.
- Extend the §3.1 motivation to measure calibration degradation over multiple levels of self-conditioning.

## Removed Points

These points were flagged but are not included as weaknesses in the main review:

- *Missing comparison to Griffin* — removed per policy on missing related work comparisons; the paper cites Griffin as a related method, but requiring a specific empirical comparison is speculation about availability.
- *Figure 2 hard to interpret from alt-text* — a parser artifact, not a paper issue.
- *Lack of statistical significance as a weakness* — moved to Nice-to-Have because single-run evaluation with no variance is standard practice in this subfield's experimental papers.
- *"SALF has slightly lower τ than beam search" characterization* — the reviewer's own analysis shows this is honestly reported and correctly interpreted by the paper; it is not a weakness.
- *"Self-conditioning only one level"* — moved to Nice-to-Have as a direction for future work, not a flaw.
- *Demands for scope-extension (dynamic threshold adaptation, etc.)* — moved to Nice-to-Have or removed as not deficiencies in the paper as written.

## Novel Insights

None beyond the paper's own contributions. The most perceptive observations from the review — the regression-loss confound and the training-time asymmetry — are identifiable from reading the paper directly rather than constituting novel external insights.

## Suggestions

1. Equalize training epochs for the Llama experiments and re-report Table 1, or at minimum add a row for "EAGLE-2 trained for 13 epochs" to quantify the effect of the asymmetric design.
2. Add an ablation row to Table 2: "HASS without regression loss" (classification-only) to isolate whether TALF's advantage stems from tree awareness or from removing the regression objective.
3. Discuss whether the rejection sampling distribution-preserving property holds under SALF & TALF for T=1 sampling.
4. Add standard deviations or confidence intervals for the end-to-end speedups in Table 1.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>