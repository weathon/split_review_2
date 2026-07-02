### Summary

This paper proposes a novel framework for safe reinforcement learning (RL) in verifiable code synthesis where formal verification constraints are integrated in the form of differentiable parts as components in the policy optimization loop. Traditional approaches to verification are seen as a post-hoc filter or a black-box reward signal, and this often results in inefficiencies and mismatches between the generated code and safety guarantees. The proposed method adds a differentiable verification layer that mimics formal verification steps with the help of smoothing surrogate functions that allows for gradient-based improvement of both code generation and safety specifications. This layer calculates soft satisfaction scores for safety properties which are then ushered in consensus with rewards completing the tasks in order to calculate the RL policy.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper is well-written and easy to follow.
2. The idea of integrating differentiable verification into the RL loop is interesting and novel.
3. The experimental results show the effectiveness of the proposed method.

### Weaknesses

#### Some Related Works


#### comment

1. The paper does not provide a detailed analysis of the computational overhead introduced by the differentiable verification layer. Specifically, it is unclear how the complexity of the verification constraints impacts the training time and resource consumption. For instance, while the paper mentions using a GNN for structural checks, it does not specify the exact architecture or the number of parameters, making it difficult to assess the computational cost. Furthermore, the paper lacks a comparison of training times with and without the differentiable verification layer, which is crucial for understanding the practical implications of this approach.
2. The paper lacks a comprehensive discussion on the limitations of the differentiable verification approach, particularly regarding its scalability to more complex verification constraints. The current examples focus on relatively simple properties, and it is unclear how the method would perform with more intricate specifications, such as those involving complex data structures or intricate control flow. The paper should address the potential challenges in approximating such constraints with differentiable functions and the impact on the accuracy of the verification process.

### Suggestions

To address the lack of detailed analysis on computational overhead, the authors should provide a more thorough breakdown of the differentiable verification layer's architecture, including the specific GNN model used, the number of parameters, and the computational complexity of each component. A comparison of training times with and without the differentiable verification layer, across different benchmark tasks, would be highly beneficial. Furthermore, the authors should analyze the impact of the complexity of verification constraints on training time and resource consumption. This could involve varying the number of nodes and edges in the PDG, or the complexity of the logical formulas used for verification, and measuring the corresponding changes in training time and memory usage. Such an analysis would provide a clearer understanding of the practical limitations of the proposed approach.

To address the limitations regarding scalability, the authors should include a more detailed discussion on the challenges of approximating complex verification constraints with differentiable functions. This could involve providing examples of more intricate specifications and discussing the potential difficulties in representing them with smoothing surrogate functions. The authors should also explore alternative approaches for handling such constraints, such as hierarchical verification or the use of more expressive differentiable functions. Furthermore, the paper should include an analysis of the trade-offs between the accuracy of the differentiable verification and the computational cost, particularly when dealing with complex constraints. This would provide a more comprehensive understanding of the applicability of the proposed method to real-world scenarios.

Finally, the authors should consider including a more detailed analysis of the feature functions used in the verification layer. Specifically, they should discuss the process of selecting these functions and the criteria used to ensure they capture the relevant aspects of the verification process. A sensitivity analysis of the impact of different feature functions on the performance of the framework would also be valuable. This would provide a better understanding of the robustness of the approach and its ability to generalize to different types of verification constraints.

### Questions

1. How does the complexity of the verification constraints impact the training time and resource consumption of the proposed method?
2. How does the proposed method scale to more complex verification constraints?
3. How are the feature functions in the verification layer selected, and how do they impact the performance of the framework?

### Rating

6

### Confidence

3

**********