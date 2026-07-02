### Summary

This paper presents a data-centric approach to training small language models with strong reasoning capabilities. The authors introduce a benchmark-free, self-evolving data optimization method that leverages cross-domain influences to dynamically tailor the data mixture. This approach enables the model to achieve state-of-the-art results among small models with a fully open-sourced recipe, matching Qwen3-0.6B with only 11.7% of its 36T-token training data. The key contributions include a principled dataset-level weighting method, a data-model co-evolution strategy, and empirical results demonstrating the effectiveness of the approach across code, math, and knowledge benchmarks.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel data-centric approach to training small language models, focusing on data quality and token efficiency rather than sheer data quantity.
2. The benchmark-free, self-evolving data optimization method is a significant contribution, allowing for robust reasoning generalization without exposing the model to benchmark data during training.
3. The data-model co-evolution strategy is innovative, adapting to changes in model capacity during training and converging as most samples reach zero or negative influence.
4. The empirical results are strong, demonstrating that MobileLLM-R1 models outperform larger models trained on much more data across several reasoning benchmarks.
5. The authors have made their models, code, and training recipes publicly available, promoting reproducibility and further research in the field.

### Weaknesses

#### Some Related Works


#### comment

1. The paper could benefit from a more detailed analysis of the computational costs associated with the proposed data curation and training methods. While the focus is on small models, understanding the resource requirements for the data optimization process is crucial for practical applications.
2. The paper primarily focuses on reasoning capabilities. It would be valuable to see how the proposed approach affects other aspects of language model performance, such as general knowledge retention, creativity, or conversational abilities.
3. The paper could provide a more in-depth discussion of the limitations of the proposed approach, including potential biases in the curated datasets and the generalizability of the findings to different model architectures or training paradigms.

### Suggestions

The paper should include a more thorough analysis of the computational resources required for the data curation and training process. This should include not only the total training time but also the memory footprint and the number of GPUs used. A breakdown of the computational cost for each stage of the data optimization process, such as the initial data filtering, the self-evolving data selection, and the final data mixing, would be beneficial. This would allow researchers to better assess the practical feasibility of the proposed approach, especially when considering the resource constraints often encountered in academic settings. Furthermore, providing a comparison of the computational costs with other data-centric methods would help to contextualize the efficiency of the proposed approach. For example, how does the computational cost of the self-evolving data optimization compare to other data selection techniques, such as active learning or importance sampling? This would help to understand the trade-offs between computational cost and performance gains.

While the paper demonstrates strong reasoning capabilities, it is important to evaluate the impact of the proposed data-centric approach on other aspects of language model performance. The authors should include an analysis of how the data curation process affects general knowledge retention, creativity, and conversational abilities. For example, does the focus on reasoning data lead to a degradation in performance on tasks that require broader general knowledge or creative text generation? It would be useful to see results on benchmarks that measure these other capabilities, such as MMLU for general knowledge, or HellaSwag for conversational abilities. This would provide a more comprehensive understanding of the strengths and weaknesses of the proposed approach and help to identify potential areas for improvement. Furthermore, it would be valuable to explore whether the data curation process introduces any biases that could affect the model's performance on specific tasks or demographics.

Finally, the paper should include a more detailed discussion of the limitations of the proposed approach. This should include an analysis of potential biases in the curated datasets and the generalizability of the findings to different model architectures or training paradigms. For example, how does the performance of the model vary when trained on different types of data, or when using different model architectures? It would also be useful to explore the sensitivity of the approach to the choice of hyperparameters, such as the learning rate or the number of training epochs. This would help to identify the robustness of the approach and its potential for broader adoption. Furthermore, the authors should discuss the potential limitations of the self-evolving data optimization method, such as the possibility of overfitting to the training data or the difficulty of generalizing to unseen data distributions.

### Questions

1. How does the computational cost of the proposed data curation and training methods compare to traditional approaches that rely on massive datasets? Are there specific optimizations that could further reduce the resource requirements?
2. What are the potential limitations of the self-evolving data optimization method? Are there scenarios where it might not be effective or could lead to suboptimal results?
3. How well does the approach generalize to different model architectures or training paradigms? Have you experimented with variations of the method, and if so, what were the results?

### Rating

6

### Confidence

3

**********