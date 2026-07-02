### Summary

This paper proposes a novel forest-based graph learning (FGL) paradigm that enables efficient long-range information propagation. The key insight is to reinterpret message passing on a graph as transportation over spanning trees that naturally facilitates long-range knowledge aggregation, where several trees—a forest—can capture complementary topological pathways. The authors theoretically demonstrate that as edge-homophily estimates improve, the induced distribution biases towards higher-homophily trees, which enables generating a high-quality forest by refining a homophily estimator. Furthermore, the authors propose a linear-time tree aggregator that realizes quadratic node-pair interactions. Empirically, the framework achieves comparable results against state-of-the-art counterparts on semi-supervised node classification tasks while remaining efficient.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper is well-written and easy to follow.

2. The proposed method is novel and interesting.

3. The experimental results are promising.

### Weaknesses

#### Some Related Works


#### comment

1. The proposed method is not well-motivated and is more like a bagging method. The core idea of using a forest of spanning trees, while interesting, lacks a strong theoretical justification. The connection to established graph learning principles is not clearly articulated, making it difficult to understand why this approach should be superior to existing methods. The method appears to be an ensemble technique applied to graph structures without a clear rationale for why this specific ensemble is beneficial.

2. The proposed method is not novel enough, as it is similar to tree-based graph methods [1,2,3]. The use of trees for graph representation is not new, and the paper does not adequately distinguish its approach from existing tree-based methods. The method's novelty is further diminished by the lack of a clear explanation of how it improves upon these existing techniques. The paper needs to provide a more detailed comparison to these methods, highlighting the specific advantages of the proposed approach.

3. The proposed method is also similar to subgraph-based methods [4,5,6]. The method's approach of using a forest to represent the graph bears resemblance to subgraph-based methods, which also aim to capture local and global structures. The paper does not sufficiently differentiate its method from these subgraph-based approaches, leaving the reader unsure of the unique contributions of the proposed method. A more detailed comparison is needed to clarify the differences and advantages of the proposed method over existing subgraph-based techniques.

### Suggestions

To address the lack of motivation, the authors should provide a more rigorous theoretical justification for using a forest of spanning trees. This could involve analyzing the properties of the sampled trees and their relationship to the underlying graph structure. The authors should also explain why this specific ensemble approach is beneficial for graph learning, perhaps by relating it to concepts such as diversity or robustness. A more detailed comparison to existing ensemble methods for graphs would also be beneficial. Furthermore, the authors should clarify the connection between their method and established graph learning principles, such as message passing or spectral graph theory. This would help to better understand the method's underlying mechanisms and its potential advantages over existing approaches. The authors should also provide a more detailed explanation of how the method's components, such as the tree sampler and the tree aggregator, contribute to its overall performance.

To address the lack of novelty, the authors should provide a more detailed comparison to existing tree-based and subgraph-based methods. This should include a thorough analysis of the similarities and differences between the proposed method and these existing techniques, highlighting the specific advantages of the proposed approach. The authors should also provide a more detailed explanation of how their method improves upon these existing techniques, perhaps by demonstrating superior performance on specific tasks or by showing that it can capture different types of graph structures. The authors should also consider incorporating ideas from existing tree-based and subgraph-based methods into their approach, perhaps by using them as a basis for their forest sampling or aggregation strategies. This would help to better position their method within the existing literature and to highlight its unique contributions.

Finally, the authors should consider expanding the scope of their method to address multi-graph datasets and multi-label node classification tasks. This could involve extending the method to handle multiple graphs simultaneously, perhaps by learning a shared forest structure or by using graph-specific forests. For multi-label classification, the method could be adapted to predict multiple labels for each node, possibly by using a multi-output classifier or by learning separate classifiers for each label. Furthermore, the authors should provide a more detailed analysis of the method's performance on datasets with varying characteristics, such as different graph sizes, densities, and homophily levels. This would help to better understand the method's strengths and weaknesses and its suitability for different types of graph data. The authors should also consider the computational cost of their method on larger graphs and provide a more thorough analysis of its scalability.

### Questions

Please see the weaknesses.

### Rating

6

### Confidence

4

**********