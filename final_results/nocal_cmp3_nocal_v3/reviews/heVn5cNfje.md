## Summary

This paper introduces High-Entropy Sum (HES), a metric that sums the entropy of only the top ~0.5% highest-entropy tokens in a reasoning trajectory, motivated by the observation that averaging entropy over all tokens dilutes signal from critical "forking" decision points. The authors validate HES across SFT, RFT, and RL paradigms using multiple models (Qwen3-8B/1.5B, DeepSeek-R1-Distilled-7B/1.5B) and datasets spanning math, code, and STEM domains. The core empirical finding is that pruning the lowest-HES 20% of SFT data improves 7-benchmark average accuracy from 32.61% (full dataset) to 35.36%, despite using fewer samples and gradient steps.

## Strengths

- **Well-motivated with clear diagnostic evidence.** Figure 1 directly demonstrates that average entropy separates correct from incorrect samples poorly (norm means 0.52 vs. 0.53), while HES separates them cleanly (0.29 vs. 0.68). The grounding in the "forking tokens" concept (Wang et al., 2025) is explicit and the reasoning for why averaging over long sequences dilutes signal is clearly articulated.

- **Thorough experimental scope across three paradigms.** The paper validates HES in SFT, RFT, and RL, with multiple models (Qwen3-8B, DeepSeek-R1-Distilled-7B, Qwen3-1.5B), multiple datasets (Open-Math-Reasoning, Open-R1-220k, DeepScaleR, codeforces-cots, STEM), and 7 evaluation benchmarks. This breadth gives weight to the "unified" framing.

- **SFT 80% result is empirically strong.** Training on the top 80% by HES achieves 35.36% average accuracy vs. 32.61% for the full dataset (+2.75 points on a 7-benchmark average), despite using less data. The control condition (Lowest-HES 20%: 14.90%) provides a striking sanity check that the metric is capturing something real — the gap between highest- and lowest-HES subsets (31.14 vs. 14.90 at 20% ratio) is decisive.

- **Small-to-large transfer experiment is practically valuable.** Using Qwen3-0.6B to score data for training Qwen3-8B (32.12% avg) performs comparably to 8B self-scoring (31.14%) at an order-of-magnitude lower inference cost. This is a concrete practical contribution.

- **RL asymmetric sampling ablation is well-designed.** The Pos-High, Neg-Rand strategy outperforms both the full-batch baseline (21.30% vs. 20.63%) and multiple ablation variants. The negative sampling ablations (Pos-Rand/Neg-Low, Pos-High/Neg-Low) convincingly show that constraining the negative pool hurts performance, supporting the design choice.

## Weaknesses

### Fatal

None.

### Major

- **No variance or statistical significance reported for any result.** Every number in every table is a single point (average@16). There are no standard errors, confidence intervals, or multiple-seed runs. This makes it impossible to assess whether smaller claimed advantages are reliable. The RFT results (e.g., Highest-HES 31.54 vs. Random 29.85 at per-query k=4, a +1.69 gap on the 7-benchmark average) and RL result (21.30 vs. 20.63, a +0.67 gap) could fall within training noise without error bars. The paper uses "significantly" colloquially throughout without any statistical support. While the SFT 80% result (+2.75) and the Lowest-HES 20% result (14.90%) have large enough effect sizes to survive this concern, the smaller-margin comparisons are undermined.

### Minor

- **HES model-dependence is under-characterized relative to the "intrinsic" claim.** The paper states that cross-model transfer "suggests that HES captures intrinsic reasoning complexity inherent to the data, rather than model-specific artifacts" (Sec 4.1.2). The evidence for this claim is limited to same-family cross-size transfer (Qwen3-0.6B → Qwen3-8B). The paper does not test whether HES rankings are stable across training checkpoints of the same model, nor whether rankings from a different model family transfer. Additionally, the paper never explicitly states which model provides the probability distributions for the default (non-transfer) HES computation — from context it is the training model itself, but this should be stated directly.

- **The Length baseline is surprisingly competitive, and the cost-benefit trade-off is not discussed.** In SFT (Table 1), Highest-HES 20% (31.14) edges Length 20% (30.67) by only 0.47 points on average. In RFT (Table 5), Length is frequently within 1 point of Highest-HES and sometimes outperforms it on individual benchmarks (e.g., per-query k=8: HMMT24 — Length 30.21 vs. Highest-HES 28.96). HES requires a full forward pass through a scoring model; Length simply counts tokens at zero marginal cost. The paper claims a "clear advantage over simpler heuristics like length" (Sec 4.1.2), but the data shows the advantage is small and inconsistent. The practical cost-benefit comparison (how much extra compute for how much gain) should be discussed explicitly.

