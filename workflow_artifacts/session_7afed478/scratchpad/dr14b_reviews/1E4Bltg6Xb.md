### Summary

This paper proposes a Dynamics Feature Representation (DFR) framework for reinforcement learning (RL)-based dynamic path planning (DPP). The DFR framework progressively refines high-dimensional global dynamics into compact, decision-relevant features, addressing the trade-off between information completeness and computational efficiency. The framework incorporates a policy attention mechanism to identify a core subset of dynamics based on distance-oriented policy and uses n-hop neighborhoods method to further decouple this subset into node-related local feature sequences. The authors demonstrate the effectiveness of the DFR framework through experiments on realistic urban graphs, showing improved performance and accelerated convergence compared to standard baselines.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel DFR framework that effectively addresses the trade-off between information completeness and computational efficiency in RL-based DPP.
2. The proposed framework incorporates a policy attention mechanism and n-hop neighborhood method, which are innovative approaches to refining global dynamics into compact, decision-relevant features.
3. The experiments on realistic urban graphs demonstrate the effectiveness of the DFR framework, showing improved performance and accelerated convergence compared to standard baselines.

### Weaknesses

#### Some Related Works


#### comment

1. The paper lacks a detailed discussion of the limitations of the proposed DFR framework. For example, the authors could discuss the potential challenges in applying the framework to large-scale urban networks or the sensitivity of the framework to the choice of hyperparameters. Specifically, the paper does not address how the computational cost of the policy attention mechanism scales with the size of the graph, which is a critical consideration for real-world applications. Furthermore, the sensitivity analysis of the n-hop neighborhood size is limited, and the paper does not explore the impact of different neighborhood sizes on the performance of the framework in various traffic conditions.
2. The paper could benefit from a more in-depth analysis of the computational complexity of the DFR framework. While the authors mention that the framework reduces the dimensionality of the state representation, they do not provide a detailed analysis of the computational cost of the framework, including the time and space complexity of the different components. A more rigorous analysis of the computational complexity would help to better understand the scalability of the framework and its suitability for different applications. For instance, a breakdown of the time complexity for the policy attention module and the n-hop neighborhood extraction would be beneficial, along with an analysis of how these complexities interact with the size of the input graph.
3. The paper could provide more details on the implementation of the DFR framework, including the specific algorithms and data structures used. This would help to improve the reproducibility of the results and facilitate the adoption of the framework by other researchers. For example, the paper does not specify the exact method used to compute the shortest paths for the policy attention mechanism, nor does it detail the data structures used to represent the n-hop neighborhoods. This lack of detail makes it difficult to replicate the results and understand the practical considerations of implementing the framework.
4. The paper could explore the potential of extending the DFR framework to other dynamic decision-making problems beyond dynamic path planning. For example, the framework could be applied to other transportation problems, such as dynamic ride-sharing or traffic signal control, or to other domains, such as robotics or supply chain management. This would demonstrate the generality of the framework and its potential impact on a wider range of applications. The paper should discuss the specific modifications that would be necessary to adapt the framework to these different problem settings, and it should also discuss the potential challenges and limitations of such extensions.

### Suggestions

The paper would benefit from a more thorough discussion of the limitations of the proposed DFR framework, particularly concerning its scalability to large urban networks. The authors should provide a detailed analysis of how the computational cost of the policy attention mechanism scales with the size of the graph, including the time complexity of computing the attention weights and the memory requirements for storing the attention maps. Furthermore, the paper should explore the sensitivity of the framework to the choice of hyperparameters, such as the size of the n-hop neighborhood, and provide guidelines for selecting appropriate values for these parameters in different traffic conditions. This analysis should include a discussion of the trade-offs between computational cost and performance, and it should provide practical recommendations for applying the framework in real-world scenarios. For example, the authors could investigate the use of approximation techniques to reduce the computational cost of the policy attention mechanism for large graphs, or they could explore adaptive methods for selecting the n-hop neighborhood size based on the local density of the graph.

To improve the reproducibility of the results, the paper should provide more details on the implementation of the DFR framework, including the specific algorithms and data structures used. The authors should specify the exact method used to compute the shortest paths for the policy attention mechanism, such as Dijkstra's algorithm or A*, and they should also detail the data structures used to represent the n-hop neighborhoods, such as adjacency lists or matrices. Furthermore, the paper should provide a clear explanation of how the global dynamics features are extracted and processed, and it should include pseudocode or algorithmic descriptions of the key steps in the framework. This level of detail would enable other researchers to replicate the results and build upon the proposed framework. The authors should also consider releasing the source code of their implementation to further enhance the reproducibility and adoption of their work.

Finally, the paper should explore the potential of extending the DFR framework to other dynamic decision-making problems beyond dynamic path planning. The authors should discuss the specific modifications that would be necessary to adapt the framework to different problem settings, such as dynamic ride-sharing or traffic signal control, and they should also discuss the potential challenges and limitations of such extensions. For example, in the context of dynamic ride-sharing, the framework would need to handle the additional complexity of matching riders and drivers, and it would need to consider the temporal dynamics of ride requests. In the context of traffic signal control, the framework would need to optimize the timing of traffic lights based on real-time traffic conditions. The paper should also discuss the potential benefits of applying the DFR framework to these other domains, and it should provide a roadmap for future research in this area.

### Questions

1. How does the computational cost of the DFR framework scale with the size of the urban network? Are there any limitations in applying the framework to large-scale networks?
2. How sensitive is the performance of the DFR framework to the choice of hyperparameters, such as the size of the n-hop neighborhood? Are there any guidelines for selecting appropriate values for these parameters?
3. Can the DFR framework be extended to other dynamic decision-making problems beyond dynamic path planning? What are the potential challenges and limitations of such extensions?

### Rating

6

### Confidence

3

**********