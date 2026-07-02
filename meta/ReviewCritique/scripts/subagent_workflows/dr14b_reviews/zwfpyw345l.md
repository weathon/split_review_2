### Summary

The paper proposes a hierarchical code embedding model for reinforcement learning (RL) state representation in code-related tasks. The model uses multi-level attention mechanisms—token-level, function-level, and module-level—to capture both local and global code semantics. Experiments are conducted on three tasks: code completion, program repair, and algorithmic problem-solving, with results indicating improvements over baseline methods.

### Soundness

2

### Presentation

2

### Contribution

2

### Strengths

- The hierarchical attention model effectively captures code semantics at multiple levels, which is beneficial for tasks requiring deep code understanding.
- The paper evaluates the model across diverse tasks, demonstrating its generalizability in different code-related RL applications.

### Weaknesses

#### Some Related Works


#### comment

 - The model may face scalability challenges with very large codebases, as multi-level attention can increase computational demands. The paper lacks a thorough analysis of how the model's performance and resource consumption scale with increasing code complexity, such as the number of functions or files. This is a critical concern for real-world applications involving large projects.
- The effectiveness of the model depends on the quality of the abstract syntax tree (AST) and code dependency graph (CDG) representations, which might not capture all semantic nuances. The paper does not discuss the potential limitations of relying on these representations, such as the inability to capture dynamic features or runtime behavior, which could be crucial for certain code understanding tasks. The impact of noisy or incomplete AST/CDG data on the model's performance is also not addressed.
- While the hierarchical structure is beneficial, it adds complexity to the model, which might make it harder to implement and fine-tune in practical applications. The paper does not provide sufficient guidance on the practical challenges of implementing and fine-tuning such a complex model, including the sensitivity to hyperparameter settings and the computational cost of training. The lack of discussion on strategies for mitigating these challenges makes it difficult to assess the practical applicability of the proposed approach.

### Suggestions

The paper should include a more detailed analysis of the model's scalability, specifically addressing how performance and resource consumption change with increasing code complexity. This should include experiments with varying numbers of functions and files, and a discussion of the computational bottlenecks. It would be beneficial to explore techniques for optimizing the model's performance on large codebases, such as pruning less important attention heads or using more efficient attention mechanisms. Furthermore, the authors should investigate the impact of different code structures, such as deeply nested functions or complex control flow, on the model's performance. This analysis should provide practical guidance on the applicability of the model to real-world scenarios.

To address the limitations of relying solely on AST and CDG representations, the authors should explore incorporating additional semantic information, such as type annotations, documentation strings, or even runtime behavior. This could involve integrating information from static analysis tools or using techniques like execution tracing to capture dynamic features. The paper should also discuss the potential impact of noisy or incomplete AST/CDG data on the model's performance and explore methods for mitigating these effects, such as data augmentation or robust training techniques. A more thorough analysis of the model's sensitivity to the quality of the input representations is needed to ensure its robustness in diverse code environments.

Finally, the paper should provide more practical guidance on implementing and fine-tuning the proposed model. This should include a discussion of the sensitivity to hyperparameter settings, the computational cost of training, and strategies for mitigating these challenges. The authors could explore techniques like transfer learning or meta-learning to reduce the need for extensive fine-tuning. Additionally, the paper should provide a detailed analysis of the model's interpretability, including which parts of the code are most influential for the RL agent's decisions. This would help in understanding the model's behavior and identifying potential areas for improvement. The authors should also consider releasing their code to facilitate reproducibility and further research.

### Questions

- How does the model perform on very large codebases with thousands of functions or files? Are there any scalability issues?
- How interpretable are the learned state representations? Can you identify which parts of the code are most influential for the RL agent’s decisions?
- Have you considered releasing the code? It would help with reproducibility and further research.

### Rating

5

### Confidence

3

**********