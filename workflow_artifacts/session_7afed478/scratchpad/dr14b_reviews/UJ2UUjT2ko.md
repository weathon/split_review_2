### Summary

This paper studies the mechanisms of entity binding and retrieval in LLMs. The authors propose three mechanisms: positional, lexical, and reflexive. The authors design a set of controlled experiments to analyze the effects of these three mechanisms and conclude that all three mechanisms are necessary for LLMs to bind and retrieve entities.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

The paper is clearly written and the experiments are well-designed. The setting of entity binding and retrieval is interesting and worth exploring. The findings are interesting as well.

### Weaknesses

#### Some Related Works


#### comment

I have a question about the generalizability of the findings. The settings of the tasks and the templates used are relatively simple. It is not clear to me that if the findings still hold in a more general setting. For example, the entity binding and retrieval tasks can be more complicated where the interactions among multiple entities are complex. The templates used in the experiments may not be diverse enough to reflect the diverse settings in the real world.

### Suggestions

The paper's investigation into entity binding and retrieval mechanisms in LLMs is valuable, but the simplicity of the experimental setup raises concerns about the generalizability of the findings. The tasks used, while well-controlled, involve relatively straightforward entity relationships and limited contextual complexity. To strengthen the paper, the authors should consider expanding the complexity of the entity binding tasks. For example, they could explore scenarios with multiple entities of the same type, or introduce tasks where entities have hierarchical or relational dependencies. This would provide a more robust test of the proposed mechanisms and better reflect real-world scenarios where entity relationships are often intricate and multifaceted. Furthermore, the current templates used for generating data might not capture the full range of linguistic variations and contextual nuances present in natural language. 

To address the limitations in template diversity, the authors should explore a broader range of template structures, including those with more complex syntactic structures and varied semantic content. This could involve incorporating templates with nested clauses, ambiguous references, or indirect relationships between entities. Additionally, the authors could consider using a template-free approach, where the tasks are constructed from naturally occurring text, to further enhance the ecological validity of their findings. This would help to ensure that the observed mechanisms are not artifacts of the specific templates used in the experiments. It would also be beneficial to analyze how the identified mechanisms behave when the context is more ambiguous or when the entity references are less explicit. Such an analysis would provide a more comprehensive understanding of the robustness and limitations of these mechanisms.

Finally, the paper would benefit from a more detailed analysis of how the three identified mechanisms interact with each other. While the authors claim that all three mechanisms are necessary, the paper lacks a fine-grained analysis of the conditions under which each mechanism is activated and how they contribute to the final entity retrieval. For example, it would be interesting to see how the relative importance of each mechanism changes as the complexity of the task increases, or how they resolve conflicts when different mechanisms point to different entities. A more thorough investigation of these interactions would provide a deeper understanding of the underlying processes and further strengthen the paper's conclusions.

### Questions

Please see the weakness section.

### Rating

6

### Confidence

3

**********