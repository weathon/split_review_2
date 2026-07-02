### Summary

This paper proposes a new framework for evaluating creativity in LLM-assisted learning, which is a timely and important topic. The authors introduce a process-level approach that attributes learner versus model contributions in multi-turn dialogues and scores four expert-elicited dimensions with rationale texts. The paper presents a novel method for capturing the dynamic emergence of creative thinking in real-time, addressing the limitations of traditional creativity assessments.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

The paper addresses a timely and important topic, as the integration of LLMs in education raises new challenges for assessing creativity. The proposed framework is well-grounded in cognitive science and educational theories, and the methodology is rigorous, with a multi-stage data preprocessing pipeline and expert annotation process. The empirical evaluation with expert assessments indicates alignment with human judgments, and the authors provide a detailed description of the data collection and annotation process, enhancing the reproducibility of the study. The paper also acknowledges the limitations of the study and suggests directions for future work, demonstrating a thoughtful and balanced approach.

### Weaknesses

#### Some Related Works


#### comment

The paper could benefit from a more detailed discussion of the limitations of the proposed framework, particularly regarding its applicability to different types of creative tasks and its sensitivity to various factors that may influence creativity. The current discussion of limitations is somewhat brief and could be expanded to provide a more nuanced understanding of the framework's strengths and weaknesses. For example, the paper does not delve into how the framework might perform with tasks requiring divergent thinking versus those requiring more convergent approaches, or how the framework accounts for individual differences in creative expression. Furthermore, the paper could explore the potential for bias in the expert annotations, which could influence the results. A more thorough analysis of these limitations would strengthen the paper's contribution.

### Suggestions

To enhance the paper, the authors should provide a more detailed analysis of how the proposed framework handles different types of creative tasks. Specifically, they should explore the framework's performance on tasks that emphasize divergent thinking, such as brainstorming or idea generation, versus tasks that focus on convergent thinking, such as problem-solving or design optimization. This could involve conducting experiments with different task types and analyzing the resulting scores and rationales. The authors should also discuss how the framework's reliance on multi-turn dialogues might affect its applicability to tasks that are typically completed in a single turn or with minimal interaction. For example, how would the framework assess a student who quickly generates a novel idea without engaging in an extended dialogue with the LLM? A more nuanced discussion of these aspects would provide a clearer understanding of the framework's scope and limitations.

Additionally, the authors should address the potential for bias in the expert annotations. While the paper mentions a multi-stage annotation process, it does not provide sufficient detail on how inter-rater reliability was assessed and maintained. The authors should include information on the training of the annotators, the specific guidelines they followed, and the measures taken to ensure consistency across different annotators. They should also discuss how the framework accounts for individual differences in creative expression. For example, some students may express their creativity through unconventional language or non-linear thought processes, which might not be easily captured by the framework. The authors should explore how the framework can be adapted to accommodate these differences and ensure that it does not unfairly penalize students with unique creative styles. This could involve incorporating more flexible evaluation criteria or developing methods for identifying and mitigating potential biases in the annotation process.

Finally, the authors should consider the computational cost and scalability of the proposed framework. While the paper mentions the use of LoRA and knowledge distillation to reduce computational overhead, it does not provide a detailed analysis of the framework's performance in terms of processing time and resource consumption. The authors should include information on the time required to process a typical dialogue, the memory requirements of the model, and the potential for parallelization or other optimization techniques. This would be particularly important for real-world applications where the framework might need to process a large number of dialogues in a short period. A more thorough discussion of these practical considerations would enhance the paper's relevance and impact.

### Questions

1. How does the framework handle different types of creative tasks, and what are its limitations in assessing creativity in various domains?
2. What are the computational costs associated with the proposed framework, and how scalable is it for real-world applications?
3. How does the framework address the potential for bias in the expert annotations, and how does it account for individual differences in creative expression?

### Rating

6

### Confidence

3

**********