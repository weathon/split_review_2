Now let me produce the final consolidated review.

---

## Summary

VideoJudge introduces a bootstrapping framework for training MLLM-based evaluators for video understanding. The approach uses a generator-evaluator pipeline to produce 103,825 training examples across 20,765 video-instruction pairs without human annotation, then fine-tunes small models (3B, 7B) as pointwise and pairwise judges. The paper also trains models to generate instance-specific rubrics at inference time, and provides a suite of benchmarks and trained models to the community.

## Strengths

- **Large-scale synthetic data generation:** The bootstrapping pipeline produces 103,825 training examples across 20,765 video-instruction pairs without human annotation (Section 4). This scale is a practical contribution that enables training judge models at all. [weight=9.09]

- **Clean ablation on temporal context (maxframes):** The analysis in Section 6.2 separately varies maxframes during training vs. evaluation, isolating the effect and yielding actionable findings (training benefits from up to 240 frames, evaluation saturates at ~120 frames). [weight=9.05]

- **Human validation of the most ambiguous pairwise data:** Human evaluation on 250 rating-2-vs.-3 pairs shows 94.8% annotator agreement with Cohen's κ of 89.5, and >92% correctness relative to gold preference (Section 5.2). This provides a genuine quality check on the hardest part of the data. [weight=10.06]

- **Temperature robustness analysis:** Figure 4 shows that while base Qwen2.5-VL-3B degrades steadily as temperature increases (Spearman from 0.56 to 0.42), the trained VideoJudge model remains stable and even improves, achieving a peak correlation of 0.73 at high temperatures. [weight=9.11]

## Weaknesses

### Fatal
None.

### Major

- **Overestimation bias severely undermines pointwise evaluation reliability:** The model overestimates scores by ≥2 points in 14.8% of cases vs. underestimating by the same margin in only 1.5%. For rating-3 responses, only 36.9% get the correct score (46.6% inflated to 5); for rating-4 responses, **81.3% are incorrectly scored as 5** (Section 6.2, Error Analysis). This means the pointwise 1–5 scale is essentially unreliable in the mid-to-high range where evaluation is most practically meaningful — the model cannot distinguish ratings 3, 4, and 5. The paper acknowledges this but the severity (81.3% of 4s called 5s) is a fundamental limitation of the current approach that the framing does not adequately reflect. [weight=3.31]

- **Self-constructed benchmarks inflate perceived advantage:** The two main pointwise meta-evaluation benchmarks (VideoJudgeLLaVA-MetaEval and VideoJudgeVCG-MetaEval) are constructed by the same bootstrapping pipeline (Algorithm 1, threshold 0) that produces the training data (Section 4.2). The strongest results — and the headline claim of matching/surpassing 32B/72B models — come disproportionately from these self-constructed benchmarks. On independent human-annotated benchmarks, the picture is substantially more mixed: VideoJudge-7B has higher RMSE (1.46) than Qwen2.5-VL-72B (1.40) on VateX-Eval, and lower PSUP (0.66 vs. 0.73/0.71) on LongVideoBench. While the Limitations section (Section 7) acknowledges the "closed-loop" effect, the abstract and conclusion do not adequately caveat this distinction. [weight=1.42]

### Minor

