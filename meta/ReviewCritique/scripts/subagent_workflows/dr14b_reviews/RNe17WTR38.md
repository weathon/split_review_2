### Summary

This paper explores the concept of model self-evolution, where a single base model acts as both generator and verifier to improve reasoning without external supervision. The authors introduce a framework involving generator-verifier (GV) games, where the model generates candidate solutions and evaluates their quality, creating preference data for fine-tuning. They propose two main variants: SimpleGV, which uses thresholded majority voting for verification, and RevisionGV, which incorporates multi-turn feedback for iterative improvement. The approach is validated on synthetic logical reasoning (Knights and Knaves) and mathematical reasoning tasks, showing consistent improvements across model sizes and data scales. The paper also explores iterative training and curriculum learning, demonstrating strong easy-to-hard generalization.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper presents a novel and well-structured framework for model self-evolution, addressing the challenge of improving language models without external supervision. The introduction of SimpleGV and RevisionGV provides a clear and systematic exploration of different verification strategies.
2. The authors conduct extensive experiments across various model sizes, data scales, and reasoning tasks, providing strong empirical evidence for the effectiveness of their approach. The inclusion of iterative training and curriculum learning further strengthens the results.
3. The paper is well-written and easy to follow, with clear explanations of the methodology and experimental setup. The use of thresholded majority voting and multi-turn feedback is technically sound and contributes to the robustness of the self-evolution process.
4. The demonstration of easy-to-hard generalization is a significant achievement, showing that models trained on simpler instances can effectively transfer to more complex tasks. This highlights the potential of the proposed framework for real-world applications.

### Weaknesses

#### Some Related Works


#### comment

1. While the paper demonstrates strong performance on reasoning tasks, it would be beneficial to explore the applicability of the framework to other types of tasks, such as natural language understanding or generation. This could further validate the generalizability of the approach.
2. The computational cost of the generator-verifier games, especially with multi-turn feedback, could be a concern for practical applications. A more detailed analysis of the computational trade-offs would be valuable.
3. The paper could benefit from a more in-depth discussion of the limitations of the self-evolution process, such as potential biases or the risk of overfitting to the self-generated data. Addressing these concerns would provide a more balanced perspective on the proposed framework.

### Suggestions

The paper's focus on reasoning tasks is a strength, but exploring the framework's applicability to other domains would significantly broaden its impact. For instance, evaluating the method on tasks requiring nuanced understanding of context, such as sentiment analysis or question answering, would provide valuable insights into its generalizability. Furthermore, investigating its performance on generative tasks, like text summarization or creative writing, could reveal potential limitations or areas for improvement. This would involve adapting the generator-verifier game to these new tasks, potentially requiring modifications to the evaluation metrics and the feedback mechanisms. Such an analysis would not only strengthen the paper's claims but also provide a more comprehensive understanding of the framework's capabilities and limitations.

Regarding computational costs, a more detailed analysis is needed to assess the practical feasibility of the proposed approach. The paper should include a breakdown of the computational resources required for each component of the generator-verifier game, including the number of forward passes, the memory footprint, and the time complexity. Specifically, the cost of multi-turn feedback should be analyzed in terms of the number of iterations and the computational overhead of each iteration. This analysis should also consider the impact of different model sizes and batch sizes on the overall computational cost. Furthermore, the paper should explore potential optimizations to reduce the computational burden, such as using more efficient sampling techniques or employing model compression methods. A clear understanding of the computational trade-offs is crucial for the practical adoption of the proposed framework.

Finally, the paper should delve deeper into the potential limitations of the self-evolution process. While the framework demonstrates strong performance, it is important to acknowledge the risk of overfitting to the self-generated data. The paper should investigate the diversity of the generated data and the potential for the model to learn spurious correlations or biases. Furthermore, the paper should explore the sensitivity of the framework to the initial model and the impact of different training strategies on the final performance. A more thorough analysis of these limitations would provide a more balanced perspective on the proposed framework and guide future research in this area. This could involve techniques such as analyzing the distribution of generated data, comparing the performance of models trained with different initializations, and exploring the impact of different training parameters.

### Questions

1. How does the performance of the proposed framework compare to other self-improvement methods in terms of computational efficiency?
2. Can the authors provide more insights into the cases where the self-evolution process fails to improve the model's performance?
3. How does the choice of the base model affect the effectiveness of the self-evolution process?

### Rating

6

### Confidence

3

**********