## Summary

This paper introduces TNT, a two-stage training framework for deep memory modules (like Titans) that decouples training efficiency from inference quality. Stage 1 uses a hierarchical memory architecture: a global memory module operating on large chunks for long-range context, and multiple parallel local memory modules whose states are periodically reset to a learned `W_init`, breaking sequential dependencies and enabling context parallelism. Stage 2 fine-tunes only the local memories with smaller chunk sizes. On 150M-parameter models trained on 10B tokens, TNT achieves substantial training speedups (up to 17× against Titans' most accurate configuration) while improving perplexity (best avg 23.13 vs Titans 25.07).

## Strengths

- **Periodic reset mechanism (Eq. 6) is a genuinely clever technical insight.** By resetting local memory states to a learned `W_init` at segment boundaries, non-linear recurrences are broken, making local shards independent and parallelizable. This cleanly addresses a real bottleneck acknowledged by prior work on Titans/TTT and is the paper's strongest conceptual contribution.

- **Strong speedup evidence in controlled settings.** Table 1 shows TNT reaches a fixed training loss substantially faster than Titans across multiple chunk sizes. At identical local chunk size (C_L=8 vs Titans C=8), TNT achieves 7.68× speedup, isolating the hierarchical architecture's contribution. Figure 4's linear scaling (TNT flat at ~400ms while Titans climbs to ~4000ms at 32K) is visually compelling and practically meaningful.

- **Clear empirical demonstration of chunk-size sensitivity (Challenge 3, Figure 2).** Showing that a model trained with C=64 degrades when evaluated at other chunk sizes provides concrete motivation for the two-stage design, rather than relying on speculation.

- **Well-structured ablation study (Table 3).** Each component (global memory, Q-K projection, Stage 2 fine-tuning, number of local modules) is ablated cleanly, providing strong empirical support for the design choices. The ~1 PPL degradation when Q-K projection is removed (21.04 vs 22.01) validates its utility.

- **Consistent quality improvements over Titans baselines.** TNT achieves better perplexity than all Titans configurations (best avg PPL 23.13 vs Titans' best 25.07) and improves average commonsense reasoning accuracy (41.0% vs 39.0%), demonstrating that the speedups do not come at the cost of quality.

## Weaknesses

### Major

- **Stage 2 fine-tuning improvements lack statistical support.** The per-module PPL differences between Stage 1 and Stage 2 are very small (best-to-best: 23.13 vs 23.09, a 0.04 difference; single-module: 24.10 vs 23.99, a 0.11 difference). No variance, confidence intervals, or multiple-seed results are reported anywhere in the paper. At 150M scale on 10B tokens, differences of this magnitude could easily fall within run-to-run noise. The claim that Stage 2 "consistently lowers the average perplexity" is not supported by the evidence as presented. This is the paper's most significant empirical weakness, as it undermines a core structural claim of the two-stage framework.

- **Abstract claims evaluation on TTT models, but no TNT-on-TTT experiments appear in the main paper.** The abstract states "Evaluated on Titans and TTT models," and the paper claims TNT is "a general training paradigm applicable to any deep memory module." However, only Titans experiments are presented for TNT — TTT appears only as a baseline. If TTT results exist in the appendix (stripped by the parser), they should be moved to the main paper; if not, the claim should be retracted.

- **Parameter count control between TNT and baselines is not clarified.** The paper states "150M parameter models" but does not specify whether this refers to total parameters or per-module parameters. TNT with N local modules plus a global module could have either more total parameters (if each module matches the baseline module size) or smaller individual modules (if total is held constant). This affects how the perplexity improvements should be interpreted. The paper must disclose whether parameter counts are matched and, if so, how they are distributed across modules.

### Minor

- **The headline 17× speedup is against the slowest (most accurate) Titans configuration (C=8).** While the paper honestly labels this as "most accurate baseline configuration" and reports the more comparable same-chunk-size speedup (7.68× at C=8, 3.73× at C=64) elsewhere, this framing disparity reduces trust. A reader might reasonably expect the primary comparison to be against the most relevant baseline, not the one that maximizes the ratio.

- **Stage 2 results in Table 2 use different chunk-size configurations than Stage 1** (e.g., Stage 1 best uses {4,8,16,32}, Stage 2 best uses {2,4,8,16}), making it difficult to isolate the fine-tuning effect from the effect of changing chunk configurations. The ablation in Table 3 provides a cleaner comparison (+1 local: 21.04 → 20.86 with Stage 2, ~0.18 improvement) but still lacks variance.

- **Challenge 2 (query-key domain mismatch) framing somewhat overstates the issue.** The Q-K projection ablation does show a meaningful ~1 PPL degradation when removed, but labeling this a "fundamental inconsistency" rather than a useful architectural improvement is stronger language than the evidence demands.

## Nice-to-Haves

- Reporting runtime with and without Q-K projection would help quantify its overhead
- FLOPs utilization numbers for TNT vs baselines would strengthen the Challenge 1 motivation
- Inference-time speed comparison (the paper motivates C'_L=1 inference but doesn't benchmark it)

## Removed Points

These points are flagged to be removed, treat them with caution:
1. **Q-K projection cost as "unaccounted for, undermining speed comparison"** — The reviewer's critique is speculative ("if the ablation is faster, which the paper does not report"); no evidence is provided that this cost is significant enough to affect conclusions.
2. **"17× speedup is cherry-picked"** — The paper transparently states "most accurate baseline configuration" and reports same-chunk-size comparisons. The framing is honest, though the choice of emphasis is debatable.
3. **"Transformer baselines beating TNT should be told explicitly"** — The paper already states this explicitly (line 233: "our implementation does not yet outperform... This is an expected result, as TNT currently lacks a custom kernel").
4. **"Challenge 2 is debatable"** — The ablation shows a real ~1 PPL improvement; the reviewer's framing preference is subjective and the evidence supports the mechanism's value.
5. **Missing Table 4 / appendix content** — Per policy, the parser strips appendices; these existed in the original submission.
6. **No inference-time speed comparison** — Outside the paper's stated scope (training efficiency focus).

## Novel Insights

The key insight — that periodic resetting of local memory states to a learned initial state enables massive context parallelism for non-linear deep memory modules — is genuinely useful and distinct from prior parallelization attempts. The two-stage framing (efficiency pretraining → performance fine-tuning) is a clean way to decouple training and inference requirements that prior work conflates in a single chunk-size hyperparameter. However, the Stage 2 results need stronger evidence to make this framing fully convincing.

## Suggestions

1. **Run multiple seeds (≥3) for Stage 2 and report mean ± std.** This is the single highest-leverage fix: it would either confirm the small PPL improvements are real or reveal they are within noise.
2. **Clarify parameter matching.** State explicitly whether TNT and Titans models have the same total parameters and, if so, how they are distributed.
3. **Either add TTT-based TNT results or revise the abstract.** The generalizability claim is important; it should be backed by evidence or moderated.
4. **When reporting Stage 2 in Table 2, fine-tune from the same Stage 1 configuration** to enable clean isolation of the fine-tuning effect.

## Score and Decision

**Calibration anchors retrieved:**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| 5lUdTogEL3 (person re-ID) | 1.00 | R1 | No | Unrelated topic, score not useful |
| JOBokGDcX0 (sequence segmentation) | 2.50 | R1 | No | Tangentially related, lower contribution |
| E34AlVLN0v (parallelizing non-linear seq) | 6.00 | R2 | Yes | Very similar core problem; TNT has more practical evaluation (150M models, 10B tokens) but weaker statistical rigor on Stage 2 |
| TvGPP8i18S (MELODI) | 6.25 | R1/R2 | Yes | Hierarchical memory for long contexts, accepted; TNT has stronger training speedup evidence but weaker Stage 2 support |
| TrKRpaOk8y (LongGen) | 6.40 | R1/R2 | Yes | Efficient long-context training, accepted; comparable empirical depth, TNT has more novel core idea |
| GrmFFxGnOR (minLSTM/minGRU) | 5.00 | R2 | Yes | Simplifying RNNs for parallelization; lower score due to novelty concerns, TNT has cleaner novelty |
| UU9Icwbhin (RetNet) | 4.75 | R2 | Yes | Chunkwise recurrence; lower score due to overclaiming, TNT has similar overclaiming issues but a stronger core mechanism |
| PHXLbaq822 (HCFR alignment) | 4.33 | R1 | No | Different topic, not useful for calibration |
| zLwCT9srfo (H-Rockmate) | 5.00 | R1 | No | Re-materialization, different topic |
| fDZumshwym (hierarchical feature sharing) | 5.75 | R2 | No | Dataset condensation, different topic |

**Bracket analysis:** Round 1 identified a plausible range of 5.5–7.5. Round 2 narrowed this by comparing against E34AlVLN0v (6.00), GrmFFxGnOR (5.00), and UU9Icwbhin (4.75). TNT's core contribution (periodic reset) is stronger than minGRU's simplification (5.00) and RetNet's retention mechanism (4.75). Its practical speedup evidence compares favorably to the parallelizing-nonlinear paper (6.00). However, its Stage 2 statistical weakness and abstract overclaiming prevent it from reaching the 6.4+ level of LongGen.

The draft's impact scores show the strongest downward-pulling weaknesses are the Stage 2 statistical fragility (~ -10) and the TTT generalizability overclaim (~ -10). These are comparable in severity to the "limited tasks" weakness in E34AlVLN0v (impact -9.54) and the "novelty overlap" weakness in minGRU (impact -10.0). However, unlike minGRU where the core novelty was challenged, TNT's Stage 1 contribution (periodic reset + hierarchical memory + speedups) remains solid. The paper's strongest upward-pushing items (ablation study at +10, chunk-size sensitivity at +9.86, speedup evidence at +9.20) position it above the 5.0–6.0 band.

**Final placement:** 6.0 — solid borderline accept. The core technical insight is novel and well-supported by the Stage 1 experiments. The paper's central weakness (Stage 2 statistical rigor) is fixable but in its current form limits confidence in a key structural claim. The abstract overclaim on TTT should be corrected.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>