### Summary

The paper shows that, in the context of control, ensembles of linear policies are optimal, while ensembles of neural policies are not. The paper also shows that, in the context of control, ensembles of linear policies are stable, while ensembles of neural policies are not. The paper also shows that, in the context of control, ensembles of linear policies are optimal, while ensembles of neural policies are not.

### Soundness

3

### Presentation

2

### Contribution

2

### Strengths

The paper is well-written and easy to follow. The paper provides a good theoretical analysis of the optimality and stability of linear policy ensembles and neural policy ensembles.

### Weaknesses

#### Some Related Works


#### comment

1. The paper does not provide a clear motivation for why the optimality and stability of policy ensembles are important in the context of control. It is not clear how the theoretical results of this paper can be applied to real-world control problems. The paper would benefit from a more detailed discussion of the practical implications of these results, perhaps by providing examples of specific control scenarios where the stability and optimality of policy ensembles are critical. Without such examples, the theoretical contributions seem somewhat disconnected from practical applications.

2. The paper does not provide a comprehensive comparison of the performance of linear policy ensembles and neural policy ensembles on a variety of control tasks. The experiments are limited to a few specific scenarios, which makes it difficult to generalize the findings. A more extensive empirical evaluation, including a wider range of control tasks with varying complexities and dynamics, would be necessary to fully validate the theoretical claims. This should include a comparison of different neural network architectures and training methods, as well as different types of linear policy ensembles.

3. The paper does not provide a detailed analysis of the computational complexity of the proposed methods. While the theoretical analysis is valuable, it is also important to consider the practical computational cost of implementing these methods. A detailed analysis of the time and space complexity of both linear and neural policy ensembles would be beneficial, especially when considering their application to real-time control systems. This analysis should also consider the impact of the size of the policy ensemble on computational cost.

### Suggestions

To address the lack of clear motivation, the authors should include a section that explicitly discusses the practical relevance of their theoretical findings. This section should provide concrete examples of control problems where the stability and optimality of policy ensembles are crucial. For instance, they could discuss scenarios in robotics or autonomous systems where unstable or suboptimal policies could lead to catastrophic failures. Furthermore, the authors should elaborate on how their theoretical results can guide the design of practical control systems. This could involve discussing specific design choices, such as the selection of policy architectures or the methods for combining policies in an ensemble, that are informed by their theoretical analysis. This would help bridge the gap between theory and practice and make the paper more impactful.

To strengthen the empirical evaluation, the authors should conduct a more comprehensive set of experiments across a wider range of control tasks. This should include tasks with varying levels of complexity, dynamics, and dimensionality. The experiments should also compare the performance of different types of linear policy ensembles (e.g., weighted averaging, switching) and different neural network architectures (e.g., MLP, CNN, RNN) and training methods. Furthermore, the authors should investigate the impact of the size of the policy ensemble on performance and stability. This more extensive empirical evaluation would provide a more robust validation of the theoretical claims and allow for a better understanding of the strengths and limitations of linear and neural policy ensembles in different control scenarios. The results should be presented with clear performance metrics and statistical analysis to support the conclusions.

Finally, the authors should provide a detailed analysis of the computational complexity of the proposed methods. This analysis should include both time and space complexity and should consider the impact of the size of the policy ensemble. The authors should also discuss the practical implications of these complexity results, especially when considering the application of these methods to real-time control systems. This analysis should also compare the computational cost of linear and neural policy ensembles, highlighting the trade-offs between performance and computational efficiency. This would provide a more complete picture of the practical feasibility of the proposed methods and help guide the selection of appropriate methods for different control applications.

### Questions

1. What are the practical implications of the theoretical results of this paper? How can the theoretical results of this paper be applied to real-world control problems?

2. How does the performance of linear policy ensembles compare to the performance of neural policy ensembles on a variety of control tasks?

3. What is the computational complexity of the proposed methods? How does the computational complexity of the proposed methods compare to existing methods?

### Rating

5

### Confidence

3

**********