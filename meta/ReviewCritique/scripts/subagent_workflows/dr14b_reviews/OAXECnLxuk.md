### Summary

The paper introduces DaVinci, a novel multimodal large language model (MLLM) designed for parsing scientific diagrams into structured TiKZ code. The authors address the challenges of diverse visual primitives, complex layouts, and strict syntax in scientific diagrams. DaVinci employs a two-stage framework: first, supervised learning of visual primitives, followed by reinforcement learning to refine structural relationships. A key contribution is the creation of the TiKZ30K dataset, which features high-quality diagram-TiKZ code pairs with optimized drawing order and comment annotations. The model's performance is further enhanced by a hybrid reward function in reinforcement learning, which combines visual fidelity, structural consistency, and code correctness. The experimental results demonstrate that DaVinci significantly outperforms existing open-source MLLMs and even surpasses leading commercial models like GPT-5 and Claude-Sonnet-4 in diagram parsing tasks.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel two-stage framework that effectively addresses the complexities of scientific diagram parsing. The combination of supervised learning for visual primitives and reinforcement learning for structural relationships is a well-reasoned approach.
2. The creation of the TiKZ30K dataset is a significant contribution. The dataset's high-quality, optimized drawing order, and comment annotations provide valuable resources for training and evaluating MLLMs in this domain.
3. The hybrid reward function in reinforcement learning is a creative solution to the challenges of evaluating diagram parsing. By combining visual fidelity, structural consistency, and code correctness, the authors have developed a more comprehensive and effective evaluation metric.
4. The experimental results are compelling, demonstrating that DaVinci outperforms both open-source and proprietary models. The ablation studies and human evaluations further validate the effectiveness of the proposed approach.

### Weaknesses

#### Some Related Works


#### comment

1. The reliance on the TiKZ30K dataset might limit the generalizability of the model to diagrams with different visual styles or structures. While the dataset is high-quality, it may not fully capture the diversity of scientific diagrams encountered in real-world scenarios. The specific focus on TiKZ code generation, while beneficial for LaTeX users, might not be as broadly applicable as more general vector graphics formats like SVG. This could restrict the model's utility in contexts where TiKZ is not the preferred or required output format.
2. The computational cost of the two-stage training process, especially the reinforcement learning stage, could be a barrier to adoption for some researchers. The paper does not provide a detailed analysis of the computational resources required for training, making it difficult to assess the practical feasibility of replicating the results. The reinforcement learning stage, in particular, is known to be computationally intensive, and the lack of clarity on the hardware and time requirements is a significant concern.
3. The complexity of the reward function in reinforcement learning might make it challenging to fine-tune or adapt for different types of diagrams. The hybrid reward function, while effective, combines multiple metrics, and the relative importance of these metrics might vary depending on the specific diagram type. The paper does not provide sufficient guidance on how to adjust the reward function for different scenarios, which could limit the model's adaptability.

### Suggestions

To address the limitations regarding the dataset, the authors should consider expanding the TiKZ30K dataset to include a wider variety of diagram types and visual styles. This could involve incorporating diagrams from different scientific domains, as well as diagrams with varying levels of complexity and abstraction. Furthermore, exploring the use of data augmentation techniques could help to increase the diversity of the training data without requiring the collection of new diagrams. The authors should also investigate the possibility of adapting the model to generate output in more general vector graphics formats like SVG, which would broaden the applicability of the model. This could involve training a separate model or adapting the existing model to handle different output formats, which would make the model more versatile and useful in a wider range of contexts.

To mitigate the computational cost of the training process, the authors should provide a detailed analysis of the computational resources required for training, including the hardware specifications, training time, and energy consumption. This would allow other researchers to assess the feasibility of replicating the results and make informed decisions about resource allocation. The authors should also explore techniques for reducing the computational cost of the reinforcement learning stage, such as using more efficient optimization algorithms or reducing the number of training iterations. Additionally, investigating the use of transfer learning could help to reduce the training time and computational resources required for new tasks. Providing a clear and detailed description of the training process would make the model more accessible and reproducible.

To improve the adaptability of the reward function, the authors should provide more guidance on how to fine-tune or adapt the reward function for different types of diagrams. This could involve conducting a sensitivity analysis to determine the relative importance of different reward components for various diagram types. The authors should also explore the possibility of using a more flexible reward function that can be easily adjusted based on the specific requirements of the task. This could involve using a hierarchical reward function or a meta-learning approach that can learn to adapt the reward function based on the input diagram. Providing clear guidelines and examples of how to adapt the reward function would make the model more versatile and useful in a wider range of applications.

### Questions

1. How does the model perform on diagrams that are significantly different from those in the TiKZ30K dataset? Are there any plans to evaluate the model on a more diverse set of diagrams?
2. What are the computational requirements for training the model, and how can they be optimized to make the method more accessible to researchers with limited resources?
3. How sensitive is the model's performance to the choice of hyperparameters in the reinforcement learning stage? Are there any guidelines for selecting appropriate hyperparameters for different types of diagrams?

### Rating

6

### Confidence

4

**********