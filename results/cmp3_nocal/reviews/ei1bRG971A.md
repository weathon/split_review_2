Now I have thoroughly verified the paper against the reviewer's claims. Let me write the final consolidated review.

## Summary

DND is a post-training method that adds a lightweight router to existing transformer layers to identify "critical" tokens and reprocess them through the same layer in a nested pass. The router is trained with a dual-objective loss (score dispersion to encourage distinguishability + distribution preservation to avoid saturation) and a threshold control scheme (buffer proportional control + EMA synchronization). DND is validated on three dense 1B-class models and a 30B MoE model, showing consistent average gains of +0.87% to +2.61% with negligible parameter overhead (~0.03M) and modest throughput degradation (~7-9%).

## Strengths

1. **Entropy-based validation of the selection mechanism (Fig. 4a/4b).** The paper directly ties token selection frequency to logit entropy (r=0.336) and shows that the nested pass reduces entropy for frequently selected tokens (r=-0.581). This is concrete evidence that the router preferentially selects high-uncertainty tokens and that the nested pass meaningfully reduces that uncertainty — stronger evidence than a pure accuracy comparison.

2. **Carefully engineered training strategy with ablation support.** The dual-objective router loss (score dispersion + distribution preservation) and threshold control (buffer proportional control + EMA synchronization) are non-trivial and the ablation (Table 4) confirms their importance: the full DND (+1.88) clearly outperforms a version using only a z-loss-like method (+1.01). The threshold visualizations (Fig. 5, 6a, 6b) provide direct evidence that the control mechanisms work as designed.

3. **Practicality:** DND works as a post-training plug-in for existing pretrained models (dense and MoE), adds only ~0.03M parameters, and achieves 91.6–93.1% of vanilla throughput on the 30B MoE model (Table 3). This is a genuine practical advantage over methods like MOR that require training from scratch.

4. **Qualitative analysis (Fig. 7b) shows hierarchical token selection.** The observation that shallower layers select nouns while deeper layers select mathematical expressions and key verbs suggests the model learns a meaningful hierarchical processing strategy, supporting the interpretability of the approach.

## Weaknesses

### Fatal
None.

### Major

1. **No statistical significance reporting; small individual gains may be noise.** The paper reports no error bars, confidence intervals, or multi-seed results for any benchmark. On the 30B MoE model (Table 2), several per-benchmark improvements are very small: BBH +0.13, MATH +0.15, MATH-500 +0.20, DROP +0.27, CMMLU +0.37. Without any measure of variance, the reader cannot determine whether these individual gains are real or within evaluation noise. The aggregate average (+0.87 across 17 benchmarks) is more reliable, but the paper also highlights domain-specific claims (e.g., "substantial improvements … on Math and STEM benchmarks") while MATH shows +0.15. This is a significant evidential gap for an empirical paper.

2. **No direct test of whether *intelligent selection* drives improvement vs. extra compute alone.** The paper's core claim is that *which* tokens receive extra computation matters. The only equal-compute comparison is against ITT on a single 1.7B model (Table 1), and the ITT training setup is not described in sufficient detail to assess fairness. The most informative control would be a random-selection baseline at the same compute budget: if DND outperforms random token selection, the selection mechanism is validated; if not, the improvement may be explained primarily by the extra FLOPs rather than the routing strategy. Without this, the paper's strongest claim ("critical token selection drives improvement") remains plausible but unproven.

### Minor

3. **ITT comparison is under-specified.** The paper states ITT was run "under the same computation cost" (line 203) but does not specify whether the same training data, training steps, or hyperparameter tuning protocol was used. ITT's gain on Qwen3-1.7B (+0.05) is negligible, raising the possibility that ITT was not well-tuned for this setting. A fair comparison requires more transparency about the baseline setup.

4. **Nested pass attention mechanism is underspecified.** The Pack/Unpack mechanism (Eq. 3) compacts selected tokens into a new sequence with new positional embeddings \(E_{\text{pos}}^i\). The paper does not state whether the nested pass (a) uses causal masking, (b) preserves the original token order in the packed sequence, or (c) how \(E_{\text{pos}}^i\) interacts with the model's existing positional encoding (e.g., RoPE). These details matter for assessing potential information leakage or representational degradation.

