### Summary

This paper introduces ConciseHint, a framework designed to enhance the efficiency of large reasoning models (LRMs) by reducing the length of their reasoning processes. Unlike existing methods that focus on pre-reasoning optimization, ConciseHint intervenes during the reasoning process by injecting learnable hints to encourage conciseness. The framework adaptively adjusts the intensity and position of hint injection based on the complexity of the query, ensuring that model performance is not compromised. Experiments on state-of-the-art LRMs demonstrate that ConciseHint effectively reduces token usage while maintaining accuracy, and can be seamlessly integrated with other methods to further enhance efficiency.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel approach to improving the efficiency of large reasoning models (LRMs) by directly intervening during the reasoning process. The proposed ConciseHint framework, which injects learnable hints to encourage conciseness, addresses a critical limitation of existing methods that focus on pre-reasoning optimization.
2. The adaptive adjustment of hint intensity and position based on query complexity is a valuable addition, showing the authors' attention to the balance between efficiency and accuracy.
3. The experiments are thorough, demonstrating the effectiveness of ConciseHint across multiple benchmarks and models. The results showing token reduction and accuracy maintenance are compelling.

### Weaknesses

#### Some Related Works


#### comment

1. The paper could benefit from a more detailed analysis of the trade-offs between conciseness and accuracy, especially for highly complex queries. While the adaptive strategy is mentioned, a deeper exploration of its limitations would be valuable. Specifically, the paper lacks a granular analysis of how the hint injection mechanism affects the model's reasoning trajectory, particularly when dealing with questions that require multi-step reasoning or intricate logical deductions. It is unclear how the framework prevents the model from skipping crucial intermediate steps in its pursuit of conciseness, which could lead to a decline in accuracy for complex problems. A more detailed investigation into the types of errors introduced by the concise hints, categorized by the complexity of the queries, would be beneficial.
2. The generalizability of the learned hint embeddings across different types of reasoning tasks could be further explored. The paper primarily focuses on a few benchmarks, and it's unclear how well the learned hints would transfer to tasks with different reasoning requirements, such as commonsense reasoning, symbolic reasoning, or tasks involving spatial or temporal reasoning. The paper should investigate whether the learned hints are task-specific or if they can be generalized across a wider range of reasoning tasks. This would involve testing the framework on a more diverse set of benchmarks and analyzing the performance variations across different reasoning domains.
3. The paper could provide more insights into the optimal settings for hyperparameters like α, β, and γ. While it mentions that the performance is not highly sensitive to β, a more detailed analysis of how these parameters affect performance across different models and datasets would be helpful. The paper lacks a systematic exploration of the hyperparameter space, and it is unclear how the chosen values were determined. A more rigorous analysis, possibly including a sensitivity analysis or a grid search, would provide a better understanding of the optimal hyperparameter settings and their impact on the framework's performance. This would also help in understanding the robustness of the framework to different hyperparameter settings.

### Suggestions

To address the lack of detailed analysis on the conciseness-accuracy trade-off, the authors should conduct a more granular evaluation of the framework's performance across different levels of query complexity. This could involve categorizing the benchmark questions into different complexity levels and analyzing the impact of hint injection on both token reduction and accuracy for each category. Specifically, the authors should investigate how the framework affects the model's reasoning trajectory, examining whether the model skips crucial intermediate steps or introduces errors when trying to be concise. A detailed error analysis, categorizing the types of errors introduced by the concise hints, would provide valuable insights into the limitations of the framework. Furthermore, the authors should explore the impact of different hint intensities on the model's reasoning process, analyzing how the frequency and strength of hint injection affect the model's ability to maintain accuracy while reducing token usage. This analysis should include a quantitative evaluation of the trade-offs between conciseness and accuracy, providing a clear understanding of the framework's limitations and potential areas for improvement.

To further explore the generalizability of the learned hint embeddings, the authors should conduct experiments on a more diverse set of reasoning tasks, including commonsense reasoning, symbolic reasoning, and tasks involving spatial or temporal reasoning. This would involve testing the framework on benchmarks that represent different reasoning domains and analyzing the performance variations across these domains. The authors should investigate whether the learned hints are task-specific or if they can be generalized across a wider range of reasoning tasks. This analysis should include a comparison of the framework's performance with and without fine-tuning the hint embeddings on each specific task. The authors should also explore the possibility of learning task-specific hint embeddings and investigate whether this approach can further improve the framework's performance. This would provide a better understanding of the framework's generalizability and its potential for application in various reasoning scenarios.

Finally, to address the lack of a systematic exploration of the hyperparameter space, the authors should conduct a more rigorous analysis of the impact of hyperparameters α, β, and γ on the framework's performance. This could involve performing a sensitivity analysis or a grid search to determine the optimal hyperparameter settings for different models and datasets. The authors should provide a detailed explanation of how the chosen values were determined and justify their selection based on the experimental results. This analysis should include a quantitative evaluation of the framework's performance across different hyperparameter settings, providing a clear understanding of the impact of each parameter on the framework's efficiency and accuracy. The authors should also investigate whether the optimal hyperparameter settings are consistent across different models and datasets or if they need to be adjusted based on the specific task and model architecture.

### Questions

1. How does the ConciseHint framework handle highly complex queries where conciseness might compromise the thoroughness of the reasoning process? Are there any mechanisms in place to balance conciseness and accuracy in such cases?
2. Can the learned hint embeddings be generalized across different reasoning tasks, or do they need to be trained specifically for each type of task? How would the framework perform on tasks that were not part of the training set?
3. How sensitive is the performance of the ConciseHint framework to the choice of hyperparameters like α, β, and γ? Is there a systematic way to determine the optimal settings for these parameters, or does it require manual tuning for each model and dataset?

### Rating

6

### Confidence

4

**********