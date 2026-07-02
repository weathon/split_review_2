### Summary

This paper introduces VideoJudge, a scalable framework for training MLLM-based evaluators for video understanding tasks. The proposed framework builds on the interplay between a generator and an evaluator, where the generator produces responses conditioned on a target rating, and the evaluator discards responses that do not match the target rating. The paper shows that a 7B-sized VideoJudge model performs comparably to larger MLLM baselines. The authors also find that providing video inputs is crucial for evaluation performance, and that long chain-of-thought reasoning does not improve performance.

### Soundness

2

### Presentation

3

### Contribution

2

### Strengths

- The paper proposes an LLM-based method to evaluate video understanding. The proposed method takes the input video as input, which is more reliable than extract text descriptions of videos.
- The paper conducts comprehensive experiments to evaluate the proposed method.

### Weaknesses

#### Some Related Works


#### comment

 - The proposed method is not that convincing. The generator can only generate responses that match the rating, it cannot generate responses that can answer the question correctly. In addition, the fine-tuned model is only evaluated on the bootstrapped data, and there is a risk of overfitting.
- The proposed method is not general, it cannot be used for complex videos, such as videos with multiple events.

### Suggestions

The paper's core weakness lies in the limited capability of the generator within the proposed framework. The generator's primary function seems to be producing responses that align with a given rating, rather than generating responses that are genuinely accurate or informative with respect to the input video. This raises concerns about the method's ability to evaluate video understanding in a meaningful way. The generator's dependence on a target rating as a conditioning factor may lead to a situation where the model is simply learning to produce responses that satisfy the rating criteria, rather than responses that are grounded in a true understanding of the video content. This is particularly problematic when dealing with complex videos where a nuanced understanding of the events is required to generate an accurate response. The paper should explore alternative generator architectures or training strategies that prioritize accuracy and informativeness over rating alignment.

Furthermore, the evaluation of the fine-tuned model solely on the bootstrapped data raises significant concerns about overfitting. While the authors claim that the bootstrapped data is diverse, the fact that the model is trained and evaluated on the same dataset means that the reported performance metrics may not accurately reflect the model's generalization capabilities. The model may be learning to exploit specific patterns or biases present in the bootstrapped data, rather than learning to evaluate video understanding in a generalizable way. To address this, the authors should evaluate the fine-tuned model on independent, human-annotated benchmarks to demonstrate its ability to generalize to unseen data. This would provide a more robust assessment of the model's performance and mitigate the risk of overfitting. The paper should also include a detailed analysis of the bootstrapped data to identify any potential biases or limitations that may affect the model's performance.

Finally, the paper's claim that the proposed method is general is not well-supported by the presented evidence. The authors acknowledge that the method may not be suitable for complex videos with multiple events, but they do not provide a clear definition of what constitutes a 'complex video' or a detailed analysis of the method's limitations in such scenarios. The paper should include a more thorough discussion of the types of videos that the method is designed to handle, as well as the types of videos that may pose challenges. This discussion should be supported by empirical evidence, such as experiments on videos with varying degrees of complexity. The authors should also consider exploring methods for handling complex videos, such as segmenting the video into smaller events or using a hierarchical evaluation approach.

### Questions

- What is the generalization ability of the fine-tune model? Can it be used for other video-understanding benchmarks?
- What is the rating distribution of the generated data?

### Rating

5

### Confidence

4

**********