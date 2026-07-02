### Summary

This paper investigates whether Large Reasoning Models (LRMs) like DeepSeek-R1 and OpenAI’s o1 require prompt optimization for complex tasks such as event extraction. While LRMs are capable of handling complex reasoning tasks, the study explores if their advanced capabilities reduce the need for prompt engineering. The authors conduct experiments comparing LRMs and general-purpose LLMs (GPT-4 and GPT-4.5) in both task performance and prompt optimization. Results show that LRMs benefit significantly from prompt optimization and are more effective as prompt optimizers themselves, producing higher-quality prompts that lead to better task performance. The findings suggest that, despite their advanced reasoning abilities, LRMs still gain substantial improvements from optimized prompts, and their role as prompt optimizers yields more effective task instructions.

### Soundness

3

### Presentation

3

### Contribution

2

### Strengths

1. The paper provides a detailed analysis of how different models perform as both task models and prompt optimizers, offering insights into prompt optimization for LRMs.

2. The study includes experiments on additional tasks beyond event extraction, suggesting that the findings might generalize to other domains.

### Weaknesses

#### Some Related Works


#### comment

1. The study focuses primarily on event extraction, which may limit the generalizability of the findings to other complex reasoning tasks. Although the authors mention that their findings extend to two additional tasks (Geometric Shapes and NCBI Disease NER), the depth of analysis for these tasks is not as comprehensive as the event extraction task. The paper lacks a detailed discussion of the specific challenges and nuances of these additional tasks, making it difficult to assess whether the observed benefits of prompt optimization for LRMs would hold in other complex reasoning domains with different characteristics. For instance, the Geometric Shapes task might rely more on spatial reasoning, while NCBI Disease NER is a named entity recognition task, which has different requirements than event extraction. The limited exploration of these differences weakens the claim of broad generalizability.

2. The paper does not explore the impact of different prompt optimization strategies, such as automated prompt engineering techniques, which could provide a more comprehensive understanding of how to optimize prompts for LRMs. The study focuses on a specific approach to prompt optimization, but it does not compare this approach to other established methods. For example, techniques like Bayesian optimization or evolutionary algorithms could potentially yield even better prompts. The lack of comparison with these alternative methods makes it difficult to assess the effectiveness of the chosen optimization strategy and limits the practical implications of the findings. Furthermore, the paper does not discuss the computational cost associated with the chosen optimization method, which is a crucial factor in real-world applications.

3. The paper does not provide a detailed analysis of the types of errors made by LRMs before and after prompt optimization, which could offer more insights into the specific benefits of optimization. While the paper reports overall performance improvements, it lacks a fine-grained analysis of the error patterns. For example, it would be beneficial to know whether prompt optimization primarily reduces errors related to specific event types or argument roles, or whether it mainly improves the model's ability to handle complex event structures. Without this detailed error analysis, it is difficult to understand the specific mechanisms by which prompt optimization improves LRM performance and to identify areas where further improvements are needed. The paper should include a more detailed analysis of the error types, perhaps using a confusion matrix or similar tool, to provide a more nuanced understanding of the impact of prompt optimization.

### Suggestions

To strengthen the paper, the authors should expand their analysis of generalizability by including a more detailed examination of the additional tasks, Geometric Shapes and NCBI Disease NER. This should involve a deeper dive into the specific challenges of each task and how prompt optimization affects performance in these different contexts. For example, the authors could analyze the types of errors made by the models on each task before and after optimization, and compare these error patterns to those observed in event extraction. This would provide a more nuanced understanding of the generalizability of their findings and help identify the types of tasks where prompt optimization is most effective for LRMs. Furthermore, the authors should consider including a broader range of tasks that represent different types of complex reasoning, such as commonsense reasoning or logical inference, to further validate their conclusions.

In addition, the authors should explore a wider range of prompt optimization strategies, comparing their chosen method to other established techniques. This could include automated methods like Bayesian optimization or evolutionary algorithms, which have been shown to be effective in optimizing prompts for LLMs. The authors should also discuss the computational cost associated with each optimization method, as this is a crucial factor in practical applications. By comparing different optimization strategies, the authors can provide a more comprehensive understanding of the most effective ways to optimize prompts for LRMs and identify the trade-offs between performance and computational cost. This would also help to contextualize the effectiveness of their chosen approach and provide more practical guidance for researchers and practitioners.

Finally, the authors should conduct a more detailed error analysis to understand the specific benefits of prompt optimization. This should involve categorizing the types of errors made by the models before and after optimization, and analyzing how these error patterns change. For example, the authors could examine whether prompt optimization primarily reduces errors related to specific event types or argument roles, or whether it mainly improves the model's ability to handle complex event structures. This analysis should be presented in a clear and concise manner, perhaps using a confusion matrix or similar tool, to provide a more nuanced understanding of the impact of prompt optimization. This detailed error analysis would provide valuable insights into the mechanisms by which prompt optimization improves LRM performance and help identify areas where further improvements are needed.

### Questions

1. How do the authors ensure that the optimized prompts do not overfit to the development set, especially given the iterative nature of the optimization process?

2. Could the authors provide more details on the computational resources required for their prompt optimization framework, particularly when using LRMs as optimizers?

3. How do the authors plan to address the potential for bias in the optimized prompts, especially in tasks like NCBI Disease NER where biases in the training data might be amplified?

4. Can the authors discuss the limitations of their approach in scenarios where labeled data is scarce, and how might their method be adapted for such cases?

### Rating

6

### Confidence

4

**********