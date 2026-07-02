### Summary

This paper introduces FedMPDD (Federated Learning via Multi-Projected Directional Derivatives), a novel algorithm that simultaneously optimizes bandwidth utilization and enhances privacy in Federated Learning. The core idea of FedMPDD is to encode each client’s high-dimensional gradient by computing its directional derivatives along multiple random vectors. This compresses the gradient into a much smaller message, significantly reducing uplink communication costs from  O(d)  to  O(m) , where  m ≪ d. The server then decodes the aggregated information by projecting it back onto the same random vectors. Our key insight is that averaging multiple projections overcomes the dimension-dependent convergence limitations of a single projection. We provide a rigorous theoretical analysis, establishing that FedMPDD converges at a rate of  O(1/K) , matching the performance of FedSGD. Furthermore, we demonstrate that our method provides inherent privacy against gradient inversion attacks due to the geometric properties of low-rank projections, offering a tunable privacy-utility trade-off controlled by the number of projections. Extensive experiments on benchmark datasets validate our theory, showing that FedMPDD drastically reduces network congestion and provides strong privacy protection, all while maintaining high model performance, outperforming existing methods in resource-constrained scenarios.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel approach to address the communication bottleneck in Federated Learning (FL) by leveraging multi-projected directional derivatives. This approach is innovative and provides a fresh perspective on gradient compression and privacy preservation in FL.
2. The paper provides a rigorous theoretical analysis of the proposed method, including convergence guarantees and privacy analysis. The theoretical results are well-supported by empirical evaluations on benchmark datasets.
3. The paper is well-organized and clearly written. The authors effectively communicate the technical details and the significance of their contributions. The use of figures and tables enhances the readability and understanding of the results.

### Weaknesses

#### Some Related Works


#### comment

1. The paper's experimental evaluation primarily focuses on image classification tasks. It would be beneficial to evaluate the proposed method on a wider range of applications and datasets to demonstrate its generalizability. Specifically, the current evaluation lacks diversity in data modalities and task complexities. For instance, the method's performance on natural language processing tasks or time-series data remains unexplored. Furthermore, the image classification tasks are limited to relatively small datasets; evaluating on larger, more complex datasets would provide a more robust assessment of the method's scalability and effectiveness.
2. The paper could benefit from a more detailed discussion of the practical implications of the proposed method. For example, how does the method perform in real-world FL settings with heterogeneous devices and varying network conditions? The paper does not address the potential challenges of deploying the method in scenarios with diverse device capabilities, such as varying computational power and memory constraints. Additionally, the impact of fluctuating network bandwidth and latency on the method's performance and convergence is not discussed. A more thorough analysis of these practical considerations is needed to assess the method's real-world applicability.
3. The paper's comparison with existing methods is limited to a few specific techniques. A more comprehensive comparison with a broader range of state-of-the-art FL algorithms would provide a better understanding of the proposed method's strengths and weaknesses. The current comparison does not include methods that employ different compression techniques or privacy-preserving mechanisms. A more extensive evaluation against a wider array of algorithms would provide a more complete picture of the method's relative performance and advantages.

### Suggestions

To enhance the paper's evaluation, the authors should consider expanding their experiments to include a more diverse set of tasks and datasets. Specifically, incorporating natural language processing tasks, such as text classification or sequence modeling, would demonstrate the method's applicability beyond image data. Furthermore, evaluating the method on larger, more complex datasets, such as those used in real-world applications, would provide a more robust assessment of its scalability. It would also be beneficial to explore the method's performance on tasks with different levels of data heterogeneity, as this is a common challenge in federated learning. This would involve using datasets with varying degrees of non-IID data distributions across clients, which would provide a more realistic evaluation of the method's robustness. Additionally, the authors should consider evaluating the method's performance under different levels of data quality, such as noisy or incomplete data, to assess its robustness in real-world scenarios.

To address the practical implications of the proposed method, the authors should conduct experiments that simulate real-world federated learning settings. This would involve considering the impact of heterogeneous devices with varying computational power and memory constraints. The authors should also investigate the method's performance under different network conditions, such as varying bandwidth and latency. This could be done by simulating different network topologies and introducing network delays. Furthermore, the authors should analyze the method's sensitivity to different hyperparameter settings, such as the number of projections and the learning rate. This would provide a better understanding of the method's robustness and its ability to adapt to different environments. The authors should also discuss the computational overhead of the proposed method, including the time and memory requirements for both the clients and the server. This would help to assess the method's feasibility for deployment in resource-constrained environments.

Finally, the authors should conduct a more comprehensive comparison with a broader range of state-of-the-art federated learning algorithms. This should include methods that employ different compression techniques, such as quantization or sparsification, as well as methods that use different privacy-preserving mechanisms, such as differential privacy. The comparison should also include methods that are designed to handle heterogeneous data distributions and network conditions. This would provide a more complete picture of the proposed method's strengths and weaknesses relative to existing approaches. The authors should also provide a detailed analysis of the trade-offs between communication efficiency, privacy, and model performance for each method. This would help to identify the specific scenarios in which the proposed method is most effective and where it may be less suitable.

### Questions

1. How does the proposed method handle scenarios with highly heterogeneous data distributions across clients? Are there any specific strategies or modifications that can be applied to improve performance in such cases?
2. Can the authors provide more insights into the computational overhead of the proposed method, especially in terms of the time and memory requirements for both the clients and the server?
3. How does the method perform when the number of clients is very large, and what are the potential bottlenecks or challenges in such scenarios?

### Rating

6

### Confidence

3

**********