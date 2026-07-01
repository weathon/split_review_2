## Summary

This paper proposes High-Entropy Sum (HES), a training-free metric for selecting high-quality reasoning data. HES focuses on the top 0.5% highest-entropy tokens in a response — the "forking points" where models must make non-trivial decisions — rather than averaging entropy over all tokens which dilutes these critical signals. The paper validates HES across SFT, RFT, and RL, on Qwen3 and DeepSeek-R1-Distilled models, across math, code, and STEM domains. Key findings: (1) training on the top 20% HES-selected data matches full-dataset SFT performance; (2) pruning the lowest-HES 20% consistently improves performance; (3) in RL, HES-selected positive rollouts outperform both random selection and full-batch training; (4) HES computed with a small proxy model transfers effectively to larger models.

## Strengths

1. **Well-motivated core idea grounded in token-level analysis.** The insight that averaging entropy over long CoT sequences dilutes signals from critical forking points is clearly articulated and supported by Figure 1, which shows that standard average entropy fails to distinguish correct from incorrect responses while HES separates them cleanly (correct: 0.29 normalized mean vs. incorrect: 0.68). The top-0.5% threshold focuses on the meaningful tail rather than the overwhelming trivial majority.

2. **Unusually broad empirical scope.** The paper validates across three fundamentally different training paradigms (SFT, RFT, RL), two model families (Qwen3, DeepSeek-R1-Distilled), multiple scales (0.6B, 1.5B, 1.7B, 7B, 8B), and three domains (math, code, STEM). Tables 1–6 cover this breadth systematically, and the trends are consistent across all settings.

3. **Lowest-HES data as a compelling sanity check.** The Lowest-HES-20% results — 14.90% vs. 32.61% full-dataset in Table 1, and consistently catastrophic performance across all tables — demonstrate that HES captures a real signal about training utility. The finding that simply pruning the worst 20% (Highest-HES-80%) consistently surpasses full-dataset performance (e.g., 35.36% vs. 32.61% in Table 1) is practically useful and conceptually clean.

4. **Small-to-large model transfer is a genuine practical contribution.** Using Qwen3-0.6B's HES scores to select data for Qwen3-8B training achieves 32.12% average accuracy — comparable to the 8B's self-selection (31.14%) — while reducing inference cost by over an order of magnitude (Table 1, lines 178–179). This shows HES captures intrinsic properties of the solution, not model-specific artifacts, and significantly lowers the barrier to adoption.

## Weaknesses

### Fatal

None.

### Major

None.

### Minor

1. **Lack of variance and statistical significance reporting.** Every result in Tables 1–6 is a single point estimate (average pass@1 over 16 sampling paths). No standard deviations, confidence intervals, or repeated runs are reported. The paper repeatedly uses "significantly" to describe performance gaps (e.g., lines 159, 206, 307), but the reader cannot assess whether modest gaps — HES vs. Length (0.47 pp in Table 1), HES vs. ES (0.22 pp in Table 1), or Pos-High, Neg-Rand vs. Full-Batch (0.67 pp in Table 6) — are reliable or within evaluation noise. The consistency of the pattern across many settings partially mitigates this concern, but formal variance estimates would strengthen the paper.

2. **Unresolved conceptual tension in the HES interpretation.** Figure 1 shows that *incorrect* responses have markedly higher HES (0.68 normalized mean) than *correct* responses (0.29 normalized mean), demonstrating HES's power to distinguish quality — with higher HES signaling *worse* quality. Yet in SFT, the paper selects the *highest*-HES correct responses as the best training data, asserting that "a higher HES score signifies a greater diversity and complexity of reasoning patterns, indicating a higher learning value" (line 36). The paper never addresses why, if higher HES correlates with incorrectness/confusion in Figure 1, it should be treated as a quality signal within correct samples. A plausible resolution exists: HES measures *complexity* (within correct responses, more complex = richer learning signal; across all responses, more complex/confused = more likely incorrect). But this dual interpretation is not discussed, creating an apparent contradiction in the paper's conceptual framing that should be clarified.

3. **RL experiment confound in the Full-Batch comparison.** In the RL experiment (Section 4.3), the paper compares Full-Batch (all 32 rollouts) with downsampling strategies using 16 rollouts. In GRPO, advantages are group-normalized: Âᵢ = (rᵢ − mean({rⱼ}))/std({rⱼ}). Changing the group from 32 to 16 rollouts alters the mean and standard deviation used for normalization, potentially changing every advantage even for identical trajectories. The comparison Pos-High, Neg-Rand (21.30%) vs. Pos-Rand, Neg-Rand (19.88%) is clean — both use 16 rollouts, isolating the HES selection effect. However, the claim that HES selection "surpasses the normal setting where all rollouts are involved" (line 38) confounds the selection mechanism with the altered group-normalization dynamics. The paper should either note this confound explicitly or run a cleaner ablation (e.g., computing advantages over all 32 rollouts while only updating from a subset).

