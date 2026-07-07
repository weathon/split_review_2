Now I have a clear calibration picture. Let me finalize the review.

## Summary

This paper proposes High-Entropy Sum (HES), a metric that sums only the entropy of the top 0.5% highest-entropy tokens in a reasoning trace, motivated by the observation that global entropy averaging washes out signal from critical reasoning forks. HES is validated across three training paradigms (SFT, RFT, RL), two model families, three domains (math, code, STEM), and multiple benchmarks. The core finding is that data selection via HES improves both sample efficiency and performance, and that HES scores computed by a small proxy model can transfer to larger models.

## Strengths

- **Clean, well-motivated core idea.** Section 3.1 and Figure 1 convincingly demonstrate that global entropy averaging masks the signal from critical reasoning forks, and focusing on the tail of the entropy distribution is a simple, interpretable fix. This is a genuine conceptual contribution grounded in token-level analysis.

- **Unusually broad experimental scope.** The paper validates HES across SFT, RFT, and RL; two model families (Qwen3-8B, DeepSeek-R1-Distilled-7B/1.5B); three domains (math, code, STEM); and 7+ benchmarks. The small-to-large model transfer experiment (Qwen3-0.6B screening data for Qwen3-8B, achieving comparable performance at far lower cost) is a particularly practical contribution.

- **The Lowest-HES ablation is a strong sanity check.** Training on the bottom 20% by HES yields AVG 14.90% vs. Full-Dataset's 32.61% (Table 1), confirming that HES captures meaningful variation in data quality rather than noise. This alone shows the metric is not arbitrary.

- **Sensitivity analysis adds robustness evidence.** Figures 3-4 explore two hyperparameters (data selection ratio, high-entropy token ratio) across multiple benchmarks and confirm that the relative choice (0.005) consistently delivers the best performance, and the method is stable across a range of settings.

## Weaknesses

### Fatal
None.

### Major
- **Absence of uncertainty quantification.** Every result is a single-point estimate (average@16, temp 0.6). No confidence intervals, standard errors, bootstrap estimates, or multiple-seed runs are reported anywhere. This is a significant evidential gap because several central claims rest on small margins:
  - **RL (Table 6):** Pos-High, Neg-Rand achieves 21.30% vs. Full-Batch's 20.63% — a **0.67pp** gain. Without variance estimates, it is unclear whether this difference is reliable.
  - **RFT (Table 5):** Per-query gains over Random are +1.01pp (k=2), +1.69pp (k=4), +0.97pp (k=8). These small, consistent margins are directionally supportive but lack formal evidence.
  - The paper repeatedly uses "significantly outperforms" (lines 159, 206, 232, 278, 307) without any statistical evidence — no p-values, no standard deviations.
  
  The larger SFT margins (e.g., HES-80% at 35.36% vs. Full-Dataset at 32.61%, a 2.75pp gain in Table 1; HES-20% at 34.61% vs. Full-Dataset at 30.22%, a 4.39pp gain in Table 2) are less concerning, but the smaller-margin claims in RL and RFT need variance estimates to be fully credible.

### Minor
- **Model source for computing token probabilities is unspecified.** The paper never states which model computes the token probabilities $P_t(j)$ for HES during data selection in the main SFT/RFT experiments. For SFT on Open-Math-Reasoning with Qwen3-8B, is HES computed using the untrained base model? The small-to-large transfer experiment (0.6B/1.7B proxy → 8B target) implies this choice matters, but it is not addressed. This is a reproducibility gap.

- **Flat MMLU STEM and LiveCodeBench results in sensitivity analysis are unexplained.** Figure 4 shows MMLU STEM achieving identical average scores (0.855) across all four high-entropy token ratios and all data selection ratios. LiveCodeBench similarly shows 0.544 for all ratios. This suggests either (a) HES is not selecting informative data for these benchmarks, or (b) the benchmarks are saturated. Neither possibility is discussed, leaving a null result unaddressed.

- **Framing of HES as a "reasoning quality" metric is imprecise.** Figure 1 shows that incorrect responses have *higher* HES than correct responses (incorrect mean 0.68 vs. correct mean 0.29). HES primarily captures reasoning complexity/difficulty, not correctness-based quality. The paper handles this correctly in practice (filtering for correctness before applying HES in RFT and RL, using fully-correct SFT data), but the rhetoric throughout claims HES measures "quality" when it more accurately measures *reasoning complexity within correct solutions*. Including qualitative examples of high- vs. low-HES correct responses would clarify what the metric captures.

- **RL experiments limited to 1.5B model.** The RL experiments (Table 6) use only DeepSeek-R1-Distilled-Qwen-1.5B, following DeepScaleR-1.5B-Preview. It is unclear whether the HES selection benefit in RL generalizes to larger models where RL is more commonly applied (e.g., 7B+). The paper should either verify on a larger model or explicitly acknowledge this scope limitation.

- **Forking-Only baseline threshold unspecified.** The Forking-Only baseline (Table 1) is described only as "applying gradient updates only to the high-entropy tokens (Wang et al., 2025)" without specifying what threshold or ratio is used. Since HES also focuses on high-entropy tokens, the comparison is informative only if the selection mechanism is matched.

