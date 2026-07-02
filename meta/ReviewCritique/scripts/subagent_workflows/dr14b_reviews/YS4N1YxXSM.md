### Summary

This paper proposes QUOKA, a query-oriented KV selection method for efficient attention in transformer models. QUOKA addresses the computational bottleneck in large language model (LLM) inference, particularly during the prefill stage, by selectively attending to a subset of key-value (KV) pairs based on their relevance to the queries. The method operates in three main steps: query subselection, cosine-similarity scoring, and group-aware aggregation. By focusing on the most informative queries and their corresponding KV pairs, QUOKA achieves significant speedups while maintaining accuracy comparable to dense attention. The paper demonstrates QUOKA's effectiveness across various benchmarks, including Needle-In-A-Haystack, LongBench, RULER, and Math500, showing substantial latency reductions on both CPUs and GPUs.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. **Efficiency and Performance**: QUOKA achieves substantial speedups in attention computation, with up to 7x speedup on CPUs and 5-6x speedup on GPUs, while maintaining near-baseline accuracy. This is particularly valuable for resource-constrained environments.
2. **Hardware Agnostic**: The method is hardware-agnostic and does not rely on custom kernels, making it easily deployable across different hardware platforms.
3. **Training-Free**: QUOKA is a training-free method, which simplifies its integration into existing models without the need for retraining.
4. **Robustness to Hyperparameters**: The method shows gradual accuracy degradation with increasing sparsity and remains stable across different hyperparameter settings, making it adaptable to various constraints.
5. **Comprehensive Evaluation**: The paper provides extensive evaluations on multiple benchmarks, demonstrating the method's effectiveness across different tasks and model architectures.

### Weaknesses

#### Some Related Works


#### comment

1. **Limited Theoretical Justification**: While the paper provides empirical evidence for the effectiveness of QUOKA, the theoretical underpinnings are somewhat limited. A more rigorous analysis of why low cosine similarity queries attend to more keys would strengthen the paper. Specifically, the paper lacks a clear explanation of the mechanism by which the cosine similarity between queries and keys translates to the number of keys attended to. It is not clear if this is a consistent phenomenon across different layers and model architectures, or if it is specific to the models and layers tested.
2. **Focus on Prefill Latency**: The paper primarily focuses on prefill latency, with less emphasis on the generation phase. While some results on Math500 are provided, a more detailed analysis of QUOKA's performance during generation would be beneficial. The paper should explore how the query subselection and KV selection strategies impact the quality of generated text, especially for tasks that require long-range dependencies and complex reasoning.
3. **Impact on Attention Patterns**: The paper does not thoroughly explore how QUOKA affects attention patterns. It would be useful to understand if the method introduces any biases or alters the model's ability to capture long-range dependencies. For example, does the method tend to focus on local context at the expense of global context, and how does this affect performance on tasks that require reasoning over long sequences?
4. **Comparison with Other Sparse Attention Methods**: While the paper compares QUOKA with several baselines, a more detailed comparison with other dynamic sparse attention methods, especially those designed for multi-query settings, would provide a more comprehensive understanding of its advantages and limitations. The paper should include a more thorough analysis of the computational overhead of QUOKA compared to other methods, including the cost of query subselection and cosine similarity calculations.

### Suggestions

To strengthen the theoretical foundation of QUOKA, the authors should provide a more detailed analysis of the relationship between query similarity and attention patterns. This could involve exploring the mathematical properties of the attention mechanism and how they relate to the cosine similarity between queries and keys. For example, the authors could investigate whether the observed phenomenon is related to the distribution of attention weights or the geometry of the query and key embeddings. Furthermore, the authors should provide a more rigorous justification for the choice of cosine similarity as a proxy for query-key relevance. It would be beneficial to explore alternative similarity measures and analyze their impact on the performance of QUOKA. A more thorough theoretical analysis would help to establish the generalizability of the method and provide a deeper understanding of its underlying mechanisms.

To address the limited focus on the generation phase, the authors should conduct a more comprehensive evaluation of QUOKA's performance during text generation. This should include experiments on a wider range of generation tasks, such as summarization, translation, and dialogue generation. The authors should also analyze the impact of QUOKA on the quality of generated text, using metrics such as BLEU, ROUGE, and human evaluation. Furthermore, the authors should investigate how the query subselection and KV selection strategies affect the model's ability to capture long-range dependencies and perform complex reasoning. It would be useful to explore adaptive strategies for query and KV selection that can dynamically adjust to the specific requirements of the generation task. This could involve using a different number of selected queries and KV pairs depending on the length of the input sequence or the complexity of the task.

To better understand the impact of QUOKA on attention patterns, the authors should conduct a more detailed analysis of the attention weights and their distribution. This could involve visualizing the attention maps and analyzing the patterns of attention across different layers and heads. The authors should also investigate whether QUOKA introduces any biases or alters the model's ability to capture long-range dependencies. For example, they could analyze the attention patterns on tasks that require reasoning over long sequences and compare them to the patterns observed with dense attention. Furthermore, the authors should explore the possibility of using different aggregation strategies for the attention weights, such as averaging or max-pooling, and analyze their impact on the performance of QUOKA. A more thorough analysis of attention patterns would provide valuable insights into the behavior of the method and help to identify potential limitations.

### Questions

1. **Theoretical Justification**: Can the authors provide more theoretical insights into why low cosine similarity queries attend to more keys? Is this phenomenon consistent across different layers and model architectures?
2. **Generation Phase**: How does QUOKA perform on tasks that require extensive generation, such as code generation or long-form text summarization? Are there any specific adaptations needed for the generation phase?
3. **Impact on Attention Patterns**: How does QUOKA affect the model's ability to capture long-range dependencies? Are there any observable changes in attention patterns that could impact performance on tasks requiring global context?
4. **Scalability**: How does QUOKA scale with increasing model size and context length? Are there any limitations or bottlenecks that could arise with larger models?
5. **Comparison with Other Methods**: How does QUOKA compare to other dynamic sparse attention methods in terms of computational overhead and memory usage? Are there any specific scenarios where QUOKA outperforms or underperforms compared to these methods?

### Rating

6

### Confidence

3

**********