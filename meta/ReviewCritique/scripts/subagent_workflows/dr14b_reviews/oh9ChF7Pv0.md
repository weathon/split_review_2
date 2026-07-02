### Summary

This paper introduces EGG-SR, a framework that integrates symbolic equivalence into symbolic regression methods to accelerate training and reduce the search space. The core idea is to use equality graphs (e-graphs) to represent equivalent expressions, which helps in pruning redundant exploration, aggregating rewards, and enriching feedback prompts. The framework is applied to three modern symbolic regression algorithms: Monte Carlo Tree Search (MCTS), Deep Reinforcement Learning (DRL), and Large Language Models (LLMs). Theoretical analysis shows that EGG-SR tightens the regret bound of MCTS and reduces the variance of the DRL gradient estimator. Empirical results demonstrate that EGG-SR consistently enhances performance across various benchmarks, discovering more accurate expressions within the same time limit.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper is well-written and easy to follow. The authors provide a clear and concise explanation of the proposed method, making it accessible to readers with varying levels of expertise in symbolic regression and machine learning.
2. The theoretical analysis is solid and provides a strong foundation for the proposed method. The authors rigorously prove that EGG-SR tightens the regret bound of MCTS and reduces the variance of the DRL gradient estimator, which are significant contributions to the field.
3. The empirical results are comprehensive and convincing. The authors evaluate EGG-SR on multiple benchmarks and compare it with several state-of-the-art methods. The results consistently show that EGG-SR outperforms the baselines, demonstrating the practical effectiveness of the proposed framework.

### Weaknesses

#### Some Related Works


#### comment

1. The paper could benefit from a more detailed discussion of the limitations of the proposed method. For instance, how does EGG-SR perform on very large or complex datasets? Are there any specific types of expressions or datasets where EGG-SR might struggle? The current analysis does not sufficiently explore the boundaries of the method's applicability, particularly in scenarios with high-dimensional input spaces or highly complex target functions. A more thorough investigation into the computational scaling of EGG-SR with respect to the size and complexity of the search space would be valuable.
2. The paper could also discuss potential future directions for research. For example, could EGG-SR be extended to other types of symbolic regression algorithms? Are there any other ways to leverage symbolic equivalence in machine learning? The discussion of future work is somewhat limited. It would be beneficial to explore how the core concepts of EGG-SR, such as the use of e-graphs for representing symbolic equivalence, could be generalized to other machine learning paradigms beyond the three methods presented. For example, could this approach be integrated with evolutionary algorithms or other optimization techniques used in symbolic regression?

### Suggestions

To address the limitations regarding the performance of EGG-SR on complex datasets, the authors should conduct a more detailed analysis of the method's behavior under varying conditions. This should include experiments with datasets that have a higher number of input variables, more complex target functions, and a larger search space. Specifically, the authors could investigate how the size of the e-graph and the computational cost of maintaining it scale with the complexity of the problem. It would also be useful to analyze the impact of different rewrite rules on the performance of EGG-SR, as the effectiveness of the method may depend on the specific set of rules used. Furthermore, the authors should explore the potential for using adaptive rewrite rules that are learned during the training process, which could improve the method's ability to handle complex expressions. A more thorough investigation into the computational scaling of EGG-SR with respect to the size and complexity of the search space would be valuable.

To expand on the potential future directions, the authors should explore how the core concepts of EGG-SR could be generalized to other machine learning paradigms. For example, the use of e-graphs for representing symbolic equivalence could be integrated with evolutionary algorithms, where the e-graph could be used to guide the search process and avoid redundant exploration. The authors could also investigate how EGG-SR could be applied to other types of symbolic regression problems, such as those involving non-linear functions or differential equations. Furthermore, the authors should discuss the potential for using EGG-SR in other areas of machine learning, such as program synthesis or code optimization, where the ability to represent and manipulate symbolic expressions is crucial. This would help to broaden the impact of the proposed method and highlight its potential for future research.

Finally, the authors should consider providing a more detailed analysis of the computational overhead introduced by the e-graph construction and manipulation. While the paper mentions that the overhead is minimal, a more rigorous analysis of the time and space complexity of these operations would be beneficial. This analysis should include a comparison with the computational cost of the base symbolic regression algorithms, as well as an investigation into how the overhead scales with the size and complexity of the expressions. This would help to provide a more complete picture of the practical implications of using EGG-SR and would allow readers to better assess the trade-offs between performance and computational cost.

### Questions

1. How does EGG-SR perform on very large or complex datasets? Are there any specific types of expressions or datasets where EGG-SR might struggle?
2. Could EGG-SR be extended to other types of symbolic regression algorithms? Are there any other ways to leverage symbolic equivalence in machine learning?

### Rating

6

### Confidence

3

**********