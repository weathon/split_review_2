## Summary

The paper proposes High-Entropy Sum (HES), a training-free metric that sums the entropy of only the top 0.5% highest-entropy tokens in reasoning trajectories, targeting the "forking points" where models exhibit high uncertainty. HES is validated across SFT, RFT, and RL training paradigms on multiple models (Qwen3-8B, DeepSeek-R1-Distilled-7B/1.5B) and diverse benchmarks (math, code, STEM). The core finding is that selecting the highest-HES correct trajectories consistently outperforms random selection and simple heuristics like length and difficulty.

## Strengths

- **Well-motivated design grounded in a specific limitation of existing metrics.** The paper identifies a genuine failure mode of global averaging metrics in long-CoT scenarios — that the few critical forking tokens are swamped by trivial tokens — and proposes HES as a targeted fix. This builds directly on the forking-points insight from Wang et al. (2025) and the intuition is clearly articulated (Section 2.2, line 94).

- **Broad experimental validation across three training paradigms (SFT, RFT, RL), multiple model scales (Qwen3-0.6B/8B, DeepSeek-R1-Distilled-7B/1.5B), and diverse benchmarks spanning math, code, and STEM domains (Tables 1–6).** This breadth is a genuine strength and demonstrates that the signal HES captures is not limited to a single setting.

- **Directionally consistent results across all experiments.** Across Tables 1–6, highest-HES subsets consistently outperform random subsets, while lowest-HES subsets severely underperform (e.g., Lowest-HES-20% achieves only 14.90 AVG vs. Random-20% 25.89 in Table 1). The pattern is robust and not cherry-picked.

- **Practical cost savings via small-to-large model transfer.** Using Qwen3-0.6B as a proxy to compute HES achieves results (AVG 32.12) comparable to or better than using the target Qwen3-8B itself (AVG 31.14), reducing inference costs by an order of magnitude (Section 4.1.2, line 216).

- **Well-executed sensitivity analysis (Section 4.4).** The demonstration that the top 0.5% token ratio consistently outperforms larger ratios (0.05, 0.5, 1.0) across math, STEM, and code domains provides direct evidence for the core thesis that only the most uncertain tokens carry disproportionate signal.

## Weaknesses

### Major

1. **Misleading framing of what HES actually measures.** The paper presents HES as capturing "reasoning quality" (abstract, line 9) and claims it "distinguish[es] high- and low-quality samples" (Figure 1 caption). However, Figure 1's own data shows that **incorrect responses have substantially higher HES than correct ones** (normalized mean 0.68 vs. 0.29). HES does not measure correctness or quality in a global sense — it measures generation uncertainty/complexity. The only reason HES works as a selection signal is the careful experimental scaffolding: in SFT and RFT, datasets are pre-filtered to correct responses only, so HES selects the *most complex correct* solutions; in RL, positive and negative pools are explicitly separated and HES selects only from the positive pool. The paper does not clearly disclose that HES is a complexity ranking *within already-correct solutions*, not a general-purpose quality discriminator. This framing issue affects how the contribution should be interpreted. (This is a Major weakness because it concerns the accuracy of the paper's central narrative, though the experimental results themselves are not invalidated.)

2. **HES is confounded with length and the paper does not control for it.** Since HES_relative sums the top 0.5% of tokens in each response, longer sequences contribute more tokens to the sum, creating a built-in length correlation. The paper states "The relative threshold makes this metric robust to variations in length" (line 115), but a relative threshold makes the number of summed tokens scale with length — the opposite of length-robustness. The correlation between HES and response length is never quantified, and no experiment controls for length (e.g., length-matched HES subsets). In SFT (Table 1), the gap between Highest-HES-20% (31.14) and Length-20% (30.67) is only 0.47 points. In RFT (Table 5), HES consistently beats Length but the margins are modest (0.5–1.9 points). Without controlling for the length confound, it is unclear how much of HES's advantage comes from its claimed mechanism vs. being a slightly better length proxy. (Major — a missing analysis that is central to the paper's claims about HES capturing something fundamentally different from length.)

### Minor

3. **No statistical significance or variance reporting.** All results in Tables 1–6 are point estimates without confidence intervals or standard errors. For benchmarks like AIME24/25 with ~30 problems, a single-problem swing changes accuracy by ~3.3 points. Many comparisons involve margins of 0.5–2 points, and the paper uses "significantly outperforms" (Section 4.1.2, line 159) without any statistical test. While single-run reporting is common in LLM benchmarking, the strength of the comparative claims ("significantly outperforms") exceeds what the evidence supports.

4. **The proxy model anomaly is noted but not analyzed.** Using Qwen3-0.6B to compute HES yields *better* results (AVG 32.12) than using the target Qwen3-8B (AVG 31.14) in Table 1. The paper frames this as a cost-efficiency win but does not explain why a weaker model provides a stronger selection signal. If HES captures "intrinsic reasoning complexity inherent to the data, rather than model-specific artifacts" (line 216), then the target model should be at least as good. This anomaly could be explained (e.g., smaller models have sharper, more discriminative entropy distributions) but the paper does not attempt an explanation, weakening the claim of model-agnosticism.

5. **The RL asymmetric sampling motivation is underspecified.** The paper selects highest-HES positive trajectories paired with random negatives and shows this outperforms other variants in Table 6. However, it provides no theoretical rationale for why random negatives are optimal over, e.g., highest-HES negatives (maximal contrast) or lowest-HES negatives. The ablation is useful, but without a rationale, the generality of the finding is unclear.

