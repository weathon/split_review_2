### Summary

This paper presents a novel approach to 1-bit post-training quantization (PTQ) for large language models (LLMs), addressing the challenge of performance degradation associated with extreme quantization. The authors propose a selective layer-wise output alignment strategy that modifies the quantization objective to explicitly account for accumulated errors. Additionally, they introduce an attention-aware masking mechanism (AMP) to preserve attention behavior. The method demonstrates significant improvements over existing 1-bit PTQ techniques across various LLMs and NLP tasks.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper provides a thorough analysis of the limitations of existing 1-bit PTQ methods, particularly the issue of error accumulation and attention mechanism degradation.
2. The proposed method achieves significant performance improvements over existing 1-bit PTQ techniques, demonstrating its effectiveness through extensive experiments on various LLMs and datasets.
3. The introduction of the Attention Matrix Preservation (AMP) mechanism is a novel contribution that addresses a critical aspect of LLM performance.

### Weaknesses

#### Some Related Works


#### comment

1. The paper could benefit from a more detailed discussion of the computational overhead of the proposed method compared to existing approaches.
2. The authors should also provide a more comprehensive analysis of the impact of different calibration datasets on the performance of the proposed PTQ method.

### Suggestions

The paper would be strengthened by a more thorough analysis of the computational overhead. While the authors mention minimal overhead, a detailed breakdown of the time complexity and memory requirements would be beneficial. Specifically, the paper should quantify the cost of the data-aware optimization process, including the time taken for forward and backward passes during the PTQ process. It would be useful to compare the proposed method's computational cost against other 1-bit PTQ techniques, not just in terms of raw execution time, but also in terms of memory footprint and energy consumption. This analysis should consider the impact of different hardware platforms, such as GPUs and CPUs, to provide a more comprehensive understanding of the method's practical applicability. Furthermore, the authors should discuss the scalability of their approach with respect to model size and the number of parameters, as this is a critical factor for deploying large language models on resource-constrained devices. A detailed analysis of the computational overhead would allow readers to better assess the trade-offs between performance gains and computational costs.

Further, the paper should include a more in-depth analysis of the impact of different calibration datasets on the performance of the proposed PTQ method. The choice of calibration data can significantly affect the accuracy of quantized models, and it is important to understand how sensitive the proposed method is to this choice. The authors should explore a variety of calibration datasets, including those with varying sizes, domain specificities, and data distributions. For instance, the performance of the PTQ method should be evaluated using calibration datasets that are closely aligned with the target downstream tasks, as well as datasets that are significantly different. This analysis should not only focus on the final performance metrics but also on the convergence behavior of the PTQ process. It would be valuable to investigate whether certain types of calibration datasets lead to faster convergence or more stable results. Additionally, the authors should discuss the potential for using synthetic or semi-synthetic data for calibration, which could be a practical solution when real data is limited or sensitive. A comprehensive analysis of the impact of calibration data would provide valuable insights into the robustness and generalizability of the proposed PTQ method.

Finally, the authors should also consider a more detailed analysis of the attention matrix preservation mechanism. While the paper introduces the AMP mechanism, it would be beneficial to provide more insights into how this mechanism affects the attention weights and biases. Specifically, the authors could analyze the distribution of attention weights before and after quantization, and quantify the degree to which the AMP mechanism prevents changes in these distributions. It would also be useful to investigate the impact of the AMP mechanism on different attention heads, as some heads may be more sensitive to quantization than others. Furthermore, the authors should discuss the potential limitations of the AMP mechanism, such as its inability to fully preserve the original attention behavior in certain scenarios. A more detailed analysis of the AMP mechanism would provide a deeper understanding of its effectiveness and limitations, and it would also help to identify potential areas for future improvement.

### Questions

1. How does the computational overhead of the proposed method compare to existing 1-bit PTQ techniques, especially in terms of inference time and memory usage?
2. Can the proposed method be combined with other quantization techniques, such as quantization-aware training (QAT), to achieve even better performance?
3. How sensitive is the proposed method to hyperparameter settings, and what are the guidelines for selecting optimal hyperparameters for different LLMs and datasets?

### Rating

6

### Confidence

4

**********