### Summary

This paper investigates the robustness of the scaling laws proposed by Hoffmann et al. (2022), known as the Chinchilla scaling laws. The authors address ambiguities in the model parameters used in the Chinchilla paper and analyze the sensitivity of the scaling law estimates and the compute-optimal tokens-to-parameter ratio to various perturbations. The paper finds that the key results of the Chinchilla paper remain robust despite potential discrepancies in model parameter interpretations and perturbations.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper is well-written and easy to follow, with clear explanations of the methodology and results.
2. The authors provide a thorough analysis of the ambiguities in model parameters and their impact on the scaling law estimates.
3. The sensitivity analysis is comprehensive, considering various types of perturbations and their effects on the key results.
4. The findings offer valuable insights into the robustness of the Chinchilla scaling laws, which are important for guiding future research and practical applications in language model scaling.

### Weaknesses

#### Some Related Works


#### comment

1. The paper could benefit from a more detailed discussion of the implications of the findings for practitioners and researchers who rely on the Chinchilla scaling laws for model development. Specifically, while the paper demonstrates robustness to parameter perturbations, it does not fully explore how these findings translate into practical guidance for model training. For instance, what are the specific recommendations for practitioners when choosing model sizes and training data quantities, given the observed robustness? The paper should provide more concrete examples of how the robustness analysis impacts the practical application of the scaling laws.
2. Further investigation into the limitations of the robustness could provide a more complete understanding of the conditions under which the Chinchilla results hold. The paper explores several types of perturbations, but it could benefit from a more systematic exploration of the boundaries of this robustness. For example, are there specific types of model architectures or training regimes where the scaling laws break down? What are the critical thresholds for parameter perturbations that lead to significant deviations from the predicted scaling behavior? A more detailed analysis of these limitations would provide a more nuanced understanding of the applicability of the Chinchilla scaling laws.

### Suggestions

To enhance the practical implications of this work, the authors should include a more detailed discussion on how the observed robustness of the Chinchilla scaling laws translates into actionable guidance for practitioners. This could involve providing specific recommendations for choosing model sizes and training data quantities based on the findings. For example, the authors could explore the trade-offs between model size and training data, and provide guidelines on how to optimize these choices for different computational budgets. Furthermore, the authors should consider including a discussion on how the robustness analysis impacts the selection of hyperparameters, such as learning rates and batch sizes. This would make the paper more valuable for practitioners who are looking to apply the scaling laws in real-world scenarios. The authors could also provide concrete examples of how the robustness analysis impacts the practical application of the scaling laws, such as how to choose the optimal model size and training data for a given task and computational budget.

To further investigate the limitations of the robustness, the authors should conduct a more systematic exploration of the boundaries of the observed robustness. This could involve testing the scaling laws under a wider range of conditions, such as different model architectures, training regimes, and types of perturbations. For example, the authors could explore how the scaling laws behave with different types of attention mechanisms or different activation functions. They could also investigate the impact of different optimization algorithms and learning rate schedules on the robustness of the scaling laws. Furthermore, the authors should consider exploring the critical thresholds for parameter perturbations that lead to significant deviations from the predicted scaling behavior. This would provide a more nuanced understanding of the conditions under which the Chinchilla scaling laws hold and would help practitioners avoid situations where the scaling laws break down. The authors could also investigate the impact of data quality and diversity on the robustness of the scaling laws.

Finally, the authors should consider including a more detailed discussion of the theoretical underpinnings of the observed robustness. While the paper provides empirical evidence of the robustness, it could benefit from a more in-depth analysis of the theoretical reasons behind this robustness. For example, the authors could explore the connection between the observed robustness and the underlying optimization landscape of language models. This would provide a more complete understanding of the mechanisms that contribute to the robustness of the Chinchilla scaling laws and would help researchers develop more robust and reliable scaling laws in the future. The authors could also explore the connection between the observed robustness and the information content of the training data.

### Questions

1. How do the authors envision the findings of this paper influencing the future development of scaling laws for language models?
2. Are there any specific conditions or scenarios where the robustness of the Chinchilla results might not hold, and how can these be identified or mitigated?

### Rating

6

### Confidence

3

**********