5. **"Average" aggregation method across benchmarks is not specified.** Tables 1 and 2 report an "Average" without stating whether it is a simple average, weighted average, or normalized score. Simple averages over benchmarks with very different scales (e.g., PIQA ~75 vs. GPQA ~28) are statistically questionable and can be misleading.

### Trivial
None.

## Nice-to-Haves

- **Disentangle the individual contributions of \(\mathcal{L}_{\text{sd}}\) and \(\mathcal{L}_{\text{dp}}\).** The ablation (Table 4) ablates the entire router control (both losses together). Reporting each loss individually would strengthen the analysis.
- **Report the inference-time threshold \(\tau\) value.** The threshold is adjusted during training but the specific value used at inference is not disclosed.
- **Disclose training cost (wall time / FLOPs) of DND vs. vanilla SFT.** Since DND processes selected tokens through an additional nested pass during training, the training overhead should be quantified.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"No comparison at equal compute — the central claim is undersupported."** The paper *does* compare against ITT "under the same computation cost" (line 203). The reviewer's framing that the question is "never asked" is inaccurate. The remaining concern (no random-selection baseline) is retained as Major weakness #2 above.
- **"Selective emphasis in abstract fails to disclose 30B gain."** Factually wrong: the abstract (line 9) explicitly states "the MoE Qwen3-30B-A3B by 0.87%."
- **"MOR should have been compared."** The paper clearly explains that MOR requires training from scratch on 200B tokens (a fundamentally different setting). Criticizing the absence of this comparison exceeds the paper's stated scope.
- **"Training data and hyperparameters are vague."** The paper states "Detailed hyperparameters and training settings are provided in Appendix Sec.B" (line 199), which was stripped during PDF extraction. This criticism is an artifact of the parser, not an author omission.
- **"Individual losses \(\mathcal{L}_{\text{sd}}\) and \(\mathcal{L}_{\text{dp}}\) should be disentangled."** Reasonable but minor; moved to Nice-to-Haves.
- **"\(\beta\) learnable parameter can compensate for scaling issues in \(p^i\)."** This is a standard design choice in gated fusion, not a weakness.
- **"Threshold \(\tau\) at inference is not disclosed."** While not given as a single number, the inference-time selection ratios (0.178–0.242) and the full threshold mechanism description provide sufficient information. Moved to Nice-to-Haves.
- **Various section-by-section notes** that are minor presentation observations or criticise content that would be in the (stripped) appendix.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's most useful observations are the need for error bars and a random-selection baseline — both straightforward extensions that the authors could address — and the underspecification of the nested-pass attention mechanics. The entropy-based validation (Fig. 4a/4b) remains the paper's strongest piece of evidence and is correctly identified as such.

## Suggestions

1. Add 2–3 runs with different random seeds and report standard deviations or confidence intervals for all benchmarks, especially the 30B MoE results. This is essential for the small individual gains.
2. Add an equal-compute ablation that randomly selects the same fraction (20%) of tokens for the nested pass, holding all other settings fixed. This directly tests whether the router's selection mechanism drives improvement beyond extra compute.
3. Explicitly state in the paper: (a) that the nested pass uses causal masking, (b) whether original token order is preserved in the packed sequence, and (c) what positional encoding scheme is used for \(E_{\text{pos}}^i\).
4. Clarify the "Average" aggregation method (simple average? row-normalized?) in Tables 1 and 2.

## Score and Decision

**Score: 6**

**Decision: Borderline Accept**

The paper addresses a well-motivated problem with a carefully engineered solution. The training strategy is non-trivial, the ablation confirms both components contribute, and the entropy-based validation provides genuine insight. The method is practical (post-training, minimal overhead, works on existing models). However, the evaluation has two significant gaps: no statistical significance reporting and no direct test of whether the selection mechanism (vs. extra compute) drives the improvement. These weaken, but do not invalidate, the core contribution. With stronger evidence the paper would be substantially stronger; as presented, it is a solid borderline-accept contribution.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>