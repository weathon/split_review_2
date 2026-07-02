### Summary

This paper proposes a new inference framework called SmartSwitch to address the underthinking problem in LLMs, where models prematurely switch thoughts without sufficient exploration. SmartSwitch detects underthinking using linguistic cues and a process reward model (PRM), and then intervenes by inserting a deepen prompt to encourage further exploration of promising thoughts. The framework is fine-tuning-free and plug-and-play, and it significantly improves the performance of various LLMs on mathematical reasoning benchmarks.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper identifies and characterizes the underthinking phenomenon in LLMs, which is an important contribution to the field of LLM reasoning.
2. The proposed SmartSwitch framework is novel and effective in addressing the underthinking problem, and it is easy to implement and integrate with existing LLMs.
3. The paper provides extensive experiments and analysis to demonstrate the effectiveness of SmartSwitch, and it shows that SmartSwitch can improve the performance of various LLMs on mathematical reasoning benchmarks.

### Weaknesses

#### Some Related Works


#### comment

1. The paper does not provide a detailed analysis of the computational overhead introduced by the SmartSwitch framework. It would be helpful to understand the trade-offs between performance gains and computational costs.
2. The paper does not explore the potential limitations of the SmartSwitch framework, such as its sensitivity to the choice of linguistic cues and PRM, or its applicability to other types of reasoning tasks.

### Suggestions

The paper would benefit from a more thorough investigation into the computational costs associated with the SmartSwitch framework. While the authors mention that the framework is plug-and-play, a detailed analysis of the time and memory overhead is crucial for practical applications. Specifically, the paper should quantify the additional computational resources required for the perception and intervention modules, including the PRM scoring and the insertion of deepen prompts. It would be beneficial to compare the computational cost of SmartSwitch with other methods for improving LLM reasoning, such as fine-tuning or prompt engineering. Furthermore, the analysis should consider the impact of the number of interventions on the overall computational cost. For example, how does the computational cost scale with the number of detected underthinking instances and the depth of the deepen prompts? A clear understanding of these trade-offs is essential for determining the practicality of the SmartSwitch framework.

Further research should explore the sensitivity of the SmartSwitch framework to the choice of linguistic cues and the PRM. The current selection of linguistic cues, while effective, may not be universally applicable across all types of reasoning tasks or LLMs. A more systematic approach to selecting these cues, perhaps based on linguistic analysis or empirical studies, would strengthen the robustness of the framework. Additionally, the paper should investigate the impact of different PRMs on the performance of SmartSwitch. The choice of PRM can significantly influence the effectiveness of the intervention, and a comparative analysis of different PRMs would provide valuable insights. It would also be beneficial to explore the potential for adaptive cue selection and PRM selection based on the specific task or LLM being used. This could lead to a more flexible and robust framework that can be applied to a wider range of scenarios.

Finally, the paper should investigate the applicability of the SmartSwitch framework to other types of reasoning tasks beyond mathematical reasoning. While the current results are promising, it is unclear whether the framework can be effectively applied to tasks such as commonsense reasoning, logical reasoning, or causal reasoning. Each of these tasks may require different types of linguistic cues and PRMs, and the paper should explore these possibilities. Furthermore, the paper should consider the potential limitations of the framework in scenarios where the reasoning process is highly dynamic or non-linear. In such cases, the detection of underthinking may be more challenging, and the insertion of deepen prompts may not always be effective. A more comprehensive evaluation of the framework across a diverse range of reasoning tasks would provide a more complete understanding of its capabilities and limitations.

### Questions

1. How does the SmartSwitch framework handle cases where the model is not underthinking but is instead exploring different approaches to the problem?
2. Can the SmartSwitch framework be applied to other types of reasoning tasks beyond mathematical reasoning, such as commonsense reasoning or causal reasoning?

### Rating

6

### Confidence

3

**********