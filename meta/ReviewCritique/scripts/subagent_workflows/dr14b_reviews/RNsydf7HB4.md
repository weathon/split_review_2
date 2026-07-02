### Summary

This paper proposes a novel method called GAMA for solving the Capacitated Vehicle Routing Problem (CVRP) using a graph-aware multi-modal attention model. The main contributions of the paper are as follows:

1. **Novel GAMA Framework**: The authors introduce a novel Learning-to-Improve (L2I) framework that formulates the operator selection process as a Markov Decision Process (MDP). This framework allows the model to adaptively select search operators based on the current search state, enabling dynamic and informed solution improvement.

2. **Graph-Aware Multi-Modal Attention Encoder**: The paper presents a graph-aware multi-modal attention encoder that independently encodes the VRP instance and the current solution as distinct semantic modalities using graph convolutional networks (GCNs). The intra-modality and inter-modality dependencies are modeled through stacked self-attention and cross-attention mechanisms, allowing the model to capture complex relationships between the problem instance and the solution.

3. **Gated Fusion Module**: The authors incorporate a gated fusion module to integrate the multi-modal representations, providing the policy network with rich, structured state features. This gated fusion mechanism helps the model to effectively combine information from different modalities and improve the decision-making quality.

4. **Empirical Evaluation**: The paper conducts extensive experiments on synthetic and benchmark datasets to evaluate the performance of the proposed GAMA framework. The results demonstrate that GAMA consistently outperforms strong neural baselines in both optimization quality and stability. Furthermore, GAMA exhibits strong zero-shot generalization to out-of-distribution instances of significantly larger sizes and different spatial distributions, without retraining.

In summary, this paper makes significant contributions to the field of combinatorial optimization by introducing a novel L2I framework with a graph-aware multi-modal attention model for solving CVRP. The proposed GAMA framework achieves state-of-the-art performance and demonstrates strong generalization capabilities, making it a promising approach for solving complex vehicle routing problems.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. **Novelty**: The paper introduces a novel approach to solving the Capacitated Vehicle Routing Problem (CVRP) by combining graph neural networks (GNNs) and attention mechanisms. This combination allows for a more nuanced understanding of the problem structure and solution space, which is a significant departure from traditional methods.

2. **Comprehensive Evaluation**: The authors have conducted extensive experiments across various synthetic and benchmark instances. This thorough evaluation provides strong evidence of the proposed algorithm's effectiveness and robustness.

3. **Ablation Studies**: The inclusion of ablation studies is a significant strength. These studies help to isolate the impact of different components of the GAMA model, such as the multi-modal attention mechanism and the gated fusion design. This level of detail is crucial for understanding the contributions of each part of the model.

4. **Clarity and Presentation**: The paper is well-written and clearly structured. The authors have done an excellent job of explaining complex concepts in an accessible manner. The use of figures and tables to present the results is effective and enhances the readability of the paper.

5. **Significance**: The problem addressed in this paper is of significant practical importance. Vehicle Routing Problems (VRPs) are common in logistics and transportation, and improvements in solving these problems can lead to substantial cost savings and efficiency gains.

### Weaknesses

#### Some Related Works


#### comment

1. **Scalability Concerns**: While the paper demonstrates strong performance on the tested instances, there is a lack of discussion on the scalability of the proposed method. How does the computational complexity of the GAMA model scale with the size of the problem instances? Are there any limitations in applying this method to very large-scale VRPs? Specifically, the paper does not provide a detailed analysis of the time and space complexity of the graph neural network and attention mechanisms as the number of nodes and edges increases. This is crucial for understanding the practical applicability of the method to real-world problems, which often involve hundreds or thousands of nodes.

2. **Generalization to Other VRP Variants**: The paper focuses primarily on the Capacitated Vehicle Routing Problem (CVRP). How well does the proposed method generalize to other variants of VRPs, such as the Vehicle Routing Problem with Time Windows (VRPTW) or the Stochastic VRP? The paper does not address the potential challenges in adapting the current model to handle time window constraints or stochastic demands, which are common in real-world applications. The current model's reliance on a specific problem structure may limit its applicability to these more complex scenarios.

