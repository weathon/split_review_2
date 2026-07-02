### Summary

This paper proposes a framework for automated code refactoring using reinforcement learning (RL) enhanced by contrastive pre-trained code graph embeddings. It aims to improve code quality by balancing syntactic improvements with semantic preservation.

### Soundness

2

### Presentation

2

### Contribution

2

### Strengths

1. The paper introduces a unique approach by combining contrastive learning with RL for code refactoring. It uses a syntax-guided contrastive encoder to create structural representations of code graphs.
2. The paper provides a thorough experimental evaluation, demonstrating the proposed method's effectiveness across multiple metrics and datasets.

### Weaknesses

#### Some Related Works


#### comment

1. The paper’s writing is difficult to follow, with overly complex language and unclear explanations. Simplifying the language and providing clearer explanations would improve accessibility.
2. While the approach is novel, it adds significant complexity by integrating contrastive learning, RL, and composite reward functions. This complexity may hinder practical implementation and scalability. The use of contrastive learning, while beneficial for representation, introduces a pre-training phase that requires substantial computational resources and careful hyperparameter tuning. The RL component, with its exploration-exploitation trade-offs, adds another layer of complexity, making the system harder to debug and maintain. Furthermore, the composite reward function, while aiming to balance multiple objectives, increases the difficulty of optimizing the RL agent.
3. The paper primarily compares against Java-based methods, limiting the assessment of the framework's generalizability across languages. The evaluation should include a broader range of languages and codebases to demonstrate the robustness of the proposed approach. The current evaluation does not sufficiently address the challenges of adapting the method to different programming paradigms or language-specific features.
4. The paper does not sufficiently discuss the computational costs associated with the proposed method, which involves expensive processes like contrastive pre-training and RL training. The lack of a detailed analysis of training time, memory usage, and the hardware requirements makes it difficult to assess the practical feasibility of the approach, especially for large-scale codebases.

### Suggestions

To improve the paper, the authors should focus on clarifying the technical explanations and providing a more detailed analysis of the computational costs. Specifically, the description of the contrastive learning process and the RL training procedure should be made more accessible to a broader audience. The authors should also include a breakdown of the time and memory requirements for each stage of the pipeline, including pre-training, RL training, and inference. This should include a discussion of the hardware used for the experiments, such as the type of GPUs and CPUs, and the number of cores used. Furthermore, the authors should provide a more thorough analysis of the scalability of the approach, including how the computational costs scale with the size of the codebase and the complexity of the code being refactored. This analysis should include empirical results on larger codebases to demonstrate the practical applicability of the method.

Additionally, the evaluation should be expanded to include a more diverse set of programming languages and codebases. The current focus on Java limits the generalizability of the findings. The authors should include experiments on languages with different programming paradigms, such as Python, C++, or JavaScript, to demonstrate the robustness of the approach. This should include a discussion of any language-specific adaptations that were necessary to apply the method to different codebases. The evaluation should also include a comparison with existing code refactoring tools and techniques, such as Checkstyle, to provide a more comprehensive assessment of the proposed method's performance. This comparison should include a discussion of the strengths and weaknesses of the proposed method compared to these existing approaches.

Finally, the authors should address the limitations of the proposed approach, particularly the complexity of the system and the computational costs associated with it. The paper should include a discussion of the trade-offs between the performance of the method and its computational requirements. The authors should also explore potential ways to reduce the complexity of the system and the computational costs, such as using more efficient algorithms or simplifying the reward function. This discussion should include a consideration of the practical implications of the proposed method for real-world software development scenarios, including the ease of integration into existing development workflows and the potential for automated refactoring of large codebases.

### Questions

1. Could the authors clarify the computational requirements of the proposed approach, particularly the costs associated with pre-training and RL training?
2. How does the framework perform when applied to codebases in languages other than Java, and are there any specific adaptations needed for different programming paradigms?
3. Could the authors provide a comparison with other automated refactoring tools, such as Checkstyle, to evaluate the relative performance and effectiveness of their approach?

### Rating

5

### Confidence

3

**********