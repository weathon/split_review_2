### Summary

This paper introduces LLM4GCL, a benchmark for evaluating large language models (LLMs) in graph continual learning (GCL) scenarios. The authors identify limitations in current GCL evaluation methods and propose a new approach, Simple Graph Continual Learning (SimGCL), that leverages LLMs to improve performance. SimGCL uses an ego-graph-derived prompt for each node, capturing textual and structural features, and employs a training-free prototype classifier in incremental sessions to avoid catastrophic forgetting. The approach demonstrates superior performance compared to existing GNN-based baselines, with an absolute increase of nearly 20% on certain datasets. The authors provide an easy-to-use open-source platform to facilitate further research in this area.

### Soundness

2

### Presentation

3

### Contribution

2

### Strengths

1. The paper identifies a previously overlooked flaw in current experimental setups for Graph Continual Learning (GCL), specifically task ID leakage in local testing. By addressing this issue, the authors contribute to improving the evaluation standards in the field.
2. The introduction of LLM4GCL as a comprehensive benchmark for evaluating LLMs in GCL is a significant contribution. It provides a standardized platform for researchers to assess and compare different methods.
3. The proposed SimGCL method demonstrates a substantial performance improvement (around 20%) over existing baselines under the rehearsal-free constraint. This highlights the effectiveness of their approach in mitigating catastrophic forgetting.

### Weaknesses

#### Some Related Works


#### comment

1. The paper's primary focus on node classification tasks limits its exploration of other important GCL scenarios, such as edge prediction or graph-level classification. This narrow focus may reduce the generalizability of the findings. The evaluation could benefit from including more diverse graph learning tasks to demonstrate the robustness of the proposed method. For example, the benchmark could include tasks that require predicting properties of the graph as a whole, or tasks that involve predicting the existence or type of relationships between nodes, which are common in many real-world applications.
2. While the paper claims that SimGCL is efficient, it lacks a detailed analysis of the computational complexity and resource requirements, especially when scaling to larger graphs. The paper should include a more rigorous analysis of the time and memory requirements of the proposed method, particularly in comparison to existing GNN-based approaches. This analysis should consider the impact of graph size and the number of nodes and edges on the overall performance and resource consumption.
3. The paper does not provide a thorough investigation into the reasons behind the underperformance of GLM-based methods in GCL. While they offer some explanations, a more in-depth analysis, possibly including ablation studies, would strengthen their findings. For example, the authors could investigate the impact of different components of the GLM architecture on the performance in GCL tasks, or analyze the gradients during training to understand why these models struggle with catastrophic forgetting.

### Suggestions

To enhance the paper, the authors should broaden the scope of their evaluation beyond node classification. Including tasks such as edge prediction, graph classification, and link prediction would significantly improve the generalizability of their findings and demonstrate the versatility of the proposed LLM4GCL benchmark. For edge prediction, the benchmark could include tasks that involve predicting the existence or type of relationships between nodes, which are common in many real-world applications. For graph classification, the benchmark could include tasks that require predicting properties of the graph as a whole, such as categorizing molecules based on their properties or classifying social networks based on their structure. This would provide a more comprehensive evaluation of the proposed method and its applicability to a wider range of graph learning problems. The authors should also consider including datasets with varying graph sizes and densities to assess the scalability of the proposed approach.

Furthermore, the authors should provide a more detailed analysis of the computational complexity and resource requirements of SimGCL. This analysis should include a breakdown of the time and memory consumption for each step of the algorithm, such as the ego-graph construction, prompt generation, and prototype classifier training. The analysis should also consider the impact of graph size, number of nodes, and number of edges on the overall performance and resource consumption. A comparison with existing GNN-based approaches would be beneficial to demonstrate the efficiency of the proposed method. This analysis should be supported by empirical results on datasets of varying sizes and complexities. The authors should also discuss the potential limitations of their approach in terms of scalability and resource usage, and suggest potential solutions for addressing these limitations.

Finally, the authors should conduct a more thorough investigation into the reasons behind the underperformance of GLM-based methods in GCL. This investigation should include ablation studies to analyze the impact of different components of the GLM architecture on the performance in GCL tasks. For example, the authors could investigate the impact of different attention mechanisms or layer configurations on the performance of GLMs in GCL. Additionally, the authors should analyze the gradients during training to understand why these models struggle with catastrophic forgetting. This analysis could provide valuable insights into the limitations of GLMs in GCL and guide the development of more effective methods for addressing these challenges. The authors should also consider exploring alternative training strategies or regularization techniques that could improve the performance of GLMs in GCL.

### Questions

1. How does SimGCL perform on other GCL tasks beyond node classification, such as edge prediction or graph-level classification?
2. What are the computational costs associated with SimGCL when applied to large-scale graphs? How does it compare to existing GNN-based methods in terms of efficiency?
3. The paper notes that current GLM-based methods underperform in GCL scenarios. Could the authors provide more detailed analysis or experiments to understand the reasons behind this limitation?

### Rating

6

### Confidence

3

**********