- **Sensitivity analysis reveals domain-dependence that goes unremarked.** In the sensitivity analysis (Figures 3-4), MMLU STEM and LiveCodeBench produce identical scores (0.855 and 0.544 respectively) for all four high-entropy token ratios tested. This means the metric's sensitivity to the p=0.005 threshold is domain-dependent. The paper presents this as supporting robustness but does not discuss why some benchmarks are flat.

- **RL improvement is concentrated on a single benchmark.** The Pos-High, Neg-Rand strategy outperforms Full-Batch by +0.67 on average, but this is largely driven by HMMT24 (14.00 → 18.13, +4.13). Other benchmarks show modest gains (AIME24: +2.09, AIME25: +1.66) or slight regressions (HMMT25: -3.33, GPQA: -1.17). The paper notes the overall result but does not discuss this per-benchmark variance.

- **The Forking-Only baseline achieves nearly identical average performance to Full-Dataset (32.51 vs. 32.61)** despite operating on the same high-entropy tokens but through a different mechanism (gradient masking vs. data selection). This comparison could be discussed to clarify what HES adds beyond the forking-token insight it builds on.

- **The "quality" framing slides between correctness and complexity/informativeness.** In SFT, where all samples are correct, "high quality" means high complexity (many forking points). In RL, HES is applied to both positive (correct) and negative (incorrect) pools, but Figure 1 shows incorrect responses have substantially *higher* HES than correct ones (0.68 vs. 0.29). The paper's language — "quality data," "low-quality data" — is used consistently but lumps together correctness and complexity, which are distinct attributes. This does not invalidate the results but makes the narrative less precise.

### Trivial

- The paper does not explicitly state which model (base model, separate scoring model, or training model) provides the probability distributions for HES computation in the default setting. The context (Table 1, with separate "Highest-HES (0.6B)" rows for transfer experiments) implies the same model being trained is used, but this should be stated directly in the HES definition or experimental setup.

## Nice-to-Haves

- Adding 2–3 random seeds with mean ± std reporting would substantially strengthen the smaller-margin results (RFT, RL) and is the single highest-priority improvement.
- A cross-checkpoint stability experiment (HES rankings from the same model at initialization vs. after partial training) would better support the "intrinsic" claim.
- A direct cost comparison between HES, Length, Perplexity, and training-based methods (wall-clock time, FLOPs) would help practitioners decide when HES is worth the extra compute.

## Removed Points

These points are flagged to be removed — treat them with caution.

- *"Practical cost is not quantified."* Brought forward to Minor above (the Length competitiveness point subsumes this).
- *"RL setup is underspecified relative to DeepScaleR."* The paper states "we train the baseline to its officially reported accuracy" (Sec 4.3.1). This is a standard reporting practice and not underspecified for a conference paper.
- *"Medium Difficulty row has formatting issue / negative value."* This appears to be a parser rendering artifact in the extracted text; the original submission does not have this problem. Removed per hard formatting rules.
- *"The paper overstates the data bottleneck framing (Intro)."* This is a scope-opinion disagreement, not a verifiable weakness. The paper's framing is reasonable for SFT data curation.
- *Section-by-section notes on the Preliminaries and HES Definition that duplicate points already captured above.* Consolidated.

## Novel Insights

The review's most useful insight beyond the paper's own contributions is the observation that the **Length baseline's competitiveness creates a cost-benefit question the paper does not address**. HES requires a full forward pass through a scoring model for every sample, while Length is essentially free. The paper shows HES outperforms Length, but the margins are often small (~0.5 points in SFT, sometimes negative on individual benchmarks in RFT), and the paper frames the advantage as "clear" without quantifying the compute trade-off. A second genuine insight is that the **sensitivity analysis flat curves for STEM/Code benchmarks suggest HES's threshold sensitivity is domain-dependent** — the metric works well on math (where forking points are concentrated) but may be insensitive on benchmarks where reasoning complexity is distributed differently. This is not discussed in the paper but is evident from its own data.

## Suggestions

- Report all main results with standard errors (e.g., mean ± std over 2-3 seeds) to distinguish signal from noise in the smaller-margin comparisons.
- Explicitly state which model provides the probability distribution for HES in every experimental setting, and add a cross-checkpoint transfer experiment if possible.
- Add a brief discussion comparing HES vs. Length on both effectiveness and computational cost, acknowledging when the gap is small and when HES provides meaningful advantage.
- Discuss the domain-dependence of the high-entropy token ratio threshold, noting that some benchmarks are insensitive to this choice.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>