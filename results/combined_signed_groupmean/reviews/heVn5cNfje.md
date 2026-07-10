Now let me write the final consolidated review.

## Summary
This paper proposes **High-Entropy Sum (HES)**, a training-free metric that sums the entropy of only the top 0.5% highest-entropy tokens in each reasoning sample, focusing on critical "forking points." The authors validate HES across three training paradigms — SFT, RFT, and RL — using multiple models (Qwen3-8B, DeepSeek-R1-Distilled-7B/1.5B), datasets, and domains (math, code, STEM). The core finding is that pruning the lowest-HES data consistently improves performance over training on the full dataset, and selecting highest-HES data among correct samples is beneficial. The paper also demonstrates small-to-large model transfer (Qwen3-0.6B scoring data for Qwen3-8B) and an asymmetric RL sampling strategy.

## Strengths
- **Clean, well-motivated metric.** The idea of summing entropy only for the top percentile of tokens rather than averaging is simple and grounded in the intuition that critical "forking points" are sparse. Figure 1 provides direct evidence that this operationalization separates correct from incorrect samples better than alternative entropy-based aggregates (correct norm mean 0.29 vs incorrect 0.68 for HES, vs 0.52/0.53 for average entropy).
- **Breadth of evaluation across three paradigms.** The paper validates HES in SFT, RFT, and RL using different models (Qwen3-8B, DeepSeek-R1-Distilled-7B/1.5B), datasets (Open-Math-Reasoning, Open-R1-220k, DeepScaleR), and domains (math, code, STEM). The consistency of the core pattern — pruning lowest-HES data helps and selecting highest-HES data is beneficial — across these diverse settings is the paper's strongest empirical contribution.
- **Small-to-large transfer result.** The experiment using Qwen3-0.6B as a cheap proxy to score data for training Qwen3-8B (Table 1, AVG 32.12% vs 31.14% with self-selection) is practically useful and theoretically interesting, suggesting HES captures properties of the data rather than model-specific artifacts.
- **Asymmetric RL sampling design.** The "Pos-High, Neg-Rand" strategy (Table 6) — selecting high-HES correct trajectories but randomly sampling incorrect ones — is a thoughtful ablation that produces a testable insight about the importance of negative sample diversity, going beyond simply applying HES as a filter.
- **Sensitivity analysis.** Figures 3–4 systematically vary both the data selection ratio and the high-entropy token ratio across three domains, showing the results are not driven by a fragile hyperparameter choice.

## Weaknesses

### Major
- **No measures of variance or statistical significance.** Every result in Tables 1–6 is reported as a single point estimate (average@16). No standard deviations, confidence intervals, or significance tests are reported anywhere. This matters concretely: in Table 6 (RL), the best HES strategy achieves 21.30% vs Full-Batch's 20.63% — a 0.67 pp gap that could fall within noise given 16 samples per problem on small benchmarks like AIME (30 problems). In Table 5 (RFT), many comparisons show gaps of 1–2 pp between Highest-HES and Random. Without variance estimates, the reader cannot assess the reliability of these differences. The strongest results (80% subset beating full data by 2–3 pp in Table 1) are likely robust, but the weaker margins throughout the paper need statistical grounding.

### Minor
- **Overstated claims about the 20% subset in the abstract and introduction.** The abstract states that training on the top 20% "matches full-dataset performance." In the primary SFT experiment (Table 1, Qwen3-8B on Open-Math-Reasoning), Full-Dataset achieves 32.61 while Highest-HES-20% achieves 31.14 — a 1.47-point gap (~4.5% relative). This is not "matching" performance. (Table 2 shows the 20% subset actually beats full data on DeepSeek-R1-7B/OpenR1-220k, so the result is dataset-dependent.) The body text uses the more accurate phrase "closely approaches" (line 159), but the abstract and introduction inflate the claim.
- **RL validation only on a 1.5B model.** The SFT and RFT experiments use 7B–8B models (Qwen3-8B, DeepSeek-R1-Distilled-7B). The RL experiments use DeepSeek-R1-Distilled-Qwen-1.5B. The paper follows DeepScaleR-1.5B-Preview, which is reasonable for cost, but does not explain why this should transfer to larger models. Given that the paper's title and abstract make general claims about "unified data selection for LLM reasoning," this limits the claim of generality across paradigms at comparable scale.
- **Conceptual tension in framing HES.** Figure 1 shows that incorrect samples have substantially higher HES than correct samples (normalized mean 0.68 vs 0.29). The paper states that HES measures "complexity" and "learning value" (line 36), but also repeatedly frames it as a measure of "reasoning quality." Since HES scores are systematically higher for incorrect samples, it is more accurately described as a measure of reasoning complexity or uncertainty rather than quality. The paper's practical use of HES (applied within pools of already-correct samples for SFT/RFT, or within correct trajectories for RL) is sensible and consistent, but the framing conflates complexity with quality in a way that could confuse readers.

