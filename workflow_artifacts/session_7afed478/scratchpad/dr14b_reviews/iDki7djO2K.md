### Summary

The paper presents a novel framework for understanding and measuring forgetting in machine learning. The authors define forgetting as a lack of self-consistency in a learner's predictive distribution over future experiences, manifesting as a loss of predictive information. This definition is formalized through a measure called the "propensity to forget," which quantifies the extent to which a learner's predictive distribution changes after updates. The authors validate their framework through a series of experiments across different learning paradigms, including regression, classification, generative modeling, continual learning, and reinforcement learning. The results demonstrate that forgetting is a pervasive phenomenon that impacts learning efficiency, and that optimal learning often involves a balance between adaptation and retention.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel, algorithm- and task-agnostic framework for understanding forgetting, which is a significant contribution to the field. By defining forgetting as a lack of self-consistency in predictive distributions, the authors provide a unified perspective that applies across various learning paradigms.
2. The theoretical foundation is well-developed, with clear definitions and a rigorous mathematical formulation. The concept of "propensity to forget" is a valuable contribution that allows for quantitative analysis of forgetting.
3. The empirical validation is comprehensive, spanning multiple learning paradigms and demonstrating the pervasiveness of forgetting. The experiments are well-designed and provide strong support for the theoretical framework.
4. The paper is well-written and clearly structured, making it accessible to a broad audience. The authors provide intuitive explanations and visualizations that aid in understanding the complex concepts.

### Weaknesses

#### Some Related Works


#### comment

1. The paper's focus on theoretical framework and empirical validation leaves limited space for practical applications. While the authors demonstrate the pervasiveness of forgetting, they do not explore how their framework can be used to develop methods for mitigating forgetting in real-world scenarios. This limits the immediate impact of the work on practitioners.
2. The experiments, while comprehensive, are primarily conducted on synthetic datasets and relatively simple models. It is unclear how the findings would generalize to more complex, real-world datasets and architectures, particularly in domains like natural language processing or computer vision.
3. The paper does not provide a detailed analysis of the computational complexity of calculating the "propensity to forget." This is a crucial aspect for practical applications, as the measure involves computing divergences between predictive distributions, which can be computationally expensive for large models and datasets.
4. The framework assumes that the learner's predictive distribution accurately reflects its state. However, in practice, many learning algorithms use approximations or heuristics that may not perfectly align with this assumption. The paper does not adequately address how these approximations might affect the validity of the "propensity to forget" measure.
5. The paper does not explore the relationship between the proposed framework and existing methods for mitigating forgetting, such as regularization techniques or replay buffers. A discussion of how the "propensity to forget" measure can be used to guide the development or evaluation of these methods would strengthen the paper's practical relevance.

### Suggestions

The authors should consider expanding their work to include more practical applications of their framework. Specifically, they could investigate how the "propensity to forget" measure can be used to design or select learning algorithms that are more resistant to forgetting. For example, they could explore whether minimizing the propensity to forget during training leads to improved performance in continual learning scenarios. This could involve incorporating the propensity to forget into the loss function or using it as a criterion for model selection. Furthermore, the authors could explore the use of their framework in conjunction with existing techniques for mitigating forgetting, such as regularization or replay buffers. This would involve analyzing how these techniques affect the propensity to forget and whether the framework can provide insights into their effectiveness.

To address the limitations of the experimental setup, the authors should conduct experiments on more complex, real-world datasets and architectures. This would involve evaluating the framework on tasks such as natural language processing or computer vision, using state-of-the-art models. The authors should also investigate how the framework scales to larger models and datasets, as the computational cost of calculating the propensity to forget may become a limiting factor. This could involve exploring approximations or efficient algorithms for computing the measure. Additionally, the authors should provide a more detailed analysis of the computational complexity of their framework, including both theoretical bounds and empirical measurements. This would help practitioners understand the practical limitations of the approach and make informed decisions about its applicability.

Finally, the authors should address the potential impact of approximations in the learner's predictive distribution on the validity of their framework. This could involve conducting experiments with different types of approximations and analyzing how they affect the propensity to forget. The authors should also discuss the limitations of their framework in the context of these approximations and provide guidance on when the measure is likely to be reliable. Furthermore, they should explore the relationship between their framework and existing methods for mitigating forgetting, such as regularization techniques or replay buffers. This would involve analyzing how these techniques affect the propensity to forget and whether the framework can provide insights into their effectiveness. This would help bridge the gap between the theoretical framework and practical applications.

### Questions

1. How does the "propensity to forget" measure scale with the size of the model and dataset? Are there any approximations or efficient algorithms that can be used to compute the measure for large-scale applications?
2. How robust is the "propensity to forget" measure to different types of approximations in the learner's predictive distribution? Are there any specific conditions under which the measure is likely to be unreliable?
3. Can the "propensity to forget" measure be used to guide the development of new methods for mitigating forgetting? For example, can it be incorporated into the loss function or used as a criterion for model selection?
4. How does the proposed framework relate to existing methods for mitigating forgetting, such as regularization techniques or replay buffers? Can the "propensity to forget" measure provide insights into the effectiveness of these methods?
5. Are there any potential biases or limitations in the experimental setup that could affect the generalizability of the results? How do the findings on synthetic datasets translate to more complex, real-world scenarios?

### Rating

6

### Confidence

3

**********