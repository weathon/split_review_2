### Summary

This paper introduces a novel task of reordering decoder input tokens into a learning-friendly sequence for Transformers, for learning arithmetic tasks. The proposed pipeline first trains a Transformer on a mixture of target sequences arranged in different orders and then identifies benign orders as those with fast loss drops in the early stage. As the search space grows factorially in sequence length, the authors propose a two-stage hierarchical approach for inter- and intra-block reordering. Experiments on four order-sensitive arithmetic tasks show that their method identifies a learning-friendly order out of a few billion candidates. Notably, on the multiplication task, it recovered the reverse-digit order reported in prior studies.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel task of reordering decoder input tokens into a learning-friendly sequence for Transformers, for learning arithmetic tasks.
2. The paper proposes a two-stage hierarchical approach for inter- and intra-block reordering.
3. Experiments on four order-sensitive arithmetic tasks show that their method identifies a learning-friendly order out of a few billion candidates.

### Weaknesses

#### Some Related Works


#### comment

1. The paper only considers arithmetic tasks.

### Suggestions

The paper's focus on arithmetic tasks, while providing a clear experimental framework, limits the generalizability of the findings. The core idea of reordering decoder input tokens to improve learning efficiency could potentially be applied to a wider range of sequence-to-sequence tasks, such as text generation or code synthesis. Exploring the effectiveness of the proposed method on tasks with more complex input structures and semantic relationships would be a valuable extension. For instance, it would be interesting to see how the method performs on tasks where the optimal ordering is not as straightforward as in arithmetic, and where the relationships between tokens are more nuanced. This would involve adapting the current evaluation metrics and potentially developing new ones that are suitable for non-arithmetic tasks. Furthermore, the current approach relies on identifying 'benign orders' based on fast loss drops in the early stage of training. It would be beneficial to investigate whether this criterion is universally applicable or if it needs to be adjusted for different types of tasks.

The two-stage hierarchical approach for inter- and intra-block reordering is a promising idea, but the paper could benefit from a more detailed analysis of the computational complexity and scalability of this approach. While the authors mention that the search space grows factorially with sequence length, it is not clear how the proposed method mitigates this issue in practice, especially for very long sequences. A more rigorous analysis of the time and memory requirements of the two-stage approach would be helpful. Furthermore, the paper could explore alternative search strategies beyond the current hierarchical approach. For example, reinforcement learning or evolutionary algorithms could be used to explore the space of possible reorderings more efficiently. It would also be interesting to investigate whether the learned reordering is sensitive to the specific architecture of the Transformer model used in the experiments. 

Finally, the paper could benefit from a more in-depth discussion of the limitations of the proposed method. While the experiments on arithmetic tasks are compelling, it is important to acknowledge the potential challenges in applying this approach to more complex tasks. For example, the notion of a 'learning-friendly' order might be task-dependent and difficult to define for tasks with less clear structure than arithmetic. The paper should also discuss the potential impact of the training data on the learned reordering. It is possible that the optimal ordering is influenced by the specific distribution of the training data, and that the method might not generalize well to out-of-distribution examples. A more thorough analysis of these limitations would help to clarify the scope and applicability of the proposed method.

### Questions

1. Can the authors apply their method on more general tasks?

### Rating

6

### Confidence

3

**********