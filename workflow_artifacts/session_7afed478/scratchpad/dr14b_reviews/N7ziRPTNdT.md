### Summary

This paper explores the role of generation in achieving human-level visual perception in AI systems. It contrasts generative models, which use a decoder to map latent variables to images, with non-generative models, which use an encoder to map images to latent variables. The authors argue that generative approaches are better suited for compositional generalization, the ability to recognize unseen combinations of visual concepts, and provide theoretical and empirical evidence to support this claim.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper presents a novel perspective on the generative vs. non-generative debate in visual perception, focusing on data efficiency and compositional generalization. This approach is both timely and relevant, addressing a fundamental question in AI.

2. The theoretical analysis is rigorous and well-supported, with clear proofs and derivations. The authors formalize the constraints required for compositional generalization and demonstrate why these constraints are more easily enforced in generative models.

3. The empirical evaluation is thorough, using photorealistic image datasets to compare generative and non-generative methods. The results convincingly show the advantages of generative approaches in compositional generalization.

### Weaknesses

#### Some Related Works


#### comment

1. The theoretical analysis assumes a specific function class for the ground-truth generator. While this is a reasonable starting point, it would be beneficial to discuss the robustness of the results to deviations from this assumption. Specifically, the paper does not explore how the performance of the generative model degrades if the true data generating process deviates from the assumed diffeomorphism with additive and polynomial interaction terms. It is unclear how much the conclusions rely on this specific choice of function class, and whether the observed benefits of generative models would persist under more general conditions.

2. The empirical evaluation focuses on relatively simple compositional tasks. While the results are compelling, it would be valuable to see how the methods perform on more complex, real-world datasets. The current experiments, while demonstrating the core idea, do not fully address the challenges of compositional generalization in scenarios with more intricate object interactions, occlusions, and variations in lighting and viewpoint. The paper should acknowledge the limitations of the current evaluation and discuss the potential challenges in scaling the proposed methods to more complex datasets.

### Suggestions

The paper would benefit from a more detailed discussion of the limitations of the theoretical analysis. Specifically, the authors should explore the sensitivity of their results to the assumed function class for the ground-truth generator. It would be valuable to see a discussion of how the performance of the generative model might degrade if the true data generating process deviates from the assumed diffeomorphism with additive and polynomial interaction terms. For example, what happens if the interaction terms are not polynomial, or if the diffeomorphism is not perfectly invertible? A more thorough analysis of these aspects would strengthen the theoretical claims and provide a more nuanced understanding of the conditions under which generative models are advantageous. Furthermore, the authors could consider exploring alternative function classes and discussing how their theoretical results might generalize to these cases. This would help to clarify the scope and limitations of the proposed approach.

To enhance the empirical evaluation, the authors should consider including experiments on more complex, real-world datasets. While the current experiments demonstrate the core idea, they do not fully address the challenges of compositional generalization in scenarios with more intricate object interactions, occlusions, and variations in lighting and viewpoint. For example, the authors could evaluate their methods on datasets with more diverse object categories, more complex backgrounds, and more realistic object arrangements. This would provide a more comprehensive assessment of the proposed approach and its potential for real-world applications. Additionally, the authors should discuss the computational cost of their methods and how they scale with the complexity of the data and the number of objects. This would help to identify the practical limitations of the proposed approach and guide future research in this area.

Finally, the paper should include a more detailed discussion of the potential challenges in scaling the proposed methods to more complex datasets. The current experiments, while demonstrating the core idea, do not fully address the challenges of compositional generalization in scenarios with more intricate object interactions, occlusions, and variations in lighting and viewpoint. The authors should acknowledge these limitations and discuss potential strategies for addressing them. For example, they could explore the use of more powerful generative models, more sophisticated training techniques, or more efficient search algorithms. This would help to identify the key challenges in scaling the proposed approach and guide future research in this area.

### Questions

1. How sensitive are the theoretical results to the specific assumptions about the function class of the ground-truth generator? Could deviations from these assumptions significantly impact the conclusions?

2. How do the proposed methods scale with the complexity of the data and the number of objects? Are there any computational bottlenecks that need to be addressed?

3. Could the authors provide more details on the gradient-based search and generative replay techniques used for out-of-domain inversion? How do these methods perform in practice, and what are their limitations?

### Rating

6

### Confidence

3

**********