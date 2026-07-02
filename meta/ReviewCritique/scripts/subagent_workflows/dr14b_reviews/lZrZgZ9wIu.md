### Summary

This paper investigates the advantages of dynamically sparsely trained ANNs for conversion into sparse SNNs. The authors employ Cannistraci-Hebb Training (CHT), a state-of-the-art brain-inspired dynamic sparse training method, to learn both weights and topology of the networks. They explore the impact of connectivity sparsity on the accuracy and theoretical energy efficiency of SNNs across different conversion approaches. The key findings include: (1) sparse SNNs can achieve accuracy comparable to or even surpassing that of dense SNNs, (2) sparse SNNs can reduce theoretical energy consumption by up to 99% compared with dense SNNs, and (3) there is a significant time lag between firing rate saturation and accuracy saturation, with the time lag being different between sparse and dense networks.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

The paper presents a novel approach by investigating the use of dynamically sparsely trained ANNs for conversion into sparse SNNs. This is a unique contribution to the field, as previous works have focused exclusively on dense networks for ANN2SNN conversion. The use of Cannistraci-Hebb Training (CHT), a brain-inspired method, adds an interesting dimension to the research.

The paper provides a comprehensive analysis of the impact of connectivity sparsity on both the accuracy and theoretical energy efficiency of SNNs. The authors explore different conversion approaches and various ANN structures, providing a thorough evaluation of their proposed method. The investigation into the temporal relationship between firing rate saturation and accuracy saturation is also a valuable contribution.

The results demonstrate significant potential benefits of using sparse SNNs, including comparable or superior accuracy to dense SNNs and substantial reductions in theoretical energy consumption (up to 99%). These findings have important implications for the development of more efficient SNNs.

### Weaknesses

#### Some Related Works


#### comment

While the paper provides a theoretical energy calculation, it would be beneficial to have some experimental validation of the energy savings on actual hardware. The theoretical calculation is based on specific assumptions about the hardware, and it is important to verify that these assumptions hold true in practice. For example, the calculation assumes perfect sparsity utilization, which may not be achievable in real-world implementations due to overheads in routing and memory access. Furthermore, the energy model does not account for the control circuitry required for SNN operation, which could contribute significantly to the overall energy consumption.

The paper focuses on specific datasets and network architectures. It would be helpful to see how the proposed approach generalizes to other datasets and more complex network architectures. While the authors have explored a range of architectures, it is unclear if the observed benefits would extend to architectures with recurrent connections or attention mechanisms, which are common in state-of-the-art models. The performance of the proposed method on larger, more complex datasets, such as those used in natural language processing, remains an open question.

The paper could benefit from a more detailed comparison with existing state-of-the-art methods for ANN2SNN conversion. While the authors mention that their approach is unique, it would be helpful to see a quantitative comparison with other methods in terms of accuracy, sparsity, and energy efficiency. Specifically, a comparison with methods that also aim to achieve sparse SNNs would be valuable. The lack of such comparison makes it difficult to assess the relative advantages of the proposed method.

### Suggestions

To strengthen the paper, the authors should consider conducting experiments on neuromorphic hardware to validate their theoretical energy savings. This would involve implementing the sparse SNNs on a platform such as Loihi or TrueNorth and measuring the actual energy consumption during inference. Such experiments would provide a more realistic assessment of the energy efficiency of the proposed approach and would help to identify any potential bottlenecks or overheads that are not captured by the theoretical model. Furthermore, the authors should explore the impact of different sparsity patterns on the performance and energy efficiency of the SNNs. For example, they could investigate the effect of structured sparsity, where groups of connections are removed together, versus unstructured sparsity, where individual connections are removed randomly. This would provide a more comprehensive understanding of the trade-offs between sparsity, accuracy, and energy efficiency.

To address the generalization concerns, the authors should evaluate their approach on a wider range of datasets and network architectures. This could include datasets from different domains, such as natural language processing or time series analysis, as well as more complex architectures with recurrent connections or attention mechanisms. For example, they could explore the performance of their method on tasks such as machine translation or speech recognition. This would provide a more robust assessment of the generalizability of the proposed approach and would help to identify any limitations or challenges that may arise when applying it to different types of problems. Additionally, the authors should investigate the impact of different training strategies on the performance of the converted SNNs. For example, they could explore the use of different learning rates or optimization algorithms during the ANN training phase.

Finally, the authors should provide a more detailed comparison with existing state-of-the-art methods for ANN2SNN conversion. This should include a quantitative comparison with methods that also aim to achieve sparse SNNs, as well as a qualitative comparison with methods that use different approaches to SNN conversion. The comparison should focus on key metrics such as accuracy, sparsity, energy efficiency, and latency. This would help to establish the relative advantages and disadvantages of the proposed method and would provide a more comprehensive understanding of the current state of the art in ANN2SNN conversion. Furthermore, the authors should discuss the limitations of their approach and suggest potential directions for future research. This would help to guide future work in this area and would contribute to the advancement of the field.

### Questions

Have you considered evaluating your approach on other datasets or more complex network architectures? How do you expect your method to generalize to different types of problems?

Can you provide more details on the experimental setup and the hardware used for the experiments? It would be helpful to have more information on the specific parameters and configurations used in the study.

How does your approach compare to existing state-of-the-art methods for ANN2SNN conversion in terms of accuracy, sparsity, and energy efficiency? It would be valuable to see a quantitative comparison with other methods in the literature.

### Rating

6

### Confidence

3

**********