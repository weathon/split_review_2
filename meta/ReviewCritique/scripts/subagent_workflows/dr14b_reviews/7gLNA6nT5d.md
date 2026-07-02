### Summary

This paper proposes to add n-gram attention heads to transformers to improve algorithm distillation.

### Soundness

3

### Presentation

3

### Contribution

2

### Strengths

- The paper is relatively clearly written.

### Weaknesses

#### Some Related Works


#### comment

 - The contribution seems a bit thin. It seems that the only contribution is adding n-gram attention heads. If so, I am not sure if this paper is better suited to a more appropriate venue (e.g., TMLR?).
- The paper lacks analysis as to why n-gram attention heads help algorithm distillation.
- The paper lacks comparison to other methods (e.g., retrieval-based methods).

### Suggestions

The paper's core idea of incorporating n-gram attention heads into transformers for algorithm distillation is interesting, but it needs further investigation to solidify its contribution. The current analysis lacks depth, particularly in explaining the mechanism by which n-gram attention heads improve performance. A more thorough analysis should explore how these heads capture sequential dependencies within the learning histories and how this relates to the policy improvement operator that algorithm distillation aims to learn. For example, do specific n-gram lengths capture different aspects of the learning process, and how does this vary across different environments? Furthermore, the paper should investigate the sensitivity of the method to the choice of n-gram size, and whether there is an optimal range for different tasks. This could involve ablations on different n-gram lengths and visualizing the attention patterns to understand what the model is actually attending to.

To strengthen the paper's contribution, it is crucial to compare the proposed method against other relevant baselines. While the authors argue that their method is orthogonal to retrieval-based approaches, it is still important to compare against them empirically. Retrieval-based methods also aim to leverage past experiences to improve learning, and it is important to understand the relative strengths and weaknesses of the proposed method compared to these alternatives. For instance, how does the performance of the n-gram attention heads compare to a method that retrieves and reuses relevant past learning histories? Such a comparison would provide a more comprehensive understanding of the method's effectiveness and its place within the broader landscape of algorithm distillation techniques. Additionally, the paper should consider comparing against other methods that use in-context learning for RL, if available, to better contextualize the contribution.

Finally, the paper should provide a more detailed discussion of the limitations of the proposed method. For example, how does the method scale to more complex environments with longer learning histories? Does the computational cost of the n-gram attention heads become a bottleneck? Also, the paper should discuss the potential for the n-gram heads to overfit to specific learning histories, and how this can be mitigated. Addressing these limitations would provide a more balanced and realistic assessment of the method's practical applicability. Furthermore, the paper should explore the potential for combining n-gram attention heads with other techniques, such as retrieval, to further improve performance. This could lead to more robust and versatile algorithm distillation methods.

### Questions

- The contribution seems a bit thin. It seems that the only contribution is adding n-gram attention heads. If so, I am not sure if this paper is better suited to a more appropriate venue (e.g., TMLR?).
- The paper lacks analysis as to why n-gram attention heads help algorithm distillation.
- The paper lacks comparison to other methods (e.g., retrieval-based methods).

### Rating

3

### Confidence

4

**********