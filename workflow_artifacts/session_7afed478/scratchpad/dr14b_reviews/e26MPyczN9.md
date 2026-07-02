### Summary

This paper revisits the claim that programmatic policies generalize better than neural policies in RL, finding that many observed differences were due to uncontrolled experimental factors. The authors show that neural policies can match programmatic ones with adjustments like sparse observations and cautious reward functions. They argue that generalization depends on both the expressivity of the policy space and the ability of the search algorithm to find generalizing solutions. They also explore cases where programmatic representations have an inherent advantage, particularly in tasks requiring working memory that grows with input size, and demonstrate a programmatic approach that can generalize better in such scenarios.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

The paper is well-written and easy to follow. The authors provide a thorough re-evaluation of previous claims regarding the generalization capabilities of programmatic versus neural policies in reinforcement learning. The experiments are comprehensive, covering multiple benchmarks and scenarios, which strengthens the validity of their conclusions. The paper effectively disentangles representational factors from experimental confounds, providing valuable insights into what contributes to out-of-distribution (OOD) generalization.

### Weaknesses

#### Some Related Works


#### comment

The paper's exploration of programmatic representations with instance-growing memory is limited to a proof-of-concept experiment. More extensive empirical evaluations in diverse settings would strengthen the claims about the inherent advantages of programmatic representations in such tasks. The current proof-of-concept, while demonstrating the potential, lacks the breadth to fully substantiate the claim that programmatic approaches are broadly superior when dealing with tasks requiring memory that scales with input size. Specifically, the paper does not explore the limitations of this approach, such as the potential for increased search space complexity as the input size grows, or the computational cost associated with finding these programmatic solutions. Furthermore, the paper does not investigate how the structure of the programmatic policy affects its generalization capabilities, such as the depth or complexity of the program.

### Suggestions

To strengthen the claims regarding programmatic representations with instance-growing memory, the authors should conduct more extensive empirical evaluations across a wider range of tasks and environments. This should include tasks with varying degrees of complexity and input size growth, to better understand the limitations and scalability of the proposed approach. For example, the authors could explore environments where the required memory grows non-linearly with the input size, or where the memory requirements are not predictable. It would also be beneficial to investigate the impact of different programmatic representations on generalization, such as using different programming languages or different types of program structures. This could involve comparing the performance of programs with varying depths, branching factors, and types of operations. Furthermore, the authors should analyze the computational cost of finding these programmatic solutions, and compare it to the cost of training neural policies with similar generalization capabilities. This analysis should include the time required for search, as well as the memory requirements for storing and executing the programmatic policies. 

In addition to more extensive empirical evaluations, the authors should also provide a more detailed theoretical analysis of the conditions under which programmatic representations are expected to outperform neural policies. This analysis should consider the properties of the tasks that make them suitable for programmatic solutions, such as the presence of regularities or patterns that can be exploited by programmatic representations. The authors should also explore the limitations of neural policies in these scenarios, such as their difficulty in learning algorithms that require explicit memory or symbolic manipulation. This theoretical analysis should be complemented by a discussion of the practical challenges of using programmatic representations, such as the need for efficient search algorithms and the potential for overfitting to the training data. The authors should also consider the trade-offs between the expressiveness of the programmatic representation and its generalization capabilities. 

Finally, the authors should investigate the impact of different search algorithms on the performance of programmatic policies. The current proof-of-concept uses a specific search algorithm, but it is unclear how the choice of algorithm affects the quality of the resulting policies. The authors should explore different search strategies, such as beam search or Monte Carlo tree search, and compare their performance in terms of both the quality of the resulting policies and the computational cost of the search process. This investigation should also consider the impact of different reward functions on the search process, and how they affect the generalization capabilities of the resulting policies. The authors should also explore the use of techniques such as imitation learning or curriculum learning to improve the efficiency of the search process and the quality of the resulting policies.

### Questions

Could you provide more insights into the conditions under which programmatic representations might inherently outperform neural ones, especially in tasks requiring scalable memory?

### Rating

6

### Confidence

3

**********