### Summary

This paper presents AdaSVD, an adaptive SVD-based compression method for large language models (LLMs). The authors propose two key techniques: adaComp, which adaptively compensates for SVD truncation errors, and adaCR, which assigns layer-specific compression ratios based on layer importance. The method is evaluated on various LLMs and VLMs, demonstrating improved performance over existing SVD-based compression methods, especially at high compression ratios.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel adaptive compensation method (adaComp) for SVD truncation, which effectively reduces compression error.
2. The adaptive compression ratio method (adaCR) is a valuable contribution, as it addresses the limitation of uniform compression ratios used in previous methods.
3. The experimental results are comprehensive, covering multiple LLM/VLM families and a wide range of compression ratios. The method consistently outperforms existing SVD-based approaches.
4. The paper is well-written and clearly explains the proposed techniques and experimental setup.

### Weaknesses

#### Some Related Works


#### comment

1. The paper lacks a detailed analysis of the computational overhead introduced by adaComp and adaCR. While the method improves compression performance, the additional computational cost may limit its practical applicability, especially for real-time inference. The analysis should include not just FLOPs but also memory usage and latency, particularly for the iterative updates in adaComp and the layer-wise importance calculations in adaCR. A breakdown of the time spent on each step of the compression process would be beneficial.
2. The evaluation primarily focuses on language modeling and image captioning tasks. It would be beneficial to see how AdaSVD performs on a broader range of tasks, such as code generation or mathematical reasoning, to better assess its generalizability. The current evaluation does not fully explore the method's performance on tasks that require different types of reasoning or generation capabilities. For example, tasks that involve complex logical reasoning or symbolic manipulation could reveal potential limitations of the proposed compression method.
3. The paper does not provide a detailed comparison of the memory footprint of the compressed models. While the compression ratio is reported, the actual memory savings in terms of model size and inference memory usage are not clearly quantified. This makes it difficult to assess the practical benefits of the method, especially when compared to other compression techniques. A detailed analysis of the memory usage during inference, including the size of the compressed weights and any additional memory required for the decompression process, is needed.
4. The paper does not discuss the potential impact of AdaSVD on model parallelism and distributed training. SVD-based compression can sometimes complicate these aspects, and it's important to address these practical considerations. The paper should discuss how the compressed layers can be integrated into a distributed training setup and whether the compression process introduces any challenges for model parallelism. The impact on communication overhead and synchronization should also be considered.
5. The paper does not explore the potential for combining AdaSVD with other compression techniques, such as quantization or pruning. This could lead to even higher compression ratios and better performance. The paper should investigate the potential benefits and challenges of combining AdaSVD with other compression methods. For example, it would be interesting to see if applying quantization after AdaSVD can further reduce the model size without significant performance degradation.

### Suggestions

The paper should include a more detailed analysis of the computational overhead introduced by adaComp and adaCR. This analysis should go beyond just FLOPs and include memory usage and latency. Specifically, the authors should provide a breakdown of the time spent on each step of the compression process, including the iterative updates in adaComp and the layer-wise importance calculations in adaCR. This would help to understand the practical implications of using these techniques, especially for real-time inference. Furthermore, the authors should investigate the impact of different hyperparameter settings on the computational cost and compression performance. This would provide valuable insights into the trade-offs between compression ratio and computational overhead.

To better assess the generalizability of AdaSVD, the authors should evaluate the method on a broader range of tasks, including code generation and mathematical reasoning. This would help to identify potential limitations of the method and to understand its performance on tasks that require different types of reasoning or generation capabilities. The evaluation should include a variety of datasets and metrics that are relevant to these tasks. For example, for code generation, the authors could use metrics such as BLEU score or code execution accuracy. For mathematical reasoning, the authors could use datasets that require symbolic manipulation or logical inference. This would provide a more comprehensive evaluation of the method's performance.

Finally, the paper should provide a more detailed comparison of the memory footprint of the compressed models. This should include not only the size of the compressed weights but also the memory usage during inference, including any additional memory required for the decompression process. The authors should also discuss the potential impact of AdaSVD on model parallelism and distributed training. This should include an analysis of how the compressed layers can be integrated into a distributed training setup and whether the compression process introduces any challenges for model parallelism. The authors should also explore the potential for combining AdaSVD with other compression techniques, such as quantization or pruning, to achieve even higher compression ratios and better performance. This would provide a more complete picture of the practical benefits and limitations of the proposed method.

### Questions

1. How does the computational overhead of adaComp and adaCR scale with model size and compression ratio?
2. What is the impact of AdaSVD on the inference latency of the compressed models?
3. How does AdaSVD affect the model's ability to generalize to unseen data, especially at high compression ratios?
4. Can the authors provide more details on the hyperparameter tuning process for adaComp and adaCR?
5. How does the performance of AdaSVD compare to other state-of-the-art compression methods, such as quantization or pruning, on a range of tasks and model sizes?

### Rating

6

### Confidence

4

**********