### Summary

The paper proposes a novel architecture for sequence modeling, called WARP, which combines weight-space learning with linear recurrence. The key idea is to represent the hidden state of the model as the weights and biases of an auxiliary neural network, enabling efficient gradient-free adaptation at test time. The authors demonstrate the effectiveness of WARP across various tasks, including image completion, energy prediction, traffic forecasting, and dynamical system reconstruction. They also show that incorporating domain-specific physical priors can significantly improve performance.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

- The paper introduces a novel and interesting approach to sequence modeling by combining weight-space learning with linear recurrence. This is a creative combination of ideas that has not been explored before in this context.
- The authors provide a thorough experimental evaluation of WARP across a diverse set of tasks, demonstrating its effectiveness and versatility. The results are generally strong and convincing.
- The paper is well-written and clearly structured, making it easy to follow the development of ideas and the proposed method.

### Weaknesses

#### Some Related Works


#### comment

 - The paper could benefit from more comprehensive comparisons with existing state-of-the-art models, particularly in areas where WARP shows strong performance, such as in-context learning and dynamical system reconstruction. Specifically, the paper lacks a detailed comparison against models that explicitly use attention mechanisms or other forms of recurrent architectures known for their effectiveness in sequence modeling. This makes it difficult to assess the true relative performance of WARP.
- While WARP is presented as a general framework, some of the claims about its capabilities, such as its performance on extremely long sequences, could be further substantiated with additional experiments and analyses. The paper does not provide sufficient evidence to support the claim that WARP can effectively handle extremely long sequences, especially when compared to models specifically designed for such tasks. The lack of experiments on datasets with significantly longer sequences is a notable gap.
- The paper could provide more detailed discussions on the limitations of WARP, particularly regarding its computational complexity and scalability when integrating domain-specific knowledge. The discussion on computational complexity is superficial, and the paper does not adequately address the practical challenges of scaling WARP to very large models or datasets. The integration of domain-specific knowledge is also not explored in sufficient depth, particularly regarding the potential for increased computational cost and complexity.

### Suggestions

To strengthen the paper, the authors should include a more thorough comparison with state-of-the-art sequence modeling techniques, such as Transformer-based models and other advanced recurrent neural networks. This comparison should not only focus on overall performance metrics but also delve into specific aspects like computational efficiency, memory usage, and convergence speed. For instance, a detailed analysis of WARP's performance against models like LSTMs or GRUs on tasks with varying sequence lengths would provide valuable insights. Furthermore, the authors should consider including a comparison with attention-based models, which are known for their effectiveness in capturing long-range dependencies in sequences. This would help to better position WARP within the landscape of existing sequence modeling techniques and highlight its unique advantages and disadvantages.

To address the concerns regarding long sequence performance, the authors should conduct additional experiments on datasets with significantly longer sequences. This could involve using benchmark datasets specifically designed for long-range sequence modeling, such as those found in natural language processing or time series analysis. The experiments should include a detailed analysis of how WARP's performance scales with increasing sequence length, and whether it exhibits any specific limitations or advantages compared to other models. Furthermore, the authors should investigate the impact of different hyperparameter settings on WARP's performance with long sequences, and provide guidelines for selecting appropriate parameters for different sequence lengths. This would provide a more robust evaluation of WARP's capabilities and limitations in handling long sequences.

Finally, the paper should include a more detailed discussion of the computational complexity and scalability of WARP, particularly when integrating domain-specific knowledge. This discussion should include a formal analysis of the time and space complexity of the proposed method, and compare it to other sequence modeling techniques. The authors should also explore the practical challenges of scaling WARP to very large models or datasets, and provide potential solutions for addressing these challenges. For example, the authors could investigate the use of techniques like model parallelism or distributed training to improve the scalability of WARP. Additionally, the paper should provide a more in-depth analysis of the impact of different types of domain-specific knowledge on WARP's performance, and discuss the potential trade-offs between performance and computational cost.

### Questions

- How does WARP compare to state-of-the-art models in terms of computational efficiency and scalability, especially when handling large datasets or complex tasks?
- What are the limitations of WARP when it comes to integrating domain-specific knowledge, and how can these limitations be addressed?
- How does the performance of WARP on extremely long sequences compare to specialized models designed for such tasks, and what are the potential areas for improvement in handling long-range dependencies?

### Rating

6

### Confidence

3

**********