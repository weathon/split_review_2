### Summary

This paper introduces a novel approach called VeriFree, designed to enhance the reasoning capabilities of large language models (LLMs) without relying on external verifiers. Traditional reinforcement learning (RL) methods often depend on rule-based verifiers to provide reward signals, which are ineffective in complex domains like healthcare and law where definitive rules are scarce. VeriFree addresses this limitation by directly maximizing the probability of generating a reference answer, thus bypassing the need for explicit verification. The method is shown to achieve performance on par with or exceeding verifier-dependent approaches across various benchmarks, including MMLU-Pro, GPQA, and SuperGPQA. VeriFree reduces computational demands and simplifies the training process, making it a promising tool for general reasoning tasks.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper is well-written and easy to follow.
2. The motivation is clear and the proposed method is simple yet effective.
3. The experiment results are convincing.

### Weaknesses

#### Some Related Works


#### comment

1. The method relies on high-quality, domain-specific reference answers, which may limit its applicability in areas lacking such data.
2. The method may struggle in scenarios where multiple reasonable answers exist, as it optimizes for a single reference answer.
3. The method may face difficulties when dealing with ambiguous or underspecified questions, as the lack of a verification step could lead to inconsistent or incorrect reasoning paths.

### Suggestions

The reliance on high-quality, domain-specific reference answers is a significant limitation that needs to be addressed more thoroughly. While the paper acknowledges this, it does not delve into potential mitigation strategies. For example, exploring methods for automatically generating or augmenting reference answers could be beneficial. This could involve techniques like few-shot learning, where the model is trained on a small set of examples and then asked to generate new answers, or using a combination of multiple weaker sources to create a stronger reference. Furthermore, the paper should investigate the sensitivity of the method to the quality of the reference answers. How does the performance degrade when the reference answers are noisy or incomplete? A systematic analysis of this aspect would provide a clearer picture of the method's robustness and applicability in real-world scenarios where perfect reference answers are rarely available.

The issue of optimizing for a single reference answer in scenarios with multiple reasonable answers is another area that requires further investigation. The current approach might inadvertently penalize valid reasoning paths that lead to slightly different conclusions. One potential solution is to incorporate a measure of diversity in the training process, encouraging the model to explore multiple reasoning paths and not just converge on a single one. This could be achieved by using a loss function that penalizes similarity between different reasoning trajectories or by explicitly training the model on multiple valid answers for the same question. Additionally, the paper should explore the impact of this single-reference optimization on the model's ability to generalize to unseen scenarios. Does this approach lead to overfitting on the training data, or does it promote a more robust understanding of the underlying reasoning principles?

The challenge of dealing with ambiguous or underspecified questions is a fundamental limitation of the proposed method. The lack of a verification step means that the model is not explicitly guided to identify and resolve ambiguities. Future work should explore ways to integrate uncertainty modeling into the training process. This could involve training the model to output a probability distribution over possible answers, rather than a single deterministic answer. This would allow the model to express its uncertainty when faced with ambiguous questions and avoid making arbitrary decisions. Furthermore, the paper should investigate the use of techniques like active learning, where the model actively seeks clarification when it encounters ambiguous questions. This would allow the model to learn more efficiently and effectively in situations where the input is not clearly defined.

### Questions

See weakness.

### Rating

6

### Confidence

4

**********