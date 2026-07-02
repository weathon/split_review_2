## Summary
This paper introduces OptMerge, a benchmark and method for merging multimodal LLMs (MLLMs). The benchmark provides fine-grained categorization of MLLM capabilities (VQA, Geometry, Chart, OCR, Grounding) with trained expert models, and explores merging across modalities (vision, audio, video). The proposed OptMerge method improves task vector optimization by applying low-rank approximations to remove noise and using tailored optimization strategies (SGD with mean initialization) for LoRA fine-tuned models, achieving average performance gains of 2.48% over baselines.

## Strengths
- **First comprehensive model merging benchmark for MLLMs**: The paper provides a well-structured benchmark with clear task categorization, multiple expert models trained on substantial datasets (100k+ samples per task), and both full fine-tuning and LoRA variants. This fills a clear gap in the literature and will be valuable for the model merging community.
- **Novel theoretical analysis**: Theorem 3.1 provides the first theoretical explanation connecting fine-tuning dynamics (learning rate, iterations) to merging performance, explaining why less intensive fine-tuning can yield better merging results. This insight is practically useful for practitioners selecting models to merge.
- **Strong empirical results**: The proposed OptMerge method consistently achieves best or near-best performance across multiple settings (capability merging, modality merging, real Hugging Face checkpoints, different model scales), and in some cases matches or exceeds mixture training baselines. The ablation study (Table 4) clearly demonstrates the contribution of each component.
- **Practical focus on real-world applicability**: The paper evaluates on actual Hugging Face checkpoints from different developers (Table 6) and demonstrates computational efficiency advantages over mixture training (Table 7), showing practical relevance beyond synthetic benchmarks.

## Weaknesses
### Fatal
None.

### Major
- **Limited novelty of the proposed method**: The core components of OptMerge—low-rank approximation via SVD, mean initialization, and optimizer choice—are individually well-established techniques. The paper's main contribution is combining these in a specific way for MLLM merging, but the method lacks a fundamentally new algorithmic insight. The improvement over WUDI Merging is modest (0.44% on InternVL2.5, 1.9% on Hugging Face checkpoints), and the ablation shows that initialization alone accounts for most of the gain (4.43% vs 4.65% total).
- **Incomplete comparison with relevant baselines**: The paper does not compare against AdaMMS or UQ-Merge, which are the most directly related MLLM merging methods. While the authors note limitations of these methods (test set requirement, two-model limitation), a quantitative comparison on the benchmark would strengthen the evaluation. The paper also does not compare against simple baselines like Fisher-weighted averaging or RegMean.
- **Theoretical analysis has limited practical impact**: Theorem 3.1 provides an upper bound with O(γ^T), O(δηT), and O(η²T²) terms, but the paper does not use this analysis to derive practical guidelines (e.g., optimal stopping criteria for fine-tuning) or to explain specific experimental observations beyond the general statement that "smaller parameter changes are better."

### Minor
- **Evaluation metrics and statistical significance**: The paper reports single-run results without confidence intervals or statistical significance tests. Given the variability in model merging outcomes, reporting standard deviations across multiple runs would strengthen the claims.
- **Limited analysis of failure cases**: The paper shows that Iso-C fails on Qwen2-VL (Table 3) and provides a brief explanation, but does not systematically analyze when different merging methods fail or succeed. A deeper analysis of task interference patterns would be valuable.
- **Modality merging evaluation is limited**: Only two datasets (MUSIC-AVQA, AVQA) are used for modality merging evaluation, and the comparison is against only two baselines (NaiveMC, DAMC). A broader evaluation with more datasets and baselines would strengthen this contribution.

### Trivial
- The paper uses "Omni-language model" and "Omni model" inconsistently; standard terminology would be "multimodal model" or "omnimodal model."
- Some table formatting issues (e.g., Table 6 has "CharQVA" instead of "ChartQA", "OCRQVA" instead of "OCRVQA").

## Nice-to-Haves
- Analysis of which layers benefit most from the proposed optimization vs. simple averaging
- Investigation of whether the method scales to merging more than 5 models
- Discussion of when model merging might fail (e.g., when task vectors are too large or tasks are too dissimilar)

## Novel Insights
The paper's key insight is that model merging performance is fundamentally bounded by fine-tuning dynamics—specifically, that the product of learning rate and iterations (ηT) controls the trade-off between task performance and mergeability. This explains why highly fine-tuned models (like Qwen2.5-Math and Qwen2.5-Coder) merge poorly, and suggests that practitioners should prefer models with smaller parameter changes when selecting models for merging. The observation that LoRA fine-tuned models present unique optimization challenges due to their low-rank structure (causing the merged vector to take shortcuts by increasing magnitude) is also practically valuable.

## Suggestions
1. Compare against AdaMMS and UQ-Merge quantitatively on the benchmark, even if they require test set access—this would establish the relative performance of data-free vs. data-dependent methods.
2. Report results with standard deviations across multiple runs (at least 3) to establish statistical significance.
3. Provide practical guidelines based on Theorem 3.1, such as recommended ranges for ηT or stopping criteria for fine-tuning to maximize mergeability.
4. Expand the modality merging evaluation to include more datasets and compare against a broader set of baselines.

## Score and Decision
The paper makes a solid contribution by introducing a much-needed benchmark for MLLM merging and providing a well-engineered method that consistently improves over baselines. However, the method's novelty is incremental, the theoretical analysis has limited practical impact, and the evaluation misses key baselines. The benchmark itself is the strongest contribution and will likely be valuable to the community.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>