- **The conclusion overstates results on independent benchmarks:** The conclusion claims VideoJudge-7B "consistently outperforms larger video-language models across multiple benchmarks," but on the independent human-annotated benchmarks the comparisons are mixed (VateX-Eval RMSE: 1.46 vs. 72B's 1.40; LongVideoBench PSUP: 0.66 vs. 32B's 0.73 and 72B's 0.71). [weight=4.01]

- **Rubric quality evaluation framing conflates two evaluations:** Figure 3 (human unanimous evaluation) shows VideoJudgeR-3B vs. GPT-4o-mini at only 53.4% win rate (barely above chance), but the paper's discussion emphasizes the 92.7% win rate from the LLM-as-Judge evaluation (which uses a weaker judge as evaluator) without clearly distinguishing which result comes from which method. [weight=3.58]

- **Dense video description vs. raw video mismatch in bootstrapping:** The bootstrapping pipeline uses dense video descriptions (not raw video) for the generator and evaluator (Section 3.1), while the final judge model uses raw video. This substitution is described as a cost-saving measure, but whether it preserves or loses temporal information that could affect data quality is not analyzed. [weight=5.44]

- **Exclusion of several video models due to instruction-following failures:** The paper excludes VideoLLaMA3-7B, VideoChat-Flash, Keye-VL, and SmolVLM2 because they "failed to follow instructions or produce valid scores under the same evaluation setup" (Section 4.1). This raises the question of whether the prompting format was optimized for Qwen2.5-VL and may not transfer fairly to other architectures. The paper should at minimum report what proportion of outputs were invalid for each excluded model. [weight=5.55]

### Trivial
None.

## Nice-to-Haves

- Report confidence intervals or statistical significance tests for the key comparisons, especially where margins are small (e.g., VideoJudge-3B Spearman 0.82 vs. Qwen2.5-VL-32B 0.80).
- Add an ablation that compares the full bootstrapping loop against a single-pass training baseline to isolate whether the iterative refinement adds value over simpler self-training.
- Specify the generator/evaluator models used in bootstrapping in the main text (currently deferred to Appendix A.2).
- Report wall-clock time and GPU-hours for training.

## Removed Points

These points were raised in the input review but removed after verification against the paper:

1. **"Feedback consistently improves" claim contradicted by data** — REMOVED. The reviewer misread Table 3. The paper states "Feedback consistently improves the 3B and 7B baselines," which refers to Qwen2.5-VL-3B and Qwen2.5-VL-7B (the base models). Table 3 confirms w/ FB outperforms w/o FB for both these rows on all three benchmarks. The paper then explicitly adds "In the VideoJudge variants, the effect is more mixed and depends on the benchmark." The reviewer mistakenly attributed the claim to VideoJudge rows.

2. **Missing related works** — REMOVED per instruction (external sources unavailable to verify).

3. **Formatting/style nitpicks, typos, grammar** — REMOVED per instruction (parser artifacts, not author errors).

4. **Missing appendix content** — REMOVED per instruction (appendices exist in original submission).

5. **Reproducibility concerns about undisclosed hyperparameters** — REMOVED per instruction (trivial implementation details within community standards).

6. **"Could the metric be measuring a proxy?" speculation without concrete anchor** — REMOVED per filtering guidelines.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Restructure the paper to lead with results on independent human-annotated benchmarks (VateX-Eval, LongVideoBench, VideoAutoArena) and treat the self-constructed benchmarks as secondary/diagnostic analyses. Adjust the abstract and conclusion to reflect the more mixed picture on independent evaluations.
- Address the overestimation bias before claiming pointwise reliability: either train on harder negatives at the high end of the rating scale, adopt a finer-grained scale, or move to a primarily pairwise setup where calibration is less acute.
- Analyze whether using dense video descriptions (rather than raw video) during bootstrapping preserves temporal fidelity, given the mismatch with the final judge's use of raw video.
- Report the proportion of invalid outputs for each excluded model in Section 4.1 to clarify whether the exclusion is fair.

## Score and Decision

**Calibration Anchors Used:**

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|--------|------|-----------|-------|-----------|------------|
| Is Your Video Language Model a Reliable Judge? | .../m8yby1JfbU.md | 6.50 | Round 1 | Yes | Similar topic (VLM-as-judge). Weaker methodological concerns but accepted; VideoJudge has stronger concrete contributions but more serious structural weaknesses. |
| Self-Taught Evaluators | .../I7uCwGxVnl.md | 5.40 | Round 2 | Yes | Most similar methodology (iterative synthetic judge training). Rejected. VideoJudge's weaknesses (1.42, 3.31) comparable in severity. |
| JudgeLM | .../87YOFayjcG.md | 5.25 | Round 2 | Yes | LLM-as-judge fine-tuning with distillation. Rejected. VideoJudge's contributions are broader but structural concerns are similar. |
| Needle In A Video Haystack (VideoNIAH) | .../ZJo6Radbqq.md | 5.75 | Round 1 | Yes | Synthetic video evaluation benchmark. Accepted. VideoJudge's strengths are stronger (9.05-10.06 vs. 7.15-9.29) but weakest weakness (1.42) is more negative than VideoNIAH's weakest (2.04). |
| Video Instruction Tuning with Synthetic Data | .../8Livf4oZxz.md | 4.50 | Round 1 | Yes | Synthetic video data generation. Rejected for novelty concerns. VideoJudge is clearly stronger. |

**Weighted-Item Comparison:** VideoJudge's strengths (9.05–10.06) are competitive with the higher-scoring anchors. However, its two major weaknesses (1.42 for self-constructed benchmarks, 3.31 for overestimation bias) are more negative than the accepted anchor papers' weakest items, and comparable to the rejected Self-Taught Evaluators paper's weakest items (1.31, -3.84). The self-constructed benchmark issue (weight 1.42) is particularly concerning because it directly affects how the headline results should be interpreted.

**Final Bracket Determination:** Round 1 placed the paper between 4.5 and 6.5. Round 2 narrowed to 5.0–5.5 by comparing item weights against the Self-Taught Evaluators (5.40, rejected) and VideoNIAH (5.75, accepted). The paper sits below VideoNIAH because its weakest item (1.42) is substantially more negative than VideoNIAH's (2.04), and above the Self-Taught Evaluators because its strengths (9.05–10.06) are stronger than that paper's (7.93–10.96) while having somewhat comparable methodological concerns.

The paper makes genuine contributions — the bootstrapping pipeline, large-scale synthetic data, careful ablations, and human validation are all valuable. However, the gap between the headline claims and what the evidence independently supports is too wide. The overestimation bias and the reliance on self-constructed benchmarks for the strongest results substantially weaken the core claims about VideoJudge's evaluation reliability.

**Score:** 5.0 — borderline reject. The paper would benefit from restructuring to center the independent evaluations and addressing the overestimation bias before resubmission.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>