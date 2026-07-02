### Summary

This paper introduces LRF-Dyn, a novel approach for spiking transformers that integrates localized receptive fields and membrane-potential dynamics to enhance performance and reduce memory usage. The method addresses two main challenges in existing Spiking Transformers: limited local modeling capability and high memory requirements during inference. LRF-Dyn introduces a Local Receptive Field (LRF) mechanism to strengthen local feature modeling and approximates self-attention aggregation through charge-fire-reset dynamics, eliminating the need to store large attention matrices. Extensive experiments demonstrate significant performance improvements and reduced memory overhead, making it suitable for resource-constrained environments.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces LRF-Dyn, a novel approach that combines localized receptive fields with neuronal membrane-potential dynamics, offering a fresh perspective on improving spiking transformers.
2. The method effectively addresses two significant challenges in spiking transformers: limited local modeling capability and high memory overhead, enhancing both performance and efficiency.
3. The paper provides extensive experimental validation across various visual tasks and architectures, demonstrating consistent performance improvements and reduced memory usage.
4. The proposed method is particularly valuable for deployment in resource-constrained environments, such as edge devices, due to its reduced memory footprint and improved efficiency.

### Weaknesses

#### Some Related Works


#### comment

1. The paper lacks a detailed analysis of the computational overhead introduced by the LRF-Dyn method. While memory efficiency is addressed, a thorough examination of the computational complexity and potential trade-offs in terms of processing time would provide a more comprehensive understanding of the method's practical implications. Specifically, the paper should analyze the number of operations (e.g., multiplications, additions, etc.) required by the LRF-Dyn method compared to standard self-attention and other spiking transformer variants. This analysis should consider the impact of different model sizes and input sequence lengths on the computational cost. Furthermore, the paper should discuss the potential impact of the proposed method on latency, which is a critical factor for real-time applications on edge devices.

2. The theoretical justification for certain design choices, such as the specific formulation of the LRF mechanism and the approximation of attention aggregation through neuronal dynamics, could be more thoroughly explained. Providing additional theoretical insights or empirical evidence to support these choices would strengthen the paper's contributions. For example, the paper should provide a more detailed explanation of how the LRF mechanism is designed to capture local dependencies and why the chosen formulation is optimal. Additionally, the paper should provide a more rigorous justification for approximating attention aggregation through charge-fire-reset dynamics, including a discussion of the potential limitations and trade-offs of this approximation.

### Suggestions

To address the lack of detailed computational overhead analysis, the authors should include a comprehensive breakdown of the computational complexity of the LRF-Dyn method. This should include a comparison of the number of operations required by LRF-Dyn, standard self-attention, and other spiking transformer variants. The analysis should consider the impact of different model sizes and input sequence lengths on the computational cost. Furthermore, the authors should provide an analysis of the potential impact of the proposed method on latency, which is a critical factor for real-time applications on edge devices. This could involve measuring the actual processing time of the method on different hardware platforms and comparing it to other methods. The authors should also discuss the potential for optimizing the implementation of the LRF-Dyn method to further reduce computational overhead.

To strengthen the theoretical justification for the design choices, the authors should provide a more detailed explanation of how the LRF mechanism is designed to capture local dependencies and why the chosen formulation is optimal. This could involve providing a mathematical analysis of the LRF mechanism and demonstrating its ability to capture local features. Additionally, the authors should provide a more rigorous justification for approximating attention aggregation through charge-fire-reset dynamics, including a discussion of the potential limitations and trade-offs of this approximation. This could involve comparing the performance of the proposed method with other approximation techniques and discussing the conditions under which the proposed approximation is most effective. The authors should also provide empirical evidence to support their design choices, such as ablation studies that demonstrate the impact of different components of the LRF-Dyn method on performance.

Finally, the authors should consider including a more detailed discussion of the limitations of the proposed method. This could involve discussing the potential challenges of applying the method to different types of data or tasks, as well as the potential for further improvements. For example, the authors could discuss the limitations of the LRF mechanism in capturing long-range dependencies and explore potential solutions to address this limitation. The authors should also discuss the potential impact of the approximation of attention aggregation on the overall performance of the method and explore alternative approximation techniques that could potentially improve performance. By addressing these limitations, the authors can provide a more complete and balanced assessment of the proposed method.

### Questions

1. Could the authors provide a more detailed analysis of the computational complexity and processing time of the LRF-Dyn method compared to existing approaches?
2. How does the LRF-Dyn method scale with larger models or more complex tasks? Are there any limitations in terms of scalability?
3. Can the proposed method be extended or adapted to other types of spiking neural networks or different types of data beyond visual tasks?

### Rating

6

### Confidence

3

**********