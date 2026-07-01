## Summary

This paper introduces **grounding-IQA**, a new image quality assessment paradigm that integrates multimodal referring and grounding (spatial localization via bounding boxes) into IQA, enabling fine-grained quality descriptions and visual question answering with explicit spatial information. The authors construct a large-scale dataset (GIQA-160K, 167K instruction-tuning samples) via an automated annotation pipeline, and a benchmark (GIQA-Bench, 100 images, 250 test samples) to evaluate description quality, VQA accuracy, and grounding precision. Fine-tuning existing MLLMs (LLaVA, mPLUG-Owl2) on GIQA-160K significantly improves their grounding-IQA performance.

## Strengths

- **Novel task definition:** Combining multimodal referring/grounding with IQA is a well-motivated extension that addresses the fine-grained limitations of existing MLLM-based IQA methods. The two subtasks (GIQA-DES and GIQA-VQA) are clearly defined and cover complementary capabilities.
- **Large-scale dataset with automated pipeline:** GIQA-160K (167K samples from 42,960 images) is a substantial resource. The automated pipeline, particularly the object tag extraction, detection, and IQA-based box refinement (Alg. 1), is carefully designed to reduce noise and align with human annotations, as evidenced by the ablation in Tab. 2a and Fig. 6.
- **Comprehensive evaluation:** The benchmark evaluates three distinct aspects (description quality, VQA accuracy, grounding precision) using multiple metrics (BLEU@4, LLM-Score, Acc(Y), Acc(W), mIoU, Tag-Recall). The ablation studies (box optimization, multi-task training, model compatibility) are thorough and provide useful insights.
- **Strong empirical results:** Across five different base MLLMs, fine-tuning on GIQA-160K yields large improvements on all benchmark metrics (Tab. 4 & 5). The method outperforms both general MLLMs and existing grounding-only or IQA-only models, demonstrating the value of the combined task and dataset.

## Weaknesses

### Major

- **Incremental novelty relative to prior work:** The paper’s core idea – combining grounding capabilities with IQA – builds directly on existing methods (Q-Instruct, Grounding DINO, Llama3, and prior grounding MLLMs like Shikra, Ferret, GroundingGPT). The claim of a "new paradigm" is somewhat overstated. The main contributions are the dataset and benchmark, which are valuable but do not introduce fundamentally new architecture or theoretical insights.
- **Benchmark size limits statistical reliability:** GIQA-Bench contains only 100 images and 250 test samples (100 DES + 150 VQA). While the multi-round expert annotation ensures quality, the small size makes reported performance differences (e.g., a few points in LLM-Score) potentially noisy and may not generalize. No confidence intervals or statistical significance tests are reported.
- **Automated annotation pipeline introduces potential label noise:** The pipeline relies on Grounding DINO for detection, Q-Instruct for quality verification, and Llama3 for object tag extraction and QA generation. Errors in any of these models propagate to the dataset. Although the box refinement step (Alg. 1) mitigates some issues, there is no human verification of the full GIQA-160K. The paper could have included a human evaluation of a random subset to quantify label quality.
- **Limited comparison with state-of-the-art score-based IQA methods:** The paper only compares with MLLM-based IQA (DepictQA, Q-Instruct). Score-based IQA methods (e.g., TopIQ, LIQE, MUSIQ, etc.) that output numeric scores are not evaluated. While the output formats differ, the ability to perform grounding-IQA could be compared on the VQA accuracy side (e.g., by converting score predictions to binary or ordinal VQA). This omission weakens the claim that grounding-IQA is "more fine-grained."

### Minor

- **BLEU@4 is a weak metric for quality description evaluation:** BLEU measures n-gram overlap, which penalizes valid paraphrases. The paper also uses LLM-Score, which is more appropriate, but the heavy reliance on BLEU@4 is questionable.
- **Tag-Recall definition requires object name similarity >0.5, but text-similarity metric or threshold justification is missing:** The paper states the object name similarity is measured but does not specify the method (e.g., BERTScore, semantic similarity, fuzzy matching) or provide a sensitivity analysis of the threshold.
- **The discretization of coordinates (grid 20×20) degrades spatial resolution from 9 tokens to 2 IDs:** The paper argues this simplifies learning, but it may lose the ability to distinguish small boxes. An ablation varying grid resolution (e.g., 10×10 vs 40×40) would strengthen this design choice.
- **No analysis of training convergence or number of epochs:** Training for only 2 epochs is reported without evidence that the model converged or assessment of overfitting on a dataset of 167K samples.

## Nice-to-Haves

- Extend GIQA-Bench to include diverse distortions and a larger sample size to increase statistical power.
- Provide a human evaluation of the quality of the automatically generated GIQA-160K annotations (e.g., sampling 500 examples and measuring agreement with human annotators).
- Include a few score-based IQA methods adapted to output binary/ordinal VQA answers (e.g., mapping predictions from TopIQ to "Yes/No" categories) to establish a stronger baseline.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add statistical significance tests (e.g., bootstrap confidence intervals) on GIQA-Bench results to demonstrate that improvements are reliable.
2. Clarify the text similarity metric used in Tag-Recall (e.g., cosine similarity of CLIP embeddings) and provide a brief justification for the 0.5 threshold.
3. Include a small human evaluation (e.g., 100 random examples from GIQA-160K) showing agreement between the automated pipeline and human judgments for grounding quality (IoU) and description quality.
4. Discuss limitations: the 20×20 grid discretization yields a maximum of 42 million possible boxes (covering about 0.5% of 320×320 image area), which may be insufficient for very fine object boundaries.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>