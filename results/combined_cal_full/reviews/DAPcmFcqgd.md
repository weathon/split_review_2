Now I have all the information I need. Let me write the final review.

## Summary

This paper introduces MoEP (Modular Expert Paths), a sparse decoder-only architecture that interleaves two dense GPT-2 layers with a stack of smaller-dimension parallel blocks. It uses two levels of MoE-style routing — shrink/grow MoE blocks to transition between dimensionalities, and top-k token selection among parallel blocks — to achieve selective activation without increasing the total parameter count relative to the dense GPT-2 baseline (28M). The model is evaluated on the BabyLM strict-small track.

## Strengths

- **Genuinely novel architecture.** The MoEP design — interleaving dense layers with a parallel stack of smaller-dimension blocks, using MoE-style routing at two levels — is a creative synthesis that is not an incremental tweak of existing methods. (Section 3, Figure 2)

- **Well-motivated problem.** Adding sparsity (selective activation) without increasing total parameter count relative to a dense baseline is a worthwhile goal, and MoEP is a concrete, non-obvious approach to it.

- **Standardized, reproducible evaluation.** The experiments follow the BabyLM strict-small pipeline (fixed corpus, shared evaluation, released code and weights), enabling direct reproduction. (Section 4)

- **Informative training-dynamics analysis (Appendix A.3).** The analysis shows MoEP reaches peak fast-evaluation score at 30M words (earlier than the SwiGLU variant) and reveals overfitting patterns, giving insight into how the architecture learns during training.

## Weaknesses

### Major

- **Selectively framed headline claim.** The Introduction (line 31) states that "MoEP was able to outperform all BabyLM strict-small baseline models." This is misleading. On the primary macro average (excluding AoA), MoEP scores 49.00 — substantially below all three GPT-BERT variants (52.40–54.10). The claim holds only on the secondary metric that includes AoA (44.50 vs. 37.40–41.20), where MoEP's advantage is driven almost entirely by its extreme AoA score. The paper's own Section 5.1 adds the caveat "when the AoA task score was included," but the initial framing does not. (Table 1, lines 31, 166)

- **Unexplained AoA outlier.** MoEP scores 53.70 on the AoA task, while every baseline scores between -3.90 and 14.50. This 4× gap is never explained, contextualized, or even acknowledged as anomalous. The paper notes that baseline AoA scores come from the BabyLM leaderboard, but MoEP's score is reported without clarifying whether the same evaluation protocol and checkpoint selection were used. If real, this is a major finding requiring analysis; if a protocol discrepancy, it undermines the headline. (Table 1, line 197)

- **Efficiency/sparsity claims unsubstantiated by compute metrics.** The title promises "Compact and Efficient Sparsity" and the abstract says MoEP "add[s] sparsity while keeping the total parameter count fixed." However, sparsity concerns activated computation, not stored parameters. The paper reports no FLOPs, inference throughput, wall-clock training time breakdown, or memory footprint comparison. Without any compute metric, the efficiency framing is asserted rather than demonstrated. (Entire paper; see also the MOEfication anchor review at /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/762u1p9dgg.md, which received a similar criticism about missing wall-clock time at weight -5.39.)

- **Contribution 3 (routing analysis) is undelivered.** The paper states "We analyze expert networks routing behavior" as a main contribution (Section 1, line 39), yet the paper contains no analysis of routing patterns: no expert utilization statistics, no routing entropy over training, no analysis of which parallel blocks are selected by which tokens, no load-balancing effectiveness data, and no ablation of top-k. The training-dynamics analysis (Appendix A.3) studies task scores over time, not routing behavior. This stated contribution is unfulfilled.

### Minor

- **Small advantage over the authors' own GPT-2 with no variance reporting.** MoEP (49.00) beats the authors' GPT-2 reimplementation (48.10) by only 0.9 points on macro avg excl. AoA. A single seed (42) is used throughout; no confidence intervals, standard deviations, or significance tests are reported. The authors' GPT-2 already outperforms the official HF GPT-2 by 1.5 points, so much of MoEP's apparent advantage over the baseline is attributable to the training configuration, not the architecture. (Table 1, Table 3)

