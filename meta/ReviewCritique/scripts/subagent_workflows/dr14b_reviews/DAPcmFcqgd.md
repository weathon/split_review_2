### Summary

This paper proposes a new architecture called MoEP (Modular Expert Paths), designed to enhance the sparsity of large language models without increasing the total number of parameters. The authors claim that MoEP integrates model parallelism with Mixture-of-Experts (MoE) techniques, achieving selective token activation and accelerating model learning. The paper evaluates MoEP on the BabyLM benchmark, reporting performance improvements over GPT-2 baselines.

### Soundness

2

### Presentation

2

### Contribution

2

### Strengths

1. The concept of combining model parallelism with MoE to achieve sparsity is intriguing and could potentially lead to more efficient models.

2. The paper provides a clear description of the MoEP architecture, detailing how modular expert paths are constructed and function within the model.

3. The authors present results showing that MoEP outperforms GPT-2 baselines on the BabyLM benchmark, suggesting that the proposed architecture can improve performance.

### Weaknesses

#### Some Related Works


#### comment

1. The experimental validation is limited to the BabyLM benchmark, which may not be sufficient to generalize the findings to other datasets or real-world applications. The BabyLM benchmark, while useful for initial testing, primarily focuses on linguistic tasks and may not fully capture the complexities of more diverse datasets or tasks requiring different types of reasoning or knowledge. This narrow evaluation scope makes it difficult to assess the robustness of MoEP across varied scenarios.

2. The paper lacks a detailed analysis of the computational efficiency and resource requirements of MoEP compared to traditional dense models. While the authors claim parameter efficiency, they do not provide concrete measurements of training and inference times, memory usage, or energy consumption. Without these metrics, it is hard to determine the practical benefits of MoEP over existing architectures, especially considering the potential overhead introduced by the modular expert paths and routing mechanisms.

3. There is insufficient discussion on the scalability of MoEP to larger models and datasets. The paper does not address how the proposed architecture would perform with significantly more parameters or on datasets orders of magnitude larger than BabyLM. The challenges of routing and managing a large number of expert paths in a scalable manner are not discussed, leaving uncertainty about the practical applicability of MoEP in large-scale settings.

4. The paper does not thoroughly explore the limitations of MoEP, such as potential issues with vanishing gradients or difficulties in optimizing the model. The modular nature of MoEP might introduce new challenges in training, such as instability or difficulty in coordinating the updates across different expert paths. The paper lacks a discussion on how these potential issues are addressed or mitigated, which is crucial for understanding the practical viability of the approach.

### Suggestions

To strengthen the paper, the authors should significantly broaden the experimental evaluation beyond the BabyLM benchmark. This should include testing on a variety of datasets that represent different tasks, such as question answering, text summarization, and code generation. Datasets like C4, which are commonly used for pretraining, or more challenging benchmarks like SuperGLUE, would provide a more comprehensive assessment of MoEP's capabilities. Furthermore, the authors should evaluate the model's performance on tasks that require different types of reasoning or knowledge, such as mathematical reasoning or commonsense reasoning. This would help to demonstrate the generalizability of the approach and identify potential limitations. The evaluation should also include a comparison with other sparse models, not just dense baselines, to properly contextualize the performance gains.

In addition to expanding the evaluation, the authors need to provide a detailed analysis of the computational efficiency of MoEP. This should include measurements of training and inference times, memory usage, and energy consumption. The analysis should compare MoEP with both dense and other sparse models, providing a clear picture of the trade-offs involved. The authors should also investigate the impact of different hyperparameters on the computational efficiency of MoEP, such as the number of expert paths and the sparsity level. This analysis should be conducted on different hardware platforms to understand the practical implications of the approach. Furthermore, the authors should provide a breakdown of the computational cost associated with different parts of the MoEP architecture, such as the routing mechanism and the expert computations, to identify potential bottlenecks and areas for optimization.

Finally, the authors should address the scalability of MoEP to larger models and datasets. This should include a discussion of the challenges of routing and managing a large number of expert paths, as well as potential solutions for mitigating these challenges. The authors should also investigate the impact of model size on the performance of MoEP, and determine the optimal model size for different tasks and datasets. The paper should also include a discussion of the potential limitations of MoEP, such as issues with vanishing gradients or difficulties in optimizing the model. The authors should provide a detailed analysis of the training dynamics of MoEP, and identify potential instabilities or difficulties in training. This analysis should include a comparison with other sparse models, to understand the specific challenges associated with MoEP.

### Questions

1. How does MoEP perform on other benchmarks or real-world datasets beyond BabyLM?

2. What are the computational costs associated with MoEP compared to traditional dense models?

3. How does the performance of MoEP scale with larger models and datasets?

4. What are the potential limitations or drawbacks of MoEP, and how are they addressed?

### Rating

3

### Confidence

4

**********