### Summary

The paper presents a novel approach to language-based audio retrieval, focusing on enhancing model robustness and accuracy in aligning audio recordings with text queries. The authors introduce three main contributions: (1) soft-label distillation from an ensemble of retrieval teachers to address non-binary audio-text correspondences, (2) an LLM-driven caption augmentation pipeline that includes back-translation and caption mixing for generating mixed audio, and (3) cluster-guided auxiliary classification to improve alignment in high-ambiguity scenarios. The proposed system leverages a dual encoder architecture, where audio and text inputs are processed separately and aligned in a joint embedding space. The authors demonstrate significant performance improvements on the CLOTHO dataset, achieving a maximum mAP@16 of 48.8 through a weighted ensemble of models.

### Soundness

2

### Presentation

2

### Contribution

2

### Strengths

1. The paper introduces a comprehensive system that integrates multiple advanced techniques, including soft-label distillation, LLM-based data augmentation, and cluster-guided auxiliary classification. This multi-faceted approach addresses the limitations of existing methods and demonstrates a significant improvement in retrieval performance.
2. The authors provide a thorough ablation study that evaluates the impact of each proposed technique. The results show consistent improvements, particularly in scenarios with high correspondence ambiguity, which is a common challenge in audio-text retrieval tasks.
3. The paper is well-structured and clearly explains the methodology, experimental setup, and results. The use of a dual encoder architecture and the detailed description of the training process contribute to the reproducibility of the work.

### Weaknesses

#### Some Related Works


#### comment

1. The paper's reliance on proprietary LLMs for augmentation introduces a dependency that may limit reproducibility and accessibility. Future work should explore open-source alternatives to make the approach more broadly applicable.
2. The cluster-guided auxiliary classification shows mixed results across different models, and the paper does not fully explore why this technique is more effective for some architectures than others. A deeper analysis of the model-specific impacts of cluster guidance would be valuable.
3. The paper does not provide a detailed analysis of the computational resources required for training and inference, which is crucial for assessing the practicality of the proposed approach in real-world applications.

### Suggestions

The authors should investigate the impact of different open-source LLMs for data augmentation, comparing their performance against the proprietary models used in the current study. This would involve not only evaluating the retrieval performance but also analyzing the diversity and quality of the generated captions. Metrics such as BLEU, ROUGE, and BERTScore could be used to quantify the similarity between generated and original captions, and human evaluation could be used to assess the semantic correctness and naturalness of the augmented data. Furthermore, the authors should explore techniques to mitigate potential biases introduced by the LLMs during the augmentation process, such as using adversarial training or data filtering methods. This would ensure that the augmented data does not skew the model's learning process and maintains the integrity of the original dataset.

To better understand the mixed results of cluster-guided auxiliary classification, the authors should conduct a more in-depth analysis of the feature spaces learned by different audio models. This could involve visualizing the cluster assignments for each model and examining how well the clusters align with the semantic content of the audio. Techniques such as t-SNE or UMAP could be used to project the high-dimensional feature vectors into a lower-dimensional space for visualization. Additionally, the authors should investigate the impact of different clustering algorithms and hyperparameters on the performance of the auxiliary classification task. This would help determine whether the observed variations are due to the inherent characteristics of the audio models or the specific clustering method used. A detailed analysis of the confusion matrices for the auxiliary classification task could also provide insights into the types of errors made by each model and guide further improvements.

The authors should provide a detailed breakdown of the computational resources required for each stage of the proposed approach, including pre-training, fine-tuning, and inference. This should include the number of GPUs, the type of GPUs (e.g., NVIDIA V100, A100), the training time, and the memory usage. Furthermore, the authors should report the inference time for a single retrieval query, which is crucial for assessing the real-time applicability of the proposed approach. It would also be beneficial to compare the computational cost of the proposed approach with existing methods, highlighting the trade-offs between performance and computational efficiency. This analysis should also include the impact of different batch sizes on the training and inference times, providing a comprehensive view of the computational requirements of the proposed approach.

### Questions

1. How does the choice of LLM for data augmentation affect the performance of the retrieval system? Have the authors experimented with different LLMs, and if so, what were the observed differences?
2. The paper mentions that cluster guidance yields mixed gains across different backbone models. Can the authors provide more insights into why this technique is more effective for some architectures than others?
3. What are the computational requirements for training and deploying the proposed system? How does the computational cost compare to existing methods, and are there any strategies to reduce this cost without sacrificing performance?
4. How does the system handle real-time audio retrieval queries, and what is the latency involved in the retrieval process?
5. The paper focuses on the CLOTHO dataset. How well do the proposed techniques generalize to other audio retrieval datasets, and what are the potential challenges in adapting the system to different datasets?

### Rating

3

### Confidence

3

**********