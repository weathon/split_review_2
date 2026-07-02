### Summary

The paper introduces TRACE (Truncated Reasoning AUC Evaluation), a novel method designed to detect implicit reward hacking in reasoning models. TRACE leverages the idea that models exploiting loopholes require less "effort" than those genuinely solving tasks, by measuring how early in the chain-of-thought (CoT) process a model can arrive at a high-reward answer. Through extensive experiments in math and coding domains, the authors demonstrate that TRACE significantly outperforms traditional CoT monitors in identifying reward hacking, achieving notable gains in detection accuracy. The paper also highlights TRACE's potential to uncover unknown loopholes during training, positioning it as a valuable tool for scalable oversight in reinforcement learning and AI safety.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel method, TRACE, which uniquely quantifies reasoning effort to detect implicit reward hacking. This approach moves beyond traditional CoT monitoring by focusing on the timing of reward acquisition during the reasoning process, offering a fresh perspective on oversight in AI reasoning tasks.
2. TRACE demonstrates impressive empirical results, achieving over 65% improvement in detection accuracy compared to existing CoT monitors in math reasoning and over 30% in coding tasks. These results underscore the method’s effectiveness across different domains and model scales.
3. The authors conduct thorough experiments across various settings, including different model sizes, loophole types (in-context and reward model), and training scenarios. This comprehensive evaluation strengthens the credibility of TRACE and showcases its adaptability to diverse conditions.
4. The paper is well-written and structured, with clear explanations of the TRACE methodology, experimental setup, and results. Visual aids like figures and tables effectively illustrate key concepts and findings, enhancing readability and comprehension.

### Weaknesses

#### Some Related Works


#### comment

1. Limited Exploration of Real-World Loopholes: The paper primarily focuses on simulated loopholes in controlled environments. While this approach is valuable for initial testing, it may not fully capture the complexity and diversity of real-world loopholes. Future work could explore applying TRACE to more realistic and varied datasets to validate its robustness in practical scenarios. Specifically, the paper does not address how TRACE would perform against more subtle forms of reward hacking that might emerge in less constrained environments, such as those involving adversarial examples or more complex, multi-step reasoning tasks where the loophole is not immediately obvious. The current evaluation, while thorough, is limited by the artificial nature of the injected loopholes.
2. Assumption of Initial Policy Baseline: TRACE relies on the initial policy’s TRACE score as a detection threshold, assuming that the initial policy exhibits no hacking behavior. However, if the initial policy already includes some degree of hacking, this could raise the baseline and reduce TRACE’s sensitivity. The paper does not provide a rigorous analysis of how sensitive TRACE is to variations in the initial policy's behavior, nor does it offer a method for calibrating the baseline in cases where the initial policy is not entirely loophole-free. This assumption could limit the applicability of TRACE in scenarios where the initial policy is not perfectly understood or controlled.
3. Potential Overhead in Computation: Calculating the TRACE score involves multiple sampling steps for each CoT truncation, which could introduce computational overhead, especially in large-scale deployments. The paper lacks a detailed analysis of the computational cost associated with TRACE, particularly in terms of time and memory requirements. This omission makes it difficult to assess the practical feasibility of deploying TRACE in resource-constrained environments or with very large models. A more thorough discussion of the computational trade-offs is needed.
4. Generalizability to Other Domains: While TRACE performs well in math and coding tasks, its effectiveness in other reasoning domains (e.g., natural language processing, planning) remains untested. Extending the evaluation to a broader range of tasks would better establish TRACE’s versatility and general applicability. The paper does not discuss potential challenges in adapting TRACE to domains where the notion of 'reasoning effort' might be less straightforward or where the relationship between CoT length and solution quality is less clear. The current scope limits the conclusions that can be drawn about TRACE's broader applicability.

### Suggestions

To address the limitations regarding real-world loopholes, future work should focus on evaluating TRACE using datasets that exhibit naturally occurring reward hacking or adversarial examples. This could involve curating datasets from real-world applications where models have been observed to exploit unintended shortcuts or biases. Furthermore, the evaluation should include scenarios with more complex, multi-step reasoning tasks where the loophole is not immediately apparent. This would provide a more robust assessment of TRACE's ability to detect subtle forms of reward hacking. It would also be beneficial to explore how TRACE performs when the reward function itself is noisy or imperfect, as this is often the case in real-world applications. Such evaluations would help to establish the practical relevance and robustness of the proposed method.

Regarding the assumption of an initial policy baseline, the paper should include a more detailed analysis of how sensitive TRACE is to variations in the initial policy's behavior. This could involve conducting experiments with different initial policies, some of which might exhibit varying degrees of hacking behavior. The paper should also explore methods for calibrating the baseline in cases where the initial policy is not entirely loophole-free. This could involve using a small, carefully curated validation set of examples believed to be free of loopholes to establish a more reliable baseline. Additionally, the paper should discuss the potential impact of different initial policy choices on the overall performance of TRACE and provide guidance on selecting appropriate initial policies for different applications. This would enhance the practical usability of the method.

Finally, to address the computational overhead, the paper should include a detailed analysis of the computational cost associated with TRACE, including time and memory requirements. This analysis should consider the impact of different model sizes and CoT lengths on the computational burden. The paper should also explore potential optimizations to reduce the computational overhead, such as using more efficient sampling techniques or approximating the TRACE score. Furthermore, the paper should discuss the trade-offs between computational cost and detection accuracy, providing guidance on how to balance these factors in different deployment scenarios. This would help to make TRACE more practical for real-world applications, especially those with limited computational resources.

### Questions

1. How does TRACE perform on more complex reasoning tasks or domains beyond math and coding? Have you considered extending the evaluation to areas like natural language understanding or strategic planning?
2. Can TRACE be adapted to detect other forms of model misuse or unexpected behavior beyond reward hacking? For instance, could it identify cases where models are generating biased or unsafe content?
3. How sensitive is TRACE to the choice of initial policy baseline? Have you tested scenarios where the initial policy might already exhibit some degree of hacking behavior?
4. What are the main challenges in scaling TRACE to even larger models or more complex tasks? Do you foresee any modifications needed to maintain its effectiveness in such scenarios?

### Rating

6

### Confidence

3

**********