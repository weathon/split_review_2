### Summary

This paper introduces On-Demand Communication (ODC), a novel approach to distributed training that adapts the parameter server (PS) paradigm to the Fully Sharded Data Parallel (FSDP) framework. ODC addresses the inefficiencies of collective communication in LLM post-training by replacing per-layer synchronization with point-to-point communication, reducing synchronization barriers and improving workload balance. The approach achieves up to a 36% speedup over standard FSDP across diverse LLM post-training tasks.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper identifies a critical limitation of collective communication in FSDP for LLM post-training and proposes a novel solution that revisits the parameter server paradigm.
2. ODC consistently improves device utilization and training throughput across various LLM post-training tasks, demonstrating its effectiveness in handling imbalanced workloads.
3. The implementation of ODC is integrated with FSDP and open-sourced, facilitating adoption and further development by the community.

### Weaknesses

#### Some Related Works


#### comment

1. The paper acknowledges that ODC's inter-node communication is less efficient than collective communication. While proposed solutions like overlapping communication with computation and hybrid sharding are mentioned, a more detailed analysis of their effectiveness and potential limitations would be beneficial.
2. The evaluation focuses primarily on LLM post-training tasks. It would be valuable to assess ODC's performance in other scenarios, such as pre-training or training with different types of models.
3. The paper could provide more insights into the practical challenges of implementing ODC, such as the complexity of integrating it with existing frameworks and the potential for introducing new bugs or instability.

### Suggestions

The paper should delve deeper into the inter-node communication efficiency of ODC. While the authors mention overlapping communication with computation and hybrid sharding, a more rigorous analysis is needed. For instance, the paper could include a detailed breakdown of the communication overhead for different model sizes and node counts, comparing ODC with optimized collective communication implementations. This analysis should consider various network topologies and bandwidth limitations to provide a comprehensive understanding of ODC's performance in diverse hardware environments. Furthermore, the paper should explore the practical limitations of hybrid sharding, such as the memory overhead and the potential for increased complexity in gradient aggregation. A quantitative analysis of the trade-offs between communication efficiency and memory usage would be highly beneficial.

To strengthen the evaluation, the authors should extend their experiments beyond LLM post-training. Evaluating ODC on pre-training tasks, particularly those involving large-scale datasets and complex models, would provide a more comprehensive understanding of its general applicability. It would be valuable to assess ODC's performance with different model architectures, such as transformers with varying attention mechanisms or convolutional networks. This would help determine if the benefits of ODC are specific to certain model types or if it can be broadly applied. Additionally, the evaluation should include a comparison with other distributed training techniques, such as tensor parallelism, to provide a more complete picture of ODC's strengths and weaknesses. The paper should also explore the impact of different batch sizes and learning rates on ODC's performance.

Finally, the paper should provide more practical guidance on integrating ODC with existing frameworks. A detailed discussion of the challenges encountered during implementation, such as debugging communication issues or ensuring compatibility with different hardware configurations, would be valuable. The authors should also provide insights into the potential for introducing new bugs or instability, along with strategies for mitigating these risks. This could include a discussion of the testing methodologies used to validate ODC's correctness and robustness. Furthermore, the paper should provide clear guidelines on how to configure ODC for different training scenarios, including recommendations for optimal parameter settings. This would make it easier for other researchers and practitioners to adopt and use ODC in their own projects.

### Questions

1. How does ODC compare to other distributed training techniques, such as tensor parallelism, in terms of communication efficiency and scalability?
2. What are the potential challenges of integrating ODC with other distributed training frameworks, such as DeepSpeed or Megatron-LM?
3. How does ODC handle node failures or network disruptions during training?

### Rating

6

### Confidence

3

**********