### Trivial
- The "Forcing-Only" entry in Table 1 is a parser artifact for "Forking-Only" (as correctly labeled in the paper text, line 155).

## Nice-to-Haves
- A brief cost comparison (FLOPs or wall-clock time) for computing HES vs. the other baselines would strengthen the efficiency claims.
- A direct correlation analysis between HES and response length would help further disentangle the two signals (Length is already a baseline in Tables 1 and 5 and often performs competitively).
- For the RL experiments, replicating on a 7B+ model or explicitly discussing the scale limitation as a caveat would strengthen the generality claim.

## Removed Points
These points were raised in the input review but are removed after verification:
- **Forking-Only baseline is an unfair comparison**: The paper clearly describes Forking-Only as token-level gradient masking (line 155) and labels it with Ratio=100 in Table 1. It is presented as a reference point, not conflated with data selection. Not misleading. **REMOVED.**
- **Ties in rank-based threshold not specified**: Trivial implementation detail not worth raising. **REMOVED.**
- **0.6B proxy outperforming self-selection not discussed**: The paper does discuss this result in line 216, noting "Remarkably, the performance achieved using the 0.6B proxy model (Avg 32.12%) is comparable to that of the 8B model's self-selection (Avg 31.14%)." Deeper analysis would be nice but absence is not a weakness. **REMOVED.**
- **0.5% threshold appears arbitrary**: Partially addressed by the sensitivity analysis in Section 4.4, which shows smaller ratios (~0.005) consistently outperform larger ones. **REMOVED.**

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
- Add variance reporting (standard deviations or confidence intervals) for all tables, especially Tables 5 and 6 where small-margin comparisons drive the conclusions.
- Calibrate the abstract and introduction claims about the 20% subset to match the actual results (particularly for Table 1).
- For the RL experiments, either replicate on a model at 7B+ scale or explicitly add a caveat about scale limitations.

## Score and Decision
**Round-1 bracket**: Between 4.5 and 6.5. This assessment was formed by comparing against calibration anchors: the paper is clearly stronger than data selection papers at the 3.0–4.4 level (which either propose no new method or report negative findings), and comparable to papers at the 5.75–6.50 level (DELIFT, Perplexed by Perplexity, "What Kind of Pretraining Data...").

**Narrowing (Round 2)**: The closest anchors are **DELIFT** (6.00, accept), which proposes a data selection method across three FT stages and was accepted despite computational cost concerns, and **Perplexed by Perplexity** (5.75, accept), which uses small-reference-model perplexity pruning and was accepted despite novelty questions. Our paper compares favorably: it is more novel than Perplexed by Perplexity (new metric vs. well-studied perplexity) and has broader scope than DELIFT (3 training paradigms vs. 3 fine-tuning stages). The shared high-magnitude items are strong strengths (+9.6 to +10.0 for both the paper and the anchors) and the weaknesses, while impactful (-9.73 to -9.99), are fixable (variance reporting, abstract calibration) rather than fundamental.

**Final score**: 6.0 — borderline accept. The paper makes a genuine contribution (novel metric, broad evaluation across three paradigms, practical small-to-large transfer) but is weakened by the absence of variance/statistical significance reporting and several inflated claims in the abstract. These issues are addressable in revision.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>