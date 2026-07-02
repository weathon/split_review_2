### Summary

This paper studies the causal bandit problem, where the arms are conditional interventions. The authors provide a graphical characterization of the minimal set of nodes guaranteed to contain the optimal conditional intervention, which maximizes the expected reward. They also propose an efficient algorithm with a time complexity of $O(|V| + |E|)$ to identify this minimal set of nodes. The authors prove that the graphical characterization and the proposed algorithm are correct. Finally, they empirically demonstrate that the algorithm significantly prunes the search space and substantially accelerates convergence rates when integrated into standard multi-armed bandit algorithms.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper is well-written and easy to follow.
2. The problem is well-motivated, and the authors provide sufficient examples to justify the motivation.
3. The theoretical results are solid, with clear and rigorous proofs.
4. The empirical results support the theoretical results.

### Weaknesses

#### Some Related Works


#### comment

1. The paper lacks a discussion of the limitations of the proposed algorithm. Specifically, it would be helpful to discuss the computational complexity of the C4 algorithm and how it scales with the size of the causal graph. While the authors claim linear time complexity, a more detailed analysis of the constants involved and the practical implications for very large graphs would be beneficial. Additionally, the assumption of no latent confounders is a significant limitation that restricts the applicability of the method in many real-world scenarios where unobserved variables are common. The paper should explicitly address how this assumption might be violated and what the consequences would be for the validity of the results.
2. The paper could benefit from a more thorough comparison with existing causal bandit algorithms, particularly those that handle hard and soft interventions. A detailed discussion of the advantages and disadvantages of the proposed algorithm compared to these existing methods would help to clarify the contribution of this work. For example, it is unclear how the proposed method compares to algorithms that use causal graphs to guide exploration in bandit problems, or those that explicitly model intervention mechanisms. A more nuanced comparison is needed to understand the specific scenarios where the proposed method is most effective.

### Suggestions

The paper would be significantly strengthened by a more detailed discussion of the computational aspects of the C4 algorithm. While a linear time complexity is promising, the practical performance can be heavily influenced by the constants involved and the specific structure of the causal graph. For instance, it would be useful to analyze the algorithm's performance on different types of graphs, such as sparse vs. dense graphs, or graphs with varying degrees of connectivity. Furthermore, the paper should discuss the memory requirements of the algorithm, which can be a limiting factor for very large graphs. It would also be beneficial to provide some empirical analysis of the algorithm's runtime on real-world or synthetic datasets of varying sizes and complexities. This would give the reader a better understanding of the practical scalability of the proposed method.

To address the limitation of the no latent confounder assumption, the paper should explore potential avenues for extending the proposed method to handle such scenarios. One possible approach is to incorporate techniques from causal discovery that can identify and adjust for latent variables. For example, the paper could discuss how the C4 algorithm could be integrated with methods that learn causal graphs from observational data, or how the algorithm could be modified to incorporate uncertainty about the presence of latent confounders. Another approach could be to explore the use of sensitivity analysis to assess the robustness of the results to violations of the no latent confounder assumption. This would provide a more comprehensive understanding of the limitations of the proposed method and its applicability in real-world settings. The paper should also discuss the implications of using the C4 algorithm on a graph that does not accurately reflect the true underlying causal structure, and how this might affect the identification of the optimal intervention.

Finally, the paper needs a more thorough comparison with existing causal bandit algorithms. The current discussion is too high-level and does not provide sufficient detail to understand the specific advantages and disadvantages of the proposed method. For example, the paper should compare the proposed method to algorithms that use causal graphs to guide exploration in bandit problems, or those that explicitly model intervention mechanisms. A detailed comparison should include a discussion of the assumptions made by each algorithm, their computational complexity, and their performance in different scenarios. This would help to clarify the contribution of this work and identify the specific contexts in which the proposed method is most effective. The paper should also discuss the limitations of existing methods and how the proposed approach addresses these limitations, or provides a complementary perspective.

### Questions

Please see the weaknesses.

### Rating

6

### Confidence

3

**********