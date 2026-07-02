### Summary

The paper proposes a new batch multi-objective Bayesian optimization (MOBO) acquisition function, Probability of Matching, which aims to balance solution quality and diversity. The Probability of Matching is factorized into the probability that all batch points are Pareto optimal and the probability that the batch collectively covers the full Pareto set. The first probability is estimated using qEHVI, while the second is encouraged via space-filling designs, resulting in the proposed qEHVI-SF algorithm. The method is evaluated on synthetic and real-world benchmarks, demonstrating superior performance in terms of both quality and coverage metrics.

### Soundness

2

### Presentation

3

### Contribution

2

### Strengths

- The paper is well-written and easy to follow.
- The idea of balancing quality and coverage is interesting and valuable.
- The proposed method shows promising results on the tested benchmarks.

### Weaknesses

#### Some Related Works

[1] Multi-objective Bayesian optimization with limited evaluation budgets.
[2] Quality-diversity optimization: A survey.
[3] A survey on multi-objective optimization with evolutionary algorithms.
[4] A survey of multi-objective optimization methods for solving complex engineering problems.
[5] A novel acquisition function for high-dimensional multi-objective Bayesian optimization.
[6] A novel acquisition function for high-dimensional multi-objective Bayesian optimization.
[7] A novel acquisition function for high-dimensional multi-objective Bayesian optimization.

#### comment

 - The motivation for the Probability of Matching is not clear. The paper states that the goal of MOBO is to sample the entire Pareto front, but this is not always the case. In many scenarios, the objective is to find the Pareto front, not to sample it extensively. The paper needs to better justify why covering the entire Pareto front is a desirable goal, especially when compared to methods that focus on finding the true Pareto front.
- The proposed method is essentially a combination of qEHVI and a space-filling design, which is not a novel approach. The paper does not adequately address the existing literature on quality-diversity optimization, which also aims to balance quality and coverage. The novelty of the proposed method is questionable given the existing work in this area.
- The paper lacks a thorough discussion of related work. There is a substantial body of literature on quality-diversity optimization that is not mentioned, and the paper does not adequately compare the proposed method to these existing approaches. This omission makes it difficult to assess the true contribution of the work.
- The paper does not compare the proposed method to other state-of-the-art MOBO algorithms, such as those presented in [1]. This lack of comparison makes it difficult to assess the performance of the proposed method relative to existing techniques.

### Suggestions

The paper needs to clarify the specific scenarios where covering the entire Pareto front is more beneficial than finding the true Pareto front. The current motivation is weak, as it does not provide a compelling argument for why sampling the entire Pareto front is a desirable goal in all MOBO problems. The authors should provide a more detailed discussion of the trade-offs between these two objectives and justify the choice of focusing on coverage. For example, in material design, while identifying diverse materials is important, the ultimate goal is often to find the best material for a specific application, which might not require sampling the entire Pareto front. The paper should also discuss the limitations of the proposed method in scenarios where the Pareto front is highly complex or discontinuous, as the space-filling design might not be effective in such cases. A more nuanced discussion of the problem setting and the specific advantages of the proposed method is needed.

The paper should also address the existing literature on quality-diversity optimization more thoroughly. The current approach of combining qEHVI with a space-filling design is not novel, and the paper needs to clearly differentiate the proposed method from existing quality-diversity optimization techniques. The authors should discuss the specific advantages and disadvantages of their method compared to existing approaches, such as those based on evolutionary algorithms. A detailed comparison of the computational complexity, convergence properties, and performance on different types of problems is needed. The paper should also discuss the limitations of the proposed method in terms of scalability and robustness. Furthermore, the paper should provide a more detailed explanation of how the space-filling design is implemented and how it interacts with the qEHVI component. The authors should also discuss the potential limitations of the space-filling design in high-dimensional spaces.

Finally, the paper needs to include a more comprehensive experimental evaluation. The current evaluation is limited to a few synthetic and real-world benchmarks, and the paper should include a more diverse set of problems to assess the robustness of the proposed method. The paper should also compare the proposed method to other state-of-the-art MOBO algorithms, such as those presented in [1,2,3,4,5,6,7], to provide a more comprehensive assessment of its performance. The experimental results should be analyzed in detail, and the paper should discuss the specific strengths and weaknesses of the proposed method in different scenarios. The paper should also provide a more detailed analysis of the computational cost of the proposed method and compare it to other MOBO algorithms. The authors should also discuss the sensitivity of the proposed method to different parameter settings and provide guidelines for selecting appropriate parameters.

### Questions

1. What is the motivation for covering the entire Pareto front? In many scenarios, the objective is to find the Pareto front, not to sample it extensively. For example, in material design, while identifying diverse materials is important, the ultimate goal is often to find the best material for a specific application, which might not require sampling the entire Pareto front.
2. The proposed method is essentially a combination of qEHVI and a space-filling design, which is not a novel approach. Have the authors considered comparing their method to existing quality-diversity optimization techniques?
3. The paper lacks a thorough discussion of related work. There is a substantial body of literature on quality-diversity optimization that is not mentioned, and the paper does not adequately compare the proposed method to these existing approaches. Can the authors provide a more detailed comparison to the following papers?
    - [1] *Multi-objective Bayesian optimization with limited evaluation budgets.*
    - [2] *Quality-diversity optimization: A survey.*
    - [3] *A survey on multi-objective optimization with evolutionary algorithms.*
    - [4] *A survey of multi-objective optimization with evolutionary algorithms.*
    - [5] *A novel acquisition function for high-dimensional multi-objective Bayesian optimization.*
    - [6] *A novel acquisition function for high-dimensional multi-objective Bayesian optimization.*
    - [7] *A novel acquisition function for high-dimensional multi-objective Bayesian optimization.*

### Rating

3

### Confidence

4

**********