- **Gating mechanism underspecified.** The paper states that a "linear router ... applies a token-level top-k selection" and "routed inputs are summed up together," but does not specify the gating function (softmax, sigmoid, or otherwise), whether routing probabilities weight the selected outputs or merely select them, or how the MoE shrink/grow gating operates. The load-balancing loss uses entropy (−∑ p_i log p_i), which is non-standard for MoE routing, and the λ hyperparameters are not reported. (Section 3.3, Section 3.4)

- **MoEP-SwiGLU comparison is confounded.** The SwiGLU variant has 38M vs. 28M parameters (36% more) and peaks later in training (80M vs. 30M words). It is unclear whether its lower performance reflects an architectural deficiency or simply insufficient training for the larger model. (Table 1, Table 2, line 152)

### Trivial

None.

## Nice-to-Haves

- Ablations of key design choices (number of parallel blocks P, top-k values, with/without load-balancing loss, with/without MoE shrink/grow blocks) would strengthen the architectural claims.
- A discussion of training stability and whether collapse actually occurs without the load-balancing loss.

## Removed Points

These points are flagged to be removed, treat them with caution:
- Generic criticisms about evaluation rigor without specific paper anchors.
- Speculation about fast-evaluation/test-set overlap (not verifiable from paper).
- "Counting task wins is a weak argument" — subjective rhetorical judgment, removed.
- Formatting/style nitpicks (parser artifacts).
- Missing related works (no external sources to confirm).
- All removed points from the "Section-by-Section Notes" that are not anchored to specific evidence.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Revise the evaluation narrative to honestly state: MoEP modestly exceeds GPT-2 baselines but substantially underperforms GPT-BERT models on the primary macro average. Either explain the AoA anomaly or drop claims that depend on it.
2. Add FLOPs and throughput comparisons for training and inference to substantiate the efficiency/sparsity framing.
3. Deliver the promised routing analysis (expert utilization, routing specialization, load-balancing effectiveness).
4. Report results across multiple seeds with variance.
5. Specify gating details and report λ values for the load-balancing loss.

## Score and Decision

### Calibration Anchors

| Path | Avg Score | Round | Itemized | Comparison |
|---|---|---|---|---|
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/762u1p9dgg.md | 3.40 | 1 | Yes | Most similar: both propose novel MoE-style sparsification, claim efficiency without measuring FLOPs/wall-clock, and have evaluation limitations. MoEP has stronger benchmarking (BabyLM) but suffers from misleading evaluation framing. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/04RLVxDvig.md | 3.00 | 1 | Yes | Similar: novel parameter-efficient MoE variant with weak empirical validation. MoEP has more thorough evaluation (14 tasks vs. AG News classification). |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/UUZuwDv8iw.md | 4.33 | 1 | Yes | Less comparable: comprehensive empirical study of expert pruning, not a new architecture. Better executed empirically but different contribution type. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/rWui9vLhOc.md | 6.33 | 1 | Yes | Less comparable: MoLEx is a PEFT method on pre-trained models, not a new architecture. More mature experimental execution but different scope. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/B9XP2R9LtG.md | 5.25 | 2 | Yes | Less comparable: studies activation sparsity measurement, not an architecture. Better executed but different paper type. |

**Round 1 bracket:** 3.0–4.5.

**Final score determination:** The paper shares its most critical weakness with the MOEfication anchor (3.40): both claim efficiency/sparsity benefits without measuring actual compute metrics. The MOEfication paper's missing wall-clock time (-5.39) and inappropriate activation ratio metric (-6.36) closely mirror MoEP's missing FLOPs/throughput (-7.02). MoEP has stronger benchmarking (BabyLM vs. MOEfication's limited baselines) but adds additional integrity concerns (selective AoA framing, -3.61; unexplained AoA outlier, -2.93; undelivered routing analysis, -5.64) that the MOEfication paper does not have. Conversely, the architectural novelty is genuine and the training-dynamics analysis is informative. On balance, the paper is slightly above the MOEfication anchor due to better benchmarking infrastructure but pulled down by evaluation integrity issues. The score rounds to 3.5.

MY FINAL SCORE: <score>3.5</score>
MY FINAL DECISION: <decision>Reject</decision>