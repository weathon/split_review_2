## Summary

This paper introduces OptMerge, a model merging benchmark and method for Multimodal LLMs (MLLMs). On the benchmark side, it curates five MLLM capability categories (VQA, Geometry, Chart, OCR, Grounding) with training data and evaluation protocols, releases expert checkpoints for InternVL2.5 (full fine-tuning) and Qwen2-VL (LoRA), and implements 10 merging algorithms. On the method side, OptMerge combines SVD-based low-rank truncation of task vectors with optimization-based merging (building on WUDI) to reduce noise and improve stability. The paper also explores modality merging (vision+audio+video), showing static merging can compete with dynamic composition methods. Code and checkpoints are publicly released.

## Strengths

- **First systematic benchmark for model merging in MLLMs.** The paper fills a genuine gap by organizing five distinct MLLM capability categories with curated training/evaluation data, releasing expert checkpoints and implementations of 10 merging algorithms. This provides a standardized testbed the community currently lacks.

- **Two training paradigms across two model families.** Using InternVL2.5 (full fine-tuning) and Qwen2-VL (LoRA) tests merging methods across meaningfully different parameter regimes. The observation that LoRA task vectors have different spectral properties than full-fine-tuning task vectors (Sec. 3.2, Fig. 2) is a useful empirical finding.

- **Modality merging experiments (Table 5).** Extending merging to combine vision-language, audio-language, and video-language models is genuinely novel and goes beyond prior merging work. The finding that static merging (TSV: 67.34, OptMerge: 67.00) competes with dynamic online composition methods (DAMC: 66.79) is interesting.

- **Practical validation on Hugging Face checkpoints (Table 6).** Testing on four real community models with diverse specializations (math RL, Pokemon, OCR, Vietnamese VQA) provides a strong practical stress test. OptMerge achieves the best average (66.70) on this challenging heterogeneous set.

- **Theoretical bound (Theorem 3.1).** The analysis connecting merging error to learning rate and iteration count provides formal grounding for the empirical observation that "less fine-tuning merges better."

## Weaknesses

### Fatal

None.

### Major

- **Numerical inconsistency between Tables 3 and 4 undermines the ablation study.** In the main results (Table 3), WUDI Merging on Qwen2-VL achieves 63.65. In the ablation study (Table 4), the same method on the same model is reported as 58.65 — a 5.0 absolute point difference. The paper provides no explanation for this discrepancy. The claimed improvements (+4.43%, +4.65%) in the ablation are computed from 58.65, not from the actual WUDI performance of 63.65. Using the correct baseline (63.65), OptMerge's 63.30 would represent a regression, not an improvement. The "average performance gain of 2.48%" cited in the abstract and contribution list derives from this ablation table but cannot be independently verified against any explicit comparison in the paper. Until this inconsistency is resolved, the method's claimed improvements are unreliable.

- **Overclaimed superiority of OptMerge.** The paper states "our approach achieves superior average results across various scenarios" (Sec. 5.2). However, across the three main experimental settings: (i) InternVL2.5 (Table 2): OptMerge 57.44 vs. WUDI 57.00 — marginal 0.44% gain; (ii) Qwen2-VL (Table 3): OptMerge 63.30 **underperforms** WUDI 63.65; (iii) Modality merging (Table 5): OptMerge 67.00 **underperforms** TSV 67.34. OptMerge is the top method on only 2 of the 4 tables with merging baselines (Tables 2 and 6), and second-best on the other 2 (Tables 3 and 5). The claim of uniform superiority is inconsistent with the paper's own data.

### Minor

- **"Merging outperforms mixture training" claim is unsupported by the controlled comparison.** In the one setting where actual mixture training was conducted (InternVL2.5, Table 2), mixture training achieves 57.66 vs. OptMerge 57.44 — mixture training is better. For Qwen2-VL, the paper substitutes Qwen2-VL-Instruct as the mixture training proxy rather than conducting actual mixture training; Instruct models undergo additional post-training (RLHF, etc.) that can reduce benchmark performance, making this an apples-to-oranges comparison. The paper's claim that merging "potentially surpasses multi-task learning" is too strong given the evidence.

- **Computational efficiency comparison (Table 7) presents only half the picture.** Table 7 compares OptMerge's merge-optimization cost (0.22h, 2.62GB) against mixture training (25.38h, 240GB), but omits the cost of training the five expert models. Producing five fine-tuned experts requires comparable compute to mixture training itself. Presenting only the merge step's cost as "model merging vs. data mixing" is a selective comparison. This should be acknowledged or restructured.

- **No statistical significance reported.** No error bars, confidence intervals, or multiple-run variance is provided for any result. Given that many margins are <1% (e.g., 0.44% on InternVL2.5, -0.55% on Qwen2-VL), it is impossible to assess whether claimed improvements are significant.

- **Confused writing in results section.** The sentence "the merged Qwen2-VL achieves 51.05 and 40.79 on Geometry (vs. 42.50 and 28.95 for individual models)" (line 224) mixes results from different methods (TSV and OptMerge) across different benchmarks (MATH-Vision mini and ChartQA), making it unclear which method produced which number.

### Trivial

None.

## Nice-to-Haves

- **Ablation baseline clarification.** If Table 4 uses a different evaluation subset or protocol than Table 3 (which would explain the 58.65 vs. 63.65 discrepancy), this must be explicitly stated. The "2.48%" claim should be recomputed against the actual baseline.
- **Include other merging methods in Table 10** to determine whether OptMerge's advantage on general tasks is specific to the method or generic to any merging approach.
- **Study λ sensitivity** for OptMerge specifically, since its λ scaling is applied after optimization rather than to raw task vectors.

## Removed Points

These points are flagged to be removed, treat them with caution:
- **"First benchmark" overclaim**: The paper organizes existing datasets into a new categorization framework for model merging. This is a reasonable benchmark contribution, not an inflated claim. REMOVED.
- **λ search range too coarse**: Six values in [0.1, 1.5] is standard practice for model merging papers; all methods use the same range. REMOVED.
- **Table 8 rank ablation shows sensitivity**: The paper correctly notes "relatively stable for k ratios between 10% and 30%" (range: 56.63–57.43, <1% variation). The criticism looked at the full range (10–50%) where the paper does not claim stability. REMOVED.
- **Missing appendix/proofs or formatting issues**: Parser artifacts, not author errors. REMOVED.

## Novel Insights

The most interesting observation across the reviews is the asymmetric effectiveness of OptMerge: it consistently improves over WUDI on InternVL2.5 (full fine-tuning) and Hugging Face checkpoints, but regresses on Qwen2-VL (LoRA). This suggests the low-rank truncation and optimization techniques interact differently with LoRA's already-low-rank parameter structure — a finding the paper acknowledges empirically but does not deeply analyze. Understanding when and why a merging method helps versus hurts across fine-tuning paradigms would be more valuable than claiming uniform superiority, and the paper has the data to support such an analysis if the writing were recalibrated.

## Suggestions

1. **Resolve the Table 3 vs. Table 4 discrepancy.** Explain whether they evaluate different task subsets; if so, state it clearly and recompute the 2.48% claim against the correct baseline.
2. **Recalibrate claims.** Replace "superior average results across various scenarios" with an honest characterization of where OptMerge helps (full fine-tuning, community checkpoints), where it is neutral or slightly behind (Qwen2-VL LoRA, modality merging vs. TSV), and why.
3. **Acknowledge the computational cost of training experts** in Table 7 or restructure the comparison to include end-to-end cost.
4. **Run at least 2–3 seeds** with variance reporting for key comparisons, especially where margins are <1%.

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Borderline (needs revision)</decision>