### Trivial

None.

## Nice-to-Haves

- **Qualitative analysis of HES-high vs. HES-low samples.** Figure 2 shows token-level entropy visualization, but the paper would benefit from showing concrete examples of what high-HES and low-HES correct solutions actually look like textually — do high-HES solutions contain more backtracking, alternative approaches, or verification steps?
- **Comparison with training-free selection methods beyond the current baseline set** (e.g., DSIR, perplexity-based filtering) would further contextualize the contribution, though the current baselines (length, difficulty, AvgE, ES, AvgHE) are reasonable.
- **Bootstrapped confidence intervals** on the AVG metrics for the main comparisons would significantly strengthen the comparative claims.

## Removed Points

These points are flagged to be removed; treat them with caution.

- *"Missing qualitative analysis of what HES-high and HES-low samples look like"* — Moved to Nice-to-Haves. Not a weakness, the paper already provides Figure 2's token-level visualization.
- *"SFT random baseline should be from correct pool"* — The paper explicitly states SFT datasets contain "correct demonstrations" (Section 2.1), making this concern moot.
- *"Comparison to more recent data selection methods (DSIR, D4, etc.)"* — Scope creep. The paper compares against the most relevant training-free baselines and explicitly discusses why costly methods (SHUM et al., Toshniwal et al.) are outside scope.
- *"Forking-Only baseline achieving near Full-Dataset performance undermines HES contribution"* — Forking-Only is a per-token method operating at a different granularity (gradient masking vs. sample selection), not a sample-level selection method. It does not undermine HES.
- Criticisms about missing appendix content or incomplete proofs — Stripped by the PDF parser; these exist in the original submission.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Reframe HES honestly.** Clearly state in the abstract and introduction that HES measures reasoning *complexity within correct solutions*, not correctness. Acknowledge explicitly that incorrect responses have higher HES (Figure 1) and that HES's utility depends on having a pre-filtered pool of correct trajectories.
2. **Quantify the HES-length correlation.** Report Pearson/Spearman correlations between HES and response length for all datasets. Add an experiment comparing HES-selected subsets against length-matched subsets (e.g., select the highest-HES samples within each length decile).
3. **Add variance estimates.** Report bootstrapped confidence intervals or standard errors for the main comparisons (at least the AVG metrics), especially for the SFT HES vs. Length comparison where margins are small.
4. **Analyze the proxy model anomaly.** Explain why the 0.6B proxy outperforms the 8B target — does the smaller model produce sharper (more discriminative) entropy distributions? This could either strengthen or qualify the claims about model-agnosticism.
5. **Motivate the RL asymmetric sampling design.** Provide intuition for why random negatives work best — e.g., constraining negatives reduces diversity of failure modes seen during training.

## Score and Decision

**Calibration:** I ran a 2-round calibration against the deepreview_13k corpus. Round 1 bracketed across all score bands using data-selection / entropy-based metrics. Round 2 narrowed within the 4.0–7.0 band. Key anchors:

| Anchor Path | Avg Score | Round | Itemized? | Comparison |
|---|---|---|---|---|
| `/home/.../qUJsX3XMBH.md` (Rethinking Data Selection at Scale) | 4.40 | 1,2 | Yes | Similar topic (SFT data selection) but weaker contribution (negative result). Our paper has a novel proposed metric and broader experiments. |
| `/home/.../cijO0f8u35.md` (Scaling Relationship on Math Reasoning) | 5.25 | 2 | Yes | Comparable quality. Stronger on controlled experiments, weaker on breadth. Our paper has wider coverage but a more serious framing issue. |
| `/home/.../Fty0wTcemV.md` (DELIFT) | 6.00 | 2 | Yes | Stronger on methodological novelty and clarity. Our paper has broader paradigm coverage but a more significant framing/narrative problem. |
| `/home/.../huuKoVQnB0.md` (Improving Pretraining Data) | 6.00 | 1 | Yes | Accepted paper with solid experiments at limited scale. Our paper's framing issue is more serious than that paper's scale limitation. |
| `/home/.../f4gF6AIHRy.md` (Combatting Dimensional Collapse) | 8.00 | 1 | Yes | Strong accept — cleaner narrative, more rigorous theory. Our paper does not reach this level. |

**Round 1 bracket:** After comparing my draft's weighted items (strength weights 7.98–9.98, major weakness block weight -0.65, minor weakness block weight 5.51) against the anchors' item-level weights, the initial plausible bracket was 4.0–6.0. The paper's major weakness (framing, weight -0.65) is less severe than some anchors' worst weaknesses (e.g., -2.73 in the 4.40 anchor) but the cumulative weight of two major issues (framing + length confounding) is meaningful. The strengths are genuine but the narrative gap prevents the paper from reaching the 6+ level of DELIFT or the Perplexity Correlations paper.

**Round 2 narrowing:** Compared against DELIFT (6.00, accept) and the Scaling Relationship paper (5.25, reject). Our paper has broader experimental coverage than both, but the framing issue is more fundamental than either anchor's weaknesses. The paper sits between these two anchors, closer to 5.25 than 6.00.

**Final placement:** The paper has a genuinely useful core idea and admirably broad experiments. However, the misleading framing of what HES measures (Major weakness #1) and the unaddressed length confounding (Major weakness #2) are significant problems that require substantial revision. The contribution would be solid after honest reframing and additional analysis, but in its current form the gap between the strength of the claims and the precision of the evidence is too wide.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>