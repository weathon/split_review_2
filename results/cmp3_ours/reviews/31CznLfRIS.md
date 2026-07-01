## Summary

This paper introduces VideoJudge, a bootstrapping framework for training small MLLM-based evaluators (3B and 7B) specialized for video understanding tasks. The key idea is a generator-evaluator pipeline that creates training data by generating responses at different quality levels (ratings 1–5), validating them through an evaluator model, and iteratively refining mismatches. The fine-tuned judge models can optionally produce instance-specific rubrics at test time. The paper releases bootstrapped datasets, meta-evaluation benchmarks, and trained models.

## Strengths

1. **The rubric-generation capability (VideoJudgeR-3B) adds interpretability and improves accuracy.** Training the judge model to produce instance-specific rubrics at test time, then score against them, is a principled and practically useful design choice. Table 2 shows MAE dropping from 1.15 (base 3B) to 0.59 (VideoJudgeR-3B), approaching the performance of 32B/72B models with a 3B model. This demonstrates that task-specific evaluation criteria can close most of the gap without scaling model size.

2. **Pairwise results on the closed-world benchmarks are striking.** VideoJudge-7B achieves 98.6% accuracy on VideoJudge (w/o FB), substantially ahead of Qwen2.5-VL-72B's 93.2%. The fine-tuned model has clearly internalized the preference structure of the bootstrapping pipeline.

3. **Temperature robustness analysis is practically meaningful.** The finding that VideoJudge's Spearman correlation remains stable or improves (0.66 → 0.73) as temperature increases, while the base model degrades (0.56 → 0.42), is a useful property for a reliable evaluation model in practice.

4. **Transparent reporting of limitations.** The paper honestly reports the severe overestimation bias (§6.2) and acknowledges the closed-loop evaluation concern (§7), enabling readers to calibrate their interpretation of results.

## Weaknesses

### Major

1. **The closed-loop evaluation confound significantly tempers headline claims.** The bootstrapping pipeline generates both the training data and two of four pointwise meta-evaluation benchmarks (VideoJudgeLLaVA, VideoJudgeVCG) and two of three pairwise benchmarks (VideoJudge, VideoJudge-Pairwise). On the independent human-annotated benchmarks, larger baselines remain ahead:
   - **VATEX PSUP**: VideoJudge-7B (0.66) vs. Qwen2.5-VL-32B (0.73) and Qwen2.5-VL-72B (0.71)
   - **VideoAutoArena** (independent human preferences, w/ FB): VideoJudge-7B (85.49) vs. Qwen2.5-VL-72B (89.80)
   - **VideoJudge-Human** (human-validated subset): Qwen2.5-VL-72B (94.51) vs. VideoJudge-7B (93.67) on w/ FB; tied (93.25) on w/o FB
   
   The paper acknowledges this in §7 but presents it as a minor caveat, and the interleaving of bootstrapped and independent benchmarks in the same tables makes the distinction hard to assess. The claim that VideoJudge-7B "outperforms or is on par with" much larger models is accurate only when bootstrapped benchmarks are included in the aggregate.

2. **The overestimation bias severely limits fine-grained discrimination.** Per §6.2: only 36.9% of rating-3 responses get the correct score (46.6% inflated to 5), and 81.3% of rating-4 responses are incorrectly rated as 5. The model overestimates by ≥2 points in 14.8% of cases vs. underestimating by ≥2 in only 1.5%. This means the model compresses the 3–5 range into effectively two levels, directly contradicting the promise of "evaluations that are both more reliable and more interpretable." The acknowledgment is a short paragraph with no mitigation proposed beyond a generic suggestion about harder negatives.

### Minor

3. **Inconsistency in criticizing BLEU/BERTScore while using them for validation.** The Introduction (§1) criticizes BLEU, ROUGE, and BERTScore for failing "to capture the nuances of human judgment." Yet Section 5.1 uses BLEU and BERTScore as the primary automated validation of data quality. This is not circular (the generator was instructed to produce distinct-quality responses, and the metrics confirm separation), but the paper would benefit from clarifying the limited scope of this check or using metrics it does not criticize. The VQAScore check (deferred to appendix) partially addresses this.

4. **Generator and evaluator models G and E are not identified in the main paper.** §3.1 refers to "generator model G" and "evaluator model E" without stating what specific models they are. Whether these are Qwen2.5-VL-72B, GPT-4o, or another model matters for understanding the supervision signal's provenance. This detail may appear in the appendix, but the main paper should state it.

### Trivial

5. **The training acceptance threshold α is not specified.** §3.1 defines α as the rating deviation threshold for accepting candidates, but the value used during training is never stated. (The meta-evaluation benchmarks use threshold 0 per §4.2.)

6. **Uneven pointwise improvement is not discussed.** The base Qwen2.5-VL-7B already achieves Spearman 0.77 on VideoJudgeLLaVA vs. VideoJudge-7B's 0.78 (gain of 0.01), while on VideoJudgeVCG the gain is 0.65 → 0.74 (gain of 0.09). This disparity goes unanalyzed.

## Nice-to-Haves

- Restructure results tables to clearly separate bootstrapped benchmarks from independent ones, enabling readers to assess the independent evidence at a glance.
- Include a root-cause analysis of the overestimation bias (e.g., training label distribution vs. intended distribution) and propose a concrete mitigation (balanced sampling, calibration-aware loss, or a penalty for overestimation).
- Provide confidence intervals or variance estimates for key metrics, especially where gaps are small.

