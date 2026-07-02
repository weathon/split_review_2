### Summary

This paper proposes a novel graphon cross-validation method for selecting tuning parameters and estimation approaches. The proposed method is both theoretically sound and computationally efficient. The authors demonstrate that the proposed cross-validation score is asymptotically parallel to the estimation error, and the selected model asymptotically converges to the optimal model. Through extensive simulations and real-world applications, the paper shows that the proposed method consistently achieves superior computational efficiency and accuracy.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper is well-written and easy to follow.
2. The proposed method is innovative and addresses a key challenge in graphon modeling.
3. The paper provides theoretical guarantees for the proposed method.
4. The paper includes extensive simulations and real-world applications to demonstrate the effectiveness of the proposed method.

### Weaknesses

#### Some Related Works


#### comment

1. The paper could benefit from a more detailed discussion of the limitations of the proposed method and potential directions for future research.
2. The paper could provide more details on the computational cost of the proposed method and compare it to existing methods.

### Suggestions

The paper should delve deeper into the specific scenarios where the proposed cross-validation method might underperform. For instance, while the method is presented as model-agnostic, it would be beneficial to explore its behavior with estimators that have very different structural assumptions or optimization landscapes. Consider, for example, how the method would perform with a spectral estimator that relies on a low-rank approximation of the adjacency matrix, compared to a neighborhood smoothing estimator. The paper should discuss whether the cross-validation score is equally effective across such diverse estimation approaches, or if certain types of estimators are more amenable to this approach. Furthermore, the paper should explore the sensitivity of the method to the choice of the perturbation strategy used to create the validation set. It is not clear if the performance is robust to different perturbation strategies or if specific strategies are more suitable for certain types of graphon models. A more detailed analysis of these aspects would significantly strengthen the paper.

Regarding computational cost, the paper should provide a more granular analysis of the time complexity of the proposed method, breaking down the cost into different components. For example, the cost of generating the perturbed graph, the cost of fitting the model on the training set, and the cost of evaluating the model on the validation set should be analyzed separately. This would allow for a more precise comparison with existing methods. The paper should also discuss the memory requirements of the proposed method, especially when dealing with large-scale networks. It is important to understand how the memory footprint scales with the number of nodes and edges, and whether the method is suitable for very large networks. A detailed comparison of the computational cost and memory requirements with existing cross-validation methods for network data would be highly valuable. This should include a discussion of the practical limitations of the method in terms of scalability.

Finally, the paper should provide more concrete guidance on how to choose the tuning parameters of the proposed method, such as the size of the validation set or the specific perturbation strategy. While the paper demonstrates the effectiveness of the method, it lacks a clear discussion of how to optimize these parameters in practice. The paper should provide some heuristics or rules of thumb for choosing these parameters, based on the characteristics of the network data and the specific estimation approach being used. This would make the method more accessible to practitioners and would increase its practical impact. The paper should also discuss the potential trade-offs between computational cost and accuracy when choosing these parameters.

### Questions

How does the proposed method perform with different types of graphon models and estimation approaches?

What are the potential directions for future research in this area?

Can the authors provide more details on the computational cost of the proposed method and compare it to existing methods?

### Rating

6

### Confidence

3

**********