3. **Sensitivity to Hyperparameters**: The performance of neural networks can be highly sensitive to the choice of hyperparameters. The paper does not provide a detailed analysis of the sensitivity of the GAMA model to different hyperparameter settings. How were the hyperparameters chosen, and how robust is the model to changes in these parameters? A more thorough investigation of the hyperparameter space, including the impact of learning rates, batch sizes, and network architectures, is needed to ensure the reliability of the results.

4. **Comparison with State-of-the-Art Methods**: While the paper compares GAMA with several baselines, it would be beneficial to include a comparison with the most recent state-of-the-art methods in the field. This would provide a clearer picture of the relative performance of the proposed method. The paper should include a more comprehensive comparison with the latest advancements in both heuristic and learning-based approaches to VRP, to better contextualize the contribution of GAMA.

5. **Interpretability of the Model**: The paper does not discuss the interpretability of the GAMA model. Understanding why the model makes certain decisions could be valuable for gaining insights into the problem and for improving the model further. The black-box nature of the attention mechanism makes it difficult to understand which parts of the graph are most influential in the decision-making process. This lack of interpretability hinders the ability to diagnose potential issues or biases in the model.

### Suggestions

To address the scalability concerns, the authors should provide a detailed analysis of the computational complexity of the GAMA model, including the time and space complexity of the graph neural network and attention mechanisms. This analysis should consider how the complexity scales with the number of nodes and edges in the problem instance. Furthermore, the authors should explore techniques to improve the scalability of the model, such as using more efficient graph neural network architectures or approximation methods for the attention mechanism. For example, they could investigate the use of sparse attention or graph sampling techniques to reduce the computational burden on larger graphs. Additionally, the paper should include experiments on larger problem instances to demonstrate the practical applicability of the method to real-world scenarios. This would involve testing the model on instances with hundreds or thousands of nodes and analyzing the performance and resource usage.

To improve the generalization capabilities of the model, the authors should investigate how the GAMA framework can be adapted to handle other VRP variants, such as VRPTW and Stochastic VRP. This would involve modifying the input representation and potentially the network architecture to accommodate the additional constraints and uncertainties. For example, the model could be extended to incorporate time window information as node features or by adding a separate module to handle time window constraints. The authors should also conduct experiments on benchmark instances of these VRP variants to evaluate the performance of the adapted model. This would provide a more comprehensive assessment of the model's generalization capabilities and its potential for real-world applications. Furthermore, the authors should discuss the limitations of the current model in handling these more complex scenarios and suggest potential directions for future research.

To address the sensitivity to hyperparameters, the authors should conduct a more thorough investigation of the hyperparameter space. This should include a systematic exploration of different learning rates, batch sizes, network architectures, and other relevant hyperparameters. The authors should also provide a detailed analysis of the impact of these hyperparameters on the model's performance. This could involve using techniques such as grid search or random search to identify the optimal hyperparameter settings. Furthermore, the authors should discuss the robustness of the model to changes in these parameters and provide guidelines for selecting appropriate hyperparameter values for different problem instances. This would ensure the reliability and reproducibility of the results and make the model more practical for real-world applications.

### Questions

1. **Scalability**: How does the computational complexity of the GAMA model scale with the size of the problem instances? Are there any limitations in applying this method to very large-scale VRPs? Could you provide more details on the computational resources required for training and inference, especially for larger problem sizes?

2. **Generalization**: How well does the proposed method generalize to other variants of VRPs, such as the Vehicle Routing Problem with Time Windows (VRPTW) or the Stochastic VRP? Have you considered any modifications to the model to handle these variants?

3. **Hyperparameter Sensitivity**: Could you provide more details on the hyperparameter tuning process? How sensitive is the model's performance to changes in hyperparameters? Are there any guidelines for selecting appropriate hyperparameter values for different problem instances?

4. **Comparison with State-of-the-Art**: Could you provide a comparison with the most recent state-of-the-art methods in the field? This would help to better understand the relative performance of the proposed method.

5. **Interpretability**: Could you discuss the interpretability of the GAMA model? Understanding why the model makes certain decisions could be valuable for gaining insights into the problem and for improving the model further.

### Rating

6

### Confidence

4

**********