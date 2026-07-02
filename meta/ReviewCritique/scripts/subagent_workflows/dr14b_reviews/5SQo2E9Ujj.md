### Summary

The paper explores curriculum learning in goal-conditioned reinforcement learning (GCRL) by focusing on data selection rather than traditional exploration. The authors propose biasing goal sampling towards "underachieved" goals to improve learning efficiency. Using Universal Value Function Approximators (UVFAs) with potential-based reward shaping in a GridWorld environment, they compare uniform and curriculum-guided training. The results indicate that curricula alter goal coverage, reduce approximation error, and enhance success rates, particularly on challenging edge goals. This study frames curriculum learning as a structured approach to data acquisition, aiming to advance more persistent and open-ended learning agents.

### Soundness

2

### Presentation

2

### Contribution

2

### Strengths

1. The paper provides a clear and well-organized presentation of the proposed curriculum learning approach, making it easy to follow the methodology and experimental setup.
2. The focus on data selection as a mechanism for curriculum learning offers a fresh perspective, distinguishing it from traditional exploration-based methods.
3. The use of UVFAs and potential-based reward shaping in a GridWorld environment allows for a controlled study of the effects of curriculum learning on goal coverage and success rates.

### Weaknesses

#### Some Related Works


#### comment

1. The experimental scope is limited to a GridWorld environment, which may not fully capture the complexities of real-world scenarios. The GridWorld environment, while useful for initial testing, lacks the high-dimensional state spaces and continuous action spaces found in many practical applications of reinforcement learning. This limitation raises concerns about the generalizability of the findings to more complex and realistic settings. For example, the curriculum learning approach might not be as effective in environments with sparse rewards or noisy observations, which are common in real-world tasks.
2. The curriculum strategies are manually designed, which may limit the scalability and adaptability of the approach to more complex domains. The manual design of curricula requires domain expertise and can be time-consuming. Furthermore, it is unclear how these manually designed curricula would perform in environments with different goal structures or reward functions. An automated or adaptive curriculum design method would be more robust and scalable. The lack of a systematic approach to curriculum design also makes it difficult to compare different curriculum strategies.
3. The performance improvements reported are modest, and the paper does not provide a comprehensive comparison with other curriculum learning methods. The reported improvements, while statistically significant, are not substantial enough to demonstrate a clear advantage over existing methods. A more thorough evaluation, including comparisons with state-of-the-art curriculum learning techniques, is needed to establish the effectiveness of the proposed approach. The absence of such comparisons makes it difficult to assess the novelty and impact of the work.

### Suggestions

To address the limitations of the experimental scope, future work should evaluate the proposed curriculum learning approach in more complex and realistic environments. This could include environments with high-dimensional state spaces, continuous action spaces, and sparse rewards. For example, the method could be tested in robotic manipulation tasks or navigation problems with complex obstacle layouts. Such experiments would provide a more comprehensive assessment of the approach's generalizability and robustness. Furthermore, it would be beneficial to investigate how the curriculum learning approach performs in environments with noisy observations or partial observability, which are common challenges in real-world applications. These experiments should also include a variety of different goal structures and reward functions to evaluate the adaptability of the proposed method.

To overcome the limitations of manual curriculum design, future research should focus on developing automated or adaptive curriculum design methods. This could involve using reinforcement learning to learn the curriculum itself, or employing techniques such as active learning to select the most informative goals for training. For example, a meta-learning approach could be used to learn a curriculum generation policy that can be applied to different environments. This would make the approach more scalable and adaptable to a wider range of tasks. Additionally, it would be beneficial to investigate how different curriculum design strategies affect the learning process and the final performance of the agent. A systematic comparison of different curriculum design methods would provide valuable insights into the principles of effective curriculum learning.

To strengthen the evaluation of the proposed approach, future work should include a comprehensive comparison with other state-of-the-art curriculum learning methods. This comparison should include a variety of different environments and evaluation metrics to provide a thorough assessment of the approach's performance. For example, the proposed method could be compared with curriculum learning methods that use difficulty-based sampling or those that use a teacher agent to guide the learning process. This comparison should also include an analysis of the computational cost and sample efficiency of the different methods. A more thorough evaluation would help to establish the novelty and impact of the proposed approach and provide a clearer understanding of its strengths and weaknesses.

### Questions

1. How does the proposed curriculum learning approach compare with other state-of-the-art curriculum learning methods in terms of performance and computational efficiency?
2. Can the authors provide more insights into the conditions under which curriculum learning is most effective, and are there scenarios where it might not provide significant benefits?
3. How might the proposed approach be extended or adapted to handle more complex or high-dimensional goal spaces, and what are the potential challenges in doing so?

### Rating

3

### Confidence

3

**********