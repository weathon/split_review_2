Now I have all the calibration data needed. Let me compose the final review.

## Summary

This paper introduces MoEP (Modular Expert Paths), a decoder-only architecture that combines parallel Transformer blocks with MoE-style top-k routing while keeping the total parameter count fixed by operating at reduced hidden dimension. The model is evaluated on the BabyLM strict-small track (10M-word training corpus) across ~15 evaluation tasks and compared against GPT-2 and GPT-BERT baselines.

## Strengths

- **Architecturally novel framing (Sections 3, Figure 2).** The core idea — combining parallel Transformer blocks with MoE-style top-k routing while keeping total parameter count fixed by operating at reduced hidden dimension — is a genuine architectural contribution. The paper identifies a real tension in standard MoE (increased total parameters despite sparse activation) and proposes a reasonable mechanism to address it: shrink the hidden dimension, replicate blocks in parallel, and route tokens sparsely through them.

- **Faithful BabyLM protocol adherence (Section 4).** The evaluation follows the official BabyLM strict-small pipeline, including the tokenizer, training data, evaluation tasks, and fine-tuning setup. This enables apples-to-apples comparison with published baselines from the BabyLM leaderboard, which is a non-trivial engineering effort.

- **Code and model release.** The paper states that code and model weights are released, supporting reproducibility.

## Weaknesses

### Major

- **Overstated central claim in the Introduction (line 31).** The Introduction states "MoEP was able to outperform all BabyLM strict-small baseline models, including the GPT-2 and GPT-BERT models as well." This is contradicted by the paper's own Table 1: on macro average **excluding AoA** (the more standard aggregate metric), MoEP scores **49.00** while GPT-BERT (causal) scores **54.10**, GPT-BERT (focus-causal) scores **53.65**, and GPT-BERT (mixed-causal) scores **52.40** — MoEP is 3.4–5.1 points behind all GPT-BERT variants. Section 5 (line 166) honestly qualifies this ("when the AoA task score was included in the Macro Average"), but the Introduction's unqualified claim is misleading. The paper's best claim to "highest performance" relies entirely on the inclusion of a single high-variance task (AoA) where MoEP scores 53.70 while GPT-BERT variants score between -3.90 and 14.50 — a swing so large it is never explained or justified. This selective-reporting issue undermines reader trust in the paper's framing.

### Minor

- **Marginal improvement over the direct dense baseline without significance testing.** MoEP (28M params) achieves macro avg 49.00 vs. the paper's own GPT-2 re-implementation (28M params) at 48.10 — a **0.9-point** difference on an aggregate over ~15 tasks. No confidence intervals, standard deviations, or significance tests are reported. The paper's own GPT-2 re-implementation outperforms the official BabyLM GPT-2 baseline (46.60) by **1.5 points** — a larger gap than MoEP's improvement over its own GPT-2 (0.9 points). This suggests that implementation-level tuning may account for as much variance as the architectural change.

- **No efficiency or throughput measurements despite sparsity being a core motivation.** The paper motivates MoEP through efficiency (Abstract: "selective token activation, which accelerates model learning"; Introduction and Section 2 extensively discuss efficiency-oriented prior work such as Switch Transformers, Branchformer, THOR, DS-MoE) but provides zero quantitative efficiency analysis — no FLOP counts, throughput, latency, or wall-clock training time comparisons. The checkpoint analysis in Appendix A.3 partially supports a faster-learning claim ("MoEP extracted useful patterns earlier during training"), but the broader efficiency narrative is unsubstantiated.

- **Oracle checkpoint selection inflates reported scores.** The final weights are chosen from the checkpoint with best evaluation performance across ~18 checkpoints (Section 4, line 152). While applied consistently across all models, this procedure does not reflect a fixed training budget and may overstate each model's true performance. The paper would benefit from also reporting performance at a fixed training step.

### Trivial

- **Load-balancing regularizer callout.** The regularizer (Equation 2) uses entropy maximization (−∑p_i log p_i), which differs from the more common importance-weighted auxiliary loss used in standard MoE work (e.g., Fedus et al. 2022, DeepSeek-AI et al. 2024). The paper calls this "the standard load-balancing regularizer" (line 126) without noting the distinction or reporting the λ values for λ^{block} and λ^{expert}, which hinders reproducibility.