### Trivial
None.

## Nice-to-Haves
- Add bootstrap confidence intervals or standard errors for all headline comparisons (especially RL Table 6 and RFT Table 5 where margins are small).
- State the exact model used for computing HES token probabilities in each experimental setting.
- Include 2-3 qualitative examples of correct responses with high vs. low HES, with token-level entropy visualizations, to build intuition.
- Discuss the flat MMLU STEM / LiveCodeBench results — is HES not informative for these benchmarks, or are they saturated?
- Provide GPU-hour estimates for computing HES at the reported data scales.
- Disclose the prompt format used for evaluation on each benchmark.

## Removed Points
- *"Inconsistent baselines weaken the SFT case"* — REMOVED: The critic claims the paper treats "matching full-dataset performance" as a positive result for Table 2, but the paper's actual discussion (line 159) is about Table 1. For Table 2, the paper correctly notes HES-20% (34.61%) surpasses Full-Dataset (30.22%) by a large margin, which is factually true and not undermined by Random-20% (30.38%) also slightly exceeding the full dataset.
- *"The 'unified framework' claim overstates"* — REMOVED: The same HES metric is used across all three paradigms; application details differ because the paradigms have different structures, which does not make the label "unified" inaccurate.
- *"No discussion of prompt format"* — MOVED to Nice-to-Have (trivial reproducibility detail).
- *"Computational cost"* — MOVED to Nice-to-Have (paper frames HES as "training-free" — correctly, since no training is needed — and the small-to-large transfer experiment mitigates cost concerns).
- *"HES measures difficulty not quality — critical issue"* — DEMOTED to Minor. The paper correctly applies HES only within correct-solution pools. The framing could be more precise, but this does not undermine any claimed result.

## Novel Insights
None beyond the paper's own contributions. The calibration review surfaces no fundamentally new observation about the method or results beyond what the paper already presents — the main value added is the identification of the missing uncertainty quantification as the most impactful weakness.

## Suggestions
1. **Add confidence intervals** (bootstrap over the 16 generations per problem, or standard errors from multiple seeds) to all headline comparisons before any camera-ready version. This is the single highest-leverage improvement.
2. **Explicitly state which model computes HES** token probabilities in each experimental setting.
3. **Discuss the flat MMLU STEM / LiveCodeBench results** in the sensitivity analysis section — even a brief acknowledgment of why these benchmarks show no differentiation would strengthen the paper.
4. **Add qualitative examples** of high- vs. low-HES correct responses to build intuition for what the metric captures.
5. **Clarify the Forking-Only baseline threshold.**

## Score and Decision

**Round 1 bracket:** 5.5–6.5

**Calibration anchors retrieved:**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| qUJsX3XMBH (Random Selection Almost All You Need) | 4.40 | R1 | Yes | Weaker: that paper's main finding was undercut by existing literature; our paper has a genuine novel metric |
| Fty0wTcemV (DELIFT) | 6.00 | R1, R2 | Yes | Comparable: both have solid contributions and similar-level weaknesses (~-3 to -4 range), but our paper validates across 3 training paradigms vs. 3 stages of fine-tuning |
| BTKAeLqLMw (What Makes Good Data) | 6.33 | R1, R2 | Yes | Comparable: our paper has similar strength weights but broader evaluation across objective benchmarks (vs. GPT-4 evaluation); that paper had more severe novelty-critique weaknesses (-8.58) |
| SpTzsQjgxF (Rule-Based Rating) | 5.75 | R2 | Yes | Weaker: that paper had a -11.06 innovation criticism; our paper's weaknesses are less severe |
| I5p1Gm8GFS (3DS) | 5.75 | R2 | Yes | Weaker: that paper had -5.90 for imprecise methodology; our paper is more clearly motivated |
| f4gF6AIHRy (Combatting Dimensional Collapse) | 8.00 | R1 | Yes | Stronger: clearly in a different tier with much higher strength weights and minimal weaknesses |

**Weighted-item comparison:** Our strongest positive weights (+4.64, +4.72) align well with the 6.00 (DELIFT: +4.72, +5.70) and 6.33 (BTKAeLqLMw: +4.94, +4.55) anchors. Our strongest negative (-3.19 for no uncertainty quantification) is comparable to DELIFT's strongest negative (-4.20) and less severe than the 6.33 anchor's strongest negatives (-5.51, -5.18, -8.58). The critical factor pushing us toward the lower end of this range is that the uncertainty quantification gap is a rigor issue affecting the evidential strength of small-margin claims in RL and RFT, whereas the stronger anchors in the 6.0–6.3 range did not face such evidential concerns about their core results.

**Final score:** 6.0 — The paper has a genuine, well-motivated contribution (the HES metric) with unusually broad validation across paradigms and domains. However, the systematic absence of uncertainty quantification weakens the smaller-margin claims in RFT and RL, and several minor presentation/reproducibility gaps should be addressed. These are fixable issues, not structural flaws.

**Decision:** Accept

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>