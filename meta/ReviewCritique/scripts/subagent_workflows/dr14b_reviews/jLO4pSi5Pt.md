### Summary

This paper proposes a Long-tailed Test-Time Adaptation (L-TTA) method for Vision-Language Models (VLMs) to address the challenges posed by long-tailed distributions in test sets. L-TTA consists of three co-designed mechanisms: Synergistic Prototypes (SyPs), Rebalancing Shortcuts (RSs), and Balanced Entropy Minimization (BEM). Extensive experiments demonstrate the effectiveness of the proposed method.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The proposed method is novel and effective.
2. The paper is well-written and easy to follow.
3. The experimental results are convincing.

### Weaknesses

#### Some Related Works


#### comment

1. The proposed method is complex and contains many hyper-parameters, which may limit its practical application.
2. The authors should provide a more detailed analysis of the computational complexity of the proposed method compared to existing approaches.
3. The authors should discuss the potential limitations of the proposed method and suggest directions for future research.

### Suggestions

The paper introduces a novel Long-tailed Test-Time Adaptation (L-TTA) method, which is a significant contribution to the field. However, the practical applicability of the proposed method could be improved by addressing the complexity and the number of hyperparameters. Specifically, the authors should explore methods to reduce the number of hyperparameters, perhaps through techniques like Bayesian optimization or by identifying the most sensitive parameters and focusing on tuning those. Furthermore, a more detailed analysis of the computational cost is needed. While the authors mention the time and memory requirements, a breakdown of the computational cost for each component of the L-TTA method (SyPs, RSs, and BEM) would be beneficial. This would allow for a more granular understanding of the method's efficiency and identify potential bottlenecks. For example, how does the computational cost scale with the number of classes or the size of the input images? This analysis should also compare the computational cost of L-TTA with existing test-time adaptation methods, not just in terms of overall time, but also in terms of memory usage and energy consumption. 

To further strengthen the paper, the authors should provide a more in-depth discussion of the limitations of the proposed method. While the paper demonstrates strong performance on several datasets, it is important to acknowledge scenarios where the method might fail or underperform. For example, how does the method perform when the test distribution is significantly different from the training distribution, beyond the long-tailed nature? Are there specific types of images or classes where the method struggles? Addressing these limitations would provide a more balanced view of the method's capabilities and help guide future research. Additionally, the authors should explore the potential impact of the choice of the base VLM on the performance of L-TTA. Does the method perform consistently across different VLM architectures, or are there specific models where it is more effective? This analysis would help to understand the generalizability of the proposed method.

Finally, the authors should provide more concrete suggestions for future research directions. While the paper introduces a novel approach, there are several avenues for further exploration. For example, how can the method be extended to handle more complex data distributions or to adapt to new classes that were not seen during training? Could the method be made more robust to noisy or adversarial examples? Another interesting direction would be to investigate the interpretability of the learned prototypes and shortcuts. Understanding how these components contribute to the final prediction could provide valuable insights into the method's behavior and guide further improvements. The authors should also consider exploring the potential of combining L-TTA with other test-time adaptation techniques to achieve even better performance.

### Questions

Please refer to the weaknesses.

### Rating

6

### Confidence

3

**********