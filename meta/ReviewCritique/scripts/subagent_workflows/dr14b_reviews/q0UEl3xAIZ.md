### Summary

The paper experimentally evaluates the GOEI algorithm on a competitive card game. The results show that the algorithm can learn a state representation that leads to a near-optimal policy, while reducing the number of states by 97%.

### Soundness

3

### Presentation

2

### Contribution

3

### Strengths

The paper shows that the GOEI algorithm can be successfully applied to a real-world problem. The algorithm is able to learn a state representation that leads to a near-optimal policy, while significantly reducing the number of states. This is an important result, as state aggregation is one of the most important problems in AI. The experiments are well-designed and the results are clearly presented.

### Weaknesses

#### Some Related Works


#### comment

The paper is more like a case study, with no additional technical contributions. The method is restricted to episodic MDPs. The algorithm is not compared to other state aggregation algorithms.

### Suggestions

The paper would benefit from a more thorough comparison to existing state aggregation techniques. While the authors demonstrate the effectiveness of GOEI on a specific card game, it is unclear how it performs relative to other established methods. For instance, a comparison against methods that use techniques like Bayesian Action Selection or other forms of state abstraction would provide a more comprehensive understanding of GOEI's strengths and weaknesses. The current evaluation lacks a clear benchmark, making it difficult to assess the practical significance of the results. A more rigorous comparison would involve evaluating the algorithms on a suite of tasks, including those from the original GOEI paper, to provide a more robust assessment of the proposed method's performance.

Furthermore, the paper should address the limitations of the episodic setting more explicitly. While many real-world problems can be framed as episodic MDPs, the assumption of a fixed time horizon and full observability at each step is a significant constraint. The paper should discuss the implications of this assumption and how it might affect the applicability of the method to more general settings. For example, in partially observable or continuous environments, the current approach may not be directly applicable. A discussion of potential extensions or modifications to handle such cases would be valuable. The authors could also consider discussing the computational complexity of the algorithm, especially in relation to the size of the state space and the number of episodes.

Finally, the paper should provide more details on the implementation of the algorithm and the experimental setup. For example, it would be helpful to know the specific hyperparameters used for the GOEI algorithm and how they were chosen. Additionally, more information on the neural network architecture used to implement the policy would be beneficial. This would allow other researchers to reproduce the results and build upon the work. The paper should also include a discussion of the sensitivity of the algorithm to different parameter settings and experimental conditions. This would provide a more complete picture of the algorithm's performance and robustness.

### Questions

1. How does the algorithm compare to other state aggregation algorithms?
2. Can the algorithm be applied to non-episodic problems?

### Rating

6

### Confidence

4

**********