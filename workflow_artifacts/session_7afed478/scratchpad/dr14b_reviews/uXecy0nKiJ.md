### Summary

The paper investigates the safety implications of activation steering in large language models (LLMs). Activation steering is a technique that manipulates the model's hidden states during inference to control its behavior. The authors demonstrate that even benign steering can compromise the model's safety mechanisms, leading to harmful compliance. They show that steering with random vectors or sparse autoencoder (SAE) features can significantly increase the probability of the model complying with harmful requests. The study also introduces a universal attack method that generalizes to unseen harmful prompts, highlighting the potential for misuse. The findings challenge the assumption that precise control over model internals guarantees safe behavior and emphasize the need for robust safety measures in LLMs.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper is well-written and easy to follow, with clear explanations of the methodology and results.
2. The study conducts extensive experiments across different model families, demonstrating the robustness of the findings.
3. The paper introduces a novel perspective on LLM safety, highlighting the risks associated with activation steering, a technique often considered safe due to its interpretability.

### Weaknesses

#### Some Related Works


#### comment

1. The paper does not explore potential mitigation strategies to counteract the identified vulnerabilities. Including such strategies would enhance the practical value of the research.
2. The study focuses on a specific set of models and steering techniques. It would be beneficial to investigate a broader range of models and methods to ensure the generalizability of the findings.

### Suggestions

The paper's exploration of activation steering vulnerabilities in LLMs is compelling, but it would be significantly strengthened by addressing potential countermeasures. The authors should consider investigating methods to detect when steering is occurring, perhaps by monitoring for anomalies in the hidden state activations. Furthermore, exploring techniques to neutralize the effects of malicious steering, such as adversarial training or input sanitization, would be valuable. For example, could a secondary model be trained to identify and filter out steering vectors before they impact the primary LLM? This would add a practical dimension to the research, moving beyond simply identifying a vulnerability to proposing solutions.

To enhance the generalizability of the findings, the authors should expand their analysis to include a more diverse set of models and steering techniques. Specifically, they should consider models with different architectures, such as encoder-decoder models, and models trained with different alignment techniques. Additionally, exploring different methods for generating steering vectors, beyond random and SAE-based approaches, would be beneficial. For instance, could gradient-based methods be used to generate more effective steering vectors? This would help to determine whether the observed vulnerabilities are specific to the models and methods used in the study or if they are a more general property of LLMs. Furthermore, the authors should investigate the impact of steering on different layers of the model, as the effect of steering might vary depending on the layer being targeted.

Finally, the paper would benefit from a more detailed analysis of the relationship between steering strength and harmful compliance. While the authors demonstrate that steering can lead to harmful outputs, they do not fully explore how the magnitude of the steering vector affects the likelihood of harmful behavior. A more granular analysis, perhaps using a range of steering coefficients, would provide a more complete picture of the vulnerability. This could involve plotting the compliance rate as a function of the steering coefficient, which could reveal critical thresholds where the model's behavior shifts dramatically. Such an analysis would also help in understanding the sensitivity of the model to different levels of steering and could inform the development of more robust safety mechanisms.

### Questions

1. Could the authors elaborate on the potential mechanisms through which SAE features, despite their benign nature, can lead to harmful compliance?
2. The paper mentions that steering in a random direction can break model alignment safeguards. Could the authors provide more insights into why this occurs and how it compares to more targeted steering approaches?
3. The authors found that steering is most effective in the middle layers of the model. Could they provide a hypothesis on why this might be the case?
4. How do the authors envision the practical implications of their findings, especially concerning the deployment of LLMs in real-world applications?

### Rating

6

### Confidence

3

**********