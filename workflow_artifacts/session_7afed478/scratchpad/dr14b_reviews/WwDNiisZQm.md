### Summary

This paper introduces Content-Aware Mamba (CAM), a novel state-space model (SSM) designed to enhance learned image compression (LIC) by adapting processing to image content. CAM addresses limitations of standard Mamba models, which use rigid, content-agnostic scans, by introducing two key mechanisms: a content-adaptive token permutation strategy and global-prior prompting. These innovations allow CAM to better capture global redundancy while maintaining computational efficiency. The resulting Content-Aware Mamba-based LIC model (CMiC) demonstrates state-of-the-art rate-distortion (RD) performance, outperforming existing models, including VTM-21.0, by significant margins on benchmark datasets.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper is well-written and easy to follow.

2. The proposed method achieves state-of-the-art performance across the tested datasets.

3. The authors provide comprehensive ablation studies and analysis to validate the effectiveness of each component in the proposed method.

### Weaknesses

#### Some Related Works


#### comment

1. The paper lacks a comprehensive comparison with other efficient methods, such as those using quantization, pruning, or knowledge distillation. Including these comparisons would provide a clearer context for the proposed method’s efficiency and performance trade-offs. Specifically, the absence of comparisons against models optimized with techniques like post-training quantization (e.g., 8-bit weight quantization) makes it difficult to assess the true efficiency gains of the proposed method relative to readily deployable alternatives. Furthermore, comparisons against pruned models, which can achieve significant speedups and memory reductions, are needed to fully contextualize the efficiency of the proposed approach.

2. The authors provide the decoding latency, but there is no information about the encoding time. Additionally, it would be valuable to compare the proposed method’s encoding and decoding speeds with those of popular models, such as VTM-21.0. The lack of encoding time data is a significant omission, as encoding is often a more computationally intensive process in learned image compression. Without this data, it's impossible to fully evaluate the practical applicability of the method, especially in scenarios where real-time encoding is required. A comparison against VTM-21.0, a widely used standard, would provide a crucial benchmark for understanding the practical trade-offs of the proposed method.

3. The paper does not include a discussion on the potential limitations or trade-offs of the proposed method, such as increased complexity or computational requirements. While the paper highlights the performance gains, it does not fully address the potential increase in computational cost associated with the content-aware mechanisms. A detailed analysis of the computational overhead, including memory usage and energy consumption, is necessary to understand the practical limitations of the proposed method, especially for deployment on resource-constrained devices.

### Suggestions

To address the lack of comprehensive comparisons, the authors should include a detailed analysis against models optimized with quantization, pruning, and knowledge distillation. Specifically, they should compare their method against models that have undergone post-training quantization to 8-bits or even 4-bits, as these are widely used in practical deployments. This would provide a clearer picture of the performance-efficiency trade-offs. Furthermore, comparisons against pruned models, which can achieve significant speedups and memory reductions, are essential to fully contextualize the efficiency of the proposed approach. The authors should also consider including models optimized with knowledge distillation, as this technique can produce highly efficient student models that maintain good performance. These comparisons should be performed on the same datasets and using the same evaluation metrics to ensure a fair comparison. The results should include not only rate-distortion performance but also encoding and decoding speeds, memory usage, and energy consumption.

To provide a complete picture of the method's practicality, the authors must include a detailed analysis of both encoding and decoding times. The encoding process is often the bottleneck in image compression, and without this data, it's impossible to fully evaluate the method's applicability, especially in real-time scenarios. The authors should compare their encoding and decoding speeds with those of VTM-21.0, a widely used standard, to provide a clear benchmark. This comparison should be performed on the same hardware and using the same evaluation metrics. Furthermore, the authors should provide a breakdown of the computational cost of each component of their method, including the content-adaptive token permutation and global-prior prompting. This would help to identify the bottlenees and potential areas for optimization. The authors should also report the memory footprint of their model, as this is a critical factor for deployment on resource-constrained devices.

Finally, the authors should include a thorough discussion of the potential limitations and trade-offs of their proposed method. This discussion should include an analysis of the increased complexity and computational requirements associated with the content-aware mechanisms. The authors should also discuss the potential impact of their method on energy consumption, as this is an important consideration for mobile and embedded applications. A detailed analysis of the computational overhead, including memory usage and energy consumption, is necessary to understand the practical limitations of the proposed method, especially for deployment on resource-constrained devices. The authors should also discuss the potential for further optimization of their method, such as through the use of more efficient hardware or algorithms.

### Questions

Please refer to the weaknesses.

### Rating

6

### Confidence

4

**********