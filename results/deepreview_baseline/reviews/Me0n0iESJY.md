## Summary

This paper introduces OptMerge, a benchmark and method for model merging in Multimodal Large Language Models (MLLMs). The authors construct a benchmark with five capability categories (VQA, Geometry, Chart, OCR, Grounding) across two model families (InternVL2.5 and Qwen2-VL), implement 10 merging algorithms, and propose a novel optimization-based method that applies low-rank approximations to task vectors and uses SGD with mean initialization to improve merging stability. The paper also explores modality merging (vision, audio, video) and demonstrates that model merging can approach or exceed mixture training performance while being significantly more computationally efficient.

## Strengths

- **First comprehensive benchmark for MLLM model merging**: The paper provides a well-structured benchmark with clear task categorization, multiple model types (full fine-tuning and LoRA), and diverse evaluation datasets. This fills a clear gap in the literature and will be valuable for the community.
- **Theoretical grounding**: Theorem 3.1 provides a formal analysis of how fine-tuning hyperparameters (learning rate and iterations) affect merging performance, offering the first theoretical explanation for empirical observations that less intensive fine-tuning can yield better merging results.
- **Practical and computationally efficient**: The proposed method requires only 0.22h for 1B models and 3.78h for 7B models, compared to 25h+ for mixture training, while achieving competitive or superior performance. This makes the approach highly practical for real-world deployment.
- **Comprehensive experimental evaluation**: The paper evaluates 10 merging methods across multiple settings (capability merging, modality merging, real Hugging Face checkpoints, different model scales) with thorough ablation studies. The results consistently show OptMerge achieving top or near-top performance.

## Weaknesses

### Fatal
None.

### Major
- **Limited novelty of the proposed method**: The core components of OptMerge (low-rank approximation via SVD, mean initialization, switching Adam to SGD) are individually well-known techniques. The paper's contribution is primarily in combining these elements for the specific context of MLLM merging, but the methodological novelty is incremental. The ablation study (Table 4) shows that the largest gain (+4.43%) comes from initialization, not from the low-rank approximation (+0.22%).
- **Inconsistent performance gains**: While OptMerge achieves the best average score in most tables, the improvements over WUDI Merging are often marginal (e.g., 57.44 vs 57.00 in Table 2, 63.30 vs 63.65 in Table 3). In Table 3, WUDI Merging actually outperforms OptMerge on several individual metrics. The claimed "average performance gain of 2.48%" appears to be selectively reported and not consistently observed across all experiments.
- **Missing statistical significance**: The paper does not report variance or confidence intervals for any experimental results. Given the small performance differences between methods (often <1%), it is unclear whether the reported improvements are statistically significant or within the noise of evaluation.

### Minor
- **Limited modality merging evaluation**: The modality merging experiments (Table 5) only evaluate on two datasets (MUSIC-AVQA and AVQA), which is a narrow assessment for claiming general modality integration capabilities. The paper would benefit from more diverse multimodal evaluation benchmarks.
- **The rank size k selection is ad-hoc**: The paper sets k as "the rank of each task vector divided by the number of tasks (i.e., 5)" without clear justification. While Table 8 shows robustness to k between 10-30%, the choice of 20% (1/5) seems arbitrary and may not generalize to different numbers of tasks.

### Trivial
None.

## Nice-to-Haves

- Include confidence intervals or standard deviations across multiple runs to establish statistical significance of the reported improvements.
- Evaluate on more modality merging benchmarks beyond audio-visual QA, such as video captioning or audio-visual retrieval tasks.
- Provide analysis of which layers benefit most from the proposed optimization versus simple averaging, to better understand where the method adds value.

## Novel Insights

The paper's most interesting insight is the theoretical analysis in Theorem 3.1, which formalizes the trade-off between task-specific performance and mergeability. The finding that cross-task interference grows with ηT (learning rate × iterations) provides a principled explanation for why "less intensive fine-tuning can yield superior merging performance." This insight could guide practitioners in selecting or training models specifically for merging, rather than treating merging as a post-hoc operation on arbitrary fine-tuned models. The empirical observation that InternVL2.5 (full fine-tuning) and Qwen2-VL (LoRA) exhibit fundamentally different task vector distributions (right-skewed vs. multi-modal) is also valuable, as it suggests that merging strategies may need to be tailored to the fine-tuning paradigm.

## Suggestions

- Provide statistical significance testing (e.g., bootstrap confidence intervals) for the main results, especially where performance differences between methods are small (<1%).
- Clarify the selection criteria for the rank size k and provide guidance for practitioners on how to set this hyperparameter when merging different numbers of tasks.
- Include analysis of failure cases or scenarios where model merging degrades performance compared to individual models, to help users understand the limitations of the approach.

## Score and Decision

The paper makes a solid contribution by introducing a much-needed benchmark for MLLM model merging and providing a systematic evaluation of existing methods. The proposed OptMerge method is sensible and achieves competitive results, though its novelty is incremental and the performance gains over strong baselines are modest. The theoretical analysis is a genuine strength. However, the lack of statistical significance testing and the marginal improvements in several settings prevent this from being a top-tier contribution.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>