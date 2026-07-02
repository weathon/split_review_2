### Summary

The paper presents a new algorithm for the AllReduce collective communication operation, which is widely used in distributed deep learning. The key insight of the paper is that the straggler-induced delay can be leveraged to perform useful computation, rather than simply waiting for the slowest GPU to reach the synchronization barrier. The proposed algorithm, called StragglerAR, transmits up to 2x fewer bytes than the known bandwidth-optimal lower bound by exploiting natural variation in GPU execution times. The authors provide a theoretical analysis of the algorithm's performance and show that it achieves a 2x speedup over popular bandwidth-efficient algorithms for large GPU clusters. They also demonstrate the effectiveness of StragglerAR on an 8-GPU server, where it provides a 25% speedup over state-of-the-art AllReduce algorithms.

### Soundness

3

### Presentation

3

### Contribution

2

### Strengths

1. The paper introduces a novel approach to AllReduce that leverages straggler-induced delay to perform useful computation, rather than simply waiting for the slowest GPU to reach the synchronization barrier. This is a creative and innovative solution that has the potential to significantly improve the performance of distributed deep learning.
2. The paper provides a thorough theoretical analysis of the proposed algorithm, StragglerAR, and shows that it achieves a 2x speedup over popular bandwidth-efficient algorithms for large GPU clusters. The analysis is rigorous and well-supported by experimental results.
3. The paper is well-written and easy to follow. The authors clearly explain the problem, their proposed solution, and the theoretical analysis. The use of figures and tables helps to illustrate the key concepts and results.

### Weaknesses

#### Some Related Works


#### comment

1. The paper focuses on a specific scenario where stragglers are caused by natural variation in GPU execution times. However, in real-world distributed deep learning systems, stragglers can be caused by a variety of factors, such as hardware failures, network congestion, and resource contention. The paper does not discuss how StragglerAR would perform in these scenarios, which limits its applicability. Specifically, the paper lacks analysis on how the algorithm would handle stragglers that are not consistent in their delay patterns, such as those caused by intermittent network issues or sudden hardware failures. The assumption of predictable, execution-time-based stragglers is a significant limitation.
2. The paper does not provide a detailed comparison of StragglerAR with other state-of-the-art AllReduce algorithms, such as Ring AllReduce and Recursive Doubling/Halving. A more thorough comparison would help to better understand the strengths and weaknesses of StragglerAR and its potential impact on the field. The paper should include a comparison of the algorithms' performance under various conditions, such as different network topologies, varying numbers of GPUs, and different data sizes. Furthermore, the comparison should not only focus on the theoretical analysis but also include empirical results on real-world systems.
3. The paper's experimental evaluation is limited to an 8-GPU server. While this is a reasonable starting point, it is not representative of the large-scale distributed systems that are commonly used in deep learning. The paper should include experiments on larger clusters to demonstrate the scalability of StragglerAR. The evaluation should also include a more diverse set of workloads, including different deep learning models and datasets, to assess the algorithm's robustness.

### Suggestions

To address the limitations of the current work, the authors should first investigate the performance of StragglerAR under more realistic straggler conditions. This would involve simulating stragglers caused by factors other than just natural variations in GPU execution times, such as network latency spikes or simulated hardware failures. The evaluation should include a sensitivity analysis of the algorithm's performance with respect to the frequency and severity of these different types of stragglers. Furthermore, the authors should explore adaptive mechanisms that can dynamically adjust the algorithm's behavior based on the observed straggler patterns. For example, if a straggler is detected to be caused by a network issue, the algorithm could temporarily switch to a more robust but less efficient AllReduce algorithm for the affected GPUs. This would make the algorithm more practical for real-world deployments.

Secondly, the paper needs a more comprehensive comparison with existing AllReduce algorithms. This comparison should not only focus on theoretical analysis but also include empirical results on various hardware and software configurations. The authors should compare StragglerAR with Ring AllReduce, Recursive Doubling/Halving, and other state-of-the-art algorithms under different conditions, such as varying numbers of GPUs, different network topologies, and different data sizes. The comparison should also include a detailed analysis of the trade-offs between the different algorithms, such as their communication overhead, synchronization overhead, and fault tolerance. The authors should also consider the impact of different communication primitives, such as point-to-point messages and collective operations, on the performance of the algorithms. This would provide a more complete understanding of the strengths and weaknesses of StragglerAR and its potential impact on the field.

Finally, the experimental evaluation should be significantly expanded to include larger-scale distributed systems. The authors should conduct experiments on clusters with dozens or even hundreds of GPUs to demonstrate the scalability of StragglerAR. The evaluation should also include a more diverse set of workloads, including different deep learning models and datasets, to assess the algorithm's robustness. The authors should also consider the impact of different system configurations, such as different GPU models and network interfaces, on the performance of the algorithm. This would provide a more realistic assessment of the algorithm's performance in real-world deployments. Furthermore, the authors should provide a detailed analysis of the algorithm's performance under different levels of system load, such as varying numbers of concurrent training jobs.

### Questions

1. How does StragglerAR perform in the presence of stragglers caused by factors other than natural variation in GPU execution times, such as hardware failures or network congestion?
2. Can you provide a more detailed comparison of StragglerAR with other state-of-the-art AllReduce algorithms, such as Ring AllReduce and Recursive Doubling/Halving?
3. How does the performance of StragglerAR scale with the number of GPUs in the cluster? Have you conducted experiments on larger clusters to demonstrate its scalability?
4. How does the performance of StragglerAR vary with different deep learning models and datasets? Have you evaluated its performance on a diverse set of workloads?
5. How does StragglerAR handle the case where multiple GPUs are stragglers simultaneously? Does it still achieve a speedup in this scenario?

### Rating

5

### Confidence

4

**********