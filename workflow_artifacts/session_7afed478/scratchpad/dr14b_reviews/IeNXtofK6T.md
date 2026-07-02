### Summary

The paper presents a defense mechanism against prompt injection attacks in LLMs by using a modern LLM as a "guardrail LLM" to detect and remove injected prompts. This approach, named PromptArmor, leverages the advanced reasoning capabilities of models like GPT-4 to accurately identify and sanitize malicious inputs, achieving low false positive and negative rates across multiple benchmarks. Unlike previous methods, PromptArmor not only detects but also removes the injected content, allowing the backend LLM to process the sanitized input. The paper demonstrates that PromptArmor is effective even against adaptive attacks and varies its performance based on the reasoning capabilities of the guardrail LLM.

### Soundness

2

### Presentation

3

### Contribution

2

### Strengths

1. **Innovative Use of Reasoning**: Leveraging the reasoning capabilities of modern LLMs for detecting prompt injections is a novel approach that significantly enhances detection accuracy.

2. **Comprehensive Evaluation**: The paper evaluates PromptArmor across multiple benchmarks and against adaptive attacks, providing robust evidence of its effectiveness.

3. **Practicality and Deployment**: PromptArmor’s modular design allows for easy integration into existing systems, making it a practical solution for real-world applications.

### Weaknesses

#### Some Related Works


#### comment

1. **Model Dependency**: The effectiveness of PromptArmor heavily relies on the capabilities of the guardrail LLM, which may not be feasible for all users due to access or cost constraints. This dependency on high-capacity models like GPT-4 raises concerns about the generalizability of the approach, especially in resource-constrained environments or for users who do not have access to such models. The paper should explore the performance of PromptArmor with more accessible and smaller models, providing a clearer understanding of its limitations and applicability across different scenarios.

2. **Adaptive Attacks**: While the paper claims robustness against adaptive attacks, attackers continuously develop new methods, and the defense may become vulnerable over time. The evaluation of adaptive attacks, while present, could be more extensive. The paper should include a more detailed analysis of the types of adaptive attacks that were tested and the specific strategies used by the red-teaming method. Furthermore, it should discuss the potential for more sophisticated attacks that might circumvent the current defense mechanisms, such as attacks that are specifically tailored to exploit the weaknesses of the guardrail LLM.

3. **Detection and Removal Accuracy**: Although the reported false positive and negative rates are low, in high-stakes applications, even these rates could lead to significant issues, either by allowing malicious prompts to slip through or by unnecessarily censoring benign inputs. The paper needs to provide a more granular analysis of the types of errors made by PromptArmor, including specific examples of false positives and false negatives. This analysis should explore the potential consequences of these errors in different application contexts, particularly in safety-critical systems where even a small error rate could have severe implications.

### Suggestions

To address the model dependency issue, the authors should conduct a more thorough analysis of PromptArmor's performance across a wider range of LLMs, including open-source models and smaller models with varying reasoning capabilities. This analysis should not only focus on the overall detection accuracy but also examine how the reasoning mode of these models impacts performance. Specifically, the authors should investigate the trade-offs between model size, reasoning ability, and detection accuracy, providing practical guidance on selecting an appropriate guardrail LLM for different use cases and resource constraints. Furthermore, the paper should explore techniques to mitigate the dependency on high-capacity models, such as using ensemble methods or knowledge distillation to transfer the detection capabilities of larger models to smaller ones. This would make the approach more accessible and practical for a broader range of users.

To enhance the evaluation of adaptive attacks, the authors should provide a more detailed description of the red-teaming method used, including the specific strategies and techniques employed to generate new attack templates. The paper should also include a more comprehensive analysis of the types of adaptive attacks that were tested, categorizing them based on their complexity and sophistication. Furthermore, the authors should discuss the potential for more advanced attacks that might exploit the weaknesses of the guardrail LLM, such as attacks that are specifically designed to evade detection by manipulating the input format or using adversarial examples. This discussion should include potential countermeasures that could be implemented to enhance the robustness of PromptArmor against such attacks. The paper should also explore the possibility of using automated attack generation techniques to continuously test and improve the defense mechanism.

To improve the analysis of detection and removal accuracy, the authors should provide a more detailed breakdown of the types of errors made by PromptArmor, including specific examples of false positives and false negatives. This analysis should explore the underlying reasons for these errors, such as ambiguities in the input or limitations in the reasoning capabilities of the guardrail LLM. The paper should also discuss the potential consequences of these errors in different application contexts, particularly in safety-critical systems where even a small error rate could have severe implications. Furthermore, the authors should explore techniques to mitigate the impact of these errors, such as using a multi-stage detection process or incorporating human oversight for high-stakes applications. The paper should also discuss the trade-offs between detection accuracy and the potential for over-censoring benign inputs, providing practical guidance on how to balance these competing objectives.

### Questions

1. **Generalizability**: How does PromptArmor perform with LLMs that have lower reasoning capabilities than GPT-4, and is there a threshold model size or capability below which it becomes ineffective?

2. **Handling Edge Cases**: What mechanisms are in place to handle ambiguous inputs that may be incorrectly flagged as prompt injections, and how does the system balance between security and usability?

3. **Evolution of Attacks**: How does PromptArmor plan to adapt to new and more sophisticated prompt injection techniques that may emerge as attackers become more adept?

### Rating

6

### Confidence

4

**********