Here is the final consolidated review:

---

## Summary

This paper introduces High-Entropy Sum (HES), a training-free metric that sums only the entropy of the top 0.5% highest-entropy tokens in each reasoning sample. HES is designed to overcome the limitation of global metrics (average entropy, perplexity) that dilute informative signal from critical tokens by averaging over long CoT sequences. The paper validates HES across three training paradigms (SFT, RFT, RL), multiple models (Qwen3-8B, DeepSeek-R1-Distilled-7B/1.5B, Qwen3-0.6B/1.7B), multiple datasets, and three domains (math, code, STEM), finding a consistent pattern: selecting high-HES samples improves over random selection while low-HES samples degrade performance.

## Strengths

- **Well-motivated problem framing (Section 1, Section 2.2).** The paper correctly diagnoses why global metrics like average entropy fail in long-CoT contexts: the averaging mechanism dilutes the signal from a small number of critical tokens. This diagnosis is clear, intuitive, and directly motivates the design of HES. The paper shows empirically (Figure 1) that average entropy of all tokens yields nearly identical distributions for correct and incorrect samples (norm means 0.52 vs 0.53), while HES separates them sharply (0.29 vs 0.68).

- **Genuinely simple and cheap metric.** HES requires nothing beyond the token-level log-probabilities already computed during autoregressive generation — no external reward model, LLM judge, or gradient computation. The small-to-large model transfer result (Section 4.1.2, Table 1) demonstrates that a 0.6B model scoring data can train an 8B model to comparable performance (32.12% vs 31.14% with self-selection), achieving over an order-of-magnitude cost savings. This is a practically useful finding.

- **Consistency of the signal across a broad range of conditions.** The pattern holds in virtually every experiment: selecting high-HES samples improves over random selection, and selecting low-HES samples produces severely degraded performance (e.g., Lowest-HES at 14.90% vs Random-20% at 25.89% in Table 1; 13.39% vs 27.83% in Table 5). This monotonic relationship between HES rank and training utility, replicated across SFT, RFT, and RL — across models, datasets, and three domains — is the paper's strongest evidence that HES captures something real about data quality. The validation breadth (three paradigms, multiple models and domains) exceeds what most papers of this type provide.

## Weaknesses

### Major

- **No uncertainty quantification across all experiments.** Every result across all 9 tables reports a single point estimate with no error bars, confidence intervals, or indication of how many random seeds were used. Several headline claims rest on differences of 0.2–2.7 percentage points (e.g., Highest-HES-20% 31.14 vs Highest-ES-20% 30.92 in Table 1; Pos-High Neg-Rand 21.30 vs Full-Batch 20.63 in Table 6). In LLM fine-tuning, single-run variance of 1–2 points is common due to random seeds alone. While the consistency of the directional effect across many conditions partially mitigates this concern, the reader cannot determine whether individual reported differences are statistically meaningful. The paper should report multiple seeds (at least 3) with means and standard deviations for key comparisons (Full-Dataset vs Highest-HES-20%/80% for SFT; per-query Highest-HES vs Random for RFT; Pos-High Neg-Rand vs Full-Batch for RL).

- **Unspecified GRPO advantage computation in RL experiments (Section 4.3).** The paper compares "Full-Batch" (32 rollouts per query) against downsampling strategies using 16 rollouts, but does not specify whether the GRPO advantage $\hat{A}_i = (r_i - \text{mean}(\{r_j\})) / \text{std}(\{r_j\})$ is recomputed from the downsampled group statistics or whether the original 32-rollout statistics are retained. If recomputed from the 16-rollout group, the comparison conflates selection strategy with a change in optimization dynamics (different advantage normalization scale/distribution). If the original statistics are retained, the implementation deviates from the standard GRPO formulation described in Section 2.1. The paper's most striking RL result — "Pos-High, Neg-Rand" (21.30%) outperforming "Full-Batch" (20.63%) — cannot be cleanly interpreted without resolving this confound. The authors should clarify both the implementation and discuss any implications for the comparison.

- **Missing sensitivity analysis for RFT and RL settings.** The sensitivity analysis (Section 4.4, Figures 3–4) only explores the high-entropy token ratio and data selection ratio for the SFT setting. No equivalent analysis is provided for RFT (per-query selection ratio, candidate pool size) or RL (positive/negative sampling ratios, number of downsampled rollouts). This limits the generality of the robustness claims.

### Minor

- **The forking-token mechanism is asserted but not verified in this paper's setting.** The paper frames high-entropy tokens as "critical forking points" where the model makes non-trivial decisions (Sections 1, 2.2, 3.1), borrowing this framing from Wang et al. (2025). An alternative explanation — HES simply measures how atypical or complex a solution path is — is equally consistent with the results. The empirical findings are strong enough to stand without a fully verified mechanism, but the language should be calibrated (e.g., "high-uncertainty tokens" rather than "critical forking points") where the evidence only supports the empirical correlation.

- **In RFT (Table 5), Length is a competitive baseline.** While HES consistently outperforms Random and achieves the best average across conditions, Length achieves 30.67 (vs HES 31.13) in Per-Query k=8, 30.27 (vs HES 31.38) in Per-Query k=2, and 30.45 (vs HES 31.07) in Global Pool k=8. The paper acknowledges this indirectly but could discuss more explicitly where Length works well and where HES provides unique value beyond length-correlated effects.

