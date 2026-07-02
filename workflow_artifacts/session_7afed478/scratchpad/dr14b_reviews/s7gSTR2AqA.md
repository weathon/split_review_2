### Summary

This paper investigates how LLMs perform on color naming tasks, a classic task in cognitive science, and whether the models’ solutions are efficient, in the sense of the Information Bottleneck (IB) framework. The paper further studies how color naming systems evolve via iterated learning in LLMs. Overall, the paper suggests that LLMs vary in their performance, with larger instruction-tuned models achieving the best human alignment and IB-efficiency.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

The paper studies a cognitively motivated task with LLMs, which is a timely research direction. The experimental results are comprehensive: the paper considers 40 models across 6 model families. The paper is also well-written and easy to follow.

### Weaknesses

#### Some Related Works


#### comment

The paper demonstrates an interesting correlation between LLMs’ performance and various model characteristics, e.g., instruction tuning and model size. However, it is not clear whether the results provide novel insights beyond what we already know about LLMs. For example, it is somewhat expected that larger instruction-tuned models perform better on this task, as they generally perform better on many tasks. It is not clear what aspects of the task or the evaluation provide new insights.

The paper claims that its findings suggest that LLMs might have an inductive bias toward IB-efficiency. However, the results only show a correlation between model size and IB-efficiency, and it is known that larger language models learn more complex and structured representations (e.g., through self-supervised pretraining on large corpora). So the results could also be explained by these more complex and structured representations in large models.

### Suggestions

The paper would benefit from a more thorough investigation into the mechanisms driving the observed IB-efficiency. While the correlation between model size and IB-efficiency is interesting, it is not sufficient to claim an inductive bias. The authors should explore whether the observed efficiency is a result of the specific training process or an emergent property of the model architecture. For example, one could investigate if similar efficiency is observed in models trained on different datasets or with different training objectives, but with similar architectural properties. Furthermore, it would be beneficial to analyze the internal representations of the models to understand how they encode color information and how this encoding relates to the observed IB-efficiency. This could involve techniques such as probing or representational similarity analysis to identify the specific features that contribute to the efficient color naming systems.

To strengthen the claim of novel insights, the authors should focus on the specific aspects of the task that reveal unique properties of LLMs. For example, the iterated learning experiment is a good start, but it could be expanded to include more detailed analysis of how the color naming systems evolve over iterations. It would be interesting to see if the evolved systems exhibit specific structural properties, such as hierarchical organization or clustering, and how these properties relate to human color naming systems. Additionally, the authors could compare the performance of LLMs with different types of iterated learning schemes, such as those that involve different levels of feedback or different types of communication between agents. This would help to isolate the specific factors that contribute to the emergence of human-like color naming systems in LLMs.

Finally, the paper could benefit from a more detailed comparison with existing work on the representation of semantic categories in LLMs. While the paper mentions some related work, it does not fully explore the connections and differences between the proposed approach and other methods. For example, the authors could compare their results with those obtained using different evaluation metrics or with those obtained in other domains, such as object or action naming. This would help to contextualize the findings and highlight the unique contributions of the paper. It would also be useful to discuss the limitations of the current approach and suggest directions for future research, such as exploring the role of grounding in the development of human-like color naming systems.

### Questions

1. Could the authors provide more insights on what novel insights about LLMs the paper provides?

2. Could the authors provide further evidence to support the claim that the results suggest that LLMs might have an inductive bias toward IB-efficiency?

### Rating

6

### Confidence

3

**********