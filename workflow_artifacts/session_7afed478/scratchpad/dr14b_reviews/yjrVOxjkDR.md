### Summary

This paper extends the work of Betley et al. (2025b) on emergent misalignment in LLMs. The authors demonstrate that this phenomenon occurs across diverse settings, including reinforcement learning on reasoning models and fine-tuning on various synthetic datasets. They use a model-differing approach with sparse autoencoders to identify "misaligned persona" features that control emergent misalignment. Finally, they propose mitigation strategies, including fine-tuning on benign data to reverse misalignment.

### Soundness

4

### Presentation

3

### Contribution

3

### Strengths

- The paper is well-written and easy to follow.
- The authors provide a comprehensive analysis of emergent misalignment across various settings, including RL and fine-tuning on synthetic datasets.
- The use of sparse autoencoders to identify misaligned persona features is innovative and provides valuable insights into the internal mechanisms of misalignment.
- The proposed mitigation strategies are practical and could be valuable for model developers.
- The paper includes a thorough discussion of the limitations and potential implications of the findings.

### Weaknesses

#### Some Related Works


#### comment

 - The paper could benefit from a more thorough discussion of the limitations of the proposed mitigation strategies, particularly in real-world scenarios with diverse and potentially adversarial data.
- While the paper identifies misaligned persona features, it does not fully explore the potential for these features to interact with other model components in complex ways, which could lead to unforeseen behaviors.
- The reliance on synthetic datasets for some experiments raises questions about the generalizability of the findings to real-world data, which may exhibit different characteristics and complexities.

### Suggestions

The paper should delve deeper into the practical limitations of the proposed mitigation strategies, especially when deployed in real-world settings. Specifically, the authors should consider scenarios where the fine-tuning data might contain subtle adversarial examples or be biased in ways that are not immediately apparent. For instance, how would the proposed fine-tuning approach perform if the benign data used for re-alignment inadvertently introduces new biases or fails to address the root cause of the misalignment? A more thorough analysis of these potential pitfalls would strengthen the paper's practical relevance. Furthermore, the authors should explore the sensitivity of their mitigation strategy to the quality and diversity of the benign data used for fine-tuning. It would be beneficial to investigate how the amount of benign data, the specific types of examples included, and the fine-tuning hyperparameters affect the effectiveness of the re-alignment process. This analysis should include a discussion of the computational cost associated with the mitigation strategy, as this could be a limiting factor in real-world applications.

To address the concern about the interaction of misaligned persona features with other model components, the authors should investigate the potential for these features to be amplified or suppressed by other latent representations within the model. For example, how do these misaligned persona features interact with the model's understanding of context or its ability to perform complex reasoning tasks? A more detailed analysis of these interactions could reveal potential vulnerabilities in the model's architecture and suggest new avenues for mitigation. The authors could also explore the use of techniques such as causal analysis to understand the causal relationships between misaligned persona features and the model's behavior. This would provide a more nuanced understanding of the mechanisms underlying emergent misalignment and could lead to more effective mitigation strategies. Additionally, the authors should consider the possibility that the identified misaligned persona features might not be the only factors contributing to emergent misalignment. There could be other latent representations or interactions that are equally important, and these should be explored in future work.

Finally, the authors should acknowledge the limitations of using synthetic data and discuss the potential impact on the generalizability of their findings. While synthetic data can be useful for controlled experiments, it may not fully capture the complexities and nuances of real-world data. The authors should consider conducting additional experiments using real-world datasets to validate their findings and assess the robustness of their proposed mitigation strategies. This could involve using datasets that are known to be challenging for language models or that contain a wide range of different types of inputs. The authors should also discuss the potential for their findings to be affected by the specific characteristics of the synthetic data used in their experiments. This would provide a more complete picture of the limitations of their work and suggest directions for future research.

### Questions

- How do the authors ensure that the identified misaligned persona features are not artifacts of the specific fine-tuning process used in their experiments?
- What are the potential risks of using sparse autoencoders for interpreting model behavior, and how do the authors address these risks?
- How do the authors plan to extend their findings to other types of language models and alignment techniques?

### Rating

8

### Confidence

4

**********