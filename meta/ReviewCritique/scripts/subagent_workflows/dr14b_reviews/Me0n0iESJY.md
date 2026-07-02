### Summary

This paper introduces a model merging benchmark for MLLMs, which includes multiple tasks such as VQA, Geometry, Chart, OCR, and Grounding, studying both LoRA and full fine-tuning models. Moreover, they explore how model merging can combine different modalities (e.g., vision-language, audio-language, and video-language models), moving toward the Omni-language model. They implement 10 model merging algorithms on the benchmark. Furthermore, they propose a novel method that removes noise from task vectors and robustly optimizes the merged vector based on a loss defined over task vector interactions, achieving an average performance gain of 2.48%. They find that model merging offers a promising way for building improved MLLMs without requiring training data. Their results also demonstrate that the complementarity among multiple modalities outperforms individual modalities. All code and checkpoints are publicly available here.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a model merging benchmark for MLLMs, which includes diverse specialized models such as VQA, Geometry, Chart, OCR, and Grounding. For each corresponding task, they collect comprehensive public datasets with at least 100k samples to ensure effective supervised fine-tuning, and select corresponding benchmarks to evaluate distinct capabilities. They derive an upper bound on the error between the merged model and expert models, proving that merging performance is influenced by the learning rate and iterations, which control the extent of parameter drift. Smaller parameter changes sacrifice task performance but lead to more effortless merging. They choose two types of vision-language models: InternVL2.5 and Qwen2-VL, providing both LoRA and full fine-tuning checkpoints. Moreover, most existing MLLMs specialize in dual modalities, and incorporating new modality encoders requires re-training on new modality-text data. Generating high-quality multimodal instruction data is resource-consuming (Jiang et al., 2024). Therefore, they explore how model merging can efficiently combine different modalities (e.g., vision-language, audio-language, and video-language models), moving toward the Omni-language model. This offers a data-free way to reuse and integrate modality-specific encoders into a unified LLM.

2. They conduct an in-depth comparison and analysis of state-of-the-art merging methods in capability and modality merging settings. Furthermore, they propose a novel merging method that improves the task vector (i.e., the parameter change between fine-tuned and base models) optimization. OptMerge optimizes the merged model based on a loss defined over task vector interactions and applies low-rank approximations to reduce redundant noise, achieving the best results. Combining multiple MLLMs without requiring data, the merged model can even outperform expert MLLMs in their respective capabilities and mixture data training. They also find that merging methods effectively integrate inputs from multiple modalities, outperforming models trained on individual modalities, thus emphasizing the complementary nature of modal information.

3. They conduct comprehensive experiments and analyses on their benchmark. Their empirical results suggest that model merging can outperform mixture training, offering a viable path to omni-model alignment and a scalable approach to developing MLLMs with reduced computational cost and training time.

### Weaknesses

#### Some Related Works


#### comment

1. The paper does not provide a detailed analysis of the computational cost and memory requirements of the proposed method. It is unclear how the method scales with the number of models being merged and the size of the models. Specifically, the paper lacks a breakdown of the time and memory consumption for each step of the OptMerge algorithm, such as task vector computation, low-rank approximation, and optimization. This makes it difficult to assess the practical feasibility of the method for large-scale applications.
2. The paper does not discuss the potential limitations of the proposed method, such as the sensitivity to the choice of hyperparameters or the robustness to different types of models. The paper does not explore how the performance of OptMerge varies with different learning rates, batch sizes, or optimization algorithms. Furthermore, it is unclear how the method performs when merging models with significantly different architectures or pre-training objectives. A more thorough investigation of these aspects is needed to understand the generalizability of the approach.

### Suggestions

The paper should include a detailed analysis of the computational cost and memory requirements of the proposed method. This analysis should include a breakdown of the time and memory consumption for each step of the OptMerge algorithm, such as task vector computation, low-rank approximation, and optimization. The analysis should also explore how the computational cost and memory requirements scale with the number of models being merged and the size of the models. This would provide a more complete picture of the practical feasibility of the method for large-scale applications. For example, the authors could provide a table showing the time and memory consumption for different numbers of merged models and different model sizes. This would allow readers to better understand the trade-offs between performance and computational cost.

Furthermore, the paper should include a more thorough investigation of the potential limitations of the proposed method. This should include an analysis of the sensitivity to the choice of hyperparameters, such as learning rates, batch sizes, and optimization algorithms. The authors should also explore how the method performs when merging models with significantly different architectures or pre-training objectives. This could involve experiments with models trained on different datasets or using different pre-training techniques. A more comprehensive analysis of these aspects would provide a better understanding of the generalizability of the approach and its limitations. For instance, the authors could perform an ablation study to show how the performance of OptMerge varies with different hyperparameter settings. They could also compare the performance of OptMerge when merging models with different architectures or pre-training objectives.

Finally, the paper should discuss the potential impact of the proposed method on the interpretability of the merged model. While the paper shows that OptMerge achieves good performance, it is unclear how the merging process affects the interpretability of the resulting model. The authors should explore whether the merged model retains the interpretability of the individual models or whether the merging process introduces new challenges for interpretation. This could involve analyzing the attention maps or other interpretability techniques to understand how the merged model makes predictions. Addressing this aspect would provide a more complete understanding of the trade-offs between performance and interpretability.

### Questions

1. How does the proposed method compare to other model merging methods in terms of computational cost and memory requirements?
2. What are the potential limitations of the proposed method, such as the sensitivity to the choice of hyperparameters or the robustness to different types of models?
3. How does the proposed method affect the interpretability of the merged model?

### Rating

6

### Confidence

3

**********