4. **No analysis of HES–length correlation or compute cost.** The paper calls HES "training-free" but computing it requires a forward pass through a model for every candidate response. The small-to-large transfer experiment mitigates this cost, but a direct wall-clock or FLOPs comparison against the length baseline (which requires no forward pass) would help readers assess the practical trade-off. Additionally, the paper never reports how correlated HES and length are in practice; if the correlation is high, the marginal benefit of computing HES over simply measuring length is narrower than claimed. A scatter plot or correlation table would clarify this.

5. **Sensitivity analysis resolution is limited.** The high-entropy token ratio sweep (Section 4.4) tests only four values (0.005, 0.05, 0.5, 1.0), confirming that the smallest threshold works best. A finer-grained analysis around the 0.1%–1% range would provide stronger guidance for practitioners. This does not undermine the results but limits the practical recommendations.

### Trivial

None.

## Nice-to-Haves

- **Compute cost quantification.** Reporting GPU-hours or FLOPs for computing HES on 100k samples with the 0.6B and 8B models would help practitioners evaluate the cost-benefit trade-off.
- **HES–length correlation analysis.** A simple scatter plot or Spearman correlation between HES and response length across the training datasets would clarify how much value the entropy computation adds over length.
- **Deeper discussion of the Forking-Only baseline.** The Forking-Only method (gradient updates only on high-entropy tokens) achieves 32.51% in Table 1, nearly matching Full-Dataset (32.61%). This suggests that focusing training on forking points during optimization — not just data selection — could be a complementary direction worth discussing.
- **Finer-grained threshold sweep.** Testing more values of the high-entropy token ratio in the range [0.001, 0.02] would give practitioners clearer guidance.

## Removed Points

These points were flagged by the input review but are removed with justification:

- **"HES often performs only marginally better than simple length-based selection"** — Removed because HES *consistently* outperforms length across all settings (Tables 1, 5, 6). Modest gaps do not constitute a weakness when the metric is always directionally correct. Moreover, the small-to-large transfer experiment (HES from 0.6B → 8B) provides a practical advantage over length that is not captured by per-table gaps.
- **"Missing baseline: concise/low-entropy selection"** — Removed because the paper already tests Lowest-HES (Table 1: 14.90%), which is exactly this baseline within the SFT setting where all data is correct.
- **"Forking-Only baseline is interesting but underexplained"** — This is a suggestion for further discussion, not a weakness of the paper's claims.
- **"Section-by-section notes on relative vs. absolute comparison"** — The paper notes (footnote 1) that HES_relative is the default and shows in Table 1 that HES_absolute (30.11%) underperforms HES_relative (31.14%). A deeper comparison is nice-to-have but not a required weakness.

## Novel Insights

The input review identifies one genuinely insightful observation that goes beyond the paper's own analysis: the Forking-Only baseline (Table 1, 32.51%) nearly matches full-dataset SFT performance (32.61%) while only updating gradients on high-entropy tokens. This suggests that the paper's core insight — that forking points carry the learning signal — could be applied at the optimization level (selective gradient updates) rather than only at the data-selection level. This connection between the paper's data-selection framing and the concurrent line of work on token-level training (Wang et al., 2025) is worth exploring and is underexploited in the current manuscript. Beyond this, the reviews do not surface additional insights not already present in the paper.

## Suggestions

1. Add variance estimates (e.g., standard deviations over 3 seeds or bootstrapped confidence intervals) for the main results in Tables 1, 5, and 6.
2. Explicitly address the apparent tension between Figure 1 (higher HES → incorrect) and the SFT selection strategy (higher HES → better training data) by distinguishing HES as a *complexity* measure within correct samples vs. a *confusion* signal across all samples.
3. For the RL experiment, either (a) acknowledge the group-normalization confound in the Full-Batch comparison, or (b) run a control that computes advantages over all 32 rollouts but only updates from a subset.
4. Report the Spearman correlation between HES and response length on the training datasets used, and provide a rough compute cost comparison (e.g., "computing HES for 100k samples with Qwen3-0.6B takes X GPU-hours").
5. Soften the use of "significantly" throughout the paper to reflect that it describes empirical consistency, not formal statistical testing.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>