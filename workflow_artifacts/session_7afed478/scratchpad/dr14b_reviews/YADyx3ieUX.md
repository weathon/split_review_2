### Summary

The paper addresses the common characterization of neural networks as "black boxes," where the internal processes leading to specific outputs are opaque and difficult to explain. The authors argue that this characterization stems from a fallacious assumption about causation in neural networks—that if a past feature of a system causally influences a present feature, an intermediary correlate must be identifiable. They contend that this assumption is false and that the model of deep learning systems as having explanations that are inherently partial and incomplete has significant conceptual implications for discussions around explainable AI. The paper uses the example of "Secret Owls," where a student model trained on data from a teacher model inherits certain behaviors (like favoring owls) even when these behaviors are not explicitly present in the training data, to illustrate the challenge of tracing causal relationships in neural networks.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

The paper takes a fresh look at the black box problem in neural networks, challenging the widely accepted assumption that causal relationships within these systems must be accompanied by identifiable correlates. By questioning this assumption, the authors open up new perspectives on how we understand and approach the explainability of AI systems. The Secret Owls example is particularly effective in highlighting the difficulty of tracing causal links in neural networks, making the paper's argument more relatable and understandable for readers. The paper's conceptual contribution is significant, as it encourages a reevaluation of fundamental beliefs about causation and explainability in AI, which could have lasting impacts on the field.

### Weaknesses

#### Some Related Works


#### comment

While the paper makes a compelling theoretical argument, it could benefit from more empirical evidence or case studies to support its claims. Including examples from recent research where the lack of identifiable correlates in neural networks led to surprising or counterintuitive outcomes would strengthen the paper's position. The paper's argument is quite dense and philosophical, which might make it less accessible to readers who are not deeply versed in the subject matter. Simplifying some of the explanations or providing additional background information could help broaden its appeal. The paper challenges a fundamental assumption in the field, but it could do more to acknowledge and address potential counterarguments or limitations of its own perspective. A more balanced discussion of the implications of rejecting the correlative continuity assumption would add depth to the paper.

### Suggestions

To strengthen the paper's empirical foundation, the authors should include specific examples from recent neural network research where the absence of clear correlates led to unexpected behaviors. For instance, they could discuss cases where adversarial attacks successfully fooled a model despite minimal changes to the input, highlighting the difficulty in pinpointing the exact features causing the misclassification. Another example could be the emergence of unintended biases in models trained on seemingly neutral datasets, where the causal links between the training data and the biased output are not obvious. These examples would provide concrete illustrations of the paper's central argument, making it more persuasive and relatable to a broader audience. Furthermore, the authors could delve deeper into the implications of their findings for current explainability techniques, such as feature importance methods or saliency maps. By demonstrating how these methods might be limited by the assumption of correlative continuity, the paper could offer a more nuanced critique of existing approaches and pave the way for new directions in explainable AI research.

To improve accessibility, the authors should consider adding more intuitive explanations of the core concepts, especially the philosophical underpinnings of their argument. For example, they could use analogies or diagrams to illustrate the difference between causal and correlational relationships in neural networks. Providing a step-by-step breakdown of the 'Secret Owls' example, with clear definitions of the key terms and concepts involved, would also help readers grasp the paper's main points more easily. Additionally, the authors could include a glossary of technical terms or a summary of key concepts at the beginning of the paper to aid readers unfamiliar with the specific terminology. This would make the paper more approachable for a wider audience, including those who may not have a strong background in philosophy or theoretical computer science. The inclusion of such aids would significantly enhance the paper's readability and impact.

Finally, the authors should explicitly address potential counterarguments and limitations of their perspective. For example, they could discuss scenarios where identifying correlates might still be beneficial, even if not strictly necessary for understanding causation. They could also acknowledge that while the assumption of correlative continuity might be flawed, it has been a useful heuristic in many cases. Furthermore, the authors could explore the implications of their argument for the development of new explainability techniques. By acknowledging these limitations and counterarguments, the authors would demonstrate a more balanced and nuanced understanding of the complex issues surrounding explainability in AI. This would also help to preempt criticisms and strengthen the overall credibility of their work.

### Questions

Could you provide more empirical examples where the lack of identifiable correlates in neural networks led to surprising or counterintuitive outcomes?

How do you see your argument impacting the development of future explainability techniques in AI?

What are the potential limitations or counterarguments to your perspective on causation and explainability in neural networks?

### Rating

6

### Confidence

3

**********