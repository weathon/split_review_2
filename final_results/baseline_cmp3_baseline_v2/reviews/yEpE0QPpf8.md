## Summary

This paper introduces **grounding-IQA**, a new task paradigm that integrates multimodal referring and grounding (spatial localization) with image quality assessment (IQA) to enable fine-grained, location-aware quality evaluation. The authors construct a large-scale dataset **GIQA-160K** (167K instruction-tuning samples) using an automated annotation pipeline that extracts object tags, detects bounding boxes, filters via an IQA-quality check, and merges boxes. They also build a human-annotated benchmark **GIQA-Bench** (100 images, 250 samples) evaluating description quality, VQA accuracy, and grounding precision. Fine-tuning several MLLMs on GIQA-160K shows gains on their benchmark compared to general, grounding-only, and IQA-only baselines.

## Strengths

- **Novel task formulation:** Combining spatial grounding with IQA is a natural and valuable extension of existing MLLM-based IQA methods, addressing the limitation of lacking precise location information in quality descriptions.  
- **Large-scale automated dataset construction:** The pipeline (object tag extraction, bounding box detection, IQA-Filter, Box-Merge, coordinate discretization) is well-designed and produces 160K samples, enabling training of grounding-IQA capabilities in existing MLLMs.  
- **Comprehensive evaluation framework:** The benchmark evaluates three diverse aspects (description quality, VQA accuracy, grounding precision) across multiple metrics, and human annotations add credibility.  
- **Compatibility with multiple base models:** The proposed dataset effectively improves grounding-IQA performance across four different MLLMs (LLaVA-v1.5-7B/13B, LLaVA-v1.6-7B, mPLUG-Owl2-7B), demonstrating generality.

## Weaknesses

### Fatal
None.

### Major

1. **Missing comparison with Q-Ground (Chen et al., 2024b):** The paper cites Q-Ground in related work as a method that achieves "degradation region grounding but lacks referring capabilities." However, Q-Ground is directly relevant: it also performs grounded IQA (via segmentation) and could be a strong baseline. Omitting it from experiments weakens the claim of novelty and the demonstrated advantage of the proposed approach.

2. **Evaluation relies almost entirely on the authors’ own benchmark (GIQA-Bench, only 100 images):** While the benchmark is carefully annotated, its small size limits statistical power and generalizability. The paper promises additional evaluations (traditional IQA tasks, user study, downstream applications) in the supplementary material, but without seeing those results, the main contribution is only validated on a small, self-created test set. This raises concerns about overfitting or dataset bias.

3. **Confusing and potentially erroneous radar chart (Figure 1):** The caption lists five methods, including two identical entries "Grounding-IQA(HPLUS-Duo-7B)" with different colors (cyan and magenta). The model "HPLUS-Duo-7B" is never defined in the paper and does not appear in the main experiments (Table 5). This inconsistency with the presented results undermines the clarity of the paper and suggests the figure may come from a different experiment or contain a mistake.

4. **Automated pipeline injects biases from existing models:** The IQA-Filter step uses Q-Instruct to verify bounding boxes based on quality. This means the training data quality is influenced by the very model that the paper aims to improve upon. The authors do not discuss how this circular dependency might affect the learned grounding-IQA capabilities or whether it limits the method to problems well-handled by Q-Instruct.

### Minor

- The improvement in description quality (BLEU@4, LLM-Score) over strong IQA baselines like Q-Instruct is modest (e.g., LLM-Score 63 vs 62). The main gains are in grounding metrics and VQA accuracy, which is expected since grounding is the new capability.
- The coordinate discretization (20×20 grid) trades off precision for token efficiency, but the authors do not analyze whether this discretization harms grounding accuracy for small or fine-detailed objects.
- The benchmark statistics are skewed (e.g., 55 "No" vs 35 "Yes" for GIQA-VQA), which could bias VQA accuracy results; the paper does not discuss or correct for class imbalance.

### Trivial

- In Table 5, the "Ground" group includes Ferret-7B which achieves the highest GIQA-DES mIoU (0.6458) and Tag-Recall (0.6778) among all methods, but the paper does not highlight or explain why this model performs so well on grounding despite not being fine-tuned on GIQA-160K.

## Nice-to-Haves

- Include Q-Ground as a baseline in experiments to directly compare grounded IQA performance.
- Evaluate on at least one external IQA benchmark (e.g., KonIQ-10k scoring) to show that grounding capability does not hurt overall quality prediction.
- Provide statistical significance measures (e.g., confidence intervals) for the GIQA-Bench results given the small test set.

## Novel Insights

None beyond the paper's own contributions: the key idea of combining referring/grounding with IQA and the automated dataset construction pipeline are the primary novel elements.

## Suggestions

- Replace or correct the radar chart (Figure 1) so it is consistent with the actual methods evaluated in Section 4.3.
- Add a discussion of potential bias from using Q-Instruct in the pipeline and suggest ways to mitigate it.
- Report ablation results on the impact of coordinate discretization granularity on grounding accuracy.

## Score and Decision

**MY FINAL SCORE: 6.0 <score>6.0</score>**
**MY FINAL DECISION:** <decision>Accept</decision>