## Summary

This paper introduces VideoJudge, a bootstrapping framework for training MLLM-based evaluators for video understanding. The key idea is a generator–evaluator loop that creates training data with a 1–5 quality ladder without human annotation, and a rubric-generation variant that produces instance-specific evaluation criteria. The framework is demonstrated on 3B and 7B Qwen2.5-VL backbones across 4 pointwise and 3 pairwise benchmarks.

## Strengths

- **A practical bootstrapping pipeline (Section 3.1) that eliminates the need for costly human annotation** for judge training data. The generator–evaluator loop produces training responses with monotonic quality degradation (Figure 2, BERTScore from 91.1→86.9, BLEU from 11.0→3.0), validating the controlled degradation design. ***(impact: very strong)***

- **Instance-specific rubric generation (VideoJudgeR-3B)** achieves MAE 0.59 / Spearman 74.16 on 1,000 samples, competitive with Qwen2.5-VL-32B/72B despite being 3B. Human evaluation shows rubric win rates above 50% against all baselines including GPT-4o-mini, demonstrating that the model learns interpretable evaluation criteria. ***(impact: very strong)***

- **Broad evaluation suite** across 4 pointwise and 3 pairwise benchmarks with multiple metrics (Spearman, Pearson, RMSE, MAE, ECE, PSUP, Δ(C-D)), plus ablations on frame count, decoding temperature, and rubric generation that provide practically useful insights. ***(impact: strong)***

## Weaknesses

### Fatal
None.

### Major

1. **The headline claim that VideoJudge "matches or outperforms much larger models" rests primarily on self-constructed benchmarks that share their generation pipeline with the training data. On independent benchmarks the results are more mixed.** The paper constructs VideoJudgeLLaVA and VideoJudgeVCG via the same bootstrapping pipeline used for training (Algorithm 1 with threshold 0, line 106). On these in-distribution benchmarks, VideoJudge performs strongly. But on truly independent benchmarks: VideoJudge-3B achieves PSUP 0.61 on VATEX vs. Qwen2.5-VL-32B's 0.73; on VideoAutoArena, VideoJudge-3B achieves 71.76 vs. Qwen2.5-VL-72B's 89.80; on VJ-Human, VideoJudge-3B achieves 89.45 vs. Qwen2.5-VL-72B's 94.51. The paper acknowledges this "closed-loop" issue in the limitations (Section 7), but the abstract and conclusion frame the results as substantially stronger than the independent evidence supports. ***(impact: decisive pull-down)***

2. **Severe overestimation bias undermines the judge's utility for fine-grained absolute scoring.** The paper's own error analysis (Section 6.2) shows: only 36.9% of rating-3 responses get the correct score, with 46.6% inflated to 5; only 18.7% of rating-4 responses are correctly rated, with 81.3% inflated to 5. The model overestimates by ≥2 points in 14.8% of cases but underestimates by the same margin in only 1.5%. This means the judge systematically cannot distinguish between mediocre (3), good (4), and excellent (5) responses in absolute terms — a fundamental limitation for fine-grained evaluation. While the paper acknowledges this, the main narrative (abstract, conclusion, Section 6.1) portrays the model as a reliable evaluator without adequate caveating. ***(impact: decisive pull-down)***

### Minor

3. **The seed "gold" responses (rating-5 anchors) are model-generated** from instruction-tuning datasets (VideoInstruct-100K, VCG-Plus-112K, VideoChat2-IT), not human-written. The entire 1–5 quality ladder is therefore grounded in synthetic quality judgments. Human validation (Section 5.2) only covers pairwise 2-vs-3 preferences (250 pairs), not absolute rating alignment, so the judge's absolute ratings may be misaligned with human notions of quality.

4. **The rubric win rate against GPT-4o-mini under unanimous human vote is only 53.4%** (Figure 3) — modest and near chance — despite the framing suggesting strong evidence for rubric quality. The stronger win rates against larger baselines (63.9% vs Qwen-72B) are more convincing, but the overall "substantially higher-quality rubrics" framing is somewhat overstated relative to this particular comparison.

5. **BERTScore and BLEU are used to validate data quality (Section 5.1)** despite the introduction (line 13) criticizing these metrics as struggling "to capture semantic fidelity, contextual grounding, or task-specific reasoning." While acceptable as a coarse sanity check for monotonicity, this inconsistency should be noted.

### Trivial
None.

## Nice-to-Haves
- Reporting variance estimates or confidence intervals for the main results (Tables 1, 2, 3) would strengthen reproducibility, though this is not standard practice for this type of large-benchmark evaluation.
- A direct human evaluation of absolute ratings (not just pairwise preferences) for at least a subset of the bootstrapped data would strengthen confidence in the 1–5 rating scheme.

## Removed Points
These points were flagged by the input reviews but are removed per policy:
- **G/E model identity in Appendix §A.2:** Criticisms about content in a parser-stripped appendix are removed.
- **α acceptance threshold not stated in main text:** Removed as a reproducibility nitpick.
- **Table 1 formatting issues:** Attributed to parser artifacts; removed.
- **Missing related works / statistical significance:** Removed per policy (cannot verify related works; significance tests are not standard for this evaluation setting).

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. **Reframe the headline claim** from "matching/surpassing larger models" to "bootstrapped training substantially improves small judge models, closing part of the gap with 10× larger models, with strong in-distribution performance and promising generalization." This is what the data actually supports.
2. **Add explicit caveats about the overestimation bias** in the abstract and conclusion, clarifying that VideoJudge is more reliable for relative ranking (pairwise) than for fine-grained absolute scoring.
3. **Clarify in the main text** that the seed "gold" responses are model-generated, and discuss the implications for what the judge learns to align with.

## Score and Decision

**Calibration anchor summary** (all rounds):

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| JudgeLM (87YOFayjcG) | 5.25 | 1 | Yes | Similar theme; our paper has stronger methodology but similarly impactful weaknesses |
| Is Your VLM a Reliable Judge? (m8yby1JfbU) | 6.50 | 1 | Yes | Our paper has stronger contributions but more severe empirical weaknesses |
| MJ-Bench (vxutwN3xQN) | 6.00 | 1 | Yes | Different domain; our paper has more novelty but more impactful weaknesses |
| Generative Judge (gtkFw6sZGS) | 5.33 | 1 | Yes | Our paper has stronger novelty and evaluation breadth |
| VideoNIAH (ZJo6Radbqq) | 5.75 | 2 | Yes | Our paper has stronger strengths but more impactful weaknesses (-9.96/-9.98 vs max -8.41) |
| Video Inst. Tuning Synthetic (8Livf4oZxz) | 4.50 | 2 | Yes | Our paper is substantially stronger across all dimensions |
| DJPO (ToWKyjwDqO) | 5.00 | 2 | Yes | Comparable structure and severity of weaknesses |

**Round 1 bracket:** 4.0–6.5. **Narrowing rationale:** Our paper shares decisive-magnitude weaknesses (-9.96, -9.98) with papers scoring ~5.0–5.25, but its strongest strengths (+9.53, +9.82, +9.97) are competitive with papers scoring 5.5–6.0. The two decisive weaknesses pull the final score down because they directly affect the paper's core claims (overclaiming on independent benchmarks, and overestimation bias limiting practical utility for absolute scoring). The paper is stronger than the 4.5 papers but weaker than the 5.75+ papers due to these unresolved empirical concerns.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>