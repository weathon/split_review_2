### Summary

This paper studies how to improve the performance of actor model on sequential decision-making tasks, such as mathematical reasoning, with the help of a critic model. The major contribution is an two-stage RL approach to train the critic model, which can provide more accurate and constructive feedback to the actor model (see conclusion 1-3 in the discussion for summary). The experiment results show that the proposed approach can improve the performance of the actor model with different initializations.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. This paper studies an important problem, i.e., scalable oversight, which is a major challenge for the application of LLMs in complex tasks.
2. The proposed method is simple and effective.
3. This paper is well-written and easy to understand.

### Weaknesses

#### Some Related Works


#### comment

1. The proposed approach is only evaluated on mathematical reasoning tasks, which can not demonstrate its generality. It would be better to also evaluate on tasks like coding and planning. Specifically, the current evaluation lacks tasks that require more complex symbolic manipulation and long-term planning, which are crucial for assessing the true scalability of the proposed method. The mathematical reasoning tasks, while challenging, may not fully capture the nuances of other complex decision-making scenarios.
2. It would be better to also evaluate on some state-of-the-art models, such as GPT-4o and Llama3.1. The absence of evaluations on these models makes it difficult to compare the proposed approach with the current state-of-the-art performance. It is important to understand how the proposed method performs relative to these highly optimized models, especially given their widespread use and established benchmarks.

### Suggestions

To address the limitations in task diversity, the authors should consider expanding their evaluation to include tasks that involve more intricate symbolic reasoning and long-term planning. For example, incorporating coding tasks that require the model to generate and debug code, or planning tasks that involve multi-step reasoning and decision-making, would provide a more comprehensive assessment of the method's capabilities. Specifically, the authors could adapt existing coding benchmarks, such as those used in the evaluation of large language models for code generation, to suit their framework. This would involve creating a dataset of coding problems with corresponding solutions and using the proposed actor-critic framework to generate code. The performance could then be measured using metrics such as pass@k or exact match. Furthermore, the inclusion of planning tasks, such as those found in the domain of AI planning, would provide a valuable test of the method's ability to handle complex decision-making scenarios. These tasks often require the model to reason about the consequences of its actions over multiple steps, which is a crucial aspect of scalable oversight.

In addition to expanding the task diversity, it is crucial to evaluate the proposed approach on state-of-the-art models. The authors should consider fine-tuning and evaluating their method on models like GPT-4o and Llama3.1, which are widely regarded as benchmarks in the field. This would involve adapting the proposed training procedure to these models and comparing their performance with the results obtained on the current models. This comparison would provide valuable insights into the effectiveness of the proposed approach relative to the current state-of-the-art. It would also help to identify any potential limitations or areas for improvement. The evaluation should include a range of metrics, such as accuracy, convergence speed, and robustness, to provide a comprehensive comparison. Furthermore, the authors should consider reporting the computational resources required for training and evaluation on these models, as this is an important factor for practical applications.

Finally, the authors should provide a more detailed analysis of the critic's feedback and its impact on the actor's performance. This could involve visualizing the critic's feedback and analyzing how it changes over the course of training. It would also be beneficial to investigate the relationship between the quality of the critic's feedback and the actor's performance. For example, the authors could measure the correlation between the critic's accuracy and the actor's improvement. This analysis would provide valuable insights into the inner workings of the proposed method and help to identify areas for further improvement. Additionally, the authors should explore the sensitivity of the method to different hyperparameter settings, such as the learning rate and the strength of the regularization. This would help to ensure the robustness of the method and provide guidance for its application to other tasks and models.

### Questions

1. In stage 2, why the regularization with Stage I can prevent the discriminability of the critique model from dropping, instead of constraining it to the SFT model?
2. How does the refinement with the critique model compare to the refinement with the oracle reward model?

### Rating

6

### Confidence

3

**********