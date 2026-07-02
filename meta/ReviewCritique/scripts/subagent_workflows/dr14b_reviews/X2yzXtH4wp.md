### Summary

This paper introduces AMBIG-SWE, a benchmark designed to evaluate the ability of LLMs to handle underspecified instructions in software engineering tasks. The study assesses models' performance across three key steps: detecting underspecification, asking clarifying questions, and leveraging interactions to improve task completion. The findings reveal that while models struggle with underspecified inputs, interactive settings significantly boost performance, highlighting the importance of interaction in handling ambiguity.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper addresses a critical gap in how AI agents handle underspecified instructions, which is highly relevant for real-world software engineering tasks.
2. The breakdown of the problem into three distinct steps (detection, clarification, and resolution) provides a clear framework for evaluation and future improvements.
3. The use of both proprietary and open-weight models offers a comprehensive view of current model capabilities and limitations.

### Weaknesses

#### Some Related Works


#### comment

1. The simulated user may not fully capture the complexity of real-world interactions, potentially affecting the generalizability of the findings.
2. The paper could benefit from a more detailed analysis of the types of clarifying questions that lead to the best outcomes, providing actionable insights for model improvement.

### Suggestions

To enhance the robustness of the evaluation, future work should explore more sophisticated simulation techniques for user interactions. This could involve incorporating a diverse set of simulated user behaviors, including varying levels of technical expertise, different communication styles, and the ability to provide ambiguous or contradictory information. Furthermore, the simulation should account for the iterative nature of real-world interactions, where users might refine their requests based on the agent's responses. This could involve incorporating a more dynamic model of user behavior that adapts to the agent's actions, rather than a static set of pre-defined responses. The current simulation, while useful as a starting point, may not fully capture the nuances of human-AI collaboration in software engineering, and addressing this limitation is crucial for the practical applicability of the findings.

To provide more actionable insights for model improvement, the paper should include a detailed analysis of the types of clarifying questions that lead to the best outcomes. This analysis should go beyond simply measuring the number of questions asked or the amount of information gained. Instead, it should focus on the specific characteristics of effective questions, such as their level of detail, their relevance to the task, and their ability to elicit the necessary information from the user. For example, the study could categorize questions based on whether they target functional requirements, implementation details, or constraints, and then analyze which categories are most effective in resolving underspecification. This analysis should also consider the impact of question ordering and the level of detail requested. A more granular analysis of the question-answer pairs would provide valuable insights into the reasoning process of the models and how they leverage the information provided by the user.

Finally, the paper should delve deeper into the relationship between the quality of the clarifying questions and the final task performance. It is not sufficient to simply measure the number of questions asked or the amount of information gained; the study should also assess how well the models utilize the acquired information to complete the task. This could involve analyzing the agent's reasoning process after receiving clarification, identifying any bottlenecks or limitations in its ability to integrate new information. The authors should also investigate whether the models are able to identify and correct errors based on the user's feedback. This could involve analyzing the agent's ability to revise its plan and adapt to new information. Furthermore, the study should explore the use of different evaluation metrics that capture the quality of the agent's reasoning process, rather than just the final outcome.

### Questions

1. How do the authors ensure that the simulated user accurately reflects the behavior of real users in terms of providing clarification?
2. What measures are taken to avoid potential biases in the simulated user responses, and how might these biases affect the results?

### Rating

6

### Confidence

4

**********