## Nice-to-Haves

- Measuring FLOPs per token and/or wall-clock training time would directly substantiate the efficiency motivation.
- Running multiple seeds and reporting confidence intervals would clarify whether the 0.9-point gap over the dense baseline is meaningful.
- Explaining why MoEP achieves such dramatically better AoA scores than GPT-BERT (53.70 vs. -3.90 to 14.50) would strengthen the paper's claims about its architecture's capabilities.

## Removed Points

These points are flagged to be removed; treat them with caution:

- "OpenAI et al. (2025) is not a conventional reference": Removed. The paper cites it; it exists.
- "MoLE prior art makes the novelty gap thin": Removed. The paper acknowledges MoLE (line 90) and describes the area as "relatively unexplored," which is accurate given only one prior work.
- "Missing AoA scores for MoEP-SwiGLU and own GPT-2": Removed. The paper explicitly addresses this in line 197.
- "Table formatting nitpicks": Removed as parser artifacts.
- "Abstract overclaims": Removed. The Abstract (line 9) only claims to "outperform the GPT-2 baseline," which the data supports.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Restructure results to prominently report macro averages both with and without AoA, and directly address why MoEP underperforms GPT-BERT on the excluding-AoA metric.
2. Measure FLOPs per token and/or wall-clock training time to substantiate the efficiency motivation.
3. Run multiple seeds and report confidence intervals.
4. Replace or supplement oracle checkpoint selection with fixed-step performance reporting.
5. Report λ values for the balancing loss and motivate the entropy-based formulation.

## Score and Decision

**Calibration details.**

I retrieved anchors from two calibration rounds. The first round used topic queries about mixture-of-experts/sparse transformers/compact parameter count. From the resulting bands, the most relevant anchors were:

| Anchor | Path | Avg Human | Round | Itemized? | Comparison |
|--------|------|-----------|-------|-----------|------------|
| NanoMoE | 04RLVxDvig.md | 3.00 | R1 | Yes | Weaker experiments (toy problems only); my paper has stronger empirical evaluation on BabyLM but shares the issue of missing efficiency measurements |
| MOEfication by Masks | 762u1p9dgg.md | 3.40 | R1 | Yes | Similar weakness re: no wall-clock efficiency; my paper has more original architecture |
| MO-CTE | thqPibDg6A.md | 4.40 | R1 | Yes | Similar tier of contribution; both have limited evaluation scope and presentation gaps |
| PERFT | PPjpGTPG5K.md | 5.33 | R1 | Yes | Rejected despite 5.33 due to lack of novelty (A+B work); my paper is more novel architecturally but has overstated claims |
| MoLEx | rWui9vLhOc.md | 6.33 | R1 | Yes | Stronger experiments on established benchmarks (GLUE); accepted |
| Merge-Then-Compress | eFWG9Cy3WK.md | 6.33 | R1 | Yes | Extensive ablations and strong empirical support; accepted |

**Round 1 bracket:** After comparing my draft's weighted items against the anchors, I identified the plausible range as 3.5–5.5.

**Round 2 narrowing:** I itemized PERFT (avg 5.33, rejected) and MO-CTE (avg 4.40, rejected) for closer comparison. My paper shares MO-CTE's level of contribution (both propose novel MoE approaches with moderate-scale evaluation) but has an additional credibility issue from the overstated Introduction claim that PERFT (whose weakness was lack of novelty) does not share. Meanwhile, my paper has a genuinely novel architecture that PERFT lacks.

**Final placement:** The weighted-item comparison shows my strengths (8.20–9.36) are comparable to those of MO-CTE (8.20–9.64) and PERFT (7.50–10.63). However, my major weakness (overstated claims, weight 1.49) is more damaging than the typical "lack-of-detail" weaknesses in the 4–5 range anchors because it undermines trust in the paper's framing. Combined with the marginal empirical improvement (0.9 points, weight 0.70), the paper's evidence does not reach the acceptance bar. I place it just below the borderline: the architectural idea is interesting but the experimental support is insufficient and the presentation is misleading.

**Score:** 4.0 (borderline reject)

**Decision:** Reject

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>