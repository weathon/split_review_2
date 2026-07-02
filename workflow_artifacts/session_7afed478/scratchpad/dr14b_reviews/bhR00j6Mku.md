### Summary

The paper investigates benchmark contamination in Large Reasoning Models (LRMs) and reveals that detection methods are ineffective due to two key findings:
1. Contamination introduced during the transition from base models to LRMs can be concealed through reinforcement learning.
2. Contamination applied to advanced LRMs leaves minimal detectable evidence.

These findings suggest that existing detection methods are insufficient for LRMs, highlighting the need for more robust detection approaches and trustworthy evaluation protocols.

### Soundness

3

### Presentation

3

### Contribution

2

### Strengths

The paper presents a novel analysis of how reinforcement learning can conceal contamination signals in large reasoning models, challenging the effectiveness of current detection methods. It provides a theoretical framework explaining why PPO-style clipping and importance sampling in RL can mask contamination, offering insights into the mechanisms behind detection evasion. The research is methodologically strong, combining empirical experiments across multiple benchmarks with theoretical analysis to support its claims. The findings are significant for the broader AI community as they highlight vulnerabilities in current evaluation practices and underscore the need for improved detection methods to ensure fair and trustworthy model assessments.

### Weaknesses

#### Some Related Works


#### comment

The study focuses on a specific set of models and benchmarks, which may limit the generalizability of the findings. Contamination detection methods are diverse, and the paper does not explore all possible approaches, potentially overlooking methods that might be more effective. Additionally, the research assumes that contamination primarily occurs through benchmark data inclusion in training, without fully considering other contamination vectors, such as data augmentation or adversarial examples. The theoretical analysis, while insightful, primarily focuses on PPO-style algorithms and may not fully generalize to other reinforcement learning methods. Furthermore, the paper does not delve deeply into the practical implications of its findings for real-world model deployment, such as the potential for malicious actors to exploit these vulnerabilities. The analysis of contamination during the SFT phase with CoT data could be more detailed, particularly regarding how the model's internal representations are affected and how this impacts detection. Finally, the paper could benefit from a more thorough discussion of the limitations of the proposed theoretical framework and its applicability to different model architectures and training paradigms.

### Suggestions

To strengthen the paper, the authors should expand their empirical analysis to include a wider range of model architectures and training datasets. This would help to validate the generalizability of their findings beyond the specific models and benchmarks used in the current study. Specifically, they should consider exploring models with different layer configurations, attention mechanisms, and pre-training objectives. Furthermore, the authors should investigate the impact of varying the size and diversity of the training datasets on the effectiveness of contamination and its detectability. This would provide a more comprehensive understanding of the conditions under which contamination is most likely to occur and be concealed. It would also be beneficial to explore the effects of different data augmentation techniques on contamination, as these techniques can introduce subtle forms of contamination that may not be easily detected by existing methods. 

In addition to expanding the empirical analysis, the authors should also explore a broader range of contamination detection methods. This should include methods that are based on different principles, such as those that analyze the model's internal representations or those that use adversarial examples to detect contamination. The authors should also investigate the effectiveness of methods that are specifically designed to detect contamination in reasoning-based models, as these methods may be more sensitive to the types of contamination that are introduced during SFT and RL training. Furthermore, the authors should provide a more detailed analysis of the theoretical framework, including a discussion of its limitations and assumptions. This should include an analysis of how the framework applies to different reinforcement learning algorithms and model architectures. The authors should also explore the potential for extending the framework to account for other forms of contamination, such as those introduced through data augmentation or adversarial examples. 

Finally, the authors should delve deeper into the practical implications of their findings for real-world model deployment. This should include a discussion of the potential for malicious actors to exploit the vulnerabilities identified in the paper, as well as the development of strategies for mitigating these risks. The authors should also explore the impact of contamination on the fairness and robustness of models, as well as the potential for contamination to lead to biased or unreliable predictions. This would help to highlight the importance of the research and its relevance to the broader AI community. The authors should also provide more details on how the model's internal representations are affected by contamination during the SFT phase with CoT data, and how this impacts the effectiveness of detection methods. This could involve analyzing the model's attention patterns or the activation patterns of its hidden layers.

### Questions

1. How do the authors plan to address the limitations of their theoretical framework, and could it be extended to cover a broader range of RL algorithms and contamination scenarios?
2. Are there specific strategies or advanced methods the authors would recommend for detecting contamination in reasoning-based models, particularly in complex, real-world applications?
3. How might the findings influence future research directions in contamination detection, and are there particular areas or methods the authors believe hold promise for more robust detection?
4. What steps do the authors propose to mitigate the risks associated with benchmark contamination in practical deployments, and how might these strategies be implemented effectively?

### Rating

5

### Confidence

4

**********