## Removed Points

1. **"The rubric win rate against GPT-4o-mini (53.4%) in human evaluation is essentially at chance and undermines rubric-driven training."** — This conflates two separate evaluations. The 53.4% is from human evaluation of *rubric quality* (a head-to-head comparison of generated rubrics). The model achieves 92.7% win rate against GPT-4o-mini in the LLM-as-Judge rubric evaluation. More importantly, the rubrics' primary purpose is to improve evaluation accuracy (Table 2), not to win rubric preference comparisons. A 53.4% human preference rate against GPT-4o-mini for a 3B model is reasonable.

2. **"No confidence intervals on any reported metric."** — Generic critique common to this evaluation paradigm; moved to Nice-to-Haves.

3. **"The seed data is model-generated, not human-verified."** — The paper clearly describes seed data as coming from established datasets (VideoInstruct-100K, VCG-Plus-112K, VideoChat2-IT). The term "gold-standard" is used operationally within the pipeline context, which is standard.

4. **"Training for only 2 epochs may indicate underfitting."** — Speculation without evidence; not actionable.

5. **"Qwen3 and long-CoT analysis is not better than MLLM judges."** — This is presented as a finding of the paper, not a weakness.

## Novel Insights

The most striking finding from this review is the decoupling between VideoJudge's strong *pairwise* ranking ability (98.6% accuracy on its benchmark) and its poor *pointwise* calibration (81.3% of rating-4 responses scored as 5). This suggests the bootstrapping pipeline trains the model to correctly order pairs of responses while failing to calibrate absolute scores against the rating scale — likely because the training data's rating distribution is skewed such that the model learns a simple heuristic ("most non-trivial responses are perfect"). This points to a concrete research direction: using calibration-aware training objectives or balanced data sampling to bridge the gap between pairwise ranking and pointwise scoring.

## Suggestions

1. Separate bootstrapped and independent benchmarks into clearly distinguished summary tables so readers can assess the independent evidence at a glance.
2. Add a root-cause analysis of the overestimation bias: report the training label distribution and compare it to the intended uniform 1–5 distribution to determine whether the bias originates in the training data.
3. Specify the generator (G) and evaluator (E) model identities in the main paper.
4. Report the α threshold used during training.
5. Consider training with a calibration-aware loss or balanced sampling to mitigate overestimation.

## Score and Decision

**Calibration anchors retrieved** (all rounds, grouped by round-1 band):

**Round 1 — Bracketing**:
- *Low band (avg < 3.5)*: ujNe7sybJu.md (2.50, video summarization MoE, weaker contribution), YGWxpOI6Y0.md (3.40, VideoGPT+ encoder fusion), HfJxXbXlYJ.md (3.00, LLM2CLIP extension), KLUDshUx2V.md (3.40, concept bank generation)
- *Mid-low band (3.5–5.5)*: uHgVrGF2Wn.md (4.50, LVBench long video benchmark, reject), bjyf5FyQ0a.md (4.75, Valley video assistant, reject), O4LoPhRSfb.md (5.17, VLM language understanding, reject), 5ddsALwqkf.md (5.33, Neptune long video benchmark, reject)
- *Mid-high band (5.5–7.5)*: m8yby1JfbU.md (6.50, "Is Your VLM a Reliable Judge?", accepted — analysis paper with single dataset; VideoJudge has stronger methodology but more central weaknesses), OxKi02I29I.md (5.67, long video understanding, accepted), ZJo6Radbqq.md (5.75, VideoNIAH synthetic benchmark, accepted — VideoJudge has more comprehensive contributions), tRNKe2Vgqt.md (6.00, MMWorld benchmark, accepted — similar overall quality)
- *High band (7.5–8.5)*: HnhNRrLPwm.md (8.00, MMIE benchmark), 9Cu8MRmhq2.md (8.00, multi-granularity correspondence), WyEdX2R4er.md (8.00, visual data-type understanding), Q6a9W6kzv5.md (8.00, PhysBench) — all substantially stronger papers with cleaner evaluations.

**Round 2 — Narrowing**: le4IoZZHy1.md (6.20, CG-Bench, accepted benchmark), Hz4BYVY8YM.md (7.50, SVBench benchmark+model, strong accept), tTDUrseRRU.md (6.80, AuroraCap, strong accept).

**Round 1 bracket**: 5.5–6.5. The paper has genuine contributions (bootstrapping methodology, rubric generation, released artifacts) placing it above the 4.5–5.33 band. However, the closed-loop evaluation confound and severe overestimation bias prevent it from reaching the 7.0+ band.

**Narrowing**: Compared to CG-Bench (6.20) and MMWorld (6.00) — both accepted benchmark papers — VideoJudge has more methodological contribution but its evaluation weaknesses are more central to the core claims. The paper is comparable in overall quality to these accepted papers.

**Final score**: 6.0 — borderline accept. The paper has genuine, non-trivial contributions (the bootstrapping framework, rubric generation capability, temperature analysis, released artifacts) and is transparent about its limitations. However, the two major weaknesses — closed-loop evaluation confounding the headline claims, and the severe overestimation bias limiting practical utility — are substantive enough that the paper falls short of strong acceptance.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>