- **Flat sensitivity on MMLU STEM (Figure 4).** The sensitivity analysis shows that performance on MMLU STEM is essentially flat across all data selection ratios and entropy thresholds (0.855 for all conditions). The paper does not discuss this, leaving unclear whether HES is less informative for this particular domain or the evaluation is saturated.

### Trivial

None.

## Nice-to-Haves

- A qualitative analysis showing example responses with high vs low HES scores would strengthen understanding of what the metric captures.
- In the RL setting, the paper could explore whether HES is informative for selecting among *incorrect* trajectories beyond the Neg-Low ablation (which tests selecting those with lowest HES). The Pos-High Neg-Rand strategy's success over Pos-High Neg-Low suggests that diverse negative sampling matters, but the HES signal for negative examples specifically remains unexplored.

## Removed Points

These points were removed from the input review and should be treated with caution:
- *"No comparison with the most relevant training-free method: response length"* — REMOVED because Length IS included as a baseline in Tables 1, 2, 5, and 6. This was a factual error by the reviewer.
- *"The Full-Dataset and Highest-HES-80% conditions differ not only in data quality but also in total training steps"* — REMOVED because 3 epochs on 80% data means *fewer* gradient updates, making it HARDER for the 80% condition to outperform full-dataset. Any observed improvement is a conservative estimate, not a confound favoring the method.
- *"HES and correctness signal not fully disentangled"* — MOVED to Nice-to-Haves. The paper's scope is selection within correct trajectories for RFT and RL; the Neg-Low ablation partially addresses the question.
- All formatting/style/typos/appendix-related complaints — REMOVED per hard rules (these are parser artifacts or stripped sections).

## Novel Insights

The most striking finding is the asymmetric sampling strategy in the RL setting: pairing the highest-HES positive trajectories with *randomly sampled* negative trajectories outperforms both random downsampling and the full-batch baseline, while constraining negative samples (e.g., selecting lowest-HES negatives) degrades performance. This suggests an asymmetry where careful curation of positive examples (identifying maximally informative correct solutions) combined with diverse (random) negative sampling is more important than fine-grained negative selection — a nuanced insight about RL data composition that goes beyond simply confirming HES works.

## Suggestions

1. Run 3 seeds per key condition (Full-Dataset, Highest-HES-20%, Highest-HES-80% for SFT; per-query Highest-HES vs Random for RFT; Pos-High Neg-Rand vs Full-Batch for RL) and report means with standard deviations.
2. Explicitly state whether GRPO advantage in downsampled conditions uses the downsampled group statistics or the original 32-rollout statistics, and discuss any implications for interpreting the RL comparisons.
3. Add sensitivity analysis for RFT (e.g., varying the per-query selection ratio) and RL (varying positive/negative sampling ratios).
4. Calibrate the forking-token language where the evidence supports only the empirical correlation, not the mechanism.

## Score and Decision

**Calibration Anchors:**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/f4gF6AIHRy.md (DiSF) | 8.00 | 1 | Yes | Significantly stronger — theoretical guarantees, extensive ablations, minimal weaknesses. Our paper is clearly below this. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/I5p1Gm8GFS.md (3DS) | 5.75 | 1 | Yes | Our paper is stronger — 3DS has more severe weaknesses (missing limitations, dataset curation concerns with favorability 0.83). |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/SpTzsQjgxF.md (Rule-Based) | 5.75 | 1 | Yes | Similarly topical but our weaknesses (lowest 2.12) are less severe than Rule-Based's missing-baseline (0.00) and limited-novelty (-6.06). |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/ouRX6A8RQJ.md (Understanding CoT) | 6.40 | 1 | Yes | Our paper has broader validation; their weaknesses include limited applicability (0.80) and computational costs (0.16). Our paper is slightly stronger. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Fty0wTcemV.md (DELIFT) | 6.00 | 2 | Yes | DELIFT has a questionable ICL-based utility metric (favorability 4.22). Our paper's approach and validation are cleaner. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/huuKoVQnB0.md (Perplexity Correlations) | 6.00 | 2 | Yes | That paper's main weakness is tiny scale (-0.84). Our paper tests on larger, more realistic settings. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/BTKAeLqLMw.md (DEITA) | 6.33 | 2 | Yes | DEITA has limited evaluation concerns (-0.18). Our paper uses objective benchmarks. Comparable overall. |

**Round-1 bracket:** [5.75, 7.5]. The paper is clearly stronger than 3DS (5.75) and Rule-Based (5.75), comparable to DEITA (6.33) and Understanding CoT (6.40), and clearly weaker than DiSF (8.00).

**Final score determination:** Comparing itemized favorability ratings: our worst weakness (uncertainty quantification, 2.12) is less damaging than the worst weaknesses of accepted anchors DELIFT (missing baseline 0.80), Perplexity Correlations (small scale -0.84), and DEITA (limited evaluation -0.18). Our top strengths (simple cheap metric 9.58, consistency 9.53) are in the same high range as these anchors' best items. The paper makes a genuine practical contribution with unusually broad validation. However, the unresolved GRPO confound and missing sensitivity analysis for RFT/RL prevent a higher score. The final score is calibrated between DEITA (6.33) and the stronger end of the 6-range anchors.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>